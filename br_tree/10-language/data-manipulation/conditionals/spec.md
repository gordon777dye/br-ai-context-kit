---
title: Conditionals (IF)
file: spec.md
source: §Control Structures → Conditional Execution
category: 10-language
subcategory: 10-language/data-manipulation/conditionals
kind: spec
status: 2b           # reference base; br_tree pages (IF/ELSE/END_IF) verified — all corroborate; no conflicts
recovered-fold: Conditional_Expression (folded+pruned — implied <>0, SKIP, operator list; verbatim retained on the BR wiki)
related: [expressions, other-flow]
keywords: [IF, THEN, ELSE]
---

# Conditionals (IF)

`IF` / `THEN` / `ELSE` / `END IF` branching. The conditions themselves — relational and logical
operators, and the two meanings of `=` — are defined in
[expressions](../expressions/spec.md#relational-operators).

<a id="syntax"></a>
## Syntax

```bnf
IF <condition> THEN <statement-or-line> [ELSE <statement-or-line>]

IF <condition> THEN <statement-or-line>
   [ELSE IF <condition> THEN <statement-or-line>]* [ELSE <statement-or-line>]

IF <condition> THEN
    <statements>
[ELSE IF <condition> THEN
    <statements>]*
[ELSE
    <statements>]
END IF
```

<a id="semantics"></a>
## Semantics

- Conditions are evaluated **sequentially**; the **first** branch whose condition is true runs,
  and **only one** branch ever executes. `ELSE` runs when no condition was true.
- The **single-line** form needs no `END IF`; the **multi-line** form **requires** `END IF`.
- **Truth values**: true = `1`, false = `0`; **any non-zero number is true**. A bare string
  cannot be used as a condition (use a relational expression). `IF A THEN …` is an implied
  `IF A<>0`, and the same conditional-expression form also drives the `SKIP` command (true → skip).
- **Comparison operators**: `=`/`==`, `<>`/`><`/`~=` (not equal), `<`, `>`, `<=`/`=<`, `>=`/`=>`, with
  `AND`/`OR`/`NOT` (`~`); full operator/precedence detail in
  [expressions](../expressions/spec.md#relational-operators).

<a id="examples"></a>
## Examples

```business-rules
00070 IF CHOICE = 1 THEN PRINT "Video games cost $17.99 each"
00090 IF CHOICE = 2 THEN PRINT "DVDs cost $14.00 each" ELSE PRINT "Item not recognized"

! Multi-line with ELSE IF — requires END IF
00100 IF AGE <= 5 THEN
00110    PRINT "Kids get 50% off"
00120    LET DISCOUNT = 50
00130 ELSE IF AGE > 5 AND AGE < 65 THEN
00150    LET DISCOUNT = 0
00160 ELSE
00170    PRINT "Senior discount 20%"
00180    LET DISCOUNT = 20
00190 END IF
```

<a id="see-also"></a>
## See also

- [expressions](../expressions/spec.md) — relational/logical conditions; `=` vs `:=`
- [other-flow](../../flow-control/other-flow/spec.md) — `DO WHILE`/`UNTIL` loops that test conditions
- (Backing keyword pages verified against this spec and pruned.)
