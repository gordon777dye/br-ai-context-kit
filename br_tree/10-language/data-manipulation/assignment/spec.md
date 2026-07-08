---
title: Assignment & data movement
file: spec.md
source: §Statements (Assignment, MAT, DATA/READ/RESTORE), §String Operations
category: 10-language
subcategory: 10-language/data-manipulation/assignment
kind: spec
status: 2b           # reference base + br_tree enrichment (multiple assignment, += compound ops, append/prepend idioms); no conflicts
related: [expressions, declaration, data-types, system-functions]
keywords: [LET, MAT, DATA, READ, RESTORE, ":="]
---

# Assignment & data movement

Putting values into variables and arrays and changing them in place: `LET`, the forced-assignment
operator `:=`, `MAT` array operations, substring mutation, and the internal data table
(`DATA`/`READ`/`RESTORE`). Operators that *form* the right-hand-side values are in
[expressions](../expressions/spec.md); declaring/sizing storage is in
[declaration](../declaration/spec.md).

<a id="syntax"></a>
## Syntax

```bnf
[LET] <variable> = <expression>
<forced-assignment> ::= <variable> ':=' <expression>

<mat-assignment> ::= MAT <array-name> [ '(' <dimension> [',' <dimension>]* ')' ] '=' <mat-rhs>
<mat-rhs>        ::= '(' <expression> ')'                          -- init all elements
                   | <array-name> | <sub-array-reference>          -- copy / copy subarray
                   | <numeric-array> { '+' | '-' } <numeric-array> -- element-wise
                   | '(' <numeric-expression> ')' <op> <numeric-array>  -- scalar × array
                   | AIDX '(' <array-name> ')' | DIDX '(' <array-name> ')'  -- sort index

<substring-target> ::= <string-variable> '(' <start-pos> ':' <end-pos> ')'   -- left of '='

READ <variable-list>            -- from the internal data table
DATA <value> [',' <value>]*
RESTORE [<line-ref>]
```

<a id="semantics"></a>
## Semantics

<a id="let"></a>
### LET
Assigns a value or computed expression; `LET` is optional (`X = Y*2+Z` is an implicit `LET`).
String values must be quoted and cannot be used in arithmetic. In immediate mode (no line number)
an assignment also prints its result. `LET` also **calls a function** (the assignment target is
optional: `FNSCRNH(LINES)` runs a function for effect; for a library function `LET` loads & runs it).
- **Multiple assignment** — assign one value to several variables at once:
  `LET SUMA = SUMB = SUMC = SUMD = 0`.
- **Compound assignment operators** `+=`, `-=`, `*=`, `/=` update a variable in place:
  `LET TOTAL += AMT` (= `TOTAL = TOTAL + AMT`).

<a id="forced-assignment"></a>
### Forced assignment `:=`
Always performs assignment — even inside a conditional, where a plain `=` would mean "is equal
to". It evaluates the RHS, assigns it, and yields the assigned value as the expression result.
- **Parenthesize** it inside `IF`/`WHILE`/`UNTIL` so the assignment happens first, then the result
  is compared.
- Works for numeric and string variables; can nest in larger expressions.
- Do **not** use it in a `LET` — plain `=` is idiomatic there. (Operator precedence of `:=` is in
  [expressions](../expressions/spec.md#forced-assignment).)

| Context | `=` means | `:=` means |
|---|---|---|
| `LET X = 5` | assignment | not idiomatic — use `=` |
| `IF X = 5 THEN` | comparison (is X = 5?) | n/a |
| `IF (X := 5) > 2 THEN` | compares X to 5 | assigns 5 to X, then tests 5 > 2 (true) |

<a id="mat"></a>
### MAT operations
Whole-array operations, much faster than element loops. Scalars must be parenthesized when used
with an operator. (Runtime *resizing* via `MAT` is in
[declaration](../declaration/spec.md#redimensioning).)
- **Initialize**: `MAT A = (0)`, `MAT B$ = ("")`
- **Copy**: `MAT A = B`, subarray `MAT A(6:10) = B` (copies `B(1:5)`)
- **Arithmetic**: `MAT A = B + C` (element-wise), `MAT SAL = (1.064) * SAL` (scalar × array)
- **Sort index**: `MAT ORDER = AIDX(CUST$)` / `DIDX(...)` builds an *index* array (original
  unchanged); see [system-functions](../system-functions/spec.md#array-functions).

<a id="substring"></a>
### Substring mutation
A substring on the **left** of `=` changes part of a string (positions are 1-based, inclusive;
`0` inserts before, `inf` appends). Reading a slice on the right is a string *expression*
([expressions](../expressions/spec.md#concatenation)).
```business-rules
00210 X$(2:3) = "23"      ! replace  → "A23D"   (from "ABCD")
00310 Y$(2:3) = ""        ! delete   → "AD"
00410 Z$(2:0) = "123"     ! insert   → "A123BCD"
00430 Z$(inf:inf) = "End" ! append
```
The string must be dimensioned large enough; an insertion that exceeds the slice extends the
result (but cannot exceed `DIM`). Idioms: **append** with `X$(inf:0)=…` (fastest) or `X$(inf:inf)=…`;
**prepend** with `X$(0:0)=…` or `X$(1:0)=…`; **insert** with `X$(pos:0)=…`; **delete** with
`X$(pos:end)=""`.

<a id="data-table"></a>
### Internal data table — DATA / READ / RESTORE
`DATA` defines an internal table of constants (non-executable; all `DATA` lines merge in
line-number order). `READ` pulls the next value(s) into variables, advancing the pointer.
`RESTORE` resets the pointer (optionally to a specific `DATA` line). `MAT READ` fills a whole
array at once.

<a id="examples"></a>
## Examples

```business-rules
00050 LET MPG = MI/GAL           ! compute
00080 PUMA = COUGAR              ! implicit LET (copy)
00150 DO WHILE (LINE$ := LINPUT$(1)) <> ""   ! assign-and-test
00160    PRINT LINE$
00170 LOOP

00100 MAT A = (0)                ! init all to 0
00350 MAT SAL = (1.064) * SAL    ! 6.4% raise to every salary
00520 READ MAT CUST$ : MAT ORDER = AIDX(CUST$)   ! ascending index

00100 DATA 6,17,38,49,66,75,93,84,77,67,42,22
00110 READ MAT SPTEMP            ! load all 12 at once
00300 RESTORE                    ! reset DATA pointer
```

<a id="see-also"></a>
## See also

- [expressions](../expressions/spec.md) — operators forming RHS values; `:=` precedence; substring extraction
- [declaration](../declaration/spec.md) — `DIM`/`MAT` sizing of the targets
- [system-functions](../system-functions/spec.md#array-functions) — `AIDX`/`DIDX`, `STR2MAT`, `SRCH`
- [data-types](../data-types/spec.md) — value kinds being assigned
- (Backing keyword pages folded into this spec and pruned.)
