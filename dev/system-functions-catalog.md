# System (built-in) function catalog

Signatures for BR's **intrinsic / system functions** — the functions baked into the runtime
(`table6k` strings + `table7k` numeric/system), as opposed to user `DEF FN…` functions or
`DEF LIBRARY` functions. This file is **system functions only, by themselves**. User-defined and
library (`DEF LIBRARY`) functions are **application-specific** — their signatures are indexed from
the target application's *own* source on demand, not cataloged here. (Functions appearing in the
decompiled corpus are arbitrary and confidential; the corpus is an example/education and
parser-validation source only, **never** a usable API — so corpus UDFs are not cataloged.)

**Authoritative name set:** `table6k` ∪ `table7k`, lifted verbatim from the BR runtime function
tables — every runtime built-in is listed below, so this file is the complete roster.
**Signatures/semantics** are folded from the `br_tree/` reference, primarily
[`system-functions/spec.md`](../br_tree/10-language/data-manipulation/system-functions/spec.md), plus
`windows-cursor`, `controls`, `keys-indexes`, and the printing leaves. All signatures below are now
**verified against the BR interpreter source** (the `table6k`/`table7k` name tables,
the `ck_num_sysfn`/`ck_alph_sysfn` arity checkers, and the `numfunct.cpp`/`strfunct.cpp`/`trig.cpp`
implementations). Entries marked **✗** are keywords in the runtime tables that are **not usable**:
either reserved-but-unimplemented (`TRUNC`, `DEG`, `RAD` — parse but error at runtime) or compiler-rejected
(`CALL` — no function form). No `†` (unverified-signature) entries remain.

## Notation

```
NAME(arg1, arg2, [opt], rep…)
```

- **Parameters follow BR's own convention — no type tags, no colons.** A `$` suffix marks a string
  argument, no suffix marks a numeric one, and `MAT name` is an array argument. Parameters are
  **comma-separated** (including the first two when there are two or more); a single argument takes no
  separator at all.
- **Return type** is the Returns column — `str` / `num` / `mat num` / `mat str`. A name ending `$`
  always returns `str`, otherwise `num` (BR's hard rule — fixes every return type here, even `✗` entries).
- `[x]` optional · `x…` one-or-more (variadic) · `(out)` a `MAT` the function **fills** (must be a
  declared array lvalue).
- **atom** = usable with **no parentheses** (a bare value); see the table below.
- **assignable** = a pseudo-variable that also accepts assignment, e.g. `LET FKEY(x)`.

## Usage notes (read before using)

1. **Functions are never abbreviated.** Unlike statement keywords, `table6k`/`table7k` require the
   **full** spelling — always written out in full.
2. **No-paren atoms** (below) are bare **values**, not `name(` calls. And a name in *this* catalog is
   a built-in function, whereas a `DIM`'d name with a parenthesis is an array subscript — that is how
   you tell apart e.g. `X(3)` (an array element) from `SIN(3)` (a function call). A **parameterless**
   function (built-in *or* user `FN…`) is called with **no** parentheses — `FNGET$`, never `FNGET$()`.
3. **`MAT`-argument functions** take the literal `MAT name` form (array-processing group, `FILE`
   rect, `STR2MAT`/`MAT2STR`, `PRINTER_LIST`, `UDIM`/`SUM`/`SRCH`/`AIDX`/`DIDX`).
4. **Assignable pseudo-variables** appear on the LHS: `CMDKEY`, `FKEY`, `CURFLD`, `CURTAB`,
   `CURWINDOW`, `PIC$`. `LET name(args)` is valid for these.
5. **Print-list-only:** `TAB(x)` is valid only inside a `PRINT` list; `NEWPAGE`/`BELL` are character
   *values* (`NEWPAGE` also works as a print target).

## No-paren atoms (lex as a value, not `name(`)

Never take arguments:

| Atom | Returns | Meaning |
|---|---|---|
| `ERR` | num | last error number |
| `LINE` | num | current line number |
| `CNT` | num | items processed by the last I/O |
| `CODE` | num | return value of the most recent procedure (`EXIT n`) |
| `PROCIN` | num | non-zero while a procedure feeds input |
| `FILENUM` | num | file number of the most recent I/O error |
| `PI` | num | 3.14159265358979 |
| `INF` | num | largest representable number (`1.0E+307`) |
| `WSID$` | str | this session's workstation ID (string only — there is **no** numeric `WSID`; the curated spec's `WSID` is a typo for `WSID$`) |
| `USERID$` | str | BR licensee name |
| `LOGIN_NAME$` | str | current user's OS login name |
| `PROGRAM$` | str | current program name (ref home: 70-commands/information) |
| `TIME$` | str | current time `hh:mm:ss` |
| `NXTROW` / `NXTCOL` | num | row / col of the next cursor position |
| `NEXT` | num | next position within a 2-D control (INPUT FIELDS `NEXT` clause) |
| `CURROW` / `CURCOL` | num | current/ending cursor row / column |
| `CURPOS` | num | cursor position within the field data |
| `SERIAL` | num | serial number of this BR copy |
| `SESSION$` | str | session id (`WSID` + session digit) |
| `PROCLVL` | num | procedure nesting level |
| `TIMER` | num | seconds since the Unix epoch (5-decimal) |
| `VARIABLE$` | str | variable that failed in the last I/O |
| `WBVERSION$` / `WBPLATFORM$` | str | running BR version / platform |
| `SYSERR` / `SYSERR$` | num / str | OS error number / description |

Optionally bare (also have a parenthesized form): `DATE$`, `PIC$`, `KSTAT$`, `NXTFLD`, `CMDKEY`,
`FKEY`, `CURFLD`, `CURTAB`, `RND` (bare = next value; `LET RND(seed)` seeds).

## String & character

| Function | Returns | Description |
|---|---|---|
| `CHR$(n)` | str | character for ASCII code `n` |
| `ORD(s$)` | num | ASCII code (0–255) of the first char of `s$` (inverse of `CHR$`); BR has **no** `ASC` — use `ORD` |
| `UPRC$(s$)` / `LWRC$(s$)` | str | upper / lower case |
| `TRIM$(s$)` | str | strip leading **and** trailing spaces |
| `LTRM$(s$, [c$])` / `RTRM$(s$, [c$])` | str | strip leading / trailing spaces (or the 1-char `c$`) |
| `LPAD$(s$, n)` / `RPAD$(s$, n)` | str | pad to length `n` on the left / right |
| `RPT$(s$, n)` | str | `s$` repeated `n` times |
| `LEN(s$)` | num | **actual** current length (not the `DIM` max) |
| `POS(s1$, s2$, [start])` | num | position of `s2$` in `s1$`, 0 if none (`^`-prefix on `s2$` = case-insensitive; negative `start` = search backward) |
| `SREP$(src$, find$, repl$)` | str | string search-and-replace |
| `XLATE$(s$, table$, [start])` | str | translate `s$` through a 256-byte table (input char value `n` → the `(n+1)`-th char of `table$`; longer values pass through; `STR2UTF`/`UTF2STR` tables do UTF-8) |

## Type conversion & formatting

| Function | Returns | Description |
|---|---|---|
| `STR$(n)` | str | number → plain string |
| `VAL(s$)` | num | string → number |
| `CNVRT$(spec$, n)` | str | number → string per a FORM code (`B BH BL D G GZ L N NZ PD PIC S ZD`) |
| `CFORM$(form$)` | str | compile a FORM string into a fast (opaque, release-dependent) format value |
| `HEX$(s$)` / `UNHEX$(s$)` | str | chars → hex notation / hex → chars |
| `PIC$` | str | current currency symbol (atom) |
| `PIC$(sym$)` | str | set the currency symbol to 1-char `sym$` (assignable; persists per workstation) |

## Numeric & math

| Function | Returns | Description |
|---|---|---|
| `INT(n)` | num | integer part (truncates) |
| `IP(n)` / `FP(n)` | num | integer / fractional part (sign preserved) |
| `CEIL(n)` | num | smallest integer ≥ `n` |
| `TRUNC(n)` ✗ | num | **reserved but not implemented** — parses (1 numeric arg) but errors at runtime (`trig()` has no case); no `[,d]` form. Use `INT`/`IP` |
| `ROUND(n, d)` | num | round to `d` decimals |
| `ABS(n)` | num | absolute value (intrinsic — resolved outside `table6k/7k`) |
| `SGN(n)` | num | sign: `-1` / `0` / `1` (a near-zero value can round to `0` per the `RD` config) |
| `SQR(n)` | num | square root |
| `MOD(a, b)` / `REM(a, b)` | num | remainder (`REM` is an alias of `MOD`); **function only — no infix `a MOD b`** |
| `MAX(n…)` / `MIN(n…)` | num | largest / smallest of a numeric list |
| `MAX$(s$…)` / `MIN$(s$…)` | str | largest / smallest string (ASCII order) |
| `SIN(n)` `COS(n)` `TAN(n)` `ATN(n)` | num | trig / arctangent (radians) |
| `LOG(n)` / `EXP(n)` | num | natural log / e^n |
| `DEG(n)` ✗ / `RAD(n)` ✗ | num | **reserved but not implemented** — recognized keywords that error at runtime (`trig()` has no case); no conversion exists in the current source |
| `RND` | num | pseudo-random `0`–`1` (seed with `RANDOMIZE`, or `LET RND(seed)` for a repeatable sequence) |
| `SHIFT[(n)]` | num | always returns `0` — a legacy System/23-compatibility no-op (argument ignored) |

## Date / time

| Function | Returns | Description |
|---|---|---|
| `DATE$` | str | current date `yy/mm/dd` (atom) |
| `DATE$(days, mask$)` | str | format a day-count to a string (time masks 4.30+) |
| `DATE(days, mask$)` | num | numeric date sibling of `DATE$` (stores the days value, for sorting) |
| `DAYS(date, [mask$])` | num | day-count; Y2K-aware (dates from 1700, 3.90+) |
| `SQL_DATE$(d, fmt$)` / `BR_DATE$(s$, fmt$)` | str | pack / unpack SQL dates (4.30+) |

## Array-processing (used with `MAT`)

| Function | Returns | Description |
|---|---|---|
| `UDIM(MAT arr, [dim])` | num | current size of an array (or of dimension `dim`) |
| `SUM(MAT arr)` | num | sum of all elements |
| `SRCH(MAT arr, arg, [start])` | num | row of a match (0/-1 if none; `^`-prefix = case-insensitive) |
| `AIDX(MAT arr)` / `DIDX(MAT arr)` | mat num | ascending / descending **index** array (source unchanged; used in a `MAT =` assign) |
| `STR2MAT(s$, MAT a$ (out), [[MAT]sep$], [flags$])` | num | split string → array (dynamically redims `a$`); returns the count. `sep$` is a user delimiter (default = any `\n`/`\r` run; `""` = per-char); `flags$` = quote type `Q`/`'`/`"` + `:TRIM`/`:LTRM`/`:RTRM` |
| `MAT2STR(MAT a$, s$ (out), [[MAT]sep$], [flags$])` | num | join array → string; returns the count. `sep$` default = `CRLF`/`CR`, placed after every element incl. the last; `""` concatenates |

## File / drive query

| Function | Returns | Description |
|---|---|---|
| `FILE$([n])` | str | open file's name; no arg = file of the most recent I/O error |
| `FILE(n)` | num | status: `-1` not open, `0` ok, `10/11` EOF, `20/21` transmission error |
| `FILE(n, kind$, MAT a (out))` | num | `"WINDOW_RECT"`/`"USABLE_RECT"` (x,y,w,h px) or `"FONTSIZE"` (cell) |
| `FREESP(n)` | num | free bytes on the drive holding file `n` |
| `EXISTS(file$)` | num | nonzero if file/PROC exists (`1`=directory, `>1`=file) — test zero/nonzero only |
| `BR_FILENAME$(os$)` / `OS_FILENAME$(br$)` | str | convert OS path ↔ BR filename (4.18+) |
| `KPS(n, [seg])` | num | key start position (`seg` = split-key section; `-1` if none) |
| `KLN(n, [seg])` | num | key length (split-key aware) |
| `KREC(n)` | num | last record in the **index/key** file (not the master) |
| `REC(n)` / `LREC(n)` | num | current / last record number |
| `RLN(n, [newlen])` | num | record length of file `n`; `newlen` resets it (EXTERNAL only, ≤ OPEN `RECL=`) |
| `VERSION(n, [ver])` | num | marked version number of INTERNAL file `n` (**not** the BR release); `ver` sets it when open `OUTPUT` |
| `LINES(n)` | num | lines printed since the last new-page |
| `LINESPP(n)` | num | current lines per page (PRINTER `LPP`, else 66) |
| `LINESTATUS$(n)` | str | serial-line/modem status of channel `n` — see 30-io-file/serial-comm |
| `PRINTER_LIST(MAT a$ (out))` | num | redim `a$` to the active Windows printer names |

## Screen & keyboard (cursor, input results)

| Function | Returns | Description |
|---|---|---|
| `KSTAT$([n], [secs])` | str | unprocessed keystrokes; with `n`, wait for `n` keys (BR scancodes — `UNHEX$` to read) |
| `NXTFLD([…])` | num | relative position of the next control to be occupied (4 forms) |
| `CURTAB([win], [1])` | num | active tabbed-window number; `CURTAB(win,1)` raises it (assignable) |
| `CURPOS` | num | cursor position **within the field data** when control returns (4.20+; excludes untyped trailing spaces, counts invisible CRLF) — atom |
| `CURFLD([field], [attr$], [fkey])` | num | 1-based field after the last `INPUT FIELDS`; with args **sets** the next input's start field/attrs (assignable) |
| `CURWINDOW(n)` | num | focused `PARENT=NONE` window (`-1` if none); `n` raises it (assignable) |
| `CMDKEY` | num | key that terminated input (`0`=Enter; `-1` before first input). `LET CMDKEY(x)` presets (assignable, atom) |
| `FKEY` | num | richer successor to `CMDKEY` (preferred); set by controls/buttons/hot windows. `LET FKEY(x)` (assignable, atom; `FNKEY`=`FKEY` as of 4.20) |
| `MENU` | num | subscript of the selected native-menu item |
| `MENU$` | str | data string of the selected native-menu item |
| `SCR_FREEZE` / `SCR_THAW` | num | **(no args)** suspend / resume **remote (client-server) display** repaint (`freezeRemoteDisplay`/`thawRemoteDisplay`); return `0` |

## System / information

| Function | Returns | Description |
|---|---|---|
| `BRERR$(code)` | str | the *description* of a BR error code (what `ERR` is to the number; 4.3+) |
| `SYSERR` | num | system (OS) error number — home: 90-reference/error-codes |
| `SYSERR$` | str | system error description — home: 90-reference/error-codes |
| `ENV$(status$, [MAT cfg$ (out)], [arg])` | str | environment / status interrogation (4.30+) |
| `SETENV(name$, [value$])` | num | set a BR **session** environment variable (function form of `CONFIG SETENV`; read back with `ENV$`). 2 args = `name$`,`value$`; 1 arg = a `NAME=VALUE` directive |
| `MSG$(text$)` | str | display text in the 2nd box of the command console |
| `MSG(action$, arg)` | num | keyboard control, Windows/CS (**not** a companion of `MSG$`): `MSG("KB",keys$)` injects keystrokes, `MSG("sleeptime",cs)` sets the delay — home: 70-commands/information |
| `SLEEP(seconds)` | num | pause (fractional seconds, ms resolution) |
| `HELP$([*]kw$, [file$], [mark])` | str | enter HELP mode / show a topic; returns a scancode or selection |
| `MSGBOX(prompt$, [title$], [buttons$], [icon$])` | num | Windows message box; returns the chosen button (also in `CNT`): 1 OK · 2 Yes · 3 No · 4 Cancel |
| `DEBUG_STR(level, str$)` | num | emit `str$` to the debug log (4.3+) |
| `PROCLVL` | num | current procedure nesting level (`0` = keyboard / not in a procedure) — atom |
| `TIMER` | num | seconds since the Unix epoch (1970-01-01 UTC) as a 5-decimal real — atom |
| `SERIAL` | num | serial number of this BR software copy — atom |
| `SESSION$` | str | this session's ID — `WSID` + a 1-digit session number `1`–`9` (e.g. `011`) — atom |
| `VARIABLE$` | str | name of the variable that failed in the **last I/O statement** (not for field-spec errors 850–890 or calculated expressions) — atom |
| `WBVERSION$` / `WBPLATFORM$` | str | running BR version / platform string (`WBPLATFORM$` = `WINDOWS` on unix CS under `CONFIG SHELL DEFAULT CLIENT`) — atoms |
| `NEWPAGE` | str | a char that form-feeds the printer / clears the screen and zeroes the line counter (atom) |
| `BELL` | str | a char that sounds the tone (atom) |
| `TAB(x)` | — | tab to column `x` — **valid only inside a `PRINT` list** |

### Integration / native (name-level — verify against the cited leaf)

Signatures below are source-verified against `strfunct.cpp`/`numfunct.cpp` (`GET$`/`SET$` → 2 strings,
`INVOKE$` → 3, `DLL` → ≥2 strings, all dispatched client-side). `CALL` is the lone `✗`: it is in
`table7k` but has **no function implementation** (compiler-rejected).

| Function | Returns | Role |
|---|---|---|
| `GET$("#f,r,c", prop$)` | str | read a `.NET`/PEM control property (remote `PEM_PROPERTY_CALL`) |
| `SET$("#f,r,c", assign$)` | str | set a control property, `"prop=value"` (dotted paths allowed) |
| `INVOKE$("#f,r,c", method$, MAT args$)` | str | invoke a control method (`method$` from `INPUT FIELDS … METHOD_NAMES`); results written back into the args array |
| `DLL(a$, b$, …)` | num | call a client-side DLL command (≥2 args, first two strings; errors 0321–0327) |
| `CALL` ✗ | num | **reserved keyword, no implementation** — in `table7k` but rejected as a function expression |

> **OS shell access — `SYSTEM` (a command, not a function).** Not in `table6k`/`table7k`, so it has no
> entry above, but it is a program's primary way to reach the operating system, so it's noted here for
> findability. A program runs it via `EXECUTE`: `EXECUTE "SYSTEM '<os-command>'"` launches another
> application / runs a shell command (flags: `-C` async, `-R` restore screen, `-@`/`-S` client/server
> side, `-M`/`-m` hide/minimize); `SYSTEM [<n>]` exits BR to the OS with exit code `<n>`; `SYSTEM LOGOFF`
> logs the client off. Runs arbitrary OS commands with the caller's privileges — security-sensitive.
> Full description: [70-commands/program-management §SYSTEM](../br_tree/70-commands/program-management/spec.md#system).

## Encryption (4.30+) — deep reference: `system-functions/Encryption.md`

| Function | Returns | Description |
|---|---|---|
| `ENCRYPT$(data$, [key$], [type$], [iv$])` | str | encrypt; types AES/BLOWFISH/DES/3DES/RC4/RC2 (default `AES:256:CBC:128`) |
| `DECRYPT$(data$, [key$], [type$], [iv$])` | str | inverse of `ENCRYPT$` |
| `ENCRYPT$(data$, "", "MD5"\|"SHA"\|"SHA-1")` | str | one-way hash |

---

**✗ not usable:** the name is a live keyword in `table6k`/`table7k` (so it lexes and, for the numeric
ones, may compile) but it has **no working implementation** — `TRUNC`/`DEG`/`RAD` reach `trig()`'s
`default` and return a bad-function error at runtime; `CALL` is rejected by `ck_num_sysfn`. Do not emit
completions for these as callable functions. (Signatures for every other entry are source-verified; the
former `†` "unverified" tier is retired.)
