---
title: System (built-in) functions
file: spec.md
source: §Functions → Internal Functions; br_tree keyword pages folded in & pruned (2b) — ENV$/Encryption/DATE$/DAYS/DATE/NXTFLD/CFORM$ retained for deep detail
category: 10-language
subcategory: 10-language/data-manipulation/system-functions
kind: spec
status: 2b           # reference base + 50 br_tree function pages folded in + runtime-table gap closure
recovered-fold: BR_FILENAME$, BRErr$, COS, MSGBOX, NEWPAGE, REM (6 redirect-collision pages folded from re-fetched source — added MSGBOX/BR_FILENAME$/NEWPAGE, REM=MOD alias, BRErr$ corrected to 4.3+; COS already in trig table; verbatim retained on the BR wiki)
runtime-gap-closure: added the table6k/table7k intrinsics that had no br_tree signature — SGN, RND, XLATE$, RLN, VERSION(file), LINESTATUS$, CURPOS, SCR_FREEZE/THAW, SERIAL, SESSION$, PROCLVL, TIMER, SETENV, VARIABLE$, WBVERSION$, WBPLATFORM$, SYSERR/SYSERR$ (xref), MSG (xref), and the PEM integration set GET$/SET$/INVOKE$/DLL. Sourced from the brulescorp wiki + release notes; the delimiter arg of STR2MAT/MAT2STR documented (there is no DLM$ function).
source-verified: 'cross-checked against the BR interpreter source (basfn.h/tblfn.cpp function tables, ck_num_sysfn/ck_alph_sysfn arity checkers, numfunct.cpp/strfunct.cpp/trig.cpp impls). Corrections: TRUNC/DEG/RAD are reserved keywords that parse but return a runtime bad-function error (NOT implemented — trig() lacks them); CALL is in table7k but has no function implementation (compiler-rejected); SHIFT is a fixed-0 System/23 no-op; SCR_FREEZE/THAW take no args (freeze/thaw remote display); DLL is ≥2 strings dispatched client-side; SETENV is 1–2 args. Exact arities confirmed for all.'
related: [expressions, assignment, declaration, data-types]
keywords: [CNVRT$, POS, LEN, TRIM$, UPRC$, LWRC$, STR$, VAL, DATE$, TIME$, RND, MAX, MIN, SUM, MSGBOX, KSTAT$]
---

# System (built-in) functions

BR's intrinsic functions — they return a value and are used inside
[expressions](../expressions/spec.md). Grouped below by purpose. User-defined functions
(`DEF`/`FN`) are a separate topic in
[flow-control/functions-udf](../../flow-control/functions-udf/spec.md).

<a id="syntax"></a>
## Syntax

Most take the form `NAME(args)`. A few system values take **no parentheses**: `DATE$`, `TIME$`,
`ERR`, `LINE`, `CNT`, `CODE`, `PROCIN`, `FILENUM`, `INF`, `PI`, `USERID$`, `LOGIN_NAME$`, `WSID`,
`SERIAL`, `SESSION$`, `PROCLVL`, `TIMER`, `VARIABLE$`, `WBVERSION$`, `WBPLATFORM$`, `SYSERR`,
`SYSERR$`, `CURPOS`, `RND` (and `PIC$`, whose parentheses are optional). All yield a value usable
anywhere an expression is allowed.

<a id="semantics"></a>
## Semantics

- String functions return strings (suffix `$`); numeric functions return numbers.
- The **array-processing** functions (`AIDX`/`DIDX`, `UDIM`, `SUM`, `SRCH`, `STR2MAT`/`MAT2STR`)
  operate on `MAT` arguments and pair with [assignment](../assignment/spec.md#mat).
- `LEN(s$)` returns the **actual** current length, not the `DIM` maximum.
- **Inverse pairs**: `CHR$`↔`ORD`, `HEX$`↔`UNHEX$`, `STR$`↔`VAL`, `ENCRYPT$`↔`DECRYPT$`.
- Several entries here query **file/window** or **screen/keyboard** state; they live in this index
  but belong operationally to [30-io-file](../../../30-io-file/statements/spec.md) and
  [20-io-screen](../../../20-io-screen/input-output/spec.md) — cross-linked in their tables below.
- `PROCIN` / `PROGRAM$` are value-returning here but their reference pages live under
  [70-commands/information](../../../70-commands/information/spec.md).

<a id="tables"></a>
## Tables

<a id="string-functions"></a>
### String & character
| Function | Returns |
|---|---|
| `CHR$(n)` | character for ASCII code `n` |
| `ORD(s$)` | ASCII ordinate (0–255) of the first char of `s$` (inverse of `CHR$`) |
| `UPRC$(s$)` / `LWRC$(s$)` | upper / lower case |
| `TRIM$(s$)` | strip leading **and** trailing spaces |
| `LTRM$(s$[,c$])` / `RTRM$(s$[,c$])` | strip leading / trailing spaces (or the 1-char `c$`, nulls allowed) |
| `LPAD$(s$,n)` / `RPAD$(s$,n)` | pad to length `n` (left / right) |
| `RPT$(s$,n)` | `s$` repeated `n` times |
| `LEN(s$)` | actual current length |
| `POS(s1$,[^]s2$[,[-]start])` | position of `s2$` in `s1$` (0 if none); `^`=case-insensitive (`CONFIG SEARCH_CHAR`); `-start`=search backward |
| `SREP$(src$,find$,repl$)` | string replace (where available) |
| `XLATE$(s$,table$[,start])` | translate `s$` through a 256-byte `table$`: each input char of ASCII value `n` is replaced by the `(n+1)`-th char of `table$`; chars past the table's length pass through unchanged. Optional `start` position. A `table$` beginning `STR2UTF`/`UTF2STR` does UTF-8 conversion |
| `LOGIN_NAME$` | current user's login name (3.83h+) |

<a id="conversion-functions"></a>
### Type conversion & formatting
| Function | Returns |
|---|---|
| `STR$(n)` | number → string (plain) |
| `VAL(s$)` | string → number |
| `CNVRT$(spec$,n)` | number → string per a FORM format code (`B BH BL D G GZ L N NZ PD PIC S ZD`); enhanced `STR$` (slower than a `FORM`) — see [form-spec](../../../30-io-file/form-spec/spec.md#syntax) |
| `CFORM$(form$)` | pre-compile a FORM string into a fast format variable (see note) |
| `HEX$(s$)` / `UNHEX$(s$)` | hex notation ↔ characters (e.g. printer escapes; printer translation starts `HEX$("2B00")`) |
| `PIC$[(sym$)]` | current currency symbol; with a 1-char `sym$`, sets it (persists until changed / BR exit; per-workstation) |

> **`CFORM$` caveat** — output is an unreadable, machine/release-dependent internal format: never
> save it to a file or pass a format that references a variable (by length/decimals) into a library —
> the compiled form points to a *dictionary slot*, not a name, and may bind to the wrong variable.

<a id="numeric-functions"></a>
### Numeric & math
| Function | Returns |
|---|---|
| `INT(n)` | integer part (truncates) |
| `IP(n)` / `FP(n)` | integer part / fractional part (sign preserved: `FP(-3.1)`=-0.1) |
| `CEIL(n)` | smallest integer ≥ `n` (always rounds up: `CEIL(-5.1)`=-5) |
| `ROUND(n,d)` | round to `d` decimals |
| `TRUNC(n)` | ⚠️ **reserved but not implemented** — parses (1 numeric arg) but returns a runtime *bad-function* error in the current BR source (`trig()` has no `TRUNC` case); there is **no** `[,d]` form. Use `INT`/`IP` to truncate |
| `ABS(n)` | absolute value |
| `SGN(n)` | sign of `n`: `-1` (negative) / `0` (zero) / `1` (positive); a near-zero value can round to `0` per the `RD` config |
| `SQR(n)` | square root |
| `MOD(a,b)` / `REM(a,b)` | remainder (`MOD(7,3)` → 1; **function only, no infix `a MOD b`**; `REM` is an alias for `MOD`) |
| `MAX(…)` / `MIN(…)` | largest / smallest of a numeric list |
| `MAX$(…)` / `MIN$(…)` | largest / smallest string (by ASCII value) |
| `SIN(n)` `COS(n)` `TAN(n)` `ATN(n)` | trig / arctangent (radians) |
| `DEG(n)` / `RAD(n)` | ⚠️ **reserved but not implemented** — recognized keywords that return a runtime *bad-function* error (`trig()` has no `DEG`/`RAD` case); no radian↔degree conversion exists in the current source |
| `LOG(n)` / `EXP(n)` | natural log / e^n |
| `PI` | 3.14159265358979 |
| `INF` | largest representable number (`1.0E+307`); `1/INF` = smallest |
| `RND` | pseudo-random number in `0`–`1`. Reseed from the clock with [`RANDOMIZE`](../../flow-control/other-flow/spec.md); `LET RND(seed)` sets a fixed seed for a repeatable sequence. Scale e.g. `INT(RND*100+1)` |

<a id="date-functions"></a>
### Date / time
| Function | Returns |
|---|---|
| `DATE$` | current date (`yy/mm/dd`) |
| `TIME$` | current time (`hh:mm:ss`) |
| `DAYS(date[,mask])` | day-count; Y2K-aware (BASEYEAR, auto century) 3.83+; dates from 1700 (3.90+) |
| `DATE$(days,"mask")` | format a day-count to a string (`"day month, ccyy"`; time masks 4.30+) |
| `DATE(days,"mask")` | numeric date sibling of `DATE$` (for sorting; stores the days value) |
| `SQL_DATE$(d,"fmt")` / `BR_DATE$(s,"fmt")` | pack/unpack SQL dates (4.30+) |

> Date *storage* types `DT`/`DL`/`DH` are FORM field types — see
> [30-io-file/form-spec](../../../30-io-file/form-spec/spec.md), not here. The currency/format-string
> behaviour interacts with `PIC$` and `OPTION INVP`. Full mask reference: [DATE$](DATE$.md),
> [DAYS](DAYS.md), [DATE](DATE_\(Internal_Function\).md).

<a id="array-functions"></a>
### Array-processing (used with MAT)
| Function | Returns |
|---|---|
| `UDIM(arr[,dim])` | current size of an array (or of dimension `dim`) |
| `SUM(arr)` | sum of all elements |
| `SRCH(MAT arr,arg[,start])` | row of match (0/-1 if none); `^` prefix = case-insensitive substring |
| `AIDX(arr)` / `DIDX(arr)` | ascending / descending **index** array (original unchanged) |
| `STR2MAT(s$,MAT a$[,[MAT]sep$][,flags$])` | split `s$` → array; **dynamically redimensions** `a$`; returns the element count (delimiter/flags below) |
| `MAT2STR(MAT a$,s$[,[MAT]sep$][,flags$])` | join array → `s$` (delimiter/flags below) |

<a id="str2mat-delimiter"></a>
**`STR2MAT` / `MAT2STR` delimiter (`sep$`) and flags.** `sep$` is an ordinary **user-supplied
delimiter string** — any string variable or literal (older wiki examples name the variable `DLM$`,
but there is **no `DLM$` function**) — or, as of **4.3**, a `MAT` of delimiter strings (`[MAT]sep$`).

- **`STR2MAT` default** (`sep$` omitted): splits on any end-of-line run — **`\n\r`, `\r\n`, `\n`, or
  `\r`** — so multiple CSV/text rows in one string each become an element.
- **Empty delimiter `sep$=""`**: `STR2MAT` puts **every character** in its own element; `MAT2STR`
  **concatenates** with no separator.
- **Adjacent identical delimiters**: `STR2MAT` honors each — all but the first produce an **empty
  element** (e.g. `STR2MAT("Mary,,John",MAT c$,",")` → `Mary`, ``, `John`).
- **`MAT2STR` default** (`sep$` omitted): **`CRLF`** on Windows / **`CR`** on Linux; the delimiter is
  placed **after every element, including the last**.
- **`flags$`** — an optional quote type `Q` / `QUOTES` / `'` / `"` (case-insensitive), optionally
  followed by a trim flag `:TRIM` / `:LTRM` / `:RTRM` (the colon is used only when a quote type
  precedes it). On `STR2MAT`, quoting means a delimiter **inside** a quoted field is not a split point,
  and a **doubled** quote (`""`) inside a quoted field is one literal quote; on `MAT2STR`, each element
  is wrapped in the quote character.
- **Versions**: `MAT2STR` introduced **4.20**; `STR2MAT` CSV/XML/quote/`MAT`-delimiter enhancements
  added in **4.3**.

<a id="file-query"></a>
### File / drive query (I/O handlers — see [30-io-file](../../../30-io-file/statements/spec.md#io))
| Function | Returns |
|---|---|
| `FILE$(n)` / `FILE$` | open file's name; with no arg = file of the most recent I/O error |
| `FILE(n)` | status: `-1` not open, `0` ok, `10`/`11` EOF in/out, `20`/`21` transmission err in/out |
| `FILE(n,"WINDOW_RECT"\|"USABLE_RECT"\|"FONTSIZE",MAT a)` | window/usable rect (x,y,w,h px) or char cell size |
| `FILENUM` | file number of the most recent I/O error (= `FILE$` with no arg) |
| `FREESP(n)` | free bytes on the drive holding file `n` |
| `EXISTS(file$)` | nonzero if file/PROC exists & readable (`1`=directory, `>1`=file) — test zero/nonzero only |
| `BR_FILENAME$(os$)` / `OS_FILENAME$(br$)` | convert an OS path to a BR filename and back (4.18+; omit any leading colon — it would bypass the conversion) |
| `KPS(n[,seg])` | key start position; `seg` selects a split-key section; `-1` if not open / no key / bad seg |
| `LREC(n)` / `REC(n)` | last record / current record number |
| `RLN(n[,newlen])` | record length of open file `n`; the optional `newlen` **resets** it (EXTERNAL files only, and not above the OPEN `RECL=`) |
| `VERSION(n[,ver])` | the marked **version number** of INTERNAL file `n` (**not** the BR release); the optional `ver` sets it when the file is open `OUTPUT` (also settable with `VERSION=` on OPEN) |
| `LINESTATUS$(n)` | serial-line/modem status of communications channel `n` — see [30-io-file/serial-comm](../../../30-io-file/serial-comm/spec.md) |
| `LINES(n)` | lines printed since last new-page (= `KREC` for display files) |
| `LINESPP(n)` | current lines per page (PRINTER `LPP`, else 66) |

<a id="screen-query"></a>
### Screen & keyboard query (see [20-io-screen](../../../20-io-screen/windows-cursor/spec.md))
| Function | Returns |
|---|---|
| `KSTAT$[(n[,secs])]` | unprocessed keystrokes; with `n`, waits for `n` keys (`secs` timeout each). Fn keys = 2 chars; values are BR scancodes (`UNHEX$` to read) |
| `NXTFLD[(…)]` | relative position of the next control to be occupied (4 syntax forms; pairs with FKEY for hot controls) |
| `NXTROW` / `NXTCOL` | row / col of the next cursor position (4.20+; mouse or keyboard; `OPTION 59` for old `CurCol`) |
| `NEXT` | next cursor position within a 2D control (4.20+; used in an INPUT FIELDS `NEXT` clause) |
| `CURTAB[(win[,1])]` | active tabbed-window number; `CURTAB(win,1)` raises that tab (4.16+) |
| `CURPOS` | cursor position **within the field data** when control returns to the program (4.20+); excludes untyped trailing spaces but counts invisible CRLF characters. Cursor row/col are `CURROW`/`CURCOL` — see [windows-cursor](../../../20-io-screen/windows-cursor/spec.md#semantics) |
| `SCR_FREEZE` / `SCR_THAW` | **(no arguments)** suspend / resume **remote (client-server) display** repainting — `freezeRemoteDisplay()` / `thawRemoteDisplay()` in the source; each returns `0` (batch updates, then thaw to repaint once) |

<a id="system-info"></a>
### System / information
| Function | Returns |
|---|---|
| `ERR` | last error number |
| `LINE` | current line number |
| `CNT` | data items successfully processed by the last I/O (`MAT A(CNT)` to size to what was read) |
| `BRERR$(code)` | the *description* of a BR error code — what `ERR` is to the number (e.g. `BRERR$(682)`; 4.3+) |
| `ENV$(status[,MAT cfg$[,arg]])` | environment / status interrogation (4.30+) — see [environment](../../../00-configuration/environment/spec.md#env-read) |
| `CODE` | numeric return value of the most recent procedure (set by `EXIT n`) |
| `PROCIN` | non-zero while a procedure is feeding input (0 = keyboard) |
| `WSID` | this session's workstation ID |
| `USERID$` | BR licensee name |
| `SERIAL` | serial number of this BR software copy |
| `SESSION$` | this session's ID — `WSID` (3–4 digits) followed by a 1-digit session number `1`–`9` (e.g. `011`, `012`) |
| `PROCLVL` | current procedure nesting level (`0` = keyboard / not in a procedure) |
| `TIMER` | seconds since the Unix epoch (1970-01-01 UTC) as a 5-decimal real; use two readings to time a section (accuracy follows the OS clock) |
| `SETENV(name$[,value$])` | set a **BR session** environment variable (read back with `ENV$`; function form of `CONFIG SETENV`). **2 args** = `name$`,`value$`; **1 arg** = a single `NAME=VALUE` directive string |
| `VARIABLE$` | name of the variable that failed in the **last I/O statement** (for debugging / `HELP$` topics); not set for field-spec errors 850–890 or for calculated expressions |
| `WBVERSION$` | the running BR version, as a string |
| `WBPLATFORM$` | the platform string; returns `WINDOWS` on a unix/aix/linux client-server run when `CONFIG SHELL DEFAULT CLIENT` is set (so client-side shell/print behavior is used) |
| `SYSERR` / `SYSERR$` | the underlying **OS** error number / its description (companion to `ERR`/`BRERR$`) — see [90-reference/error-codes](../../../90-reference/error-codes/_index.md) |
| `SHIFT[(n)]` | always returns **`0`** — a legacy **System/23-compatibility** no-op (any argument is accepted and ignored) |
| `MSG$("text")` | display text in the 2nd box of the command console |
| `MSG(action$,arg)` | keyboard control (Windows / Client-Server): `MSG("KB",keys$)` injects keystrokes (special keys in pipes, e.g. `"|CTRL+|c|CTRL-|"`), `MSG("sleeptime",cs)` sets the per-keystroke delay — see [70-commands/information/MSG.md](../../../70-commands/information/MSG.md) |
| `SLEEP(seconds)` | pause; fractional seconds, ms resolution (3.83h+) |
| `HELP$([*]kw[,file][,mark])` | enter HELP mode / show a topic (see [windows-cursor §help](../../../20-io-screen/windows-cursor/spec.md#help-facility)) |
| `NEWPAGE` | a char that form-feeds the printer / clears the screen and **zeroes the line counter** (`LINES`/`KREC`); `PRINT #255: NEWPAGE` no longer emits a trailing CR — avoid it immediately before `TAB(x)` in an *unformatted* `PRINT` |
| `BELL` / `TAB(x)` | sound the tone / tab to column `x` within a `PRINT` list |

<a id="integration-functions"></a>
### External / .NET (PEM) integration
| Function | Returns |
|---|---|
| `GET$("#f,r,c",prop$)` | read a property of the `.NET`/PEM control at field `#f,r,c` (e.g. `GET$("#1,5,10","city")`) — see [controls PEM](../../../20-io-screen/controls/Properties,_Events,_and_Methods_(PEM)_and_.NET_controls.md) |
| `SET$("#f,r,c",assign$)` | set a control property, `"prop=value"` (dotted paths allowed, e.g. `"address.city=…"`) |
| `INVOKE$("#f,r,c",method$,MAT args$)` | invoke a control method (`method$` must be a full entry from `INPUT FIELDS … METHOD_NAMES`) |
| `CALL` | ⚠️ **reserved keyword — no function implementation**: it is in the numeric function name table (`table7k`) but the compiler rejects `CALL(…)` as an expression (no `CALL_FN` handler in `numfunct.cpp`). Not usable as a function |
| `DLL(a$,b$,…)` | call a client-side DLL command — **≥2 args, first two strings**; dispatched to the client via `callClientDictCommand` (errors 0321–0327) — see [00-configuration/installation-tooling](../../../00-configuration/installation-tooling/spec.md#dotnet) |

<a id="msgbox"></a>
### Message box (Windows)
`MSGBOX(prompt$ [,title$] [,buttons$] [,icon$])` pops a Windows message box and **returns the chosen
button in `CNT`** (and as the function value). Only `prompt$` is required. `buttons$` ∈
`OK`(default)/`YN`/`OKC`/`YNC`, and the **capitalized** letter is the default (Enter) button (`Yn`→Yes,
`yN`→No); `icon$` ∈ `INF`/`ERR`/`EXCL`/`QST`. Return values: `0` error (rare), `1` OK, `2` Yes, `3` No,
`4` Cancel/Esc. Force a line break in the text with `CHR$(13)` or `HEX$("0D0A")` (two in a row = a blank
line).
```business-rules
00060 IF MSGBOX('Are the labels aligned?','Check Printer','Yn','Qst')><2 THEN GOTO ALIGN
```

<a id="encryption"></a>
### Encryption (4.30+) — deep reference in [Encryption](Encryption.md)
| Function | Notes |
|---|---|
| `ENCRYPT$(data$[,key$[,type$[,iv$]]])` | types AES/BLOWFISH/DES/3DES/RC4/RC2; default `AES:256:CBC:128` |
| `DECRYPT$(...)` | inverse of `ENCRYPT$` |
| `ENCRYPT$(data$,"","MD5"\|"SHA"\|"SHA-1")` | one-way hashes |

<a id="examples"></a>
## Examples

```business-rules
00470 LET LASTNAME$(N) = UPRC$(ANSWERS$(2))    ! normalize for sorting
00100 PRINT LEN("John")                        ! 4 (actual length)
00200 PRINT POS("AaEeIiOoUu", X$)              ! >0 if X$ is a vowel
00300 LET S$ = CNVRT$("NZ 5.2", AMOUNT)        ! number → formatted string

00520 READ MAT CUST$ : MAT ORDER = AIDX(CUST$) ! ascending index
00540 FOR I=1 TO 5 : PRINT CUST$(ORDER(I)) : NEXT I   ! print sorted
00030 READ MAT A EOF 40 : MAT A(CNT)           ! resize to items actually read
00050 STR2MAT(CSV_LINE$, MAT FIELDS$, ",", "Q:TRIM")  ! parse a CSV line

00900 LET FMT$ = CFORM$("FORM C 10, V 20, BH 3")  ! compile once, reuse in a loop
01010 FOR X=1 TO 100 : READ #1,USING FMT$: MAT V : NEXT X

00100 EXECUTE "PROC BACKUP"
00110 IF CODE = 0 THEN PRINT "Backup OK" ELSE PRINT "Failed, CODE="; CODE
00120 LET K$ = KSTAT$(1)                       ! idle until one key pressed
```

<a id="see-also"></a>
## See also

- [expressions](../expressions/spec.md) — using functions within expressions
- [assignment](../assignment/spec.md#mat) — `AIDX`/`DIDX`/`STR2MAT` with `MAT`
- [declaration](../declaration/spec.md) — `UDIM`/`LEN` for array & string sizes
- [30-io-file/statements](../../../30-io-file/statements/spec.md#io) — `FILE`/`FREESP`/`EXISTS`/`KPS`/`LREC`/`REC` in I/O context
- [20-io-screen/windows-cursor](../../../20-io-screen/windows-cursor/spec.md) — `KSTAT$`/`NXTFLD`/`NXTROW`/`CURTAB` cursor & keyboard
- [00-configuration/environment](../../../00-configuration/environment/spec.md#env-read) — `ENV$`/`LOGIN_NAME$`/`WSID`
- [70-commands/program-management](../../../70-commands/program-management/spec.md) — `CODE`/`PROCIN` and procedures
- [30-io-file/form-spec](../../../30-io-file/form-spec/spec.md#syntax) — the format codes used by `CNVRT$`/`CFORM$`
- Backing keyword pages (deep detail retained): [ENV$](ENV$.md), [Encryption](Encryption.md),
  [DATE$](DATE$.md), [DAYS](DAYS.md), [DATE](DATE_\(Internal_Function\).md), [NXTFLD](NXTFLD.md),
  [CFORM$](CFORM$.md)

*(6 redirect-collision pages re-fetched in 2b — `BR_FileName$`, `BRErr$`, `CoS`, `MsgBox`, `NewPage`,
`Rem (internal function)` — were folded into this spec and pruned; verbatim wikitext remains on the BR wiki.)*
