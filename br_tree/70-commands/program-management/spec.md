---
title: Program management & procedures
file: spec.md
source: §Commands (System Entry/Exit, System Commands), §Procedures
category: 70-commands
subcategory: 70-commands/program-management
kind: spec
status: 2b           # reference base + br_tree fold (LOAD modes, CHAIN passing, CLEAR variants, GO form, MERGE, express procs); CHAIN/Procedure_files retained; no conflicts
recovered-fold: REPLACE (folded+pruned — source-vs-object/.BRS/.BRO rules, .BAK + OPTION 26, default-extension; verbatim retained on the BR wiki)
related: [file-directory, information, editing]
keywords: [RUN, LOAD, SAVE, REPLACE, MERGE, CLEAR, GO, EXECUTE, CHAIN, PROC, SYSTEM, SUBPROC, PROCERR, ALERT, FILES, ECHO, NOECHO, SOURCE, OBJECT, ONLY, NOSTEP, NOTRACE]
corrections:
  - "RUN syntax now shows the program name and the PROC option: `RUN [<program>] [PROC] [STEP|TRACE]`. Added a run-proc subsection giving the literal forms (`RUN <program> PROC`, or `LOAD <program>` then `RUN PROC`) and saying they work only inside a procedure. The page had described RUN PROC's effect and never its syntax. From BR 4.4 source: command9.cpp PROC_TYPE sets RUN_PROCIN and raises BREPROCPARAMETER (2103) when no proc is active. commandc.cpp RUN reads a first word that is an option (PROC among them) as that option, not a file name. Confirmed on brserver 4.33c with a probe: both forms gave PROCIN=1 and fed the LINPUT; plain RUN gave PROCIN=0; the startup argument `RUN <prog> PROC` gave 2103. Reported in context/lsp/ERRORS.md 2026-09-09."
  - "Eleven keywords added to the frontmatter: the CHAIN clause FILES, the commands SUBPROC, PROCERR and ALERT, and the qualifiers ECHO, NOECHO, SOURCE, OBJECT, ONLY, NOSTEP and NOTRACE. Every one is documented in this page's BNF or semantics and none was declared, so BR's own spelling of each reached nothing. Found in brls phase 13."
  - "CHAIN's backing/deep-reference page carried `kind: command` and lived under this
    70-commands subtree, but CHAIN is a **statement** (line-numbered, runs at RUN; every
    other 70-commands backing page is `kind: command`, and CHAIN was the one outlier). Moved
    the backing page to 10-language/flow-control/other-flow/CHAIN.md, alongside the other
    program-termination statements, and corrected its `kind:`. The CHAIN coverage on this
    page (BNF, semantics, examples) is unaffected and remains the authoritative summary —
    only the deep-reference link and the file's physical location changed."
  - "The CHAIN BNF ordered `FILES` ahead of the `MAT <array>`/`<var>` list, as
    `[, FILES] [, MAT <array>]… [, <var>]…`. BR does not enforce that position:
    `00010 chain A$, XXX, FILES` LOADs clean, confirmed directly. Rewritten as one
    repeating alternation, `[, { FILES | MAT <array> | <var> }]…`, so the clause may
    stand at any of the comma-separated positions. BR's own syntax table orders the
    units the same way the old BNF did, which is why the error stayed invisible: past
    the FILES unit, the repeating operand read the word as an ordinary variable *named*
    FILES, so a misplaced FILES was accepted for the wrong reason and anything reading
    the parse got a variable that does not exist. Whether BR accepts `FILES` more than
    once in one CHAIN was not tested, so the alternation neither permits nor forbids it
    deliberately. Found and fixed in brls (internal/parse/walk.go, matchUnit)."
---

# Program management & procedures

Loading, saving, running, and chaining programs, plus **procedure files** (command scripts).
Commands run immediately (no line number) and — crucially — from program code via
[`EXECUTE`](#execute). Line-editing commands are in [editing](../editing/spec.md); file/dir
commands in [file-directory](../file-directory/spec.md).

<a id="command-vs-statement"></a>
## Command vs statement

A **command** executes immediately when typed (no line number) and manages the environment
(`LOAD`, `SAVE`, `RUN`, `LIST`, `DIR`). A **statement** has a line number and runs at `RUN`.
Any statement can be run immediately as a command; a bare expression is an implied `PRINT`
(`6+4`→`10`). Commands can't appear in a program **except** via `EXECUTE` or inside a `PROC`.

<a id="entry-exit"></a>
## Entry & exit
```bnf
BR [<instructions>] [-<id>] [-<config>] [-<ref>]   -- start BR (optionally run a command / set WSID / config)
SYSTEM | SY                                         -- exit BR to the OS (closes files)
SYSTEM <integer>                                    -- exit to the OS, returning <integer> as the process exit code
SYSTEM LOGOFF                                        -- log the BR client off
SYSTEM [<flags>] "<os-command>"                      -- run an OS shell command, then return to BR
```

<a id="system"></a>
### SYSTEM — exit BR / call the OS shell
`SYSTEM` is a **command** (not a primary-op statement); a program reaches it via
[`EXECUTE`](#execute) or a `PROC`. Three forms:

- **Exit** — bare `SYSTEM` (`SY`) closes files and returns to the OS; `SYSTEM <n>` returns `<n>` as the
  process **exit code** (readable by a calling shell/script). `SYSTEM LOGOFF` logs the BR client off.
- **Shell call** — `SYSTEM "<os-command>"` runs an operating-system command (launch another program,
  run a script), then returns to BR — **the program's main way to invoke other applications through the
  OS.** This is consequential for app development and for security review (it executes arbitrary OS
  commands with the caller's privileges).

**Shell-call flags** precede the command string and are **case-sensitive** (an unknown flag → error
**4501**; conflicting flags → *flag-conflict* error):

| Flag | Effect |
|---|---|
| `-@` | run the command on the BR **client** side |
| `-S` / `-s` | run on the BR **server** side (default follows the `SHELL DEFAULT CLIENT`/`SERVER` config) |
| `-R` / `-r` (or leading `*`) | **restore** the BR screen after the call |
| `-C` / `-c` | **continue asynchronously** — don't wait for the command to finish (conflicts with `-R`) |
| `-M` / `-m` | **hide** / **minimize** the launched program's window |
| `-H` / `-h` | **hide** / **minimize** BR's own window during the call |
| `-W` / `-w` | a **Windows** program is being launched (conflicts with `-R`) |
| `-E` / `-e` | permit a shell-call **error** to be reported/trapped |
| `-P` / `-p` | page |
| `-T`/`-t<secs>` | override the shell-call **timeout** |
| `+<n>` | request `<n>` of memory for the child |

(`SYSTEM ONQ …` invokes the built-in ONQ interface rather than a generic shell command.)

<a id="program-commands"></a>
## Program lifecycle commands
| Command (abbrev) | Action |
|---|---|
| `LOAD f [SOURCE\|OBJECT]` (LO) | clear memory, load `f`; see [loading](#loading) for modes & extensions |
| `SAVE f [SOURCE]` (SA) | save to a **new** file (error 4150 if exists) |
| `REPLACE [f]` (REP) | overwrite an existing file (keeps a `.bak`) |
| `RUN [<program>] [PROC] [STEP\|TRACE]` (RU) | execute from the lowest line (resets vars); with `<program>`, load it first. `PROC` takes input from the running procedure (see [run-proc](#run-proc)); STEP/TRACE → [information](../information/spec.md) |
| `MERGE f [-<from>] [-<to>] [<first>\|ADD]` (ME) | merge program lines from a file (see [merge](#merge)) |
| `CLEAR [PROC\|RESIDENT\|ALL]` (CL) | clear program/vars/procedures/libraries (see [clear](#clear)) |
| `GO [RUN][STEP][TRACE][.<line>]` | resume / step a halted program (see [go](#go)); `GO END` terminates it |
| `STOP` | halt execution (also a statement) |

<a id="loading"></a>
### Loading & the default extension
`LOAD` (`LO`) clears memory, then loads. **`SOURCE`** loads an ASCII `.brs` program line-by-line as
if typed (syntax-checked per line; on a syntax error BR halts for a fix — unless `PROCERR RETURN` is
active in a procedure, which instead returns the code in `ERR` and the failing line in `LINE` so a
`SKIP` can test it). **`OBJECT`** loads the `.bro` object; **`RESIDENT`** loads the file as a
resident library. **The mode is set by the keyword, not inferred from the extension:** `LOAD` defaults
to object, so loading a source program **requires an explicit `SOURCE`** — `LOAD "prog.brs" SOURCE`.
Naming the `.brs` file alone (`LOAD "prog.brs"`) does *not* trigger source mode; BR tries to read it
as an object file and fails. Extension search: a bare name tries `.BR` then `.BRO` (`.BRS` for
`SOURCE`), overridable via `CHAINDFLT` in
[BRConfig.sys](../../00-configuration/config-directives/spec.md); a **trailing period**
(`LOAD NAME.`) suppresses the search and loads the name as-is. A failed `LOAD` leaves memory intact.

<a id="merge"></a>
### MERGE
`MERGE f [-<from>] [-<to>] [{<first>|ADD}]` (syntax mirrors `RENUM`) pulls lines from another `.br`
into memory. With no `first`/`ADD`, merged lines keep their numbers and **replace** any existing
lines that share them. `ADD` appends all lines after the current program's last line; `<first>`
renumbers the first merged line (others follow the source increments). A single line number merges
only that line.

<a id="replace"></a>
### SAVE / REPLACE — source vs object
`SAVE` writes a **new** file (error 4150 if it exists); `REPLACE` overwrites an **existing** one and
leaves the lines in memory. Both save **source** only when the name ends `.BRS` or the **`SOURCE`**
keyword is given; otherwise they save **object** (`.BR`/`.BRO`). With no filename, `REPLACE` reuses the
file's full original name (a trailing period suppresses the default extension). **`OBJECT`** (`.BRO`)
omits source — *unrecoverable*, used to ship protected code. Before overwriting, BR copies the original
to **`.BAK`** (recoverable until the next `REPLACE`); **`OPTION 26`** suppresses `.BAK` creation. End
execution before `REPLACE`; to save without ending, `LIST >tmp` then `LOAD` it from source.

<a id="clear"></a>
### CLEAR
`CLEAR` (`CL`) with no argument clears the program for new entry. `ALL` ends the program, closes all
procedures and clears memory. `PROC` closes all procedures but **keeps** memory (variables remain
for debugging); `PROC ONLY` additionally keeps the program running. `RESIDENT` clears all resident
libraries (`"name"` clears one); adding `STATUS` instead *demotes* resident → present rather than
unloading. `CHAIN` and `LOAD` perform an implicit `CLEAR`.

<a id="go"></a>
### GO — resume / step
`GO [RUN] [STEP|NOSTEP] [TRACE [PRINT]|NOTRACE] [.<line>]` resumes a halted/interrupted program with
all variables and open files intact. `RUN` first clears prior STEP/TRACE settings; `STEP` pauses
before each action statement, `TRACE` echoes line numbers (`PRINT` → printer). `GO <line>` resumes
*at* a line; **`GO .<line>`** runs *until* a line then issues a STEP interrupt (`GO .5280:2` stops
before line 5280 clause 2; a bare `GO .` reuses the last temp breakpoint; `GO` with no period clears
it). After an error, `GO` retries the failing statement. In STEP mode, Shift+F1–F5 step with
widening scope (into-clause / over-clause / into-line / over-line / to `RETURN`|`FNEND`).
**`GO END`** terminates the interrupted program and closes all files.

<a id="execute"></a>
## EXECUTE — run a command from code
```bnf
EXECUTE "[*]<command-string>"
```
Runs any command/statement string at runtime — the bridge that makes commands part of the
coding surface (build index files, run a SORT, start a PROC, …). A leading `*` suppresses screen
restoration (the default does **not** restore the screen). Inspect
[`CODE`](../../10-language/data-manipulation/system-functions/spec.md#system-info) afterward for a
procedure's return value. **Restrictions:** because it is illegal to *terminate* a program from
`EXECUTE`, the program-ending commands `LOAD`, `SAVE`, `REPLACE` and the `CHAIN` statement may not
be used inside it. This `LOAD` restriction applies to a `LOAD` that replaces the running program;
`LOAD ...,RESIDENT` (loading a resident library) does not terminate the current program and is
allowed. `INDEX`/`SORT` *can* be started from `EXECUTE` (no prior `CLEAR`, so less memory
— may run slowly; out-of-memory → error `7607`/`7811`). All errors (including command syntax
errors) are passed back, trappable with `ERROR`/`IOERR`/`Exit`; an `EXECUTE` may itself be the
subject of another `EXECUTE`.

<a id="chain"></a>
## CHAIN — end this program, start another
```bnf
CHAIN { "<program>" | "PROC=<name>" | "SUBPROC=<name>" } [, { FILES | MAT <array> | <var> }]…
```
`CHAIN` (a statement) ends the current program and loads/runs another program, or starts a
procedure. By default it **closes all files** (except procedure files) and resets the new program's
variables; **`FILES`** keeps files open at their current positions (pointers are *not* moved — use
`RESTORE` to reposition), and trailing `MAT array`/`var` names carry those values into the chained
program (dimensions needn't match; the caller's win). `FILES` may stand at any of those
comma-separated positions, not only the first — `chain A$, XXX, FILES` is accepted. The
program name follows the same default extension rules as `LOAD` (`.BR`→`.BRO`, `CHAINDFLT`).
`"PROC=…"` ends the program and starts a
procedure (closing the lowest active proc first); `"SUBPROC=…"` starts a **nested** procedure
without disturbing the running one — both keep the terminated program in memory so its variables
stay available to the procedure. `CHAIN "PROC=XYZ"` is like `EXECUTE "PROC XYZ"` except `CHAIN`
ends the program. (Deep reference, incl. the 11 technical notes:
[CHAIN](../../10-language/flow-control/other-flow/CHAIN.md) — filed alongside the other
program-termination statements since CHAIN is a statement, not a command.)

<a id="procedures"></a>
## Procedure files
A **procedure** is an ASCII (DISPLAY) text file of commands run in order — one command per line,
`!` comments, `:label` branch targets, no line numbers, up to 800 chars/line. A `.$$$` extension
makes it **self-deleting** after execution.

<a id="proc"></a>**Starting**: `PROC {name|*name|ECHO|NOECHO}` (runs it; `*` suppresses F2 logging;
NOECHO hides lines). `SUBPROC file` runs a **nested** procedure (up to 9 deep) then resumes.
From code: `CHAIN "PROC=…"` / `CHAIN "SUBPROC=…"` (ends program) or `EXECUTE "PROC …"` (keeps
program running). `RUN PROC` feeds procedure lines to a program's `INPUT`/`LINPUT`.

<a id="run-proc"></a>**`RUN … PROC`** — `PROC` is an **option of `RUN`**, not a command. It is not
followed by a file name: the lines fed to the program are the ones that follow the `RUN` line in
the procedure that is *already running*. Two forms work, both only as lines **inside a procedure**:

```
RUN <program> PROC           ! load <program>, then run it with proc-fed input
LOAD <program>               ! or: load first ...
RUN PROC                     ! ... then run what is in memory with proc-fed input
```

- **Outside a procedure** (typed at READY, or as the startup command-line argument)
  `RUN … PROC` fails with error [2103](../../90-reference/error-codes/2103.md), "illegal PROC
  parameter".
- **`RUN PROC <file>` does not name a proc file.** `RUN`'s first word is checked against its
  options before being read as a program name, so `PROC` is taken as the option and no program is
  loaded. `<file>` never becomes a program name. With nothing in memory, BR reports error 2104
  (no active lines).
- **A plain `RUN` inside a procedure does not feed it.** `PROCIN` stays 0 and the program reads
  the keyboard; under `UNATTENDED` logging it aborts at its first input statement.
- **How the lines are used.** Each input statement consumes the next proc line. When the program
  ends, the following proc lines are commands again. Confirmed on 4.33c.
- **The `RUN … PROC` line must not be the proc's last line.** See [look-ahead](#look-ahead).

**Flow & errors**: `SKIP n|:label [IF <cond>]` branches; `PROCERR STOP` (default) halts on error,
`PROCERR RETURN` continues (sets `ERR`); `ALERT msg` pauses for the operator (`GO` resumes; under
`PROC NOECHO` the message shows but the operator must press F2/F3 to see the *command* — bracket
`ALERT` with `PROC ECHO`…`PROC NOECHO`); `CLEAR PROC` / `CLEAR ALL` close procedures.

<a id="look-ahead"></a>**Look-ahead close**: BR closes a procedure *before* executing its **last
line**, so that line behaves as an independent one-line command — it **cannot** be a `SKIP` that
branches backward or a `RUN PROC` (the file is already closed), and shouldn't be error-prone; add a
blank/comment line if you need the proc to stay open. This look-ahead is what lets a `.$$$` proc (or
one whose last line is `FREE`) delete itself, and avoids stacking an extra open file. Each active
procedure counts as one open file; nesting goes 9 deep (status-line columns 58–59 show `P1`…`P9`),
and `RUN PROC` feeds procedure lines to a program's `INPUT`/`LINPUT`/`RINPUT` — **one proc line per
input statement** (too many/few lines causes unpredictable misreads; `PROCIN` →
[information](../information/spec.md#procin-program) tells the program input is coming from a proc).

<a id="express"></a>**Express procedures** run *during* a program via `EXECUTE "PROC …"` /
`"SUBPROC …"` (or operator-keyed during an interruption): they imply `NOECHO`, are subordinate to
the running program, and resume it when done. An error in an executed express proc closes the proc
and returns to the `EXECUTE` statement's error trap. `EXECUTE "PROC XYZ"` cancels the
last-activated proc (and ends any `RUN PROC` input mode); `EXECUTE "SUBPROC XYZ"` preserves the
hierarchy (and keeps `RUN PROC` active). A program can shed one procedure layer by running an empty
express `PROC`. The full procedure-system reference (start methods, syntax rules, express-vs-standard
chart) is retained in [Procedure_files](Procedure_files.md).

<a id="examples"></a>
## Examples

```business-rules
04200 EXECUTE "PROC DAILY"            ! start a procedure, program keeps running
99000 EXECUTE "INDEX ACCT.INT ACCT.KEY 1 4 REPLACE"
00900 CHAIN "proc=MONTHEND"           ! end program, run procedure
```

A procedure that runs a program with its input supplied (`PROCIN` returns 1). Start it with
`PROC nightly.prc`. The program's first input statement reads `FIRST-ANSWER` and its second
`SECOND-ANSWER`. When the program ends, `SYSTEM` runs as an ordinary command:

```
RUN myprog PROC
FIRST-ANSWER
SECOND-ANSWER
SYSTEM
```
```text
! procedure: purge deleted records safely (multi-user)
PROCERR RETURN
PROTECT CUST.FIL,RESERVE
SKIP BUSY IF ERR<>0
COPY CUST.FIL TEMP[WSID].FIL -D
RENAME TEMP[WSID].FIL CUST.FIL
PROTECT CUST.FIL,RELEASE
SKIP DONE
:BUSY
ALERT File is busy, try again later -- type GO
:DONE
RUN MENU
```

<a id="see-also"></a>
## See also

- [editing](../editing/spec.md) — `AUTO`/`RENUM`/`DEL`/`LIST` line editing
- [file-directory](../file-directory/spec.md) — `COPY`/`RENAME`/`FREE`/`CHDIR` used in procedures
- [information](../information/spec.md) — `RUN STEP/TRACE`, `DISPLAY`, `BREAK` debugging
- [50-libraries/library-facility](../../50-libraries/library-facility/spec.md) — `LIBRARY` (vs `CHAIN`)
- [information](../information/spec.md#break) — `BREAK` breakpoints (folded there)
- [other-flow](../../10-language/flow-control/other-flow/spec.md#termination) — `STOP`/`END`/`PAUSE`,
  `CHAIN`'s sibling program-termination statements
- Backing keyword pages retained (deep reference):
  [CHAIN](../../10-language/flow-control/other-flow/CHAIN.md) (11 technical notes; relocated there
  because CHAIN is a statement, not a command — see that page's `corrections:` note),
  [Procedure_files](Procedure_files.md) (the full procedure-system reference)

*(Backing pages `LOAD`, `MERGE`, `GO`, `Go_End`, `CLEAR`, `EXECUTE`, `PROC`, `Procedure_Commands`,
`Program_Management_Commands`, `Alert` were folded into this spec and pruned; `Break_(Command)` was
folded into [information](../information/spec.md#break).)*
