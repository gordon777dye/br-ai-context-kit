---
title: Second corpus (E:\tmp) — real BR LOAD validation
file: second-corpus-load-validation.md
category: app
kind: report
status: complete
date: 2026-08-18
description: Every failing line brls's own parser finds in E:\tmp, run through the real BR executable to settle which are genuine brls gaps — 10 confirmed and fixed, 1 reclassified as already-correct, and the whole remaining residual traced to either correct rejections or corpus noise.
---

# Second corpus (E:\tmp) — real BR LOAD validation

## Why this and not brls's own parse rate

`E:\tmp` is "the second corpus" in `context/lsp/brls/LSP_PLAN.md` (§ two-corpora) — a flat harvest of
15,646 `.brs` files "from many systems," used since phase 6 for brls's own self-consistency checks
(parse rate, clause-completion survey). What it had never been used for is a real-BR-oracle
validation: taking every line brls's own parser rejects and running it past the real BR executable,
treating BR's own `LOAD` result as ground truth rather than brls's opinion of itself — the way
`context/app/br-load-save-validation.md` did for the whole QSMRP application tree. This report is
that validation, adapted to this corpus's shape (see "Method," below, for what changed and why) — the
working record is `context/lsp/brls/CORPUS-2.md`; this is the settled result.

## Corpus split

`E:\tmp` originally held 15,646 files, 3,097 of them (19.8%) classified `Lexi` by
`internal/dialect.IsLexi` — the same content-based classifier (`#DEFINE#`/`#SELECT#`/`#CASE#`
markers, or no numbered line at all) `LSP_PLAN.md`'s own two-corpora figures already relied on.
Those 3,097 were physically moved to `E:\lexi_files`, so `E:\tmp` from this report onward means the
**12,549-file real-BR-only set** — enforced by directory layout rather than by every tool re-deriving
the exclusion. Counts reconcile exactly: 12,549 + 3,097 = 15,646, and 12,549 matches `LSP_PLAN.md`'s
own "BR files" figure for this corpus.

## Method

Unlike the QSMRP validation, this one does not run every file through `LOAD`/`SAVE`. Two things about
this corpus make that impractical and unnecessary:

- **Scale.** 15,646 files is 3.7× QSMRP's line count; one BR process per file (mandatory — an
  `UNATTENDED` hard-abort under real BR terminates the whole process, hiding the result of anything
  queued after it) is not practical the way it was for QSMRP's 1,108.
- **It is not one coherent application.** A flat harvest "from many systems" may reference
  `CHAIN`/`LIBRARY` paths that don't resolve here, or contain files that were never meant to be BR
  programs at all (see "Corpus noise," below) — failures from either are corpus artifacts, not
  brls-vs-BR disagreements.

Instead: **brls's own parser is the triage.** `TestCorpusParses`/`TestHarvest`
(`internal/parse/corpus_test.go`, `fail_test.go`) walk the corpus and collect every **distinct
line** brls's parser calls a real (non-advisory) failure, deduplicated by text. Only those lines —
not whole files — went to real BR, one process each, via the same headless harness the QSMRP
validation used (`context/dev/BR_launch.md`; `LOAD "<file>" SOURCE`; PASS/FAIL read from
`context/app/startlog.txt`'s two distinguishing phrases). A line real BR accepts and brls rejects is
a confirmed brls gap; a line both reject is confirmed agreement, root-caused to an exact cause before
being counted, same as the QSMRP report's own standard.

## Results

| | Before this pass | After |
|---|---:|---:|
| Real (non-advisory) parse failures | 196 | 119 |
| Distinct failing-line shapes | 126 | 76 |
| Lines parsing clean | 99.994% | **99.996%** |

Of the 126 distinct shapes measured at the start, 128 literal candidate lines were run through real
BR (some shapes had multiple near-identical instances worth confirming individually): **53 passed**
(real BR accepts what brls rejected — a candidate gap) and **75 failed** (both systems agree,
confirmed by BR's own error code, not just "rejected"). The 53 PASS lines reduced to **9 distinct
differences**, all resolved:

| # | Difference | Outcome |
|---|---|---|
| 1 | `PRINT #ch,USING <ref>: <list> PAGEOFLOW <label>` | **Fixed** |
| 2 | Bare `MAT name` with no `=`/`(` | **Fixed** |
| 3 | `RESTORE` clause combinations (two unrelated bugs) | **Fixed** |
| 4 | `USE` with trailing content after its name list | **Fixed** |
| 5 | `LIBRARY` with a leading empty item | **Fixed** |
| 6 | `FORM`/`PIC` picture shapes (two unrelated bugs, one red herring) | **Fixed** |
| 7 | `PRINT …USING "literal FORM spec string"` | **Not a bug** — misclassified; brls already handles it correctly (`bad-using-format`) |
| 8 | `MAT` array reference as a function-call argument | **Fixed** |
| 9 | `MAT` items mixed into an ordinary `READ` I/O list | **Fixed for free**, by #8's fix |

Root-causing the remaining 75 FAIL lines individually turned up a **tenth** difference, found this
session and not part of the original 9 — a `PRINT`'s `DAT`-abbreviation guard not surviving when
that `PRINT` sits inside an `IF`'s `THEN`/`ELSE` consequent. **Fixed.**

A fresh re-run of the whole triage after all ten fixes landed found **no further brls gaps**: every
one of the 76 remaining distinct failing-line shapes is either an already-confirmed-correct rejection
or corpus noise (detail below). Nothing currently indicates a further round of fixes is needed
against this corpus.

## The ten fixes

Each was confirmed against real BR before being fixed — not inferred from reading BR's C source alone,
which this project has repeatedly found produces confident, wrong theories. Full detail, including
every test command and intermediate false lead, is in `CORPUS-2.md`; this is the settled cause and
fix for each.

### 1. `PRINT`'s `PAGEOFLOW` clause

Not "unimplemented," as it first looked: `internal/parse/walk.go`'s `falsePositiveClauseKeyword`
discarded *any* `ClassClause`-abbreviating word found in `PRINT`'s plain print-list — a
generalisation, from the one case it was ever confirmed for (`FIELDS`), that was never tested against
a second word. Every affected corpus line ends `…,SEQ pageoflow <label>` — `SEQ` abbreviates the
unrelated clause `SEQUENTIAL`, gets wrongly discarded, and the discard latches a flag that then
blocks recognising the genuine `PAGEOFLOW` clause right after it. Narrowed the discard to `FIELDS`
specifically, the only word ever confirmed against real BR. Fixed 28 audited lines and 14 more real
corpus lines beyond them.

### 2. Bare `MAT name`

`internal/parse/special.go`'s `parseMat` rejected a fully bare `MAT name` (no `(...)` at all)
outright, citing its own comment that it is "a legal operand of READ, PRINT and INPUT, but not a
statement on its own" — a claim never checked against real BR, and wrong. The real mechanism was
already implemented one branch above, for a bare subarray (`MAT A(1:5)` alone): `MAT_PRI` takes the
array reference, finds no `=`, and falls straight to `MAT_END`, discarding the descriptor it
computed — pointless but not wrong. A fully bare `MAT name` behaves identically; folded into the same
accept-and-return path.

### 3. `RESTORE` clause combinations — two unrelated bugs

1. **`=>`/`=<` vs `>=`/`<=`.** Accepted alternate spellings of the same BR relational operators
   everywhere (`internal/lex`'s `twoCharOps`; `operators.json` lists both spellings for
   `GR_OR_EQ`/`LESS_OR_EQ`), but the seven compound keywords ending in one (`KEY=`, `KEY>=`, `LINK=`,
   `POS=`, `REC=`, `SEARCH=`, `SEARCH>=`) were matched by literal token text, so `SEARCH=>` failed to
   match the keyword at all. New helper `sameRelationalOperator` resolves both spellings to their
   opcode identity via `langdata.FindOperator` before comparing.
2. **`RESTORE`'s `LAST` carried a spurious "alpha expression" descriptor** in the dumped syntax
   table — present for `LAST` in `RESTORE` alone, confirmed absent from its own siblings
   (`FIRST`/`END`/`NEXT`/`SAME`) and from `LAST` as used by `DELETE`/`READ`/`REWRITE`. It silently
   swallowed a genuine following `RELEASE` as bogus data, and separately, silently *accepted*
   `RESTORE #f,LAST X$:`, which real BR rejects outright (error 1000) — a false negative found while
   tracing the first bug. `matchUnit` now skips the descriptor for this one keyword in this one
   statement.

### 4. `USE` swallows everything after its name list

Broader than "a trailing format name": `USE`'s own doc comment already quoted the real explanation
(CHAIN.md — "USE is treated as a comment … maintained only for compatibility with IBM Business
BASIC") and it is literal. Not just arbitrary trailing garbage, but even a `:`-led second statement
that is invalid BR entirely on its own (`USE A$: LET =5`, no target for `=`) LOADs clean — proof BR
is not tokenizing anything past `USE`'s name list at all, not merely skipping one bad clause.
`parseUse` now consumes to true end of line instead of stopping at the next `:`.

### 5. `LIBRARY`'s leading empty item

The same "separates nothing from nothing" shape `DEF LIBRARY`'s own stray-comma rule already covers,
at a different site: plain `LIBRARY` (imports functions) rather than `DEF LIBRARY` (exports one), and
with no introducing keyword to skip past the way `DEF LIBRARY`'s does. `matchUnit` now tolerates a
leading comma at this one optional, keyword-less position — and, once a second, independently-reached
site turned up the identical shape (see #6.2), generalised to any optional unit rather than kept
`LIBRARY`-specific.

### 6. `FORM`/`PIC` picture shapes — two unrelated bugs, one red herring

1. **An unclosed `PIC(`/`DATE(` picture is not an error.** A FORM line whose picture never finds its
   closing `)` LOADs clean, running to true end of line the same way a closed one runs to its `)`.
   `formatScanner.readTo` no longer reports it.
2. **The real corpus failure was a stray double-comma, not the `RU`/`RUE` width-code suffixes it
   first looked like.** `RINPUT #98,,FIELDS "…,C 1,RU": OK$` — bisecting showed `RU`/`RUE` parse clean
   with a single comma; the double comma was the actual cause, reaching #5's fix by a different route:
   `RINPUT`'s channel reference consumes one trailing comma unconditionally as part of its own unit,
   stranding the second comma exactly where the optional `WAIT=` clause goes.

### 7. `PRINT …USING "literal FORM spec string"` — not a bug

`USING "FORM POS 5, C 20)"` has a stray `)` with no `(` to close — invalid, and brls already knows
it: the diagnostic already carries the dedicated rule `bad-using-format`
(`internal/diag/rules.go`), built for exactly this shape — "a `USING` operand is compiled **at run
time** … so it compiles cleanly, ships, and fails the first time that report runs," the same reasoning
already applied to `evaluates-to-zero`. Real BR's `LOAD` succeeding was never new information; it is
the rule's own premise. No code change.

### 8. `MAT` array reference as a function-call argument

`parseName` built a bare `MatExpr` for `MAT name` with nowhere to put a following dimension list, so
`FNX(MAT A(5))` reached the generic "only a name can be called or subscripted" error — the one a
genuinely invalid `(expr)(args)` gets. The colon-range reading (`MAT A(1:5)`) already worked, via a
separate path; only the dimension-list reading was missing. `parsePostfix` now recognises a `MatExpr`
specifically at that error site and reads the dimension list into a new `Dims` field, the same list a
`MAT` statement's own tree reads. A trailing `=(99)` initializer needed no extra code — once the dims
parse, `=` is just the next token to whatever parses the caller's own expression.

### 9. `MAT` items mixed into a `READ` I/O list — fixed for free

The full original candidate parses clean with no further code change: `MAT B$(2)` in a `READ` list is
the identical construct #8 fixed, reached through the same general expression parser regardless of
whether it sits in a function-call argument or an I/O list.

### 10. `THEN`/`ELSE` not opening a statement position (found root-causing the FAIL side)

Found while root-causing one of the confirmed-agreement FAIL lines, not part of the original 9 — a
`PRINT`'s `DAT`-abbreviation guard (a historical fix keeping a `DATA`-abbreviated word right after a
channel-I/O statement's own clause-closing colon from reopening a fresh statement head) held for an
ordinary top-level `PRINT`, but not when the same `PRINT` was an `IF`'s `THEN`-consequent. Root cause:
the lexer's `atStatementHead` tracking had exactly two triggers — a line number and a
statement-separating colon — with no concept of `THEN` or `ELSE` opening a new statement position at
all. `internal/lex/lex.go`'s `scanWord` now also sets it right after a `THEN`/`ELSE` word. Confirmed
as the only reasonable fix site: `AtStatementHead` has exactly two real consumers anywhere in the
codebase, both already in `lex.go`.

## Not brls gaps

### The reversed "Lexi group" episode

Mid-audit, 28 of the 75 confirmed-agreement lines — every `IF … THEN CASE` / `… ELSE CASE`
occurrence (a bare `CASE`/`CASE ELSE` used as a `THEN`/`ELSE` target, error 1030, "invalid character
expression") — were split out into a separate "Lexi group," on a hypothesis about their origin. That
hypothesis was never substantiated (the harvested text carries none of Lexi's actual markers) and was
reversed after fresh, standalone re-confirmation against real BR. They are ordinary core-BR-grammar
agreement, folded back into the FAIL count above.

This shape is also reconciled against `LSP_PLAN.md` finding 32 (`non-functional-form`): consistent,
not contradictory. Finding 32 covers `SELECT`/`CASE` **standing alone as a complete statement** —
accepted, dead code, does nothing at runtime. This shape is `CASE` used **as what `THEN`/`ELSE` hands
control to** — a different position, rejected outright rather than silently accepted. brls's own
error message already draws exactly this line.

### Corpus noise

A handful of harvested "failures" are not BR program statements at all — `.prc`/shell-command-mode
text misfiled with a `.brs` extension somewhere in this flat, multi-system harvest:

| Text | Traced to |
|---|---|
| `\bop16.br` | `E:\tmp\scratchpaper.brs`, line 112 — sitting between two duplicated blocks of otherwise-genuine, correctly-numbered `OPEN` statements; editor/copy-paste debris in a personal scratch file |
| `CONFIG STYLE CLEAR`, `free srchproc` | `E:\tmp\pgmsize.brs` — whose own first line is a comment reading "this procfile is used to search every br program for the search string specified," confirming directly that it is a `.prc`-style procedure file, not application code |
| `subproc srchproc`, `system -c -m start temp.[wsid]` | Not located by a direct grep in this pass |

### The `!:` mid-line shape

A `!:` sequence followed by more text on the *same* physical line (`let PAST_DUE$="N" !:todo: remove
this line…`, `Edit1: for X=6 to 28 !:::: Edit fields for screen 1`, and others) is not simply "start a
comment, `:` included," the way a bare `!` is. Checked directly rather than assumed: both shapes fail
real BR's `LOAD` with error 1000, "unidentified source remaining" — `!:` is BR's own genuine statement
continuation marker, and neither brls nor BR accepts one followed by ordinary trailing text with no
continuation partner. Confirmed brls's rejection is correct; not chased further into what `!:`
followed by *nothing* (a genuine continuation) requires, since that shape doesn't appear as a
standalone-line failure here.

### Genuinely malformed source

A few lines are plain errors in the original programs, correctly rejected by both systems: `LET RUN
KEY>=LOC` (`LET` takes no `KEY>=` clause), `OPEN #3: "…",INTERNAL,OUTPUTBEGIN` (`OUTPUTBEGIN` is not a
documented BR keyword anywhere in `br_tree`; almost certainly a typo for `OUTPUT` with something else
intended after it), and five `*`-prefixed pseudo-comment lines (BR's comment marker is `!`, not `*`).

## Scope not covered

- **Whole-file `LOAD`/`SAVE`**, the way the QSMRP validation ran it. This report worked from
  brls-flagged *lines*, synthesized standalone, not whole files — sufficient to settle every
  parser-level disagreement found, but it does not check `SAVE`-time-only failures (unresolved
  references, missing `LIBRARY` links) the way the QSMRP report's Findings 4 and 5 did. Extending this
  audit to whole-file `LOAD`/`SAVE` would need the file-level `LIBRARY`/`CHAIN`-dependency check this
  report's method section describes but never needed.
- **Sema-tier rules** (`reserved-name`, `duplicate-target`, `unclosed-*`, and the cross-file linkage
  rules). `TestCorpusAnalyses`'s whole-workspace pass crashed with an out-of-memory error on this
  corpus's 12,549 files (confirmed directly, not just cited from `LSP_PLAN.md`, which already flagged
  the same limit). A per-file `sema.Analyze` walk with no shared workspace would avoid the crash and
  catch the single-file-scoped rules, at the cost of the cross-file ones — not attempted here.
- Two corpus-noise lines (`subproc srchproc`, `system -c -m start temp.[wsid]`) were not traced to
  their source files.
