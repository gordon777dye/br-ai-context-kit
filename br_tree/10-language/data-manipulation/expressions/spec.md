---
title: Expressions
file: spec.md
source: §Operators and Expressions
category: 10-language
subcategory: 10-language/data-manipulation/expressions
kind: spec
status: 2b           # reference base; br_tree pages verified (all corroborate); corrected 2026-07-03: MOD is a function, not an infix operator (removed from precedence table); no conflicts
related: [assignment, conditionals, data-types, declaration]
---

# Expressions

Operators, precedence, and the numeric / string / relational / logical expressions that BR
evaluates. Substring *mutation* and the `LET` form of assignment live in
[assignment](../assignment/spec.md); the `IF` / `WHILE` / `UNTIL` constructs that consume
relational expressions live in [conditionals](../conditionals/spec.md).

<a id="syntax"></a>
## Syntax

```bnf
<expression>            ::= <numeric-expression> | <string-expression> | <relational-expression>
<numeric-expression>    ::= <numeric-term> [ <numeric-operator> <numeric-term> ]*
<string-expression>     ::= <string-term> [ '&' <string-term> ]* | <substring>
<substring>             ::= <string-expr> '(' <start-pos> ':' <end-pos> ')'
<relational-expression> ::= <expression> <relational-operator> <expression>
```

<a id="semantics"></a>
## Semantics

### Evaluation order
Innermost parentheses first, then by operator precedence (see [precedence table](#precedence)),
left to right within the same level. The algebraic core is PEMDAS — **P**arentheses,
**E**xponents, **M**ultiplication/**D**ivision, **A**ddition/**S**ubtraction.

<a id="forced-assignment"></a>
### The two meanings of `=`, and forced assignment `:=`
`=` is overloaded by context:
- Inside a conditional expression (`IF`, `WHILE`, `UNTIL`), `=` is **always** the
  "is equal to" comparison operator.
- In a `LET` statement (or any non-conditional context), `=` is **always** assignment.

Use **`:=`** to force *assignment* semantics even inside a conditional; the assignment must be
parenthesized:

```business-rules
00010 IF (X := 5) > 2 THEN PRINT "assigned X then compared"
```

The assignment-statement side of `:=` (and `LET`) is detailed in
[assignment](../assignment/spec.md#forced-assignment).

<a id="relational-operators"></a>
### Relational expressions
Comparisons return **1** (true) or **0** (false), and work on both numeric and string operands.
String comparisons run **character-by-character, left to right, by ASCII value**, stop at the
first unequal pair, and are **case-sensitive**. Operators are *binary* (two operands: `+`, `=`,
`<`, …); `NOT` / `~` is the *unary* negation operator (`NOT` preferred for readability).

<a id="logical-operators"></a>
### Logical operators
`NOT`/`~`, `AND`/`&&`, `OR`/`||` combine relational expressions. Precedence within a logical
expression: parentheses → `NOT` → `AND` → `OR`, left to right within a level. See the
[truth tables](#truth-tables).

<a id="concatenation"></a>
### String expressions
- **Concatenation** joins strings with `&` (precedence level 5):
  `C$ = A$ & " " & B$`. As an operator it forms a `<string-expression>`.
- **Substring extraction** reads a slice with 1-based, inclusive positions —
  `S$(2:4)` yields characters 2–4; `INF` denotes beyond end-of-string
  (`S$(6:INF)`). Used on the right-hand side it is a string expression.
- **Substring replacement / insertion / deletion** (slice on the *left* of `=`) is a data
  *change*, documented in [assignment](../assignment/spec.md#substring).

<a id="tables"></a>
## Tables

<a id="precedence"></a>
### Operator precedence (highest to lowest)
| Level | Operators | Description | Example |
|------:|-----------|-------------|---------|
| 1 | `()` `[]` | Grouping, array indexing | `(5+3)*2`, `ARRAY(5)` |
| 2 | `^` `**` | Exponentiation | `2**3` = 8 |
| 3 | `*` `/` | Multiplication, division | `10/2`, `8/2` |
| 4 | `+` `-` | Addition, subtraction | `5+3`, `10-7` |
| 5 | `&` | String concatenation | `"Hi" & " there"` |
| 6 | `==` `~=` `<>` `><` `<` `>` `<=` `=<` `>=` `=>` | Comparison / relational | `X > 10` |
| 7 | `=` | *is equal to* (comparison; inside `IF`/`WHILE`/`UNTIL`) | `IF X = 5 THEN …` |
| 8 | `NOT` `~` | Logical NOT (negation) | `NOT FOUND` |
| 9 | `AND` `&&` | Logical AND | `X>0 AND Y>0` |
| 10 | `OR` `\|\|` | Logical OR | `A=1 OR B=1` |
| 11 | `=` | Assignment (`LET` / non-conditional context) | `LET X = 5` |
| 12 | `:=` | Forced assignment (assigns even inside a conditional) | `IF (X := 5) > 2 THEN …` |

**Modulo is a function, not an operator** — use `MOD(a, b)`; there is **no** infix `a MOD b`. See
[system-functions](../system-functions/spec.md).

The compound assignment operators `+=` `-=` `*=` `/=` (and multiple assignment `A=B=C=0`) are
assignment-level — see [assignment](../assignment/spec.md#let).

### Relational operators
| Operator | Alternatives | Meaning |
|---|---|---|
| `<` | | Less than |
| `>` | | Greater than |
| `=` | `==` | Equal to |
| `<>` | `><`, `~=` | Not equal to |
| `<=` | `=<` | Less than or equal to |
| `>=` | `=>` | Greater than or equal to |

<a id="truth-tables"></a>
### Logical truth tables
| A | B | `A AND B` | `A OR B` |
|---|---|:---:|:---:|
| true | true | true | true |
| true | false | false | true |
| false | true | false | true |
| false | false | false | false |

<a id="examples"></a>
## Examples

Worked evaluation (precedence in action):
```business-rules
((5+1)*(1+2))+2**3/4
  = (6*3)+2**3/4       ! parentheses first
  = 18+2**3/4          ! more parentheses
  = 18+8/4             ! exponentiation
  = 18+2               ! division
  = 20                 ! addition
```

Relational and logical conditions:
```business-rules
00100 IF X > 10 AND Y < 5 THEN GOTO 500
00110 IF NAME$ = "John" OR NAME$ = "JOHN" OR NAME$ = "john" THEN GOTO 200
00120 IF (A > 0 OR B > 0) AND C = 100 THEN PRINT "Valid"
00130 IF NOT SCORE >= 0 THEN GOTO SCORE_PROMPT
```

String comparison (ASCII, case-sensitive):
```business-rules
00010 IF "a" < "b" THEN PRINT "a is less than b"            ! true
00020 IF "Aaron" > "Aardvark" THEN PRINT "Aaron > Aardvark" ! true (o > d)
```

<a id="see-also"></a>
## See also

- [assignment](../assignment/spec.md) — `LET`, the assignment form of `:=`, substring mutation
- [conditionals](../conditionals/spec.md) — `IF`/`WHILE`/`UNTIL` that consume these expressions
- [data-types](../data-types/spec.md) — the numeric and string operands
- (Backing keyword pages verified against this spec and pruned.)
