# Business Rules — application development guide

This is the capstone for this context kit. It stitches the language reference, the built-in function
catalog, and the schema-extraction tooling into one starting point for writing correct **Business Rules!
(BR)** code — whether you're a developer onboarding to a BR codebase or an LLM acquiring
context. Each section says **where the authoritative detail lives** so this stays a map, not
a duplicate. It is application-agnostic: point the tooling at whatever BR app you're working
on.

---

## Start here — by task type

**Don't load the whole kit**; for one program it's mostly ballast. **[`topics.json`](topics.json) is the
entry point for reading or writing BR code:** it routes a keyword to its anchored
[`statement-semantics.md`](statement-semantics.md) section (with a line range, so you load ~5–10k,
not the whole file) and carries the `lexicon` — the classified inventory of which spellings are
reserved. The path is **`topics.json` → `statement-semantics.md` → [`../br_tree/`](../br_tree/)** (the
authoritative backstop), pulling in the catalogs and your app's data-model as needed.

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

These bite newcomers (and LLMs trained on other BASICs). Per-statement detail in
[`statement-semantics.md`](statement-semantics.md) indexed by [`topics.json`](topics.json), full detail in 
the br_tree reference; the critical ones:

- **Every line is numbered**; labels go right after the number (`00050 LOOP1: …`).
- **`=` is context-sensitive.** Inside `IF`/`WHILE`/`UNTIL` it means *compare*; elsewhere it
  *assigns*. Use **`:=`** to force assignment inside a condition (must be parenthesized).
- **String variables end in `$`**; size is declared `DIM NAME$*30`. Arrays are 1-based.
- **Keywords abbreviate on entry** (shortest-unique-prefix; functions and clause words need full
  spelling), but BR **expands them when a program is LISTed** — so `.brs` source always shows full
  keywords. You never read or write abbreviations in source files.
- **I/O carries trailing error clauses**, not exceptions: `READ #1,…: A$ NOKEY L900 EOF L990`.
  Handle `EOF`, `NOKEY`, `IOERR`, `CONV`, `LOCKED` explicitly.
- **`[WSID]`-style substitutions** appear in file names for per-workstation temp files
  (`"SORTCTL.Z[WSID]"`).
- **`DEF`/`FNEND` functions** can have a typed/sized return (`DEF FNX$*255(...)`), optional
  parameters after `;`, and by-reference parameters marked `&`. Two traps: `FN<name>` in a mid-body
  expression is a *recursive call*, not the value-so-far — build an incremental result in a scratch
  variable, never by reading `FN<name>` back (you may assign it freely, last write wins); and a
  function has **one exit** — no early return, `GOTO` a label before `FNEND`.

---

## 4. Working with data files

### Get the schema first

A BR data file is a fixed-length keyed record store; you need its field layout and key
composition before reading it. The app's `filelay/` (or equivalent) directory is the data
dictionary. Turn it into a structured model with the bundled tool:

```
node tools/extract-schema.js <path-to-app/filelay>
```

This produces `data-model.md` + `data-model.json` for *that* app: per file, the data path,
record length, each key index **with its composing fields** (the order you concatenate to
build a `KEY=` lookup), and every field's FORM type/position. No app's data model is bundled
here — generate the one you need. (No `filelay/`? Convert your data dictionary to the filelay format —
see [`../app/INSTRUCTIONS.md`](../app/INSTRUCTIONS.md) Appendix A — then run the tool.)

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

The kit ships two build-time helpers — [`tools/extract-schema.js`](tools/extract-schema.js) (schema →
`data-model.md`, §4) and [`tools/gen_topics.py`](tools/gen_topics.py) (rebuild `topics.json` after
editing `statement-semantics.md`). **Everything else is done by BR itself, driven headlessly:** write a
`.prc` procedure containing the commands you want and run it through the BR invocation your app records
in [`../app/toolset.md`](../app/toolset.md).

Use a BR config with **`gui off`** and **no auto-launch of the app menu**, so BR drops to READY and runs
the proc unattended (`toolset.md` covers creating such an "AI access" config when the normal
`brconfig.sys` auto-starts the menu). Unlike the GUI `brnative.exe` path (which blocks on a splash
screen without `LexiTip`), a `gui off` runtime runs procs to completion.

| Task | How (BR, headless) |
|---|---|
| **Syntax-check** a program | `LOAD "<prog>.brs" source` — parses line-by-line, halts on the first error with `ERR`/`LINE` set. The **`source`** keyword is required (`LOAD` defaults to object). |
| **Run** a program | `RUN "<prog>"` (or `EXECUTE "<prog>"` from code); end the proc with `EXECUTE "system"` so BR exits instead of waiting at READY. |
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
