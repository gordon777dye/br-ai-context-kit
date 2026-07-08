---
title: FORM specifications
file: spec.md
source: §File Operations → FORM Statement for File I/O
category: 30-io-file
subcategory: 30-io-file/form-spec
kind: spec
status: 2b           # reference base + br_tree enrichment (repetition/groups, SKIP, variant codes); no conflicts
recovered-fold: BH_4, CC, CU, DR, GU, GZ, NZ (7 redirect-collision pages folded from re-fetched source — CU/CL/GU FORM error 1006, CC centering, NZ/GZ blank-on-zero, BH 4 range+sentinel; verbatim retained on the BR wiki)
related: [statements, file-model, keys-indexes]
keywords: [FORM, USING, PIC, POS, SKIP]
canonical: form-spec   # canonical home for the FORM spec (printing/screen guides link here)
---

# FORM specifications

`FORM` describes the byte-level layout of a record (or a print line) — the field type codes that
`READ`/`WRITE`/`REWRITE` and `PRINT … USING` decode/encode against. **This is the canonical FORM
reference**; the file-I/O statements ([statements](../statements/spec.md)) and the printing guide
link here rather than redefining it.

<a id="syntax"></a>
## Syntax

```bnf
FORM <item> [ ',' <item> ]*
<item> ::= { POS | X | SKIP } <n>            -- positioning / line skip (n = integer or num-var)
         | [ <n> '*' ] <format-spec>          -- a field, optionally repeated n times
         | [ <n> '*' ] '(' <item> [',' <item>]* ')'   -- repeat a parenthesized group
         | "<literal>" | PIC( <pic-spec> )     -- literal text / picture
<format-spec> ::= <form-string-spec> | <form-numeric-spec> | <pic-spec>
<form-striing-spec> ::= <string>` `<form-qty>
<form-qty> ::= <integer> | <numeric-variable>
<form-numeric-spec> ::= <string>` `{<integer>[`.`<integer>] | <numeric-variable>}
<pic-spec> ::= PIC`(`<string>`)` | FMT`(`<string>`)`

```

A `USING` clause names either a `FORM` line number/label or a literal `"FORM …"` string.

<a id="repetition"></a>
### Repetition, groups & positioning
- **`n*spec`** repeats a field: `FORM 4*C 30` = four `C 30` fields. **`n*( … )`** repeats a group:
  `FORM 3*(C 10,C 1,C 4)`. `n` may be a (non-subscripted) variable; if its value `< 1`, **0** is
  used (the spec is skipped). For a **string** repeat with no explicit length, the field length
  defaults to the **first** string's length — so list the longest first (or give a length) to avoid
  string-overflow.
- **`POS n`** positions to byte/column `n` (forward or backward); **`X n`** skips `n` positions;
  **`SKIP n`** skips `n` print lines (`SKIP 0` = carriage-return, no line-feed → overstrike; `POS 0`
  suppresses output and holds the line position). PRINT defaults to `SKIP 1` at statement end.

<a id="format-codes"></a>
## Tables — format codes

| Code | Meaning |
|---|---|
| `N n[.d]` | Numeric (ASCII), `n` total digits, `d` decimals |
| `C n` | Character, `n` bytes |
| `V n` | Variable-length string, max `n` bytes |
| `X n` | Skip `n` byte positions |
| `POS n` | Position to byte `n` |
| `B n` | Binary integer |
| `BH n.d` | Binary with decimals (high-order) |
| `PD n.d` | Packed decimal |
| `ZD n.d` | Zoned decimal |
| `DT 3` / `DT 4` | Date, binary storage (Y2K-compliant) |
| `DL 3` / `DL 4` | Date "long", binary storage |
| `DH 3` / `DH 4` | Date "high", binary storage (indexable as characters) |

**String variants:** `C`/`CC`/`CR`/`CL`/`CU` (char: left/center/right/lower/upper), `V`/`VL`/`VU`
(variable length: normal/lower/upper). **Numeric variants:** `N`/`NZ` (zero-suppressed),
`G`/`GZ` (general char-or-numeric), `GF` (generic floating — left-justifies strings, right-justifies
numbers; for FORM and INPUT/PRINT FIELDS). **Internal:** `B`/`BL`/`BH` (binary), `PD` (packed),
`ZD` (zoned). **Floating-point:** `D`/`S`/`L` — very fast but **hardware-dependent / non-portable**.
A bare `"literal"` prints as text on output and acts like `X` (skip its length) on input.

**Case/centering variants are screen-oriented.** `CU`/`CL`/`GU`/`GL` convert case **as keys are typed**
during `INPUT FIELDS`/`RINPUT FIELDS` (internal files) and never alter data already on screen or in the
record; `PRINT FIELDS` accepts them but treats them as plain `C`/`G`; **using any of them in a `FORM`
statement raises error 1006**. `CC` (centered) strips leading/trailing spaces then pads evenly, with
**odd padding going to the right**; given no length it centers within the string's own length.
**`NZ`/`GZ`** output a zero value as **all blanks** (non-zero prints like `N` — right-justified, blank-
padded, rounded to the stated decimals) and are a shorter, faster, more compact substitute for simple
`PIC(- -.- -)` constructions; on **input** they behave as `N`/`G`. (`DR` is a `PIC` insertion code for
displaying negative values — see [fields-attributes](../../20-io-screen/fields-attributes/spec.md).)

<a id="semantics"></a>
## Semantics

- The FORM's fields are applied in order to the record's bytes; `POS`/`X` move or skip the
  cursor so fields can be placed at exact offsets.
- On **REWRITE**, only the fields the FORM lists are written — bytes not covered are unchanged.
- Date types `DT`/`DL`/`DH` store a day-count in binary and are Y2K-compliant with a proper
  `BASEYEAR`; `DH` can be indexed as character data for sorting (see
  [keys-indexes](../keys-indexes/spec.md)).
- Efficient internal record lengths are `2^N − 1` (see [file-model](../file-model/spec.md#tables)).
- A **`BH 4`** field holds a signed 32-bit integer (≈ −2,147,483,648 … 2,147,483,648). An **empty,
  never-written `BH 4` reads as `538,976,288`** (the value of four ASCII spaces) — test for that
  sentinel, not `0`, when detecting unwritten records.

<a id="examples"></a>
## Examples

```business-rules
! CHECKBOOK.INT record: check#, amount, flag, date written, date cleared, payee
00100 FORM N 5, N 10.2, C 1, N 6, N 6, C 25

! Used by READ/WRITE
00150 READ  #1, USING 160: CHECK, AMOUNT, DW$, DWR, DCL, PAYEE$ EOF 200
00160 WRITE #1, USING 160: CHECK, AMOUNT, DW$, DWR, DCL, PAYEE$
```

<a id="see-also"></a>
## See also

- [statements](../statements/spec.md#io) — `READ`/`WRITE`/`REWRITE … USING <form>`
- [file-model](../file-model/spec.md) — record/field concepts, RECL
- [keys-indexes](../keys-indexes/spec.md) — date field types as keys
- Printing-side FORM/PIC usage → [40-io-printing/statements](../../40-io-printing/statements/spec.md)
- Backing keyword page (deep FORM reference retained): [FORM](FORM.md)

*(7 redirect-collision pages re-fetched in 2b — `BH_4`, `CC`, `CU`, `DR`, `GU`, `GZ`, `NZ` — were
folded into this spec and pruned; verbatim wikitext remains on the BR wiki.)*
