# Business Rules — application development guide

This is the capstone for this context kit. It stitches the language reference, the built-in function
catalog, and the schema-extraction tooling into one starting point for writing correct **Business Rules!
(BR)** code — whether you're a developer onboarding to a BR codebase or an LLM acquiring
context. Each section says **where the authoritative detail lives** so this stays a map, not
a duplicate. It is application-agnostic: point the tooling at whatever BR app you're working
on.

Please document any errors in dev\ERRORS.md. This includes any inaccuracies *or ambiguities* found (within the context folder) while using this kit. Let the user know when you post something to ERRORS.md so users can forward the report to ADS. 

---

## Models Start here — by task type

**Don't load the whole kit**; for one program it's mostly ballast. **[`topics.json`](topics.json) is the
entry point for reading or writing BR code:** it routes a keyword to its anchored
[`statement-semantics.md`](statement-semantics.md) section (with a line range, so you load ~5–10k,
not the whole file) and carries the `lexicon` — the classified inventory of which spellings are
reserved. The path is **`topics.json` → `statement-semantics.md` → [`../br_tree/`](../br_tree/)** (the
authoritative backstop), pulling in the catalogs and your app's data-model as needed.

For access to the Business Rules compiler:
1. Read BR_launch.md to extract the environment variable definitions
2. Extract the PowerShell snippet that sets $env:BR_EXE, $env:BR_AI_UTIL, etc.
3. Execute those environment variable assignments before attempting any BR invocation
4. Use those variables in subsequent commands (e.g. $VAR_NAME in Bash)
5. See section 6 below for advice on how to run BR and identify program errors.

The language axis has **two parallel keyword indexes** — use whichever fits the token:
- **[`topics.json`](topics.json)** for statements/clauses — fast, line-ranged semantics + the `lexicon`.
  This is the default for reading or writing statement code.
- **[`brtree-index.json`](brtree-index.json)** for *any* BR keyword — config directives, screen
  controls, printing, functions, commands — or to jump straight to the authoritative spec. Its
  `keyword_index` maps a token to its br_tree spec path(s) + anchors: **`brtree-index.json` →
  `../br_tree/<spec>/spec.md#<anchor>`**. It complements `topics.json`; it does not replace it.

| Task | Start with | Then pull in |
|---|---|---|
| **Interpret / debug** — read existing BR | `topics.json` → `statement-semantics.md` | [`system-functions-catalog.md`](system-functions-catalog.md), [`error-reference.md`](error-reference.md), the app data-model (§4) |
| **Coding** — write correct, idiomatic BR | `topics.json` → `statement-semantics.md` | the two catalogs + data-model, closed by a fast **`brls -check`** pass (§6) then the authoritative **`LOAD … source`** syntax check in BR (write→check→fix; §6) |
| **App design** — architecture, data model, modules | [`../app/architecture.md`](../app/architecture.md) + generated **data-model** (§4) + [`../app/conventions.md`](../app/conventions.md) | br_tree concept leaves — [`file-model`](../br_tree/30-io-file/file-model/spec.md), [`library-facility`](../br_tree/50-libraries/library-facility/spec.md), [`screenio`](../br_tree/50-libraries/screenio/spec.md) |
| **Testing** — validate behaviour | headless BR (§6) | syntax-check via `LOAD "<prog>.brs" source`; run programs and procs headlessly through the BR invocation |

*Why `topics.json` and not a flat keyword list: BR's lexicon is **positional** — only system
functions are reserved against variable names, so telling a keyword from a variable needs the
`lexicon` block, not a keyword table. And the decision itself is made by **arity**, not by a
symbol table: see
[name resolution](../br_tree/10-language/syntax/spec.md#name-resolution), which is also why
declaring a name never shadows an intrinsic.*

### The app layer (after onboarding)

The above is the **language axis**. Once a codebase is onboarded (see
[`../app/ONBOARDING.md`](../app/ONBOARDING.md)), a third layer under [`../app/`](../app/) carries
*this application's* specifics — reached **directly**, not through `topics.json` (which stays a
language keyword router; app conventions/architecture aren't keyword-addressable):

- **Always-load** when reading or writing this app's code:
  - [`../app/conventions.md`](../app/conventions.md) — house coding style (naming, error handling, FileIO-vs-raw-OPEN idiom)
  - [`BR_launch.md`](BR_launch.md) — BR launch environment + build / run / test / deploy commands
- **On-demand** (pull the one you need):
  - [`../app/data-model.md`](../app/data-model.md) — file schemas & key composition; look up **by file** (generated — §4)
  - [`../app/architecture.md`](../app/architecture.md) — module map, entry points, core data flows (orientation)
  - [`../app/exemplars/`](../app/exemplars/) — blessed real programs; pick **by archetype** and imitate

The `app/` files above are generated/written during onboarding and are app-private (git-ignored) — a
fresh kit skeleton won't have them yet. `BR_launch.md` is the exception: it lives in `dev/` (this
file's directory), is part of the tracked kit, and is application-agnostic.

---

## 1. How a BR codebase is shaped

BR is a line-numbered Business BASIC. Programs are `.brs` source, compiled to tokenized `.br`, and run inside the BR runtime. Systems are commonly multi-user.

BR apps converge on a few conventions worth recognizing:

- **Module directories** group programs by function (admin/menus, printing/output, the data
  modules, etc.). Learn the target app's layout — there's no fixed standard, but related
  programs and their data files usually sit together.
- **Program-name suffixes** often signal a program's role: `…fm` = file-maintenance screen,
  `…f` = file-maintenance utility, `…p` = print/report, `…e` = entry/input, `cvt/` =
  upgrade-conversion utilities. (Conventions vary per app — verify against the codebase.)
- **`filelay/` (or similar)** holds the **data dictionary**: text schemas describing each
  data file's fields, FORM types, and key composition. This is the single best source for
  the data model — see §4.

---

## 2. The reference map — what to open for what

| You need… | Go to |
|---|---|
| A statement's behavior / semantics / side effects / error clauses | [`topics.json`](topics.json) routes to the right [`statement-semantics.md`](statement-semantics.md) section (anchor + line range); each topic links to br_tree for depth |
| Full syntax, edge cases, version notes, related concepts | the [`../br_tree/`](../br_tree/) language reference tree (authoritative; the semantics file's See-also links land here) |
| Which br_tree spec documents keyword `X` — across *all* topics (config, screen, printing, functions, commands), not just statements | [`brtree-index.json`](brtree-index.json) `keyword_index` maps a BR keyword to its spec path(s); each spec record carries its anchors + a one-line summary. Complements `topics.json` (which is statement-centric) |
| Is `X` a keyword or a variable? Which words are reserved | [`topics.json`](topics.json) `lexicon` — the classified inventory; only system functions are reserved, every other keyword is positional (a variable may reuse its spelling) |
| Built-in (system) functions (`STR$`, `CNVRT$`, `SRCH`, …) | [`system-functions-catalog.md`](system-functions-catalog.md) — the full `table6k∪table7k` roster with signatures |
| App library / UDF signatures | index the **target app's own** `DEF LIBRARY`/`DEF FN` source — not the corpus (its UDFs are confidential) |
| Standard libraries (FileIO, ScreenIO, JSON) | [`library-catalog.md`](library-catalog.md) (signatures) → [`../br_tree/50-libraries/`](../br_tree/50-libraries/) for full docs |
| Error code meaning (for diagnostics) | [`error-reference.md`](error-reference.md) (70 curated, with fixes) → [`../br_tree/90-reference/error-codes/`](../br_tree/90-reference/error-codes/) (all 773) |
| **This app's** data model (files/fields/keys) | [`../app/data-model.md`](../app/data-model.md) — generated by §4 (`tools/extract-schema.exe`); look up **by file** |
| **This app's** coding conventions (house style) | [`../app/conventions.md`](../app/conventions.md) — *always-load* when writing app code |
| **This app's** build / run / test commands + BR launch env | [`BR_launch.md`](BR_launch.md) — *always-load* |
| **This app's** architecture (modules, entry points, data flows) | [`../app/architecture.md`](../app/architecture.md) — orientation, on-demand |
| **This app's** worked examples to imitate | [`../app/exemplars/`](../app/exemplars/) — blessed real programs; pick **by archetype** |

---

## 3. Language essentials you must get right

Moved to [`essentials.md`](essentials.md) — the language rules that bite newcomers (and LLMs
trained on other BASICs), **plus a growing set of runtime gotchas confirmed empirically** while
actually RUNning BR programs - built-ins that didn't behave as expected, and more. Read it before writing or debugging any BR code; per-statement detail
stays in [`statement-semantics.md`](statement-semantics.md) indexed by [`topics.json`](topics.json),
full detail in the br_tree reference.

---

## 4. Working with data files

### Get the schema first

A BR data file is a fixed-length keyed record store; you need its field layout and key
composition before reading it. The app's `filelay/` (or equivalent) directory is the data
dictionary. Turn it into a structured model with the bundled tool:

```
tools/extract-schema.exe <path-to-app/filelay>
tools/gen_datamodel_index.exe
```

This produces `data-model.md` for *that* app: per file, the data path,
record length, each key index **with its composing fields** (the order you concatenate to
build a `KEY=` lookup), and every field's FORM type/position. No app's data model is bundled
here — generate the one you need. (No `filelay/`? Convert your data dictionary to the filelay format —
see [`../app/ONBOARDING.md`](../app/ONBOARDING.md) Appendix A — then run the tool.)

`data-model.md` is large. `gen_datamodel_index.exe` builds `data-model-index.json` beside it — a
per-file map to 1-based inclusive line ranges (the same sharding `topics.json` gives
`statement-semantics.md`). **Don't load the whole data model:** look the file up in the index and
read only its line slice. Re-run the indexer whenever the model is regenerated.

### Read records (raw BR keyed I/O)

Open a keyed file, build the composite key from the schema, read by key or scan to EOF. A
record's layout comes from a **named `FORM`**.

Worked examples — keyed read and sequential scan — are in the `OPEN`/`READ` sections of
[`statement-semantics.md`](statement-semantics.md#read). Adapt the file name, key layout, and `FORM`
to your data model. Key construction is positional concatenation in schema order (e.g. a 3-field key
= field1 + field2 + field3, each padded to its width).

### Or use a file-access library

Many BR apps wrap raw I/O in a library layer (the standard **FileIO** library, or an app's
own access functions). Prefer the codebase's established layer for new code so it matches
surrounding programs — find the candidates in the **app's own library source** and the FileIO
reference under [`../br_tree/50-libraries/fileio/`](../br_tree/50-libraries/fileio/).

---

## 5. Screens, printing, web library

- **Screens**: ScreenIO drives interactive forms; persisted definitions live in the binary
  `screenio.dat`/`screenfld.dat`, edited within BR/ScreenIO itself — never hand-edit those files. A
  screen's event `DEF FN…` code is compiled **into** the screen, so after editing an event function you
  **recompile the screen** (not the event source alone).
  Reference: [`../br_tree/50-libraries/screenio/`](../br_tree/50-libraries/screenio/).
- **Printing**: `PRINT #n, USING form:` to an opened print file; PCL/PDF detail in
  [`../br_tree/40-io-printing/`](../br_tree/40-io-printing/).
- **web integration**: BR has JSON and web-integration facilities —
  [`../br_tree/60-integration/`](../br_tree/60-integration/). 

---

## 6. Running BR (headless, via procedures)

### 6.1 Syntax pre-check (`brls.exe`, standalone)

[`$BRLS_EXE`](tools/brls.exe) (defined in [`BR_launch.md`](BR_launch.md)) is a standalone BR
**syntax checker**. It does not invoke BR, so it avoids the operational hazards in §6.3 (no splash
delay, no WSID slot, no keyboard-focus theft), needs no config file, and requires no BR license.

Currently brls.exe is early release. So, whicle it has been thoroughly lab tested, 
there is nothing like real world testing. So please report (in context\ERRORS.md) any 
failures that it doesn't detect along with any false positives.

**Scope boundary (read once):**
1. `-check` runs syntax only. It does **not** check undefined names, argument counts, unresolved links,
  or reserved-name misuse.
2. `-check -sema` this performs a semantic (linkage) validation.
3. `-sema` on bare CLI is still single-file analysis. Without workspace indexing, cross-file `LIBRARY`
  links cannot resolve.
4. Therefore, clean `-check -sema` is stronger than clean `-check`, but the authoritative gate is still
  real BR: `LOAD <prog>.brs source`, then `SAVE` or `REPLACE` (§7, step 6).

**Default AI loop:**
1. Edit file using `-next` as needed.
2. Run `$BRLS_EXE -check -sema`.
3. Fix findings.
4. Repeat until exit code `0`.
5. Close with real BR `LOAD ... source` plus `SAVE` or `REPLACE`.

All examples assume the kit-root working directory that [`BR_launch.md`](BR_launch.md) establishes for
`$BR_EXE` and related tools. `$BRLS_EXE` is set the same way and needs none of
`$BR_CONFIG`/`$BR_AI_UTIL`/`$BR_AI_USER`. 

#### 6.1.0 Command capability matrix

| Mode | Purpose | Input | Output shape | Exit code (verified) | Automation notes |
|---|---|---|---|---|---|
| `-check <file|->` | Parse BR syntax, report line diagnostics | one or more file paths (any may be `-` for stdin) — the `-check` value plus every further plain argument | one `file:line:col: message` block per file, each bad line with a `see:` pointer | `0` all files clean, `1` any file has a parse error | Primary automation flag. Every positional argument is checked, in order — batch support closed [`INTERFACE.md`](INTERFACE.md) finding 2 |
| `-sema` (modifier of `-check`) | Also run brls's semantic pass (undefined names, argument counts, …) over each file `-check` is given | — | adds severity-prefixed findings (`error`/`warning`) to `-check`'s per-file block | folds into `-check`'s own exit code — a `SeverityWarn` finding (e.g. `duplicate-parameter`) does not flip it, only a `SeverityError` one does | Single-file only — no workspace, so a cross-file link cannot resolve; see the scope-boundary note above. Errors (exit `1`) if given without `-check` |
| `-json` (modifier of `-check` or `-keyword`) | Structured output instead of text | — | `-check -json`: a JSON array, one object per file (`file`, `clean`, `diagnostics[]`). `-keyword -json`: a JSON array, one object per class hit | same as the underlying mode | Field shapes are in `cmd/brls/check.go` / `cmd/brls/main.go`; not yet declared stable across builds the way the exit code is. Errors (exit `1`) if given with any other mode |
| `-next '<partial line>'` | Legal continuations at end of a partial statement | one line of text (embedded `\n` is fine) | `statement`/`complete`/`head` flags + admissible keyword list (with a spec pointer for each) | always `0` — any string is valid input, an empty keyword list is itself a real answer | Safe to call speculatively; never signals failure. `keywords: (none — nothing else is valid here)` prints whenever no keyword fits, whether or not BR still owes a non-keyword operand — this build reports no separate hint for that case, so use `complete:`/`head` to judge whether more input is required |
| `-statement <NAME>` | Full syntax tree for one statement | statement keyword | table-rendered tree | `0` found, `1` unknown name (stderr: `brls: no statement "…" in the syntax table`) | |
| `-keyword <NAME>` | Keyword metadata + doc pointers | keyword | class/subscript/abbreviation/spec/topic | `0` found, `1` unknown name (stderr: `brls: "…" is not a keyword in any of BR's tables`) | |
| `-stats` | Embedded language-pack summary | none | counts and table breakdowns | `0` (only `1` on an internal pack-load failure — not seen in practice) | |
| `-version` | Print build version | none | one version line | always `0` | |
| *(no flags)* | LSP transport for editor integration | JSON-RPC framed over stdin/stdout | protocol frames, not text | N/A — blocks waiting for a handshake | **Not** for shell/agent use; see 6.1.7 |
| *(unrecognized flag)* | — | — | usage text to stderr | `2` | Distinct from every mode's own `0`/`1` — a `2` means a bad invocation, not a diagnostic result |

**Argument ordering (quick truth table):**

| Invocation shape | Works? | Notes |
|---|---|---|
| `"$BRLS_EXE" -check a.brs -json` | Yes | Canonical check mode; modifiers may follow file paths. |
| `"$BRLS_EXE" -json -check a.brs` | Yes | `-check` can come after modifiers, as long as no positional file path appears first. |
| `"$BRLS_EXE" -sema -check a.brs` | Yes | Same rule as above. |
| `"$BRLS_EXE" a.brs -check` | No | First positional argument stops flag parsing; brls behaves like no-flag mode and waits for LSP input. |

Rule: place a mode-selecting flag (`-check`, `-next`, `-keyword`, `-statement`, `-stats`, `-version`) before the first positional file/path argument.

**Output stability:**
1. Treat prose output as human-oriented and non-stable (alignment, wording, and field order may change
  between builds).
2. For automation, rely on exit code first, plus stable textual anchors only:
  `file:line:col:` for `-check` diagnostics and `brls: ` on hard stderr errors.
3. Prefer `-json` for machine consumption. Its field names (`file`, `clean`, `diagnostics[]`, `line`,
  `col`, `severity`, `rule`, `message`, `see`) are a stronger contract than prose. Exit code still
  decides clean vs. not-clean because `SeverityWarn` may appear with `clean: true`.

#### 6.1.1 `-check <file|->` — syntax errors, one per bad line

The fast half of the write→check→fix loop (§4, §7 step 6): parses the file without invoking BR and
prints one diagnostic per bad line, each with a `see:` pointer into `br_tree/`. `-check -` reads the
file from stdin, so it also works on text that has not been saved yet. Exit status is `0` for a
clean parse and `1` otherwise — script against the exit code, not the presence of output. Every
further plain argument after the first is checked too, in one invocation, one block per file.

Semantic checks (undefined names, argument counts) are **not** run by plain `-check` — the message
says so on a clean file, as a reminder not to over-read the result. Add `-sema` to run them: it
appends brls's semantic findings to the same per-file block, each line prefixed `error:` or
`warning:`, and folds into the same exit code — a `warning:` finding does not turn a `0` into a `1`,
only an `error:` one does (the rationale is the scope-boundary note above: `SeverityError` here means
"real BR's LOAD/SAVE rejects this or flags it non-executable", not "this looks wrong").

```powershell
PS> "$BRLS_EXE" -check cnp/compare.br.brs
cnp/compare.br.brs: no syntax errors (semantic checks — undefined names, argument counts — are not run by -check)
PS> $LASTEXITCODE
0

PS> @'
100 OPEN #1: "NAME=X"
110 CLOSE #1: WAITEQ
'@ | & "$BRLS_EXE" -check -
<stdin>:1:22: unexpected end of statement; expected DISPLAY, EXTERNAL, INTERNAL or SQL
    see: .../br_tree/10-language/syntax/spec.md#syntax
<stdin>:2:15: unexpected "WAITEQ" after the end of this statement
    see: .../br_tree/10-language/syntax/spec.md#syntax
PS> $LASTEXITCODE
1
```

```bash
$ "$BRLS_EXE" -check cnp/compare.br.brs
cnp/compare.br.brs: no syntax errors (semantic checks — undefined names, argument counts — are not run by -check)
$ echo $?
0

$ printf '100 OPEN #1: "NAME=X"\n110 CLOSE #1: WAITEQ\n' | "$BRLS_EXE" -check -
<stdin>:1:22: unexpected end of statement; expected DISPLAY, EXTERNAL, INTERNAL or SQL
    see: .../br_tree/10-language/syntax/spec.md#syntax
<stdin>:2:15: unexpected "WAITEQ" after the end of this statement
    see: .../br_tree/10-language/syntax/spec.md#syntax
$ echo $?
1

$ "$BRLS_EXE" -check somefile.brs -sema
somefile.brs:1:18: warning: A appears twice in this parameter list
    see: .../br_tree/10-language/flow-control/functions-udf/spec.md#parameters
somefile.brs:4:11: error: FNFOO is not defined in this file and no LIBRARY statement links it. A
function has to be linked before it can be called, even one defined locally with DEF LIBRARY
    see: .../dev/system-functions-catalog.md
$ echo $?
1

$ "$BRLS_EXE" -check cnp/compare.br.brs cnp/color.br.brs -json
[
  {
    "file": "cnp/compare.br.brs",
    "clean": true,
    "diagnostics": []
  },
  {
    "file": "cnp/color.br.brs",
    "clean": true,
    "diagnostics": []
  }
]
```

`-sema` and `-json` are recognised anywhere in the command line, not only ahead of the file list —
`-check a.brs b.brs -json` works the same as `-check -json a.brs b.brs`, and `-json -check a.brs`
works too. The one hard ordering rule is that a mode flag has to appear before the first positional
file/path argument.

**Agent use:** the closing step of writing or editing a `.brs` file — run `-check -sema` on the file,
or pipe the in-progress buffer through `-check - -sema` immediately after each edit, fix what it
reports, and loop until it exits `0`, before ever spending a real BR `LOAD ... source` cycle on it.
Checking several files already on disk at once (e.g. every file a refactor touched) is one
invocation — `-check a.brs b.brs c.brs` — not a loop of single-file calls; use `-json` when the
result needs to be parsed rather than read.

#### 6.1.2 `-next '<partial line>'` — what BR admits at the end of a partial statement

Runs the same table walk that drives editor completion, but over plain text with no caret and no
editor attached: given everything typed so far, it reports which statement that text is in, whether
the statement is already complete, whether a new statement may begin at that point, and the exact set
of clause keywords admissible next (with a spec pointer for each).

```
$ "$BRLS_EXE" -next 'OPEN #1: "NAME=X", EXTERNAL '
statement: OPEN
complete:  false
head:      false
keywords:
  INPUT      clause of OPEN               br_tree/30-io-file/file-model/spec.md
  OUTPUT     clause of OPEN               br_tree/30-io-file/statements/spec.md
  OUTIN      clause of OPEN               br_tree/30-io-file/statements/spec.md
```

An empty `keywords:` list does **not** mean the statement is finished — it only means no single
keyword can extend the line at this position. BR frequently still owes a non-keyword operand (an
expression, a file reference, a required `:`), and this build of `brls` gives no separate signal for
that case: the list prints the fixed placeholder `(none — nothing else is valid here)` whether or not
something is still required.

```
$ "$BRLS_EXE" -next 'LINPUT #10:'
statement: LINPUT
complete:  false
head:      false
keywords:  (none — nothing else is valid here)
```

Here BR still owes a string variable to read the line into (`LINPUT #10: A$` is what completes it) —
`keywords:` alone looks identical whether one more thing is required or nothing is. `complete:false`
is the only signal that more input belongs here; there is currently no field that says *what*.

```
$ "$BRLS_EXE" -next 'READ #1,KEY="X",RESERVE '
statement: READ
complete:  false
head:      false
keywords:  (none — nothing else is valid here)
```

Same pattern — BR still owes a `:` here, but `-next` reports it the same way it would report a
position where nothing further is legal. Rely on `complete:`/`head` for the finished/unfinished
question, and treat an empty `keywords:` list as "no keyword fits here," not as "done."

**Agent use:** while composing a statement clause-by-clause, especially one with several mutually
exclusive branches (`OPEN`, `CLOSE`, `PRINT USING`), quote the line built so far and ask `-next` what
is legal at the end of it rather than guessing from memory or recalling the BNF from `br_tree/` by
hand — this is the rule-1 "search the context first" step applied to syntax specifically. An empty
`keywords:` list with `complete:false` means BR still owes something that isn't a keyword (an
expression, a file reference, a required `:`); check the statement's syntax tree (`-statement`) or the
relevant `br_tree/` spec to see what, since `-next` does not currently say.

#### 6.1.3 `-statement <NAME>` — one statement's syntax tree, as BR stores it

Prints the full syntax tree for a single statement exactly as BR's own table encodes it — every
branch, every optional/required operand, every keyword and exit clause, in table order. This is the
same tree `-next` walks; reading the whole tree at once is useful when the question is not "what fits
at this exact point" but "what are all of this statement's forms".

```
$ "$BRLS_EXE" -statement CLOSE
CLOSE
          required operand
          *file reference (#n)
          two branches follow
             required operand
             WAITEQ
             *numeric expression
             optional operand
             FREE
             *colon required
             may be followed by exits (ends branch)

          three branches follow
                required operand
                FREE
                end.. but resume at level 1

             required operand
             DROP
             end.. but resume at level 1

          optional operand
          RELEASE
          *colon required
          may be followed by exits (ends branch)
```

**Agent use:** before writing a call to a statement whose clause structure is unfamiliar or easy to
misremember (`CLOSE`'s three mutually exclusive branches above are a good example), pull its tree
first rather than pattern-matching off a similar-looking statement seen earlier in the corpus.

#### 6.1.4 `-keyword <NAME>` — class, token subscript, abbreviation, documentation

Reports everything the language pack knows about one keyword: which of BR's keyword tables declare
it, its shortest accepted abbreviation, whether it has a syntax tree (vs. being hand-parsed by BR),
and the `br_tree/` spec and topic that document it. A spelling that is both a statement and a clause
keyword (e.g. `DISPLAY`) prints one block per class it belongs to.

```
$ "$BRLS_EXE" -keyword CLOSE
CLOSE  (statement, table3k[3])
  abbreviates to   CL  (in a table lookup; any prefix where a syntax tree expects it)
  syntax tree      yes — brls -statement CLOSE
  spec             br_tree/30-io-file/statements/spec.md
  topic            close
  documented as    CLOSE — Finalize file
```

**Agent use:** before trusting a keyword abbreviation seen in existing source (or writing a new one),
confirm it against `-keyword` rather than assuming the shortest form that "looks right" — BR's
abbreviation minimums are table-driven and not always the intuitive prefix; and to jump straight to
the `br_tree/` spec page that documents a keyword instead of guessing which folder it lives in.

#### 6.1.5 `-stats` — what the binary knows about BR

Prints a summary of the embedded language pack: statement count and syntax-item-kind breakdown,
keyword counts per class, system-function count, statement-topic count, error-code count (and how
many have a full write-up), and library-function count.

```
$ "$BRLS_EXE" -stats
brls 0.1.0-dev
syntax table: 47 statements
  required_operand        209
  optional_operand        100
  keyword                 219
  descriptor               240
  branches                103
  may_repeat                33
  special_syntax           109
  exits                     99
  end_of_branch             37
  resume_level_1            71
  no_retreat                  4
  semicolon_terminator        1
keywords: 233
  statement                49  (table3k)
  clause                   81  (table4k)
  command                  41  (table1k)
  command-qualifier        34  (table2k)
  status-option            20  (table8k)
  debug-option               8  (table9k)
system functions: 131  (126 reserved in table6k/table7k)
statement topics: 49
error codes: 728  (70 with a full write-up)
library functions: 112
```

**Agent use:** a one-shot sanity check after picking up a new or updated `$BRLS_EXE` — confirms
the binary and its embedded data pack loaded before relying on it for `-check`/`-next` results in a
longer session, and gives a quick sense of scale (e.g. "728 error codes, 70 curated") before deciding
whether to look something up here or in `br_tree/` directly.

#### 6.1.6 `-version` — print the build version and exit

```
$ "$BRLS_EXE" -version
brls 0.1.0-dev
```

**Agent use:** recording which build produced a given `-check`/`-next` result when reporting a
suspected brls defect, or confirming two machines (e.g. a dev box and CI) are running the same build
before treating a discrepancy between their outputs as a real bug rather than a version skew.

#### 6.1.7 No flags — LSP transport mode (editor integration only)

Run with no flags at all, `brls.exe` speaks the Language Server Protocol over stdin/stdout for editor
integration (VS Code, etc.) — it will sit waiting for a framed JSON-RPC handshake rather than
printing anything. **Never use this mode from a script or an agent's shell** — use whichever of the
explicit flags in 6.1.1–6.1.6 fits the task (`-check` for the write→check→fix loop, but `-next`,
`-statement` and `-keyword` are equally valid shell-time calls, not fallbacks).

### 6.2 How to Execute BR

Before running BR check the BR configuration file (specified in [`BR_launch.md`](BR_launch.md)) to see where the `LOGGING` 
output file is located. This will need to be interrogated after your batch run to see how the program 
ended. The log level should be set to 8 or greater.

When interrogating the configuration file take note of the first `DRIVE` statement **to see what folder 
BR starts in**. You may need to have the proc or program CD to the folder of your choice at the 
beginning of each test.

You can write a `.prc` procedure containing the commands you want and run it through the BR invocation 
described in [`BR_launch.md`](BR_launch.md).

Use a BR config with **no auto-launch of the app menu** (`brconfig.ai_util`), so BR runs your initial
command (e.g. `PROC <procname>`) unattended; [`BR_launch.md`](BR_launch.md) covers creating such an "AI access" 
config from the normal app `brconfig.sys`.  When BR runs unattended, it exits as soon as it stops. 
Then check the log file to what caused BR to stop. This may take a little investigation to 
understand how to efficiently interrogate the log file. Tip- grep based on date and time after you see
how it is formatted.

**Reading the log — don't regard "failed"/"error" text as final:** at `LOGGING` level ≥8 BR traces
routine internal retries that contain those words on operations that still *succeed* — e.g. an
`OPEN … REPLACE`/`USE` logs `"...failed during CreateFile...system error 2"` for an
open-existing-first probe even when the file is then created fine. Grepping for `error`/`failed`
alone over-reports. Instead:
- Confirm the **actual outcome** — did the file end up with the expected content, did the program
  reach its own final `STOP`/`PRINT`/log marker — not just the presence of alarming-looking text.
- The unambiguous fatal signal in `UNATTENDED` mode is **`"Unattended processing terminated by
  error <n> while processing..."`**, which names the real error number and the line it happened at.
  `"Input attempted in unattended mode"` is usually a symptom arriving *after* an earlier untrapped
  error (see [`essentials.md`](essentials.md) §2) — trace backward from it, don't treat it as the
  root cause line.

| Task | How (BR, headless) |
|---|---|
| **Syntax-check** a program | `LOAD "<prog>.brs" source` — parses line-by-line, halts on the first error with `ERR`/`LINE` set. The **`source`** keyword is required (`LOAD` defaults to object). |
| **Run** a program | `RUN "<prog>"` If running attended, end the proc with `EXECUTE "system"` so BR exits instead of waiting at READY. |
| **Read / maintain data** | Write a short BR program/proc that `OPEN`s the file (layout from `data-model.md`) and `READ`/`REWRITE`/`WRITE`s it — the kit has no external query tool. |
| **Decompile** `.br` → `.brs` | a proc of `LOAD "<prog>.br"` / `LIST >"<prog>.br.brs"` pairs, ending `EXECUTE "system"` (see [`../app/ONBOARDING.md`](../app/ONBOARDING.md) STEP 4). |

A proc is just BR commands, one per line, ending in `EXECUTE "system"`; run it with
`"$BR_EXE" 'PROC <path>' -"$BR_CONFIG"` (exact executable and config in [`BR_launch.md`](BR_launch.md)). A command that
errors leaves BR waiting at READY, so keep procs self-contained. File references resolve through the
config's `DRIVE` map — use the **drive-relative** form (`<d>:dir\prog`, *no* leading backslash after the
colon), per [`../br_tree/00-configuration/config-directives/spec.md`](../br_tree/00-configuration/config-directives/spec.md#paths).

### 6.3 Operational hazards of a headless run

These bite the *runner*, not the program, and each one masquerades as something else:

- **Every *non-headless* BR start pays a splash delay (~20s observed) before it does anything.** 
  Budget a generous timeout — **≥90s** — or a perfectly healthy run looks like a hang and gets 
  killed just before it starts working. Note this applies to BRconfig.AI_user not BRconfig.AI_util.
- **A headless BR GUI run can steal OS keyboard focus from a live, interactive BR session.** A
  keystroke typed into the real session has been observed landing in the headless one (and the reverse
  is presumably possible). Therefore users should not run production concurrently with AI programming.
- **Force-killing a hung BR process does not cleanly release its workstation (`WSID`) session slot.**
  After a `taskkill -F`, a *later* run can fail during WSID assignment (observed: exit code 99) —
  which reads exactly like a bug in the program you just changed, and isn't. **If a headless run
  mysteriously dies at the assign-WSID stage, suspect a leaked slot from an earlier force-kill before
  you suspect your code.** Letting every run reach its own `EXECUTE "system"` exit avoids this;
  `UNATTENDED` logging (below) is what makes that achievable, since it turns hangs into fast aborts.
- **`LIST` regenerates source through the config's `style` directive, so a decompile *restyles* it.**
  Keywords, label case, indentation and comment alignment are normalized to the config (e.g.
  `style indent 3 45 keywords lower labels mixed expressions upper`). A program whose stored source
  used a different style therefore shows a **huge textual diff that is almost entirely cosmetic, not a
  code change** — don't read it as one, and don't hand-"fix" it back.

### 6.4 When something silently fails: how to actually debug it

- Run headless with a `gui off` config and **`UNATTENDED`** logging (above). This turns an
  otherwise-indefinite hang into a fast, logged abort with the offending program and line number —
  the difference between one diagnostic pass and manually killing a stuck process every time.
- Don't assume the reported line number is the *root cause* line — it's where the symptom
  surfaced. Trace backward from there; the actual defect (an un-sized variable, a bad `GOTO`
  target) is often several statements upstream.
- **Plain `PRINT` (no channel) is invisible when driven headlessly through `brnative.exe`** — it
  outputs to the command console, which nothing captures in an unattended/scripted run; 
  an `ON ERROR` handler's `PRINT "Error";ERR` produced no
  visible output at all, making a real failure look like silent success. **Route any diagnostic
  output a headless run needs to see through a file** (`OPEN #n: "NAME=...,REPLACE,EOL=LF",
  DISPLAY, OUTPUT` then `PRINT #n:`), not bare `PRINT`.
- When a documented, spec-correct construct still fails, **isolate it** with a minimal `mini*.brs`
  probe — a handful of lines, one `OPEN`/`PRINT`/`CLOSE` to a debug file — before assuming your own
  program logic is the bug. Several of the gotchas in [`essentials.md`](essentials.md) cost real time
  specifically because the failing construct *looked* like it must be a logic error in the larger
  program, when it was actually a runtime limitation unrelated to the surrounding code. If you find
  that the runtime execution conflicts with the br_tree or semantics specifcations preserve and
  reference the mini program that demonstrates the failure.
- **A symptom disappearing is not proof you found the cause.** Adding statements prior to finding the 
  cause, is equivalent to guessing, which is prohibited by rule #1. 
- **Writing a large BR program? Generate it, don't hand-type it.** Past ~100–150 lines, write a 
  script that emits the `.brs` — without the line numbers to a list and auto-number them
  in one final pass — rather than typing line numbers by hand. Renumbering to insert a line becomes
  problematic, not bookkeeping, and repetitive or derived content (`DATA` blocks, static JSON skeletons)
  can be emitted **from the actual source data** instead of hand-transcribed, which at that scale is a
  real source of silent bugs.

---

## 7. Checklist for writing a new BR program

1. Identify the data files you touch → generate/consult the app's data model (§4) for fields,
   types, and **key composition**.
2. Pick the access pattern → the codebase's file-access library for app code; raw keyed I/O
   (§4 recipes) for standalone utilities.
3. Find existing functions before writing new ones → search the app's own libraries
   (its `DEF LIBRARY`/`DEF FN` source).
4. Follow the codebase's naming and module conventions.
5. Handle every I/O error clause (`EOF`/`NOKEY`/`IOERR`/`LOCKED`).
6. Syntax-check it — `$BRLS_EXE -check` first for a fast iteration loop, then
  `LOAD <prog>.brs source` and `SAVE` or `REPLACE` in real BR (§6) — checking the log before 
  considering it done.

---

## 8. Kit Maintenance Helpers

The kit ships four build-time helpers, each a standalone executable — no Python or Node.js runtime
needed to run them (the `.py`/`.js` sources beside each `.exe` are kept only for maintenance):
[`tools/extract-schema.exe`](tools/extract-schema.exe) (schema →
`data-model.md`, §4), [`tools/gen_topics.exe`](tools/gen_topics.exe) (rebuild `topics.json` after
editing `statement-semantics.md`), [`tools/gen_datamodel_index.exe`](tools/gen_datamodel_index.exe)
(rebuild `data-model-index.json`), and [`tools/gen_brtree_index.exe`](tools/gen_brtree_index.exe)
(rebuild `brtree-index.json` from br_tree spec frontmatter). The three generators take
**`--verify`** — a non-writing drift check (source hash + range/structure validation +
regenerate-and-compare, exit 1 on drift) for catching a stale index after the source was edited but
not regenerated. **Everything else is done by BR itself, driven headlessly**