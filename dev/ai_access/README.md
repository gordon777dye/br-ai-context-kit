# br_mcp_driver

`br_mcp_driver.exe` connects an AI assistant, such as Claude or Codex, to a running BR 5.0
session. It uses no language interpreter and needs no toolset installed. This file is the  
reference for anyone using AI for writing, running or testing BR programs (`.brs`): its 
modes, its tools, its rules, and the standard procedures in [`prc/`](prc/).

## 1. What it is for: three scenarios

The driver serves BR in three situations. They differ in who is at the keyboard, and in whether
the driver calls a model or the assistant already has one.

1. **An assistant helping a developer.** The assistant has its own model, so the driver calls
   none. `start` brings up a `DEVELOP`-mode session, or `serve` serves one that BR opened itself,
   and the assistant's own `connect` reaches it. The assistant reads the screen, checks source,
   runs commands inside an open turn, and types with the keyboard the procedure lent it.
   Testing a changed program is this scenario.
2. **An assistant working alongside an end user.** The same machinery as scenario 1, but
   `start --user` runs the session in user mode. The keyboard is lent for an hour, keys go in
   only while a program is waiting for input, and BR stops and asks the person before an
   operating-system command or a destructive file operation.
3. **An application that uses AI for its users and programs.** A person types `AI <text>` at
   `READY`, or a program asks for something: `EXECUTE "AI ..."`, or agentlib's `FNAGENT_CODE` for
   a program to be written. The driver calls the model itself: `chat` answers the console, and
   `report` writes BR programs for the application, which `run_report` runs in a restricted
   session (§7, §9). No assistant is involved.

`uitest` (§4) and `watch` use the same channel as scenarios 1 and 2, and call no model.

**Start somewhere else if you have a task:**

| To | Read |
|---|---|
| test a changed program: check it, run it headless, script a screen test, or watch it live | [`../BR_testing.md`](../BR_testing.md) |
| set up and start a session with an assistant attached | [`../BR_launch.md` — Live sessions](../BR_launch.md#harness-launch) |
| read and type into a running program's screen | [`../BR_harness.md`](../BR_harness.md) |

Once attached, **call the `guide` tool first.** It gives the order of operations, the grant and
the turn in full, the ways BR differs from other BASICs, and the list of reference topics and data
files the other tools can answer for.

## Contents

- [1. What it is for: three scenarios](#1-what-it-is-for-three-scenarios)
- [2. Files and settings](#2-files-and-settings)
- [3. Modes](#3-modes)
- [4. `uitest`: a screen test script](#4-uitest-a-screen-test-script)
- [5. The tools](#5-the-tools)
- [6. What an assistant may do](#6-what-an-assistant-may-do)
- [7. `run_report`: running a program in a restricted session](#7-run_report-running-a-program-in-a-restricted-session)
- [8. The standard procedures](#8-the-standard-procedures)
- [9. Modes that call a model: `chat` and `report`](#9-modes-that-call-a-model-chat-and-report)
- [10. Error numbers and exit codes](#10-error-numbers-and-exit-codes)
- [11. Further reading](#11-further-reading)

## 2. Files and settings

| File | What it is |
|---|---|
| `br_mcp_driver.exe` | the driver |
| `brls.exe` | the BR syntax checker; the `check_source` tool runs it |
| `prc/BR_dev.prc`, `prc/BR_user.prc` | the procedures `start` launches BR on. **Copy them into BR's start folder** ([`BR_launch.md`](../BR_launch.md#the-procedure-has-to-sit-in-brs-start-folder)) |
| `prc/BR_report.prc` | the procedure `run_report` runs. **Copy it into the folder `run_report` runs in** (§7) |

BR itself (`brserver-x64-Release.exe`) is in [`../tools/`](../tools/), not here.

The driver reads these settings. A flag has precedence over an environmental variable.

| Setting | Used for | Without it |
|---|---|---|
| `--br`, then `$BRSERVER`, then `$BR_EXE` | the BR that `start` and `run_report` launch. The first variable that is set decides, even if what it names is missing | `brserver.exe` beside the driver, then `PATH`; neither is shipped, so `start` refuses |
| `--config`, then `$BR_AI_USER` | the configuration file `start` gives BR, named in full | BR finds a `brconfig.sys` of its own, with the wrong `DRIVE` mappings and no `LOGGING`. Nothing warns you |
| `$BRLS` | a different `brls.exe` | `brls.exe` beside the driver, then `PATH` |
| `$BR_CONTEXT_KIT`, or `--kit` for `report` | the kit folder, for `get_reference`, `get_layout` and the catalogue in `guide` | `C:\ADS\qsmrp\context` |
| `--port` | which session to reach | the port in the session's token file. Needed only with more than one session open |

The driver checks a named BR or configuration file before it launches BR, and refuses a missing
one by name.

**How a session is found.** A BR session that opens its channel writes its port and a token to
`%LOCALAPPDATA%\ADS\harness.token`. The first client to connect uses the token up and the file is
removed. A session therefore accepts **one connection**: when that client disconnects, the channel
closes, and only `MSG("harness", port)` inside BR opens it again.

## 3. Modes

The first argument picks the mode.

| Command | What it does |
|---|---|
| `br_mcp_driver start [--user] [--config F] [--br PATH] [--port N] [--pipe NAME] [--wait D]` | launch BR on `BR_dev.prc` (or `BR_user.prc` with `--user`), claim the channel it opens, and serve it to `connect` |
| `br_mcp_driver serve [--port N] [--pipe NAME] [--ready-file PATH]` | claim a channel a BR session opened itself, and serve it |
| `br_mcp_driver connect [--pipe NAME]` | what an assistant launches as its MCP server: a relay onto the pipes `start` or `serve` holds |
| `br_mcp_driver uitest <script>... [--port N] [--settle SECONDS]` | run screen test scripts against a session (§4) |
| `br_mcp_driver watch [--port N] [--events "..."] [--seconds N] [--quiet D]` | print the session's events as they arrive. The default events are `INPUT SCREEN GRANT KEYSDONE NOTE CLOSING` |
| `br_mcp_driver tools` | print the published tool list, as JSON, with no session |
| `br_mcp_driver chat ...` | answer the `AI` command at BR's console (§9) |
| `br_mcp_driver report ...` | write the BR program an application asks for (§9) |

### `start`

`start` takes no BR command; BR always starts on the standard procedure. It removes a stale token
file, launches BR detached, waits for the channel, and prints three lines worth reading, because
they say which configuration and which BR it got:

```
configuration from BR_AI_USER: context\dev\tools\brconfig.ai_user
BR started from context\dev\tools\brserver-x64-Release.exe (pid 26860) on BR_dev.prc; waiting for the channel
harness claimed on port 8720, protocol 5
```

A protocol below 5 means an old BR that lacks several requests; see
[`BR_harness.md` §1.1](../BR_harness.md#setup).

BR's own screen goes to its window and its diagnostics to the `LOGGING` file, not to the shell.
To end the session, close BR, or type `LET X=MSG("harness",0)` in it.

### `serve` and `connect`

The assistant's configuration is always the same:

```json
{
  "mcpServers": {
    "br": { "command": "C:\\path\\to\\br_mcp_driver.exe", "args": ["connect"] }
  }
}
```

or `claude mcp add br -- br_mcp_driver connect`. `connect` holds no connection or credential, so
the assistant can restart it at any time. `start` or `serve` holds the one connection to BR for
the life of the session.

Use `serve` when a BR program opens the channel itself:

```
LET X=MSG("harness", 8720)
EXECUTE "SYSTEM -@ -C -W -M br_mcp_driver serve"
```

One assistant at a time: a second `connect` is told `another assistant is already attached`.

## 4. `uitest`: a screen test script

A script says what should be on a screen, what to type, and what should come up. `uitest` runs
it and exits **0** if every check passed, **1** if one failed or no session could be reached, and
**2** for a usage error. Its last line is `<n> checks, <m> failures`. A failed `expect` prints the
screen. **[`BR_testing.md` §4](../BR_testing.md#uitest) has a complete, tested example**: the
procedure that opens the channel, the script, and the PowerShell that runs them.

```
# the order entry screen, and what a bad code does
expect row 0 "ORDER ENTRY"
expect "Customer code:"
absent "Customer not found"
field 0 spec "C 8"
type ACME
press ENTER
expect "Customer not found"
```

| Step | What it does |
|---|---|
| `expect "text"` / `expect row N "text"` | the text must be on the screen, or on row `N` (rows count from 0). Retries for up to `--settle` seconds, 5 by default |
| `absent "text"` | the text must not be on the screen. Checked once, so `wait` first if timing matters |
| `field N spec "C 30"` | control `N` must expect that spec. Retries like `expect` |
| `type ACME` | type printable text. Needs the grant |
| `press ENTER` / `press F1` / `press 13` | a named key, a function key (`F1` to `F99`), or a scancode. Needs the grant |
| `pace 300` | milliseconds between typed keys |
| `wait input` / `wait screen` / `wait 2` | until a program asks for input, until the screen changes and settles, or for seconds |
| `view offset N` / `view` | the console history view must be at offset `N` / report the offset and lines held |
| `grant?` / `screen` | record whether the script may type / print the screen |

The named keys are `ENTER` (`RETURN`), `TAB`, `BACKTAB`, `BACKSPACE`, `ESC` (`ESCAPE`), `UP`,
`DOWN`, `LEFT`, `RIGHT`, `HOME`, `END`, `INSERT`, `DELETE`, `PAGEUP`, `PAGEDOWN`, `HELP`, `UNDO`,
`FIELDPLUS`, `FIELDMINUS`, `UPFIELD`, `DOWNFIELD`, `BREAK`, `COPY`, `PASTE`, `CUT`, `WHEELUP`,
`WHEELDOWN`, the `SHIFT-` forms of the arrows, `ENTER`, `HOME`, `END`, `PAGEUP` and `PAGEDOWN`,
and `CTRL-HOME` and `CTRL-END`.

Rules for scripts:

- **A failed check does not stop the script**, so one run reports everything that is wrong.
- **No variables, loops or conditions.** A test that needs them is a program.
- **Name every script in one command.** The session accepts one connection, so a second `uitest`
  cannot get in.
- **`uitest` connects once and does not wait for the session.** Start it after BR has opened its
  channel, which is when the token file appears.
- **The script must take the program to its end.** When `uitest` disconnects, the program is still
  waiting for input, and BR stays up until something answers it.
- **`expect` and `absent` read the character cells**, which hold the program's screen under
  `GUI OFF`. Under `GUI ON` they hold the Command Console instead. `field` works in both.
- Typing needs a grant, which only the session can give, with `MSG("grant", <seconds>)`.

## 5. The tools

These are the tools an assistant gets through `connect`. `br_mcp_driver tools` prints the current
list with each tool's full description. **The descriptions carry every limit, error and refusal**,
so read them rather than guessing.

| Tool | Arguments | What it does |
|---|---|---|
| `guide` | | the server as a whole, in one answer. Call it first |
| `read_view` | `offset` | the screen as shown: live rows and any history the person scrolled back to, each marked `LIVE` or `HISTORY` |
| `read_history` | `count`, `first` | console output that has scrolled off, newest first. `GUI ON` only (§6) |
| `controls` | | the fields and buttons, with the scancode that presses each |
| `grid` | `control`, `first_row` | the cells of a grid, 200 rows a page |
| `list` | `control`, `first_row` | the rows of a list or combo box |
| `attrs` | | how the screen is painted: highlighted, reversed, underlined, error colours |
| `cursor` | | where the cursor is |
| `field_info` | `control` | what an input field expects: spec (`C 30`, `N 10.2`), picture, lengths, protection. Only while a program waits for input |
| `windows` | | BR's windows, and which can be pictured. Its `cells` flags show whether the session is `GUI ON` or `GUI OFF` |
| `shot` | `mode`, `window` | a PNG of a window: its character cells, or the whole window as Windows draws it |
| `program` | | the loaded program: full path, size, `source` or `object`, `clean` or `edited` |
| `listing` | | the loaded program as BR holds it, written to a file to open — for a chained program, a library, or edited source |
| `grant_state` | | whether the assistant may type, and for how long |
| `pending` | | how many of the assistant's keys are still waiting to go in |
| `release` | | give the keyboard back, discarding queued keys |
| `wait_for_event` | `event`, `seconds` | block until BR reports something, instead of polling |
| `check_source` | `source` or `path` | run `brls -check -sema` on source text or a file, and return its words unchanged |
| `command` | `line` | run one line at BR's console during a turn, and wait for its result (§6) |
| `questions` | | what the session is waiting for an answer to, and where a delivered program will be written |
| `get_layout` | `file` | one data file's record layout from the application's data dictionary |
| `get_reference` | `topic` | the reference for one BR statement or topic |
| `deliver_source` | `question_id`, `source` | give BR a whole program for a question the session opened. Audited first (§6) |
| `send_message` | `question_id`, `text` | give BR a long text for a program to show |
| `run_report` | `program`, `dir`, `procedure`, `config`, `seconds`, `wbserver` | run a program in a restricted session (§7) |
| `report_status` | | how the last `run_report` went, and its exit code |
| `pace` | `ms` | the delay between typed keys. Needs the grant |
| `keys` | `text` | type text. Needs the grant |
| `press` | `scancode` | send one key. Needs the grant |

**Which tool reads the program's screen depends on the session's GUI mode:** `read_view` under
`GUI OFF`, `controls` under `GUI ON`. See [`BR_harness.md` §0](../BR_harness.md#the-one-thing).

**A tool that answers `ERR 4 unknown request`** is one this BR is too old for. The driver
publishes every tool whatever BR it is attached to.

**Writing a program for the session**, the order is `questions` → `get_layout` for every file the
program opens → `deliver_source` → `command` to `LOAD` and `RUN` the path `questions` reported.
Build every `FORM` from `get_layout`, never from field names.

## 6. What an assistant may do

**Reading needs nothing.** Every tool that reads works without a grant.

**Typing needs a grant**, which a person or procedure gives inside the session with
`MSG("grant", <seconds>)`. A negative number lends the keyboard with no expiry; `0` takes it back.
The assistant cannot give, raise or extend a grant (a line it sends that tries is refused with
4166). It can hand one back with `release`.

**Where keys go depends on how the channel was opened.** In user mode (`MSG("harness", port)`)
keys go in only while a program is waiting for input, never at `READY`. In `DEVELOP` mode
(`MSG("harness", port, "DEVELOP")`) they also go in at `READY`. Only BR can choose `DEVELOP` mode.
A user-mode session also raises the AI-user-mode flag when the assistant connects, so any BR
session started while it is up runs restricted.

**`command` needs an open turn.** A turn opens when a person types `AI <text>` and BR waits for
the answer. `command` returns BR's error number for the line (0 for success) and BR's message. It
returns when the work is finished: a `RUN` returns when the program stops.

- **Read the message even when the number is 0.** A program that handles its own error still
  returns 0. A program that ends with `STOP <n>` returns `the program stopped with CODE <n>` in
  the message. That code is the program's own verdict, not a BR error number.
- **Destructive file operations ask the person** at the console: yes, no, or yes for the rest of
  the turn. A refusal is 4167. A grant does not change this.
- **`SYSTEM` with an operating-system command, a spool command, the terminal's shell escape, and
  `EDIT` ask the operator** while an assistant is attached, whoever typed them. A refusal is 4167.
  A site can turn this question off with `OPTION 83` in the configuration file; `CONFIG OPTION 83`
  is refused with 4172.
- **The powerful `CONFIG` operations are refused** with 4168.
- **A turn cannot open over a running program or procedure** unless it set
  `SETENV("AI_TURN_OK","Y")`; otherwise 4169. A line from the assistant cannot set it (4170).
- **Inside a turn, `PROC <file>` pushes**, like `SUBPROC`, so the procedure that allowed the turn
  survives. **`CLEAR PROC` and `CLEAR ALL` end the turn**, and the command returns -1.
- **The `AI` command is refused** from the assistant, with 4171.

**`deliver_source` is audited before anything is sent.** Line numbers must ascend and be unique;
`brls` must report no error; a data-dictionary file may be opened only after `get_layout` for it;
each `FORM` is compared with that layout; and statements a restricted session refuses (`DLL(`,
`SYSTEM` with a command) are refused here. A failed delivery is not sent, and the reasons come
back. A delivery is accepted only for a question a running program opened, so it needs no grant.
BR writes the program to the path `questions` reported; nothing runs it until a person or a
`command` says so.

**`deliver_source` and `send_message` carry printable ASCII only**, up to 256 KB. The driver names
any character it will not send, such as a curly quote or a dash.

**Under `GUI OFF` the console history is withheld.** An application in `GUI OFF` paints its forms
on the console, so the history holds the records the person has looked at. `read_history` is
refused (error 9) and `read_view` returns its `HISTORY` rows blank. The live screen stays
readable. Under `GUI ON` both work normally.

## 7. `run_report`: running a program in a restricted session

`run_report` runs a program a model wrote, after it has passed `check_source` and a person has
approved it. It writes a one-line `loader.prc` into `dir`, starts
`brserver --restricted proc <procedure>` there, and **returns at once**. `BR_report.prc` must
already be in `dir`; the tool refuses to run without it. `report_status` gives the
exit code when the run ends.

A restricted session may write only files it creates, cannot run `SYSTEM` commands or `DLL(`, and
reads only what a `brrestrict.sys` beside BR permits; with no such file it reads anything. So the
tool needs no grant. Each run is logged by BR to `restricted-<wsid>.log` in
`%LOCALAPPDATA%\ADS`. A `LOGGING` line in the run's configuration is refused.

| Argument | Meaning |
|---|---|
| `program` | the program to run. **It must number its lines from 10 up**: `BR_report.prc` adds lines 1 to 3 as an error trap |
| `dir` | the folder BR runs in, which gets `loader.prc`. Every other name is relative to it. Default: the folder the driver runs in |
| `procedure` | the procedure, relative to `dir`. Default `BR_report.prc`. An absolute path is refused, because BR then sits at the console and runs nothing |
| `config` | a configuration file for the session |
| `seconds` | the time limit, 300 by default. The session is killed at the limit. 0 is refused |
| `wbserver` | the folder of the `wbserver.dat` the site's other sessions share, so the run takes part in their record locking. Not defaulted |

One run at a time; a second while one is running is refused.

**Exit codes**, from `report_status`:

| Code | Meaning |
|---|---|
| `0` | the program ran and ended normally |
| `1` | the program would not load |
| other | BR's error code for an untrapped error (for example 4152, file not found), or the value the program gave `STOP` |

**Read the exit code as a 32-bit number.** A POSIX shell keeps only the low byte, so 4152 reads as
56 there and 605 as 93.

## 8. The standard procedures

| Procedure | Session | Channel | Grant | Started by |
|---|---|---|---|---|
| `BR_dev.prc` | ordinary | `DEVELOP` mode, port 8720 | keyboard, no expiry | `br_mcp_driver start` |
| `BR_user.prc` | ordinary | user mode, port 8721 | keyboard, one hour | `br_mcp_driver start --user` |
| `BR_report.prc` | **restricted** | none | none | the `run_report` tool |

A procedure echoes every line as it runs, comments included, so the comments in these files are
what the operator sees, and they say how to take the keyboard back or send the assistant away.

**`BR_report.prc`** runs `SUBPROC loader.prc`, whose one line is a literal
`LOAD "<program>" SOURCE`. It then adds this trap before `RUN`:

```
 1 ON ERROR GOTO TRAP : GOTO 3
 2 TRAP: STOP ERR
 3 !
```

An untrapped error therefore ends the program with its error number in `CODE`, and the procedure
exits BR with that number. Without the trap, an error would leave the session at `READY` with
nobody to answer it.

To bring up a session of your own for a test, write a procedure that opens the channel, gives a
grant and runs the program: [`BR_testing.md` §4](../BR_testing.md#uitest).

## 9. Modes that call a model: `chat` and `report`

These two modes call a model themselves. Every other mode serves an assistant that already has
one.

### `chat`: answering the `AI` command

```
br_mcp_driver chat [--port N] [--model NAME] [--via api|cli|echo] [--ready-file PATH] [--no-tools]
```

`chat` answers each `AI <text>` typed at the console, printing the reply in the `HILITE`
attribute. A line of the reply that starts with `> ` runs as a command, shown as `[AI] >`. A
program can ask too, with `SETENV("AI_TURN_OK","Y")` then `EXECUTE "AI <text>"`; the reply is fed
to the program as keyboard input. With nothing listening, `AI` fails at once with 4158. Up to two
requests wait behind one in progress; a fourth is refused.

| `--via` | Uses | The model can read the session |
|---|---|---|
| `api` | an API key | yes, with the reading tools, unless `--no-tools` |
| `cli` | the Claude Code CLI's own claude.ai login (`claude auth login`, done once by a person) | no, prose only |
| `echo` | nothing; answers locally | n/a |

Without `--via`, the driver uses `api` if there is a key, and otherwise `cli`. It says which it
used when it starts. A turn has 100 seconds and twelve passes; BR's console gives up at 120.

**The API key** comes from `ANTHROPIC_API_KEY`, or from the Windows Credential Manager, never from
a file. To store it:

```
cmdkey /generic:br_mcp_driver /user:api /pass
```

`/pass` with no value asks for the key, so it stays out of the shell history. Do not store a
`claude setup-token` token there: it is not an API key and fails with a 401.
`ANTHROPIC_BASE_URL` sends requests to a gateway instead.

`--ready-file` is written once `chat` is listening and removed when it exits, so a BR program can
tell when someone may type `AI`.

### `report`: writing a program for an application

```
br_mcp_driver report [--port N] [--kit DIR] [--model M] [--echo] [--once] [--ready-file PATH] [--quiet]
```

An application asks with agentlib's `FNAGENT_CODE`, which opens a question with
`MSG("agentask", id$, "CODE")` and announces it with a `NOTE`. `report` reads the question off the
screen, writes the program with the model, and answers with one `SOURCE` delivery. It runs
nothing: agentlib's `FNAGENT_SHOW` asks a person to approve the program, and `run_report` runs it.

The model gets three tools: `get_layout`, `get_reference`, and `check_syntax`, which runs `brls`.
Its first pass must call one of them. The same audit as `deliver_source` (§6) applies, and also
refuses a program that opens the application's own data for output or update. It needs an API
key; `--echo` returns a canned program and calls no model.

**Start `report` before the program asks.** A question announced while nothing is listening is
lost, and the program waits out its own timeout. `report` retries its connection for 60 seconds,
so it can be started first, and `--ready-file` tells a program when it is listening.

## 10. Error numbers and exit codes

| Number | Where | Meaning |
|---|---|---|
| `ERR 4 unknown request` | any tool | this BR is older than the driver |
| 9 | `read_history` | refused under `GUI OFF` (§6) |
| 4152 | a run | file not found |
| 4158 | `AI` | nothing is listening for it |
| 4166 | a line from the assistant | it tried to change its own grant |
| 4167 | `command` | the person refused the question |
| 4168 | `command` | a `CONFIG` operation that is refused while an assistant is attached |
| 4169 | `AI` | a program or procedure is running and did not set `AI_TURN_OK` |
| 4170 | `command` | the assistant tried to set `AI_TURN_OK` |
| 4171 | `command` | the assistant tried to use the `AI` command |
| 4172 | `CONFIG OPTION 83` | the option can be set only in a configuration file |
| -1 | `command` | the turn ended before the result was known (`CLEAR PROC`, `CLEAR ALL`) |

Driver exit codes: `uitest` 0, 1 or 2 (§4); `run_report` through `report_status` (§7). Other modes
exit 1 on an error, with the reason on stderr.

## 11. Further reading

In this folder:

- [`AI-Access-Protocol.md`](AI-Access-Protocol.md) §5: the protocol itself — every request,
  record and error.
- [`AI-Access-Summary.md`](AI-Access-Summary.md): what the facility is, for a reader who will not
  implement it.
- [`AI-Restricted-Operations.md`](AI-Restricted-Operations.md): what a restricted session may and
  may not do.

If anything here disagrees with what a tool actually does, the tool is right. Record it in
[`ERRORS.md`](../../ERRORS.md).
