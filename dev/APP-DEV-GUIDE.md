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
1. Read app/toolset.md to extract the environment variable definitions
2. Extract the PowerShell snippet that sets $env:BR_EXE, $env:BR_TEST, etc.
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
| **Coding** — write correct, idiomatic BR | `topics.json` → `statement-semantics.md` | the two catalogs + data-model, closed by a **`LOAD … source`** syntax check in BR (write→check→fix; §6) |
| **App design** — architecture, data model, modules | [`../app/architecture.md`](../app/architecture.md) + generated **data-model** (§4) + [`../app/conventions.md`](../app/conventions.md) | br_tree concept leaves — [`file-model`](../br_tree/30-io-file/file-model/spec.md), [`library-facility`](../br_tree/50-libraries/library-facility/spec.md), [`screenio`](../br_tree/50-libraries/screenio/spec.md) |
| **Testing** — validate behaviour | headless BR (§6) | syntax-check via `LOAD "<prog>.brs" source`; run programs and procs headlessly through the BR invocation |

*Why `topics.json` and not a flat keyword list: BR's lexicon is **positional** — only system
functions are reserved against variable names, so telling a keyword from a variable needs the
`lexicon` block, not a keyword table.*

### The app layer (after onboarding)

The above is the **language axis**. Once a codebase is onboarded (see
[`../app/INSTRUCTIONS.md`](../app/INSTRUCTIONS.md)), a third layer under [`../app/`](../app/) carries
*this application's* specifics — reached **directly**, not through `topics.json` (which stays a
language keyword router; app conventions/architecture aren't keyword-addressable):

- **Always-load** when reading or writing this app's code:
  - [`../app/conventions.md`](../app/conventions.md) — house coding style (naming, error handling, FileIO-vs-raw-OPEN idiom)
  - [`../app/toolset.md`](../app/toolset.md) — BR launch environment + build / run / test / deploy commands
- **On-demand** (pull the one you need):
  - [`../app/data-model.md`](../app/data-model.md) — file schemas & key composition; look up **by file** (generated — §4)
  - [`../app/architecture.md`](../app/architecture.md) — module map, entry points, core data flows (orientation)
  - [`../app/exemplars/`](../app/exemplars/) — blessed real programs; pick **by archetype** and imitate

These are generated/written during onboarding and are app-private (git-ignored) — a fresh kit skeleton
won't have them yet.

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
| **This app's** data model (files/fields/keys) | [`../app/data-model.md`](../app/data-model.md) — generated by §4 (`tools/extract-schema.js`); look up **by file** |
| **This app's** coding conventions (house style) | [`../app/conventions.md`](../app/conventions.md) — *always-load* when writing app code |
| **This app's** build / run / test commands + BR launch env | [`../app/toolset.md`](../app/toolset.md) — *always-load* |
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
node tools/extract-schema.js <path-to-app/filelay>
python tools/gen_datamodel_index.py
```

This produces `data-model.md` for *that* app: per file, the data path,
record length, each key index **with its composing fields** (the order you concatenate to
build a `KEY=` lookup), and every field's FORM type/position. No app's data model is bundled
here — generate the one you need. (No `filelay/`? Convert your data dictionary to the filelay format —
see [`../app/INSTRUCTIONS.md`](../app/INSTRUCTIONS.md) Appendix A — then run the tool.)

`data-model.md` is large. `gen_datamodel_index.py` builds `data-model-index.json` beside it — a
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

## 5. Screens, printing, EDI (pointers)

- **Screens**: ScreenIO drives interactive forms; persisted definitions live in the binary
  `screenio.dat`/`screenfld.dat`, edited within BR/ScreenIO itself — never hand-edit those files. A
  screen's event `DEF FN…` code is compiled **into** the screen, so after editing an event function you
  **recompile the screen** (not the event source alone).
  Reference: [`../br_tree/50-libraries/screenio/`](../br_tree/50-libraries/screenio/).
- **Printing**: `PRINT #n, USING form:` to an opened print file; PCL/PDF detail in
  [`../br_tree/40-io-printing/`](../br_tree/40-io-printing/).
- **EDI / integration**: BR has JSON and web-integration facilities —
  [`../br_tree/60-integration/`](../br_tree/60-integration/). EDI-heavy apps typically stage
  raw documents and translate them through dedicated programs.

---

## 6. Running BR (headless, via procedures)

### Non-BR Kit Helpers
The kit ships four build-time helpers — [`tools/extract-schema.js`](tools/extract-schema.js) (schema →
`data-model.md`, §4), [`tools/gen_topics.py`](tools/gen_topics.py) (rebuild `topics.json` after
editing `statement-semantics.md`), [`tools/gen_datamodel_index.py`](tools/gen_datamodel_index.py)
(rebuild `data-model-index.json`), and [`tools/gen_brtree_index.py`](tools/gen_brtree_index.py)
(rebuild `brtree-index.json` from br_tree spec frontmatter). The three Python generators take
**`--verify`** — a non-writing drift check (source hash + range/structure validation +
regenerate-and-compare, exit 1 on drift) for catching a stale index after the source was edited but
not regenerated. **Everything else is done by BR itself, driven headlessly**

### How to Execute BR

Before running BR check the BR configuration file (specified in toolset.md) to see where the `LOGGING` 
output file is located. This will need to be interrogated after your batch run to see how the program 
ended. The log level should be set to 8 or greater.

When interrogating the configurstion file take note of the first `DRIVE` statement **to see what folder 
BR starts in**. You may need to have the proc or program CD to the folder of your choice at the 
beginning of each test.

You can write a `.prc` procedure containing the commands you want and run it through the BR invocation 
described in [`../app/toolset.md`](../app/toolset.md).

Use a BR config with **no auto-launch of the app menu** (BR_TEST.sys), so BR runs your initial
command (e.g. `PROC <procname>`) unattended; `toolset.md` covers creating such an "AI access" 
config from the normal app `brconfig.sys`.  When BR runs unattended, it exits as soon as it stops. 
Then check the log file to what caused BR to stop. This may take a little investigation to 
understand how to efficiently interrogate the log file. Tip- grep based on date and time after you see
how it is formatted. Therror 

| Task | How (BR, headless) |
|---|---|
| **Syntax-check** a program | `LOAD "<prog>.brs" source` — parses line-by-line, halts on the first error with `ERR`/`LINE` set. The **`source`** keyword is required (`LOAD` defaults to object). |
| **Run** a program | `RUN "<prog>"` If running attended, end the proc with `EXECUTE "system"` so BR exits instead of waiting at READY. |
| **Read / maintain data** | Write a short BR program/proc that `OPEN`s the file (layout from `data-model.md`) and `READ`/`REWRITE`/`WRITE`s it — the kit has no external query tool. |
| **Decompile** `.br` → `.brs` | a proc of `LOAD "<prog>.br"` / `LIST >"<prog>.br.brs"` pairs, ending `EXECUTE "system"` (see [`../app/INSTRUCTIONS.md`](../app/INSTRUCTIONS.md) STEP 3). |

A proc is just BR commands, one per line, ending in `EXECUTE "system"`; run it with
`"$BR_EXE" 'PROC <path>' -"$BR_CONFIG"` (exact executable and config in `toolset.md`). A command that
errors leaves BR waiting at READY, so keep procs self-contained. File references resolve through the
config's `DRIVE` map — use the **drive-relative** form (`<d>:dir\prog`, *no* leading backslash after the
colon), per [`../br_tree/00-configuration/config-directives/spec.md`](../br_tree/00-configuration/config-directives/spec.md#paths).

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
6. Syntax-check it in BR — `LOAD "<prog>.brs" source` (§6) — before considering it done.
