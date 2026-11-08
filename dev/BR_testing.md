---
alwaysApply: false
---

# Testing a BR program

**Read this when you have changed a BR program and need to show that it works.** It picks the way
to test and gives the commands for each. The details are in the files it links to.

Run every command here from the kit root (the folder that holds `context/`), with the variables of
[`BR_launch.md`](BR_launch.md#br-launch-environment) set. In Windows, use PowerShell or cmd, not
Git Bash: a POSIX path handed to `PROC` fails with error 4215.

## 1. Pick the way

| What you need to show | Way | Pass or fail is |
|---|---|---|
| The program compiles | [§2 Check](#check) | `brls` reports no error |
| A program with no screen does its job | [§3 Headless run](#headless) | the files it writes, and the `LOGGING` file |
| An interactive program, given set answers, does its job | [§3 Headless run](#headless), with proc-fed input | the same |
| A screen shows what it should, and still does after the next change | [§4 UI script](#uitest) | `uitest` exits 0 |
| You need to watch, explore or debug a running screen | [§5 Live session](#live) | what you see; not a repeatable test |
| A program a model wrote runs safely | [§6 Restricted run](#restricted) | the exit code from `report_status` |

Always do §2 first. The other ways cost a BR start, and a syntax error wastes it.

<a id="check"></a>
## 2. Check

```
"$BRLS_EXE" -check -sema program.brs
```

`-sema` catches what a line-by-line check misses, such as an unclosed block. With an assistant
attached, the `check_source` tool runs the same check and takes source text as well as a path.
`brls` does not start BR.

BR's own check is `"$BR_EXE" "LOAD program.brs source" -"$BR_AI_UTIL"`, which stops at the first
error ([`BR_launch.md`](BR_launch.md#compile--syntax-check)).

<a id="headless"></a>
## 3. Headless run

For a program that needs no person at the screen. Use `$BR_AI_UTIL`: it is `UNATTENDED`, so BR
exits when the program stops, and an untrapped error ends the run instead of leaving BR waiting.

```
"$BR_EXE" "RUN glp\trial_bal" -"$BR_AI_UTIL"          # a program
"$BR_EXE" "PROC tmp\run_it.prc" -"$BR_AI_UTIL"        # a procedure
```

To give an interactive program its answers, put `RUN <program> PROC` in a procedure, then one
line per input statement, then `SYSTEM`
([`BR_launch.md`](BR_launch.md#run-a-program-with-proc-fed-input)).

**Judge the result by what the program did, not by the exit code alone.** Check the files it
wrote. In the `LOGGING` file, the line that says a run failed is
`Unattended processing terminated by error <n> while processing...`, which names the error and
the line. Exit code 99 follows any unattended fatal error, so it does not say which. Reading the
log, and the hazards of a headless run, are in
[`APP-DEV-GUIDE.md` §6](APP-DEV-GUIDE.md).

<a id="uitest"></a>
## 4. UI script

For a screen you want to check now and again after the next change. You write what should be on
the screen, what to type and what should come up. `br_mcp_driver uitest` runs it against a live
session, and exits **0** when every check passes, **1** when one fails or no session could be
reached, and **2** for a usage error. It ends with `<n> checks, <m> failures`. A failed `expect`
prints the screen, so the reason is in the output.

You need three files: the program under test, a procedure and a script. The example below is
complete; create the files in `context\scratch\bt_recipe\` to try it. *Measured, 2026-11-08*,
exactly as written here: 7 checks and exit 0, and with one wrong expectation, 1 failure, the
screen printed, and exit 1. Both times BR ended on its own with exit code 0.

**The program under test** is an ordinary program. It does nothing for the harness itself:

```
00010    DIM NAME$*20,A$*1
00020    PRINT NEWPAGE
00030    PRINT FIELDS "1,2,C 20": "GREETING TEST"
00040    PRINT FIELDS "3,2,C 12": "Your name:"
00050    RINPUT FIELDS "3,14,C 20,U": NAME$
00060    PRINT FIELDS "5,2,C 40": "Hello "&RTRM$(NAME$)
00070    RINPUT FIELDS "7,2,C 1,U": A$
00080    STOP
```

**The procedure** opens the channel, lends the keyboard and runs the program. For a real test,
replace the `LOAD` line with your own program.

```
! context\scratch\bt_recipe\greet.prc
PROCERR RETURN
LET X=MSG("harness",8751)
LET X=MSG("grant",300)
LOAD context\scratch\bt_recipe\greet.brs source
RUN
SYSTEM
```

**The script**, one step a line, `#` for a comment:

```
# context\scratch\bt_recipe\greet.uis
expect row 0 "GREETING TEST"
expect "Your name:"
field 0 spec "C 20"
type ADA
press ENTER
expect "Hello ADA"
# the last key lets the program end, so the procedure reaches SYSTEM
press ENTER
```

**The run**, in PowerShell. It removes a stale token file, starts BR, waits for the channel to
open, runs the script, and waits for BR to end:

```powershell
$tok = Join-Path $env:LOCALAPPDATA "ADS\harness.token"
if (Test-Path $tok) { Remove-Item $tok }
$br = Start-Process -PassThru $env:BR_EXE -ArgumentList '"PROC context\scratch\bt_recipe\greet.prc"', "-$env:BR_AI_USER"
$deadline = (Get-Date).AddSeconds(90)
while (-not (Test-Path $tok) -and (Get-Date) -lt $deadline -and -not $br.HasExited) { Start-Sleep -Milliseconds 500 }
& $env:BR_MCP_DRIVER uitest context\scratch\bt_recipe\greet.uis
$result = $LASTEXITCODE
if (-not $br.WaitForExit(30000)) { "BR did not end: the script left the program waiting" }
exit $result
```

Each line of that is there for a reason:

- **`uitest` dials once and does not wait**, so it must start after BR has opened the channel. The
  token file appears when the channel opens. A token file left by a session that has died would be
  dialled and refused, so it is removed first.
- **Allow 90 seconds.** An interactive BR start can show a splash screen for about 20 seconds
  first. (It took 3 seconds in the measured runs.)
- **The script must drive the program to its end.** When `uitest` disconnects, the channel closes
  but the program is still waiting for input. If the script stops early, BR stays up. Do not
  force-kill it unless you must: a killed BR can leave its workstation slot taken, and the next run
  then fails during WSID assignment.
- **One connection per session.** The token is spent when `uitest` connects. To run several
  scripts, name them all in one `uitest` command, in order. A second `uitest` against the same
  session cannot get in.
- **User mode is enough.** Without `"DEVELOP"` as the third argument to `MSG("harness")`, keys go
  in only while a program is waiting for input, which is all a screen test needs. Use `DEVELOP`
  only if the script must type at `READY`. How a grant works is in
  [`BR_harness.md` §7](BR_harness.md#typing).
- **The procedure opens the channel, so `br_mcp_driver start` is not used here.** `start` claims
  the channel itself, and `uitest` would find nothing left to claim.

**`expect` and `absent` read the character cells**, as the `read_view` tool does, so they read
the program's screen only under `GUI OFF`, which is how this application runs
([`BR_harness.md` §0](BR_harness.md#the-one-thing) explains why). `field N spec` works in both
modes.

The steps:

| Step | What it does |
|---|---|
| `expect "text"` / `expect row N "text"` | the text must be on the screen, or on that row (rows count from 0). Retries for up to `--settle` seconds, 5 by default |
| `absent "text"` | the text must not be on the screen. Does not retry, so `wait` first if timing matters |
| `field N spec "C 30"` | control `N` must expect that spec |
| `type ACME` | type printable text |
| `press ENTER` / `press F1` / `press 13` | a named key, a function key, or a scancode. Also `SHIFT-UP`, `CTRL-END` and the like |
| `pace 300` | milliseconds between typed keys |
| `wait input` / `wait screen` / `wait 2` | until a program asks for input, until the screen settles, or for seconds |
| `grant?` / `screen` | record the grant state, or print the screen |

A failed check does not stop the script, so one run reports everything that is wrong. There are no
variables or loops: a test that needs them is a program, not a script. More about the format, and
the console-history steps, is in [`ai_access/README.md`](ai_access/README.md#4-uitest-a-screen-test-script).

<a id="live"></a>
## 5. Live session

For watching a program, exploring a screen, or finding out why a script fails. This is not a
repeatable test: you look and decide. It is all in [`BR_harness.md`](BR_harness.md), whose §9 is
the loop to follow; starting the session is in [`BR_launch.md`](BR_launch.md#harness-launch).

<a id="restricted"></a>
## 6. Restricted run

For a program a model has written. The `run_report` tool runs it in a restricted session, which
may write only files it creates and cannot run operating-system commands. `report_status` gives
the exit code: 0 for a clean run, 1 if the program would not load, and otherwise BR's error code
or the program's own `STOP` value. The program must number its lines from 10 up. Details are in
[`ai_access/README.md` §7](ai_access/README.md#7-run_report-running-a-program-in-a-restricted-session).

## 7. When something goes wrong

| You see | It means |
|---|---|
| `uitest: could not reach a BR session` | the channel was not open yet, or the token file was stale. Wait for the token file (§4) |
| a `type` or `press` step is refused | no grant; the procedure must call `MSG("grant", <seconds>)` |
| exit 99 from a headless run | an unattended fatal error; the `LOGGING` file names it (§3) |
| error 4215 from `PROC` | a POSIX path, usually from Git Bash; use PowerShell or cmd |

Problems in a live session, including a tool answering `ERR 4 unknown request`, are in
[`BR_harness.md`](BR_harness.md) §1 and §8.

Found anything here that is wrong or unclear? Put it in [`ERRORS.md`](../ERRORS.md) and tell the
user.
