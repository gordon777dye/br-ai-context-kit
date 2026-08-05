---
title: File I/O statements
file: spec.md
source: §File Operations (OPEN, READ/WRITE/REWRITE/DELETE/RESTORE/CLOSE, REC=)
category: 30-io-file
subcategory: 30-io-file/statements
kind: spec
status: 2b           # reference base verified comprehensive; misfiled command pages relocated; added 2026-07-03: CLOSE trailing-colon terminates the statement (second colon needed before a following statement); no conflicts
recovered-fold: LINPUT, OPEN_DISPLAY, OPEN_external, READ(disambig), REREAD, RESTORE(disambig), RESTORE_file (7 redirect-collision pages folded from re-fetched source — external short-record 4271, DELETE-invalid-on-external, TRANSLATE/0608/4146, RESTORE modes+linked anchors, LINPUT/WAIT/TIMEOUT, REREAD dup-key idiom; verbatim retained on the BR wiki)
related: [file-model, form-spec, keys-indexes, serial-comm]
keywords: [OPEN, CLOSE, READ, WRITE, REWRITE, DELETE, RESTORE, REREAD, REC, KEY, FIRST, LAST, PRIOR, NEXT, SAME, EOF, NOKEY, NOREC, OUTIN, SEQUENTIAL, OUTPUT, WAIT, DROP, FREE]
corrections:
  - "The exit clauses were enumerated per statement and are one repeatable production. Section io gave READ `[EOF] [NOKEY] [NOREC] [ERROR]` and REWRITE `[NOKEY] [NOREC]`, which reads as the admissible set for each statement and is not: BR matches an exit clause by a table lookup (`getExit`, command4.cpp) rather than against an expected keyword, so any of the 17 error conditions is admissible wherever a statement's syntax tree admits exits, and they repeat with a space rather than a comma. Replaced with an `<exits>` production pointing at the roster in 10-language/flow-control/error-handling, keeping the per-statement note about which conditions can actually fire - that part was the useful content and is a semantic claim, not a grammatical one. DELETE and RESTORE already used `[ <error-condition> ]`, a third notation for the same thing, and now use `<exits>` too. This spec's enumeration is where brls transcribed a 14-name roster from, which is how the error was found; see lsp/brls/LSP_PLAN.md finding 33. Sources are level 1: BR's `synexits`/`table4v`/`table4k` and the READ/REWRITE trees in `lsp/syn.txt`. Added in brls phase 7."
  - "`USING` was given as taking a `<line-ref>` only, on all four record-I/O statements. BR's syntax tree gives each of READ, REREAD, WRITE and REWRITE a **two-way branch** there — a line reference or an alpha expression — exactly as PRINT has, so `READ #1, USING \"FORM C 20,N 6.2\": A$, B` and `USING F$` are as legal as naming a FORM line, and the inline string is not a PRINT-only convenience. A `<form-ref>` production added, with a note that the two forms differ in *when* the layout is compiled and so in what a mistake in it costs. Source is level 1: the USING nodes in all five statements' trees in `lsp/syn.txt`. The printing spec already had this right. Added in brls phase 10."
  - "Twelve keywords added. The spec's own BNF defines the <position> production (FIRST/LAST/PRIOR/NEXT/SAME), the I/O exit clauses (EOF/NOKEY/NOREC), the OPEN modes OUTIN/SEQUENTIAL/OUTPUT and the WAIT= clause, and Positional_Parameters.md sits beside it covering the positional five in detail - but the frontmatter declared none of them. The keyword index is built from this list, so all twelve routed to no spec at all: BR's own record-positioning vocabulary was documented here and reachable from nowhere. Only single-sense spellings were added, plus NEXT. DROP, FREE and INPUT are also defined in this BNF and still omitted, because each also names a command or a statement and a class-blind index would attach this spec to that sense too."
---

# File I/O statements

Opening internal files and reading/writing/updating records. Concepts (types, modes, access,
locking) are in [file-model](../file-model/spec.md); record layout in
[form-spec](../form-spec/spec.md); keyed access (`KEY=`/`SEARCH=`) in
[keys-indexes](../keys-indexes/spec.md). Display-file `PRINT`/`INPUT`/`LINPUT` and printer/serial
opens are cross-referenced below.

<a id="syntax"></a>
## Syntax

<a id="open"></a>
### OPEN (internal & external)
```bnf
<share-spec> ::= 'NOSHR' | 'SHR' | 'SHRI'
<key-spec>   ::= 'KPS=' <start> ['/' <start>]* ',' 'KLN=' <len> ['/' <len>]*   -- ≤6 sections, ≤128 bytes

<file-open-string> ::= '"' 'NAME=' <file-pathname>
                       [ ',' 'KFNAME=' <key-file> ]
                       [ ',' { 'NEW' | 'USE' | 'REPLACE' } ]
                       [ ',' 'RECL=' <integer> ]
                       [ ',' <key-spec> ] [ ',' <share-spec> ] [ ',' 'RESERVE' ]
                       [ ',' 'VERSION=' <integer> ] [ ',' 'WAIT=' <integer> ]
                       [ ',' 'TRANSLATE=' <table> ] [ ',' 'NOCLOSE' ] [ ',' 'LINKED' ]
                       [ ',' { 'BTREE' | 'ISAM' } ] [ ',' 'TMPIDX' ] '"'
                     | <string-expression>

OPEN '#'<channel> ':' <file-open-string> ',' 'INTERNAL' ','
     { 'INPUT' | 'OUTPUT' | 'OUTIN' } [ ',' { 'SEQUENTIAL' | 'RELATIVE' | 'KEYED' } ]
     [ <error-condition> <line-ref> ]*
OPEN '#'<channel> ':' <file-open-string> ',' 'EXTERNAL' ','
     { 'INPUT' | 'OUTPUT' | 'OUTIN' } [ ',' { 'SEQUENTIAL' | 'RELATIVE' } ]
```

<a id="io"></a>
### Record I/O
```bnf
READ    '#'<channel> [ ',' 'USING' <form-ref> ] [ ',' <position> ] [ ',' { 'RESERVE' | 'RELEASE' } ] ':' <variable-list> <exits>
REREAD  '#'<channel> [ ',' 'USING' <form-ref> ] ':' <variable-list> <exits>      -- re-reads buffered record; no EOF
WRITE   '#'<channel> [ ',' 'USING' <form-ref> ] [ ',' { 'RESERVE' | 'RELEASE' } ] ':' <expression-list> <exits>
REWRITE '#'<channel> [ ',' 'USING' <form-ref> ] [ ',' { 'REC='<n> | 'KEY='<k$> } ] [ ',' { 'RESERVE' | 'RELEASE' } ] [ ',' 'WAIT=' <integer> ] ':' <expression-list> <exits>   -- WAIT= only with REC=/KEY=
DELETE  '#'<channel> [ ',' { 'REC='<n> | 'KEY='<k$> } ] [ ',' { 'RESERVE' | 'RELEASE' } ] ':' <exits>
RESTORE '#'<channel> [ ',' <position> ] [ ',' { 'RESERVE' | 'RELEASE' } ] ':' <exits>
CLOSE   '#'<channel> [ ',' { 'DROP' | 'FREE' } ] [ ',' 'RELEASE' ] ':'

<position> ::= 'REC=' <numeric-expr> | 'KEY[>]=' <string-expr> | 'SEARCH[>]=' <string-expr>
             | 'FIRST' | 'LAST' | 'PRIOR' | 'NEXT' | 'SAME'
<form-ref> ::= <line-ref> | <string-expr>          -- a FORM line, or the layout as a "FORM …" string
<exits>    ::= [ <error-condition> <line-ref> ]*   -- space-separated, repeatable, any of the 17
```

**`USING` takes either form on all four statements.** BR's syntax tree gives each of them a two-way
branch — a line reference, or an alpha expression — so the inline string is not a `PRINT`-only
convenience: `READ #1, USING "FORM C 20,N 6.2": A$, B` is as legal as naming a `FORM` line, and so is
`USING F$` with the layout held in a variable. The two are **not** interchangeable in one respect,
which is when the layout gets compiled and therefore what a mistake in it costs — see
[form-spec](../form-spec/spec.md#when-a-form-is-compiled).

**`<exits>` is one production, not a per-statement list.** BR matches an exit clause by a table
lookup rather than against an expected keyword, so **any** of the 17 error conditions is admissible
wherever a statement admits exits at all — the roster and the ordering rule are in
[10-language/flow-control/error-handling](../../10-language/flow-control/error-handling/spec.md#conditions).
Which of them can actually *fire* is per statement: `EOF`, `NOKEY`, `NOREC` and `ERROR` are the ones
that matter on a `READ`, `NOKEY` and `NOREC` on a `REWRITE`.

<a id="semantics"></a>
## Semantics

- **OPEN defaults** (internal): reuse existing file (not create), not keyed, `NOSHR`, `WAIT=15`,
  `SEQUENTIAL`. Include `RECL`/`KPS`/`KLN` **only when creating**; never on an existing file
  (they live in the header). `NEW` errors (4150) if the file exists; `USE` opens-or-creates;
  `REPLACE` overwrites.
- **`TRANSLATE=<table>`** names a 256- or 512-byte character-translation file applied to all
  `C`/`V`/`G`/`N`/`ZD`/`PIC` I/O (first 256 bytes = input table; an optional second 256 = output table,
  else BR inverts the input table). **`WAIT=`** also governs how long an `OPEN` waits for a file another
  workstation has locked before **error 4146** (previously it affected only locked *records* → error
  0061). When a file is opened both `OUTIN` and `INPUT`, the **`OUTIN` open must come first** or you get
  **error 0608**.
- <a id="external"></a>**External files** (`OPEN … EXTERNAL`) read/write *any* bytes of *any* file (no BR
  header, no delete byte) — so **`DELETE` is invalid** on them. Position with `REC=` (record × `RECL`) or
  `POS=` (absolute byte); don't mix the two on one file. `EOF` fires only when the final record is a full
  `RECL`; a **short** final record raises **error 4271** (trap with `IOERR`) with `CNT` = bytes read and
  the record null-padded — a following `REREAD` retrieves the padded record, after which reads give the
  normal `4270` EOF. For an external RELATIVE file last positioned with `POS=`, `REC(n)`/`LREC(n)` return
  a *byte* number rather than a record number.
- <a id="display"></a>**Display files** (`OPEN … DISPLAY`) open a text file or a printer for `INPUT` *or*
  `OUTPUT` (never `OUTIN`), sequential only; defaults add `PAGEOFLOW` 60 lines and `EOL=` CRLF (DOS) / LF
  (Unix). Print-side parameters (`EOL=`, `PAGEOFLOW=`, `COPIES=`, `PRINTER=`, `CONV=`, `RETRY=`) are in
  [40-io-printing/statements](../../40-io-printing/statements/spec.md); `OPEN #0:` (re)sizes the BR main
  window and sets `BUTTONROWS`.
- <a id="read"></a>**READ** pulls the next record (or the one at `REC=`/`KEY=`) into the variable
  list via a `USING` [FORM](../form-spec/spec.md). `EOF` handles end-of-file.
- <a id="rewrite"></a>**REREAD** re-decodes the buffered current record (no file I/O, no `EOF`) —
  handy to re-interpret fields. It must follow a successful `READ`/`REREAD` and takes **no**
  `REC=`/`POS=`/`KEY=` clause; a common idiom reads a *key-only* FORM, tests the key, then `REREAD`s the
  *full* FORM (e.g. to walk duplicate keys). **REWRITE** updates the last record read (file must be
  `OUTIN`); it changes only the fields the FORM names, leaving the rest intact. When REWRITE
  **repositions** via `REC=`/`KEY=`, `WAIT=<sec>` bounds how long to wait for a record another
  workstation has locked before **error 0061** (default 15s); `WAIT=` is meaningless on a plain
  REWRITE of the already-locked current record.
- <a id="linput"></a>**LINPUT** reads an entire line/record into **one** string variable, keeping
  commas, quotes and leading blanks (unlike `INPUT`, which splits on commas) — from the keyboard
  (`#0`/none), a display/communications file, or a procedure file under `RUN PROC`. `WAIT=<sec>` arms
  a `TIMEOUT` trap (**error 4145**; `WAIT=0` = no wait,
  `WAIT=-1` = wait forever, reset on each keypress). LINPUT targets a **single** string variable — it
  **cannot** read into a string `MAT` (unlike `INPUT`, which can fill an array); read multiple lines by
  looping LINPUT (trap `EOF` when the file runs out). `RECL` doesn't limit input (it governs output only).
  On a **DISPLAY** open only (a display or `FORMAT=ASYNC` communications file — never INTERNAL/EXTERNAL),
  the open's `EOL=` governs how `LINPUT` delimits input: `EOL=NONE` reads to the variable's dimensioned
  length (one byte at a time if `DIM X$*1`); `EOL=CRLF`/`LF` accepts and strips the delimiter. This
  affects `LINPUT`, **not** the plain `INPUT` statement.
- <a id="write"></a>**WRITE** appends a new record (or writes at `REC=` if that slot is
  deleted/new — else `DUPREC`).
- <a id="delete"></a>**DELETE** removes the last record read, or the one at `REC=`/`KEY=`; space
  is **not** reclaimed automatically (use `COPY -D`).
- <a id="restore"></a>**RESTORE** repositions the file pointer. With no clause it goes to the **start**
  — and **drops all data** on a file opened `DISPLAY OUTPUT` or `…OUTPUT SEQUENTIAL`, and **errors** on
  `OUTPUT RELATIVE`/`OUTPUT KEYED`. Clauses: `REC=` (RELATIVE record), `KEY=`/`SEARCH=` (KEYED, exact or
  `>=` next-greater), `POS=` (external RELATIVE byte); plus positional `FIRST`/`LAST`/`PRIOR`/`NEXT`/
  `SAME`. In a **linked** file, `RESTORE …,REC=<anchor>` repositions to a list (and sets `KREC`), while
  bare `RESTORE` (or `REC=0`) starts a *new* anchor for insertion. RESTORE's channel must be a valid
  file-channel number (`1–199` or `300–999`). By default RESTORE **releases all record locks** held on
  the channel; **`,RESERVE`** keeps them and **`,RELEASE`** releases them explicitly. (To *merely*
  release record locks, `REREAD #n: RELEASE` is faster than `RESTORE #n:`.)
- <a id="close"></a>**CLOSE** options (both require the file opened `NOSHR`): **`DROP`** empties the
  file's *contents* — the file remains (internal files keep only the header record, all space freed);
  **`FREE`** *erases* the file from the system. A trailing **`,RELEASE`** also releases the file's
  **name reservation** (a filename reserved via `PROTECT`/OPEN becomes available to others again). (These
  are the statement parameters; the same-named
  `DROP`/`FREE` **commands** do the equivalent from the console —
  [70-commands/file-directory](../../70-commands/file-directory/spec.md).) Files auto-close at program
  end (unless `NOCLOSE`). **The trailing `:` terminates the statement** — to code another statement
  after `CLOSE` on the same physical line, add a *second* colon as the separator: `CLOSE #n: : STOP`
  (a single `CLOSE #n: STOP` folds the following statement into the CLOSE and misfires).

<a id="rec"></a>
### Relative access — `REC=`
`REC=<numeric-expr>` selects a record by 1-based position (any numeric expression; non-integers
are truncated). Available on all I/O except `REREAD`. Position clauses need **not** be the last
clause before the `:` — they may appear in any order among the statement's clauses.
Missing/deleted target → `NOREC`.

<a id="examples"></a>
## Examples

```business-rules
! Create / open / sequential read
00110 OPEN #1: "NAME=MILES.DAT,RECL=24", INTERNAL, INPUT, SEQUENTIAL
00150 READ #1, USING 160: DATE, MILES, GALLONS, MPG EOF 200
00160 FORM N 6, N 6.2, N 6.2, N 6.3
00200 CLOSE #1:

! Relative access by record number
00310 OPEN #2: "NAME=MILES.DAT,RECL=24", INTERNAL, INPUT, RELATIVE
00330 READ #2, USING 340, REC=I: DATE, MILES, GALLONS, MPG
00340 FORM N 6, N 6.2, N 6.2, N 6.3

! Update in place
00150 OPEN #1: "Name=test.int,RECL=128,USE", INTERNAL, OUTIN
      READ #1, USING F, REC=N: A$, B
      REWRITE #1, USING F: A$, B          ! only FORM fields change
```

<a id="see-also"></a>
## See also

- [file-model](../file-model/spec.md) — types, modes, access methods, sharing/locking
- [form-spec](../form-spec/spec.md) — the `USING FORM` record layout
- [keys-indexes](../keys-indexes/spec.md) — `KEY=`/`SEARCH=` keyed I/O and the INDEX facility
- [serial-comm](../serial-comm/spec.md) — OPEN of a serial channel
- Display-file `PRINT`/`INPUT`/`LINPUT` → [40-io-printing/statements](../../40-io-printing/statements/spec.md)
  and [20-io-screen/input-output](../../20-io-screen/input-output/spec.md)
- File/dir **commands** (`COPY`/`DIR`/`FREE`/`DROP`/`DELETE` command) → [70-commands/file-directory](../../70-commands/file-directory/spec.md)
- Backing keyword page (deep OPEN-parameter reference retained): [Positional_Parameters](Positional_Parameters.md).
  Others folded/covered and pruned. The 2b redirect-collision pages
  `Open_Display`, `Open_External`, `LInput`, `Reread`, `Restore_File` (and the `Read`/`Restore`
  disambiguation stubs) were folded here and pruned; verbatim wikitext remains on the BR wiki.
