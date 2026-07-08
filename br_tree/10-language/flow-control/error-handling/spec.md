---
title: Error handling
file: spec.md
source: §Error Handling
category: 10-language
subcategory: 10-language/flow-control/error-handling
kind: spec
status: 2b           # synthesized from the reference; new leaf
recovered-fold: ATTN_Mode, CONV, EOF, NOREC, Operating_Mode, Operating_System_Error, PAUSE_mode, RETRY (8 redirect-collision pages folded from re-fetched source — full operating-mode table, OS-error 4300/4320+SysErr, ON-eligibility, RETRY caveats; verbatim retained on the BR wiki)
related: [other-flow, conditionals]
keywords: [ON ERROR, ERROR, IOERR, RETRY, CONTINUE, EXIT, ERR, LINE, SOFLOW, ZDIV]
---

# Error handling

Trapping and recovering from runtime errors without halting. The numeric error **codes**
themselves are the lookup table in
[90-reference/error-codes](../../../90-reference/error-codes/_index.md); this spec is the
**mechanism**.

<a id="system-variables"></a>
## System variables (set on error)

| Variable | Meaning |
|---|---|
| `ERR` | most recent 4-digit error code |
| `LINE` | line number where the error occurred |
| `CNT` | I/O items successfully processed (I/O errors only; `CNT+1` = first failed field) |
| `FILENUM` | file number of the failing I/O (use with `FILE$(n)`) |

**Always save `CNT` first** in a handler — any I/O (including `PRINT`) resets it.

<a id="levels"></a>
## Four levels of trapping (processed in order)

```bnf
-- 1. Statement-level conditions (on the statement itself)
<statement> [ <error-condition> <line-ref> ]*
-- 2. EXIT groups (named, reusable condition sets)
EXIT <error-condition> <line-ref> [',' <error-condition> <line-ref>]*
... <statement> EXIT <line-ref>
-- 3. ON <condition> (program-wide, per condition)
ON <error-condition> { GOTO <line-ref> | GOSUB <line-ref> | IGNORE | SYSTEM }
-- 4. ON ERROR (catch-all for anything untrapped)
ON ERROR { GOTO <line-ref> | GOSUB <line-ref> | IGNORE | SYSTEM }
```

<a id="conditions"></a>
## Error conditions

`CONV` (conversion/type), `DUPREC` (WRITE over existing record), `EOF` (no more records / no
space), `IOERR` (any untrapped I/O error), `NOKEY` (key absent), `NOREC` (record deleted/out of
range), `OFLOW` (numeric overflow), `PAGEOFLOW` (page length reached), `SOFLOW` (string overflow),
`ZDIV` (divide by zero), `HELP` (Help key), `NONE` (no `ON GOTO/GOSUB` match), `EXIT` (references
an `EXIT` group). These are the same condition words used on I/O statements
([30-io-file/statements](../../../30-io-file/statements/spec.md#io)) and screen
([20-io-screen/input-output](../../../20-io-screen/input-output/spec.md)).

**Not every condition works with `ON`.** `CONV` may appear on a statement, in an `EXIT` group **and**
with `ON`; but `EOF` and `NOREC` are accepted **only** on a statement or in `EXIT` — never with
`ON error`. Specifics worth knowing:
- **`CONV`** traps four conversions: non-numeric characters in a numeric field (or vice versa); a number
  too big for the field; an I/O-list item whose type disagrees with its `FORM` spec; or a negative value
  output through a `PIC` that specifies no sign.
- **`EOF`** (error **4270** for files / **57** for data) traps three: no more records on input
  (`READ`/`INPUT`/`LINPUT`), no file space on output (`PRINT`/`WRITE`), or no more `DATA` on a `READ`.
- **`NOREC`** (error **57**) traps three, only under `RELATIVE` access with a `REC=` clause: the record
  was deleted, the number is ≥2 past the last record (`WRITE`), or past the last record (`READ`).

<a id="recovery"></a>
## Recovery & ON options

- **`RETRY`** re-executes the statement (clause) that caused the most recent error — analogous to
  `RETURN` at the end of a subroutine; **`CONTINUE`** instead resumes at the *next* statement (common
  with `PAGEOFLOW`). Caveats: with no outstanding error (or one suppressed by `ON … IGNORE`) `RETRY`
  itself errors; a **second error before `RETRY` loses the first return address** — so handlers often do
  `ON ERROR SYSTEM` on entry and reinstate their traps just before `RETRY` to avoid loops. The
  exception is a **`4273`** (help-topic-not-found) trapped by `NOKEY` (typically from `HELP$` inside a
  handler): it leaves `ERR`/`LINE` unset and keeps `RETRY`/`CONTINUE` aimed at the *original* error. If
  the retried statement is `INPUT FIELDS`/`RINPUT FIELDS`, the cursor auto-positions on the offending
  field. Typing `RETRY` at an interrupted program is the same as `GO`. (`RETRY=<n>` is also an unrelated
  `OPEN` *communications* parameter — send/receive attempts, default 5.)
- **ON options**: `GOTO` branch to a handler; `GOSUB` call a handler that `RETURN`s (which re-executes
  the error-producing statement, unless the interrupt followed an I/O operation); `IGNORE` skip silently
  (no `ERR`/`LINE` set; `SOFLOW` truncates instead); `SYSTEM` restore default beep-and-suspend behavior.
- **`ON FKEY <n> {GOTO|GOSUB|IGNORE|SYSTEM}`** traps function keys during RUN (F1–F10 default IGNORE;
  during INPUT, keys set `CMDKEY` instead).

<a id="modes"></a>
## Execution modes
The **operating mode** shows in the status line (columns **1–7**); the most recent **error code** shows
in columns **38–41**, in reverse video until ENTER/an arrow key is pressed, then normal. The code
**persists until the next error** — `CLEAR` removes it but also wipes the program/memory, so it's rarely
worth it. The modes BR reports:

| Mode | Meaning / how to resume |
|---|---|
| **READY** | waiting for commands or program lines |
| **RUN** | program executing (`RUN` command or `CHAIN`) — no action |
| **INPUT** | awaiting `INPUT`/`LINPUT`/`RINPUT`/`INPUT FIELDS` entry |
| **SELECT** | awaiting an `INPUT SELECT`/`RINPUT SELECT` menu choice |
| **ERROR** | runtime/syntax error — `GO` resumes, `STOP`/`END`/`CLEAR` end; `LIST`/`PRINT` allowed for debugging; SAVE/RUN/REPLACE/SYSTEM blocked |
| **ATTN** | Ctrl-A interrupt — line# field shows the next line; `LIST`/`PRINT`/line-editing/`STEP`/`TRACE` and changing variable values are all allowed; `GO` resumes |
| **PAUSE** | hit a `PAUSE` statement — inspect state, then `GO` resumes |
| **HOLD** | Esc pressed — no keyboard input accepted; press Esc again to resume |
| **STEP** | single-stepping — ENTER executes each line; line# field shows the next line |
| **INSERT** | Ins-key character-insert editing (else typing overwrites); Ins/ENTER exits |
| **HELP** | help facility active (HELP/F1 key or the `HELP$` function) |
| **PROC** | a procedure file is executing (`GO` resumes if interrupted) |
| **CHAIN / LOAD / SAVE / REPLACE / PR-EDIT** | transient program-management states — no action required |
| **SYSERR** | a system error occurred; the code appears in the error field |

<a id="os-errors"></a>
## Operating-system errors
OS errors vary by platform. **Before 4.16** BR reported them as `4200 + <OS error number>` (the 4200
series), which could exceed 4299 and collide with Unix/Linux codes. **4.16+** instead raises **`4300`**
and **`4320`** and exposes the OS detail through the **`SysErr`** (number) and **`SysErr$`** (text)
variables — always read those for the actual cause. (E.g. OS 72 = print/disk redirection paused;
267 = invalid directory name. See MSDN "System Error Codes" for the Windows list.)

<a id="examples"></a>
## Examples

```business-rules
00001 ON ERROR GOTO GENERAL_ERROR     ! catch-all
00002 ON ZDIV IGNORE                   ! skip divide-by-zero
00003 ON IOERR GOTO 90000
00020 INPUT MI CONV 80                 ! statement-level condition
00050 EXIT CONV CONV_HANDLER, SOFLOW OVERFLOW   ! reusable group
00080 CONV_HANDLER: PRINT "Enter numbers" : RETRY

99000 GENERAL_ERROR: LET SAVECNT=CNT   ! save CNT before any I/O
99030   PRINT "Error";ERR;"at line";LINE
99060   IF FILENUM>0 THEN PRINT "File #";FILENUM;"--";FILE$(FILENUM)
99120   STOP
```

<a id="see-also"></a>
## See also

- [other-flow](../other-flow/spec.md) — `ON … GOTO`/`GOSUB`, `GOTO`, loop flow
- [conditionals](../../data-manipulation/conditionals/spec.md) — `IF` in handlers
- [90-reference/error-codes](../../../90-reference/error-codes/_index.md) — the numeric code lookup table
- [system-functions](../../data-manipulation/system-functions/spec.md#system-info) — `ERR`/`LINE`/`BRERR$`/`FILE$`
- [30-io-file/statements](../../../30-io-file/statements/spec.md#io) — I/O error conditions in context

*(8 redirect-collision pages re-fetched in 2b — `ATTN_Mode`, `CONV`, `EOF`, `NOREC`, `Operating_Mode`,
`Operating_System_Error`, `PAUSE_mode`, `Retry` — were folded into this spec and pruned; verbatim
wikitext remains on the BR wiki.)*
