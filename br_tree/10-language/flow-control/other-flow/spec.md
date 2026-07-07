---
title: Loops & branching
file: spec.md
source: §Control Structures (Loops, Branching)
category: 10-language
subcategory: 10-language/flow-control/other-flow
kind: spec
status: 2b           # reference base + br_tree enrichment (STOP/END/PAUSE termination); no conflicts
recovered-fold: GOSUB, ON_GOSUB, RANDOMIZE (3 redirect-collision pages folded from re-fetched source — added RANDOMIZE, GOSUB error-1011 immediate restriction, ON-GOSUB NONE-is-a-GOSUB-branch; verbatim retained on the BR wiki)
related: [conditionals, syntax, functions-udf]
---

# Loops & branching

Iteration and control transfer: `FOR/NEXT`, `DO/LOOP`, `GOTO`, `GOSUB`/`RETURN`,
`ON … GOTO/GOSUB`, and `EXIT`. The `IF` decision itself is in
[conditionals](../../data-manipulation/conditionals/spec.md); the conditions are in
[expressions](../../data-manipulation/expressions/spec.md). Targets are `<line-ref>`s
(line number or label) — see [syntax](../../syntax/spec.md#line-labels).

<a id="syntax"></a>
## Syntax

```bnf
FOR <num-var> = <num-expr> TO <num-expr> [STEP <num-expr>]
    <statements>
NEXT <num-var>

DO [{WHILE|UNTIL} <condition>]
    <statements>
    [EXIT DO]
LOOP [{WHILE|UNTIL} <condition>]

GOTO  <line-ref>
GOSUB <line-ref>          ... RETURN
ON <num-expr> GOTO  <line-ref> [',' <line-ref>]* [NONE <line-ref>]
ON <num-expr> GOSUB <line-ref> [',' <line-ref>]* [NONE <line-ref>]
EXIT DO                   -- there is no EXIT FOR; leave a FOR loop with GOTO
RANDOMIZE                 -- reseed RND from the system clock
```

<a id="semantics"></a>
## Semantics

<a id="for-next"></a>
### FOR / NEXT
Counts the loop variable from start to end by `STEP` (default `1`; negative steps count down).
The test happens **before** each pass; the variable **retains its final value** after the loop.
`NEXT` must name the same variable as `FOR`. Loops **nest up to 20 levels** and must be fully
contained (no partial overlap — the inner `NEXT` comes before the outer `NEXT`). Leave early with
`GOTO`.

<a id="do-loop"></a>
### DO / LOOP
Flexible condition loop; the `WHILE`/`UNTIL` test may sit on `DO` (tested first — may run zero
times) or on `LOOP` (tested last — runs **at least once**). No labels needed for the structure;
leave early with `EXIT DO`. `WHILE` continues while true; `UNTIL` continues until true.

<a id="goto"></a>
### GOTO
Unconditional transfer to a `<line-ref>`. Backward jumps form loops; forward jumps skip code.
The target must exist before `SAVE`/`REPLACE`.

<a id="gosub"></a>
### GOSUB / RETURN
Calls a subroutine (a labeled/numbered block ending in `RETURN`); control returns to the line
after the `GOSUB`. The depth of nested GOSUBs is limited by the call stack (`FLOWSTACK`), which is
**configurable** via the BRConfig.sys `FLOWSTACK` directive (default **100**, 4.3+; shared with
user-defined-function returns — see
[config-directives](../../../00-configuration/config-directives/spec.md)); subroutines may call
other subroutines. `GOSUB` **can't run from the command line** (**error 1011**,
illegal immediate statement), and active GOSUBs can't be edited during an interruption; `RETURN`
resumes at the statement after the call even if that's mid-way through a multi-statement line.

<a id="on-goto"></a>
### ON … GOTO / GOSUB
Multi-way branch: the numeric expression is **rounded to the nearest integer** and selects the
*n*-th `<line-ref>` (1 = first). If the value is `< 1` or beyond the list, control goes to the
`NONE` target if present, otherwise falls through to the next line. `ON … GOSUB` returns after the
selected subroutine's `RETURN` (menu dispatch pattern); its `NONE` target is itself a **GOSUB** branch
(the routine there must also `RETURN`), not an error handler, and an `ON … GOSUB` may carry trailing
error-condition clauses.

<a id="exit"></a>
### EXIT
`EXIT DO` terminates the **innermost** `DO`/`LOOP` and continues at the first statement after it.
There is **no `EXIT FOR`** in BR — leave a `FOR`/`NEXT` loop early with `GOTO` (see
[FOR / NEXT](#for-next)).

<a id="randomize"></a>
### RANDOMIZE
Reseeds the `RND` random-number generator from the **system clock** so each run differs. **Without
`RANDOMIZE`, `RND` repeats the same sequence every time BR is loaded.** (`RND` returns 0–1; scale it,
e.g. `INT(RND*100+1)` for 1–100.)

<a id="termination"></a>
### Program termination & interruption
- **`STOP`** halts the program (it can be resumed with `GO` from the console); used to mark the end
  of the main line before subroutines.
- **`END [<num-expr>]`** ends the program, **closes all files**, and sets the [`CODE`](../../data-manipulation/system-functions/spec.md#system-info)
  return value (`END 12` sets `CODE`=12; default 0). `END` is optional — a program auto-ends with
  `CODE`=0.
- **`PAUSE`** interrupts execution so the operator can enter commands / inspect variables; `GO`
  resumes and restores the screen (a handy debugging breakpoint).

<a id="examples"></a>
## Examples

```business-rules
! FOR with STEP, early EXIT
00300 FOR DELAY = 1 TO 10
00310   SLEEP(1)
00320   IF EXISTS("file.dat") THEN GOTO 340
00330 NEXT DELAY
00340 !

! DO with test at bottom (runs at least once)
00100 DO
00110   INPUT "Enter password: ": PASSWORD$
00120 LOOP UNTIL PASSWORD$ = "SECRET"

! File loop with EOF branch and EXIT DO
00200 DO
00210   READ #1: DATA$ EOF DONE
00220   IF DATA$ = "STOP" THEN EXIT DO
00230   ! process...
00240 LOOP
00250 DONE: CLOSE #1

! Multi-way dispatch
00130 ON CHOICE GOSUB ELEC, NATGAS, PHONE, CABLE
00200 ON DAY GOTO 500,1000,1500,2000,2500 NONE 100

! Subroutine
00250 GOSUB SALESTAX
10000 SALESTAX: LET TAX = PRICE * 0.06 : RETURN
```

<a id="see-also"></a>
## See also

- [conditionals](../../data-manipulation/conditionals/spec.md) — `IF` (the decision construct)
- [expressions](../../data-manipulation/expressions/spec.md) — loop/branch conditions
- [syntax](../../syntax/spec.md#line-labels) — `<line-ref>` line numbers & labels
- [functions-udf](../functions-udf/spec.md) — `DEF`/`FN` (the function alternative to `GOSUB`)
- (Backing keyword pages folded into this spec and pruned. The 2b
  redirect-collision pages `GoSub`, `On_GoSub` and `Randomize` were folded here and pruned; verbatim
  wikitext remains on the BR wiki.)
