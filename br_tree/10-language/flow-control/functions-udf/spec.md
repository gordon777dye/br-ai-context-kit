---
title: User-defined functions (DEF / FN)
file: spec.md
source: §Functions → User-Defined Functions, §Libraries (DEF LIBRARY, parameter passing & scope)
category: 10-language
subcategory: 10-language/flow-control/functions-udf
kind: spec
status: 2b           # reference base + br_tree enrichment (single-line DEF, string-fn length, recursion, function-authoring gotchas: return-name-is-call, single exit, no-paren calls, no array dims in params); no conflicts
related: [other-flow, syntax, system-functions]
---

# User-defined functions (DEF / FN)

Defining your own `FN…` functions with `DEF … FNEND`, their parameters (by value vs. by
reference), local scope, and return value. The library *facility* that loads and links functions
across programs (`LIBRARY` statement, loading strategies, search order) is in
[50-libraries/library-facility](../../../50-libraries/library-facility/spec.md). Built-in
intrinsic functions are in
[system-functions](../../data-manipulation/system-functions/spec.md).

<a id="syntax"></a>
## Syntax

```bnf
-- single-line form (the whole function is one expression)
DEF FN<name>[$ '*' <len>] [ '(' <parameter-list> ')' ] '=' <expression>

-- multi-line form
DEF FN<name>[$ '*' <len>] [ '(' <parameter-list> ')' ]
    <statements>
    [LET] FN<name> = <expression>      -- the return value
FNEND

<parameter-list> ::= <params> [ ';' <params> ]   -- ';' : every param after it is OPTIONAL
                   | ';' <params>                -- an all-optional list (no required params)
<params>         ::= <parameter> [ ',' <parameter> ]*
<parameter>      ::= [ MAT | '&' ] <variable> [ '*' <len> ]   -- '&' = by reference; MAT = array
<def-library>    ::= DEF LIBRARY <function-name>[(<parameter-list>)] … FNEND
```

A function name is `FN` + up to 28 more chars (**30 max, `FN` included**); a **string** function's
trailing `$` is extra (size via `$*<len>`).
Parameters **before** the `;` are required; those **after** it are optional — and any optional the
caller omits becomes a fresh **local variable** (see [Scope & local variables](#local-variables)).
A **scalar** parameter prefixed with `&` (e.g. `&RATE`) is passed **by reference**. **Arrays (`MAT`)
are always passed by reference** and must **not** take `&` — `&MAT` is illegal.

**Calling.** A call to a function with no parameters takes **no parentheses** — `X$ = FNGETNAME$`,
not `FNGETNAME$()` (empty `()` is a syntax error). Call a function for its side effects with a bare
`LET FN<name>`.

<a id="semantics"></a>
## Semantics

<a id="def"></a>
### Defining a function
- **Single-line** functions compute one expression: `DEF FNY(X) = (X-INT(X/100)*100)*10000+INT(X/100)`.
- **Multi-line** functions run between `DEF FN<name>` and `FNEND` and **return a value** by assigning
  to their own name: `LET FN<name> = <expression>` (if never assigned, they return 0 / null). Only
  multi-line functions can do file I/O, change by-reference params, and **recurse** (a fresh local
  copy of each by-value parameter is created per call).
- **The return name is write-only.** Inside the body, `FN<name>` used in an **expression** is a
  **recursive call**, not a readable "value so far". You may assign `FN<name>` as often as you like
  (the last write wins), but build an incremental result in an ordinary scratch variable — never by
  reading `FN<name>` back.
- **One exit per function.** A function has exactly one `FNEND` and no early-return statement
  (`RETURN` belongs to `GOSUB`). To leave early, `GOTO` a label placed just before `FNEND`.
- **`DEF LIBRARY`** marks a function as callable from other programs through the library facility
  (it must still be linked with a `LIBRARY` statement before another program can call it — see
  [library-facility](../../../50-libraries/library-facility/spec.md)). An entire program can be
  wrapped as one `DEF LIBRARY` function.

<a id="parameters"></a>
### Parameters — by value vs. by reference
- Plain parameters are passed **by value** (the function gets a copy).
- Prefix with **`&`** to pass **by reference** — the function reads/writes the caller's variable.
  For arrays this also **avoids copying**, which is faster:
  ```business-rules
  DEF LIBRARY FNPROCESS(&DATA$, &VALUE)   ! efficient — no copy
  DEF LIBRARY FNPROCESS(DATA$, VALUE)     ! copies the values
  DEF LIBRARY FNPROCESS(MAT ARRAY)        ! always passed by reference
  ```
- **No array dimensions in the parameter list.** A parameter is `[MAT|&] name [*len]`: you may size a
  *string* parameter (`NAME$*20`) but **not** dimension an array in the signature (`ROW(1)*255` is
  illegal). Arrays arrive as `MAT name`, dimensioned by the caller or a separate `DIM`; declare array
  *locals* with their own `DIM`, never in the parameter list.

<a id="local-variables"></a>
### Scope & local variables
- **By-value parameters are local** — a plain parameter is a private copy; assigning it never touches a
  like-named variable outside the function. `&` (by-reference) and `MAT` parameters are local *names*
  too, but writing them updates the caller's variable.
- **Declaring locals via the `;` (optional-parameter) list** — a semicolon in the parameter list marks
  **every parameter after it as optional**. When the caller omits an optional parameter, BR creates a
  **fresh temporary variable** for it, initialised to `0`/null on *each* call. This is the standard idiom
  for **local variables**: after the `;`, list first any optional parameters the caller *may* pass, then
  the names you want purely as private scratch variables (which no call ever passes). An unpassed
  by-reference optional defaults an array to dimension 1 and a string to length 18. A function may be
  all-optional (`DEF FNX(;A,B$)`); a caller may **not** pass more arguments than are defined, and the
  variable types (numeric/string) must match.
- Each library has it's own set of global variables. The rules for clearing these variables are sophisticated and need to be carefully considered.
- When library globals are cleared depends on how the library was loaded (resident vs. release vs.
  `OPTION RETAIN`) — see the table in
  [library-facility](../../../50-libraries/library-facility/spec.md).
- On an error inside a function, `LINE` is the call site in the caller, `ERR` the error number,
  and `CNT` is set for context.

<a id="examples"></a>
## Examples

```business-rules
! Simple library function with a return value
00240 DEF LIBRARY FNCALC(AMT)
00250    LET FNCALC = AMT * (1 + TAX_RATE) * (1 - DISCOUNT_PCT)
00260 FNEND

! Initialization function sets library globals via by-reference params
00100 DIM TAX_RATE, DISCOUNT_PCT          ! library globals
00200 DEF LIBRARY FNINIT(&RATE, &DISCOUNT)
00210    LET TAX_RATE = RATE
00220    LET DISCOUNT_PCT = DISCOUNT
00230 FNEND

! Caller
00100 LIBRARY "CALC": FNINIT, FNCALC
00110 LET FNINIT(TAX_RATE, DISCOUNT_PCT)
00120 LET RESULT = FNCALC(AMOUNT)

! Optional parameter + locals after the ';':
!   QTY, UNIT are required; DISCOUNT is an optional the caller may pass;
!   TAX and TOTAL are never passed → fresh locals (0) on each call.
00300 DEF FNPRICE(QTY, UNIT; DISCOUNT, TAX, TOTAL)
00310    LET TOTAL = QTY * UNIT
00320    IF DISCOUNT > 0 THEN LET TOTAL = TOTAL * (1 - DISCOUNT)
00330    LET TAX = TOTAL * 0.06
00340    LET FNPRICE = TOTAL + TAX
00350 FNEND
```

<a id="see-also"></a>
## See also

- [50-libraries/library-facility](../../../50-libraries/library-facility/spec.md) — `LIBRARY` statement, loading, search order, clearing rules
- [system-functions](../../data-manipulation/system-functions/spec.md) — built-in functions
- [other-flow](../other-flow/spec.md) — `GOSUB`/`RETURN` subroutines (the non-function alternative)
- [syntax](../../syntax/spec.md) — line labels / paragraph labels inside functions
- (Backing keyword pages folded into this spec and pruned. The
  normal-vs-library feature comparison lives in [library-facility](../../../50-libraries/library-facility/spec.md).)
