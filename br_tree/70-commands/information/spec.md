---
title: Information & debugging commands
file: spec.md
source: §Commands → System / Debugging / Information Commands
category: 70-commands
subcategory: 70-commands/information
kind: spec
status: 2b           # reference base + br_tree fold (BREAK detail, DISPLAY -p/MAT, STATUS/VERIFY, DEBUG_STR, LIST search); PROCIN/PROGRAM$ home resolved; no conflicts
recovered-fold: NOSTEP (redirect-collision page re-fetched; NOSTEP/NOTRACE already covered by the GO bnf in program-management — pruned; verbatim retained on the BR wiki)
related: [program-management, editing]
---

# Information & debugging commands

Inspecting state and debugging a running program: date/time, the command console,
single-stepping, breakpoints, variable display, and logging.

<a id="syntax"></a>
## Syntax

```bnf
DATE [<mm-dd-yy>|<mm/dd/yy>]   TIME [<hh:mm:ss>]   -- DA/TI; show/set session date & time (this terminal)
RUN [STEP] [TRACE] [NORESTORE|RESTORE]             -- step / trace execution (resume with GO → program-management)
BREAK [-p <prog>] { <line>[:<clause>] | <label>: | <var> | FN<name> | BEGIN } [OFF]   -- ST mode triggers
BREAK ALL OFF                                       -- clear every breakpoint
DISPLAY [-p <prog>] { <var> | MAT <array> | ALL } [OFF | PRINT | '>'['>'] <file>]
LIST [<range>] [~]{ "<str>" | '<str>' }[…3x] [REPLACE "<new>"] [PRINT | '>'['>'] <file>]   -- search/replace
LOGGING <level> ',' <logfile> [',' UNATTENDED] [',' +CONSOLE]
STATUS <topic>                                      -- ST; e.g. STATUS BREAK / LIBRARY / FONTS / ENV / ALL
VERIFY                                               -- V; check the system recorded the disk correctly
```

<a id="semantics"></a>
## Semantics

- <a id="date-time"></a>**DATE/TIME** (commands, `DA`/`TI`) set or show the clock for this terminal,
  **session only** (per-workstation, lost on exit, no effect on the OS clock) — distinct from the
  [`DATE$`/`TIME$`](../../10-language/data-manipulation/system-functions/spec.md#date-functions)
  *functions* that only read it. Quirk: `DATE` is *set* as `mm-dd-yy` (or `mm/dd/yy`) but *reported*
  as `yy/mm/dd` (legacy — programs normally use the function, not the command).
- **RUN STEP** pauses after each action statement (Enter = next, `GO` = resume); **TRACE** prints
  line numbers as they execute; combine `STEP TRACE`. The fuller `GO [STEP|TRACE] [.line]` resume /
  temporary-breakpoint forms and Shift+F1–F5 stepping are in
  [program-management](../program-management/spec.md#go).
- <a id="break"></a>**BREAK** drops a program into STEP mode when its target is hit: a `line`
  (must be an executable line — flow/assignment/I-O; not comments, `DATA`, or `DIM`), a `label:`,
  a changed `variable`/array/array-element (e.g. `BREAK CUSTOMER$(6)`, as of 4.16), a `FNname`, or
  `BEGIN` (on entry). `BREAK var` also implies `DISPLAY var`. `OFF` clears one setting, `ALL OFF`
  clears all; `-p <prog>` masks which program/libraries it applies to. **Conditional** breakpoints
  aren't set with `BREAK` — store a statement like `IF A>B THEN EXECUTE "go step"` instead.
- <a id="display"></a>**DISPLAY** monitors variables as they change, printing
  `line  var  new-value`. It takes whole arrays (`DISPLAY MAT CUSTOMER$`) and single elements
  (`DISPLAY CUSTOMER$(5)`); `-p <prog>` masks programs; `OFF` stops it. In STEP/error mode, just
  typing a variable name prints its current value.
- <a id="list-search"></a>**LIST "str"** searches the program (and `REPLACE "new"` replaces):
  **single** quotes match case-insensitively, **double** quotes require an exact-case match, `~`
  negates a term, and up to three terms combine (all must match). Edit-while-running tip: change a
  line, then `LIST … >file` to record it; `LOAD` that source later. (Plain `LIST <range>` for
  display/editing is in [editing](../editing/spec.md#list).)
- **LOGGING** writes a level-filtered log (0 major-error … 5 minor-event … 9 debugging).
  <a id="debug-str"></a>**`DEBUG_STR(level, str$)`** (function, BR 4.3+) emits `str$` to the log
  (when `level` ≤ the active log level) and to the debugger, or to the command console if no
  debugger is attached and GUI is ON (levels >10 clamp to 10).
- <a id="status-verify"></a>**STATUS** (`ST`) reports system state by topic (`BREAK`, `LIBRARY`,
  `FONTS`, `ENV`, `ALL`, active procedures, …); **VERIFY** (`V`) checks the disk was recorded
  correctly.
- <a id="console"></a>**Console**: the **command console** is the programming/run window (the
  bottom row is the **command line**); commands typed there run immediately, and you can inspect
  variables mid-run. `MSG`/`BELL` signal the operator.
- <a id="msg"></a>**`MSG("KB", str$)`** (function, Windows/CS only — not raw Unix/Linux terminals)
  drives the Windows-client keyboard from BR; special keys go in pipes (`MSG("KB","|CTRL+|c|CTRL-|")`),
  and `MSG("sleeptime", sec)` paces it (default 0.2s). Full key table: [MSG](MSG.md).
- <a id="printer-list"></a>**`PRINTER_LIST(MAT a$)`** (function) redims `a$` to the active Windows
  printers (default first) and returns the count; the names double as `OPEN "NAME=PRN:/…"` targets
  (any matching substring suffices). Idiom + spooling tip: [PRINTER_LIST](PRINTER_LIST.md).
- <a id="procin-program"></a>**`PROCIN`** returns 1 when input is coming from a procedure file
  (else 0 from the screen) — useful to echo `RUN PROC` input. **`PROGRAM$`** returns the full
  path (`br_filename$`) of the loaded `.br`/`.wb` program — handy in shared error routines. *(Both
  are value-returning functions; they live here as console/debugging aids and are cross-linked from
  the [function index](../../10-language/data-manipulation/system-functions/spec.md#system-info).)*

<a id="examples"></a>
## Examples

```text
RUN STEP TRACE
BREAK 1000           ! stop at line 1000;  BREAK TOTAL stops when TOTAL changes
DISPLAY MAT CUSTOMER$
LIST 'error'                 ! find error/ERROR/Error (case-insensitive)
LIST 60 300 '2,40,C 20,R' REPLACE "3,42,C 30,R"
LOGGING 9, trace.log
```

<a id="see-also"></a>
## See also

- [program-management](../program-management/spec.md) — `RUN`/`GO`/`STOP`, `GO STEP/.line`, procedures
- [editing](../editing/spec.md#list) — `LIST` for display/editing (vs `LIST "search"` here)
- [system-functions](../../10-language/data-manipulation/system-functions/spec.md#system-info) — `ERR`/`LINE`/`CODE`, and the `PROCIN`/`PROGRAM$` cross-links
- Backing keyword pages retained (deep reference): [MSG](MSG.md) (keystroke table),
  [PRINTER_LIST](PRINTER_LIST.md) (printer-select idiom), [PROCIN](PROCIN.md), [PROGRAM$](PROGRAM$.md)

*(Other backing pages — `Information_Commands`, `Command_Console`, `Command_line`,
`Display_(Command)`, `Date_(Command)`, `DEBUG_STR`, `ECHO`, `Increment`, `BELL` — were folded into
this spec and pruned; the `Break_(Command)` page from program-management was folded into `#break`
here.)*
