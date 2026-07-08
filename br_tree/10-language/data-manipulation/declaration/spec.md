---
title: Declaration (variables & arrays)
file: spec.md
source: §Variables, §MAT (redimensioning)
category: 10-language
subcategory: 10-language/data-manipulation/declaration
kind: spec
status: 2b           # reference base + br_tree enrichment (OPTION BASE/statement, DIMONLY); no conflicts
recovered-fold: Array_Name, Numeric_Variable (2 redirect-collision pages folded from re-fetched source — name must start with a letter (corrected from "letter or _"), FN-prefix reserved, scalar/array/string co-existence; verbatim retained on the BR wiki)
related: [data-types, assignment, expressions]
keywords: [DIM, MAT, OPTION]
---

# Declaration (variables & arrays)

Declaring storage: variable kinds and naming, `DIM` for string length and arrays, and runtime
redimensioning with `MAT`. Putting *values* into variables/arrays (`LET`, `MAT` copy/arithmetic,
`READ`/`DATA`) lives in [assignment](../assignment/spec.md); the value kinds themselves are in
[data-types](../data-types/spec.md).

<a id="syntax"></a>
## Syntax

```bnf
<numeric-variable> ::= <identifier>
<string-variable>  ::= <identifier> '$'
<numeric-array>    ::= <identifier> '(' <subscript> [',' <subscript>]* ')'
<string-array>     ::= <identifier> '$' '(' <subscript> [',' <subscript>]* ')'

DIM <variable-list>
<variable-list>        ::= <variable-declaration> [',' <variable-declaration>]*
<variable-declaration> ::= <numeric-variable>
                         | <string-variable> '*' <max-length>
                         | <array-declaration>
<array-declaration>    ::= <array-name> '(' <dimension> [',' <dimension>]* ')' ['*' <max-length>]
<dimension>            ::= <integer>
```

<a id="semantics"></a>
## Semantics

### Variables
- **Numeric** (`X`, `TOTAL_COST`) default to `0`; **string** (ends in `$`, e.g. `NAME$`) default
  to the empty string and cannot do arithmetic.
- **Case-insensitive** (`NAME$` = `name$`) and **implicitly declared** on first use.
- **Naming**: **begin with a letter** (1–30 chars of letters, digits and `_`); not a reserved word,
  and **never an `FN…` name** (those are reserved for user-defined functions). The *same* identifier
  can coexist as a numeric scalar, numeric array, string scalar **and** string array — `A`, `MAT A`,
  `A$`, `MAT A$` are four distinct variables.
- Values **persist** until reassigned, or cleared by `CLEAR`, `RUN`, `LOAD`, `CHAIN`, or exit.

<a id="dim"></a>
### DIM
- Sets a string variable's **maximum** length (required above the 18-char default) and **declares
  arrays**. Syntax `DIM name$*length`; actual length ≤ maximum (use
  [`LEN`](../system-functions/spec.md#string-functions) for the current length).
- Non-executable (processed before the run); may appear anywhere; multiple declarations per `DIM`.

<a id="arrays"></a>
### Arrays
- Hold many values of **one type** (numeric *or* string) under one name, indexed by subscript.
- **1-based** by default (first element is index 1). Arrays of **≤10 elements need no `DIM`**
  (auto-dimensioned to 10). **1 to 7 dimensions**. Elements are contiguous; defaults are `0`
  (numeric) / empty (string).
- **Size limit** 99,999,999 bytes (4.30+; previously 512 KB).

<a id="option"></a>
### OPTION statement & base
The `OPTION` statement sets program-wide choices: **`OPTION BASE 0`** makes every array include a
**zero element** (`OPTION BASE 1` is the default, 1-based); **`OPTION COLLATE`** picks letters-vs-
numbers-first sort order — **`NATIVE`** (platform/character-set order, e.g. ASCII digits-before-letters)
or **`ALTERNATE`** (EBCDIC-like, digits after letters); **`OPTION`** also selects American vs inverted-European decimal/comma
format. (The numbered `OPTION <nn>` feature toggles are configuration — see
[config-directives](../../../00-configuration/config-directives/spec.md#behavior).) `OPTION` is a
non-executable directive: it **must occupy its own line** (it cannot be compounded with `:`), but it
may appear **anywhere** in the program and takes effect **program-wide** regardless of position.
The **`DIMONLY`** BRConfig.sys/`CONFIG` setting forbids creating a variable during editing unless it
was declared in a `DIM` — a discipline aid against typo-variables.

<a id="redimensioning"></a>
### Redimensioning (MAT)
Resize at runtime with `MAT`; existing values are preserved when growing and lost when shrinking,
and you cannot exceed the original `DIM` size without re-`DIM`ming.
```business-rules
00400 DIM A(100), B(50)
00410 MAT A(200)        ! grow to 200
00420 MAT B(25)         ! shrink to 25
00430 MAT A(10,10) = A  ! reshape 100 → 10×10
```
The value-moving forms of `MAT` (copy, arithmetic, sort) are in
[assignment](../assignment/spec.md#mat).

<a id="tables"></a>
## Tables

| Dimensions | Declaration | Use |
|---|---|---|
| 1-D | `DIM AGE_COUNTS(120)` | linear list |
| 2-D | `DIM OFFICE_COUNTS(40,5)` | matrix (row, col) |
| 3-D | `DIM TEMPERATURES(99,99,24)` | cubic |
| up to 7-D | `DIM X(...)` | complex structures |
| string array | `DIM NAMES$(100)*30` | 100 strings, ≤30 chars each |

<a id="examples"></a>
## Examples

```business-rules
00100 DIM NAME$*30, AMOUNT, SCORES(100), MATRIX(10,10)
00120 DIM LONG_MESSAGE$*80      ! string up to 80 chars
00140 DIM NAMES$(100)*30        ! array of 100 strings, each ≤30 chars
00080 DIM MATRIX(5,4)           ! 5×4 two-dimensional array
00090 DIM DATA$(5,3,2)*20       ! three-dimensional string array
```

<a id="see-also"></a>
## See also

- [assignment](../assignment/spec.md) — `LET`, `MAT` copy/arithmetic, `READ`/`DATA` to populate arrays
- [data-types](../data-types/spec.md) — the value kinds being stored
- [system-functions](../system-functions/spec.md#array-functions) — `UDIM`, `SUM`, `AIDX`/`DIDX`, `LEN`
- [30-io-file/form-spec](../../../30-io-file/form-spec/spec.md) — `DT`/`DL`/`DH` date FORM specs (relocated there)
- [20-io-screen/input-output](../../../20-io-screen/input-output/spec.md) — MAT grouping in FIELDS I/O lists (relocated there)
- Backing keyword page (deep MAT reference retained): [MAT](MAT.md)

*(2 redirect-collision pages re-fetched in 2b — `Array_Name`, `Numeric_Variable` — were folded into this
spec and pruned; verbatim wikitext remains on the BR wiki.)*
