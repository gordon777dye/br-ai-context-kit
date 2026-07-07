---
title: Lexical structure & program syntax
file: spec.md
source: §Lexical Structure, §Language Overview
category: 10-language
subcategory: 10-language/syntax
kind: spec
status: 2b           # reference base + br_tree enrichment (line continuation); no conflicts
recovered-fold: Keyword_Abbreviation (rules folded; full-table page RETAINED), DIAGRAM_CONVENTIONS (folded+pruned). 2 redirect-collision pages re-fetched; verbatim retained on the BR wiki
related: [conditionals, other-flow, functions-udf]
---

# Lexical structure & program syntax

How BR source is written: line numbers, comments, identifiers, line labels, and multiple
statements per line. The control statements that *use* line refs are in
[other-flow](../flow-control/other-flow/spec.md) and
[conditionals](../data-manipulation/conditionals/spec.md).

<a id="syntax"></a>
## Syntax

```bnf
<line-number> ::= <integer>                      -- 1 to 99999, required on every line
<comment>     ::= '!'  [ <text-to-end-of-statement> ]
               |  REM  [ <text-to-end-of-line> ]
<identifier>  ::= { <letter> | '_' } { <letter> | <digit> | '_' }*
<line-label>  ::= ' ' <identifier> ':'           -- immediately after the line number
<line-ref>    ::= <line-number> | <line-label>
```

Statement separators: `:` or `!:` join multiple statements on one physical line.

<a id="semantics"></a>
## Semantics

<a id="line-numbers"></a>
### Line numbers
- **Required on every program line**; range **1–99999**; conventionally incremented by 10
  (`100, 110, 120 …`) to leave room for insertions.

### Language-wide lexical rules
- **Case-insensitive** keywords and identifiers (`PRINT` = `pr` = `Print`; `NAME$` = `name$`).
- **Abbreviated keywords** — most statements/commands have short forms (`PRINT` → `PR`); see
  [§Keyword abbreviations](#abbreviations).
- **Implicit typing** — variables need no explicit declaration (created on first use).

<a id="comments"></a>
### Comments — `!` vs `REM`
Both are non-executable and preserve case. They differ in **scope**:
- **`!`** ends at the end of the current **statement**. A later statement on the same line
  (after `:` / `!:`) still runs:
  ```business-rules
  00100 LET X = 5 ! set initial value :LET Y = X * 2   ! Y is still assigned
  ```
- **`REM`** ends at the end of the **line** — everything after it, including `:`-joined
  statements, is comment text:
  ```business-rules
  00200 REM whole line is a comment : LET Y = 5        ! Y is NOT assigned
  ```
- Use `!` for inline comments (by far the most common), `REM` for stand-alone comment lines.

<a id="identifiers"></a>
### Identifiers
1–30 characters; must start with a letter or `_`; may contain letters, digits, `_`;
case-insensitive; cannot be a system function name. (String variables add a trailing `$`.)

<a id="line-labels"></a>
### Line labels
A name immediately after the line number, ending in `:`. Usable anywhere a line number is
expected (a `<line-ref>`). Must be unique in the program; may reuse keyword/variable spellings.
```business-rules
00050 FORMULA: LET MPG = MI/GAL   ! label definition
00100 GOTO FORMULA                ! jump to the labeled line
```

<a id="multiple-statements"></a>
### Multiple statements per line
Separate statements on one physical line with `:` (or `!:`). Useful for compact branches and
loop bodies — but see the comment-scope rules above when mixing with `!`/`REM`.

<a id="line-continuation"></a>
### Line continuation — `!:`
`:` joins statements on one physical line; **`!:`** joins them but tells BR to **LIST** each part on
its own physical line while they keep the same line number — each such part is a **sub-line**. This
is the standard way to write one logical line across several display lines.
```business-rules
00010 LET A = 1 !:
      LET B = 2 !:
      LET C = 3          ! all three are line 00010, listed separately
```
A **paragraph (line) label** may **not** follow a `!:` continuation, but it may follow a sub-line that
is commented out with a bare `!`:
```business-rules
00010 TOP: ! !:
      PRINT NEWPAGE
```

<a id="abbreviations"></a>
### Keyword abbreviations
Primary keywords (statement/command **names**) and secondary keywords (other words in a statement) may
be abbreviated to a documented minimum (`DELETE`→`DEL`; any longer prefix also works — `DELE`, `DELET`).
**Primary** abbreviations are unique; **secondary** ones are not — BR resolves them by context/position.
Common minimums: `PRINT`→`PR`, `PRINT FIELDS`→`PR F`, `PRINT USING`→`PR U`, `INPUT`→`IN`,
`INPUT FIELDS`→`IN F`, `LET`→`LE`, `LINPUT`→`LI`, `GOSUB`→`GOS`, `GOTO`→`GOT`, `EXECUTE`→`EXE`,
`RINPUT`→`RI`, `MAT`→`M`, `NEXT`→`N`; the five `OPEN …` forms and both `READ` forms all share
`OPE`/`REA`. Commands: `CHDIR`→`CH`/`CD`, `CONFIG`→`CON`, `COPY`→`COP`, `DIR`→`DI`, `LIST`→`LIS`,
`RENAME`→`REN`, `RENUM`→`RENU`, `STATUS`→`ST`, `TYPE`→`TY`. **Caution:** BR auto-expands abbreviations
**only inside program statements** — never in commands, procedure files, `BRConfig.sys`, or `EXECUTE`
literal strings, and never inside literals — so **spell keywords out in full** in those places. Full
appendix (every command/statement minimum): [Keyword_Abbreviation](Keyword_Abbreviation.md).

<a id="diagram-conventions"></a>
### Reading the manual's syntax diagrams
The original BR manual/wiki uses railroad diagrams (this corpus uses BNF instead). In those diagrams:
**UPPERCASE** = an exact keyword (type it, or an allowed abbreviation); **lowercase** = a parameter you
replace (defined in the following Parameters section); shown punctuation (`,` `:` `/`) must be typed;
items on the **main line** are required (if you can reach the end without passing a parameter, it's
optional); a **returning dotted line** means the item may repeat (separated by the shown `,`/`;`); `<n>`
in angle brackets is a default keyed to the Defaults list; **insertable** sub-diagrams (e.g.
`helpstring`, `share-spec`) have no start/end circles; the **end circle** marks the statement's end.

<a id="program-structure"></a>
## Program structure

- **Size limits**: up to **32,000 lines** (line numbers 1–99999); dictionary up to **2 MB**.
- **Conventional layout**: header comment block → initialize (`DIM`, `ON ERROR GOTO`) → main
  (dispatch via `GOSUB`s) → `STOP` → subroutines at high line numbers → error handler → `END`.
- **Best practices**: meaningful line labels over bare numbers; comment section dividers; keep
  related code together; one consistent error handler (`ON ERROR`); place subroutines at the end.
- **Menu-driven** programs loop: display options → read choice → dispatch (`ON … GOSUB` or `IF`s)
  → repeat until quit. (Branching constructs: [other-flow](../flow-control/other-flow/spec.md).)

```business-rules
00200 DIM CUST$*30 : ON ERROR GOTO 9000   ! initialize
00310 GOSUB 1000 : GOSUB 2000             ! main: process
00999 STOP
01000 ! subroutine … : RETURN
09000 PRINT "Error";ERR;"at line";LINE : STOP   ! handler
99999 END
```

<a id="examples"></a>
## Examples

```business-rules
00001 ! ========================================
00002 ! Program: MILEAGE   — header comment block
00003 ! ========================================
00020 INPUT MI CONV CONVRSN      ! reference a label
00050 FORMULA: LET MPG = MI/GAL  ! labeled line
00080 CONVRSN: PRINT "Enter numbers, not letters."
00090 RETRY
00100 GOTO FORMULA               ! jump by label
```

<a id="see-also"></a>
## See also

- [other-flow](../flow-control/other-flow/spec.md) — `GOTO`/`GOSUB`/`ON GOTO` that consume `<line-ref>`
- [conditionals](../data-manipulation/conditionals/spec.md) — `IF` line/label targets
- [functions-udf](../flow-control/functions-udf/spec.md) — `DEF`/`FN` definitions
- Backing keyword page retained (deep reference — full command/statement abbreviation appendix):
  [Keyword_Abbreviation](Keyword_Abbreviation.md)
- (Other backing pages folded into this spec and pruned. The 2b
  redirect-collision page `Diagram_Conventions` was folded here and pruned, and `Keyword_Abbreviation`
  retained; verbatim wikitext remains on the BR wiki.)
