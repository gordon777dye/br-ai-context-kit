# Onboarding the BR Kit to a New Application

**Purpose.** This document is a procedure for teaching an AI Large Language Model (LLM) the *coding style, 
data model, and toolset* of *your particular* BR application, on top of the generic BR kit in `context\`. 
Follow it once per application. Let your favorite AI model do the work (except for step 2). 

Once onboarding is complete, the reader may be a human or an LLM.

Please document any errors in dev\ERRORS.md.

---

## The principle — add a layer, don't edit the language

`context\` ships in three layers. **Only the third is app-specific; leave the other two alone.**

| Layer | Path | Scope | Edit during onboarding? |
|---|---|---|---|
| Language truth | `br_tree\` | BR syntax/semantics (37 verified `2b` specs) | ❌ Never — it is app-independent |
| Generic coding kit | `dev\` | Router, semantics, catalogs, tools | ◐ Only `APP-DEV-GUIDE.md` (add app pointer rows) |
| **App layer** | **`app\`** | **This** application's data model, style, and tools | ✅ This is what you build |

Onboarding adds an **app axis** beside the existing **language axis**; keep them distinct:
- **Language axis**: `topics.json` (BR keyword) → `statement-semantics.md` → `br_tree\`
  — a *lexical* router, reached from a token you're about to read or write.
- **App axis** (new): `dev\APP-DEV-GUIDE.md` → always-load `conventions.md` + `toolset.md`; on-demand
  `data-model.md` (by file), `exemplars\` (by archetype), `architecture.md`.

The app axis links *into* the language axis for statement detail — it does not live inside it.
`topics.json` stays a keyword→semantics index and is **not** where app conventions/architecture live
(they aren't keyword-addressable).

As you add layer 3 keep the kit's **progressive restatement** discipline: state each app fact in full
in the `app\` docs and as a terse pointer in `dev\APP-DEV-GUIDE.md` (the app entry point) — increasing
brevity as it ascends. (Language facts still ascend into `topics.json`; app facts do not.)

---

## Target shape when finished

```
context\app\
  INSTRUCTIONS.md       # this sheet (stays)
  data-model.md/.json   # STEP 1 — generated from the app's filelay\
  toolset.md            # STEP 2 — BR launch env, canonical invocations, run/build commands
  exemplars\            # STEP 4 — ~10–20 blessed real programs, annotated
  conventions.md        # STEP 5 — house style, derived from the app's own source
  architecture.md       # STEP 6 — module map + core data flows
```

`dev\APP-DEV-GUIDE.md` holds pointers to the generated app docs (STEP 7); `topics.json` is the
language keyword router. 

---

## Prerequisites

The prompts needed to generate the *docs* ship inside `context\`. However, two types of shell calls will be used in the 
onboarding process that are **not** part of `context\` and support for them must exist on the machine doing the onboarding:

| Needed for | Dependency | Notes |
|---|---|---|
| STEP 1 — data model | **Node.js** (v14+), to run `dev\tools\extract-schema.js` | Command-line only; run once per `filelay\` change. Not needed at model runtime — it produces static `data-model.{json,md}`. |
| STEP 2 BR executable path | **The BR runtime** (`br` / `brnative`) | This is the app's own *existing* BR executable — nothing extra to obtain. **You will need to edit** its executable path/name and the `brconfig.sys` location in `app\toolset.md` (see STEP 2). This is the only step that cannot be done by AI.|

Also assumed present (inputs, not tools):

- The application's **`filelay\`** data-dictionary directory (input to STEP 1). If your data dictionary does not use filelay record layouts **it will be necessary to create a set of filelay layouts from your toolset**. AI models are really good at such conversions, and the specs for the filelay format are in the appendix to this document. So, if you do not have filelay file layouts, ask your AI agent to create them from either your toolset or your program source code. 
- Read access to the application's **source tree** (`*.brs`) — the raw material for exemplars (STEP 4)
  and conventions (STEP 5). In the event some of your `.brs` files are stale or missing, STEP 3 audits source 
  status and refreshes out of date `.brs` files before examining source in subsequent steps.

---

## Procedure

Do them in order; ROI is highest at the top. The data model (STEP 1) and exemplars (STEP 4) alone
deliver most of the value (correct file I/O + demonstrated style) — but STEP 3 (audit source
currency, using the BR runtime configured in STEP 2) comes first so the source used to create those 
exemplars is current.

### STEP 1 — Data model (automated, do first) ◆ highest ROI
The LLM cannot write valid `OPEN` / `READ…USING` / `KEY=` without the real field layouts and key
composition. This step is deterministic.

```
node dev\tools\extract-schema.js <app>\filelay context\app
python dev\tools\gen_datamodel_index.py
```

- **Produces:** `app\data-model.md` (readable) — per file: data path, record length, key indexes
  **with their composing fields in order**, and every field's FORM type/position. Each file section
  carries an `<a id="…">` anchor.
- **Index:** `gen_datamodel_index.py` then builds `app\data-model-index.json` — a per-file map to
  1-based inclusive line ranges (like `dev\topics.json` for statement-semantics). Load one file's
  slice instead of the whole (large) `data-model.md`.
- **Verify:** the extractor prints `layouts: N, total fields: M`; the indexer prints `files: N …`.
- **Re-run both** whenever `filelay\` changes — they are generated, never hand-edited.

### STEP 2 — Toolset entries (fill in the blanks)
**Modify `app\toolset.md`** and fill in these **required** values first — they are everything the model
(and the STEP 3 / feedback-loop tooling) needs to run and check code. Keep it minimal; the rest of the
runbook (dev commands, utilities, deploy notes — template: the `## Development Commands` block in the
repo's root AI memoery file can grow later.

Modify toolset.md to have the correct paths: 
```
BR executable  ($BR_EXE)    : <path/name>            # e.g. C:\BRnative\brnative.exe — machine-specific
brconfig.sys   ($BR_CONFIG) : <path>                 # usually the app root — ships with the app
BR version                  : <e.g. native 4.3x>     # directives/behavior differ across versions
```

- **Executable path is machine-specific** → kept in `$BR_EXE`; provide an absolute path to your BR executable.
- **`brconfig.sys` is app-owned** → a fixed path (override via `$BR_CONFIG` only if a box needs to).
- **Canonical invocation** — an optional quoted BR statement first, then the config as `-<file>`
  (a dash **attached** to the path): `"$BR_EXE" ["<statement>"] -"$BR_CONFIG"`. Syntax:
  [br_tree — Startup command line](../br_tree/00-configuration/platform/spec.md).
Full worked example: [`toolset.md`](toolset.md).

### STEP 3 — Audit source currency (`.brs` vs `.br`) ◆ automated; no user decision
STEPS 4–5 learn the house style by reading the app's **`.brs` source**. Because BR can edit a program
while it is compiled (*incremental compilation*), the `.brs` on disk may be **stale or absent**. A
timestamp audit settles this mechanically — no need to ask which copy is authoritative:

> **Audit every compiled `.br`/`.wb`: confirm a corresponding source file (e.g. `prog.br.brs` for
> `prog.br`) exists whose modification date-time is the *same as or later than* the compiled file.**

- **Pass** (source exists and is ≥ its `.br`) → that source is current; nothing to do.
- **Fail** (source missing, or older than its `.br`) → the compiled file was changed more recently, so
  the `.brs` is genuinely stale. **Decompile just those programs** to refresh the source. This is safe
  to run unattended: a *newer* `.brs` always passes the audit and is never touched, so no hand-edit can
  be lost — which is why STEP 3 needs no user decision or permission gate.

Decompiling: After identifying a missing or stale .brs file refresh it by running BR with the command: 
`LIST < <path\program-name> > <path\program-name.br.brs> : EXECUTE "system"` 

Or put the LIST commands into a procedure (batch) file and execute it with "PROC <batch-file-pathname>". 
If you go this route then end the proc with `EXECUTE "system"`

### STEP 4 — Blessed exemplars ◆ the real way style is learned
An LLM learns style far better from a few gold-standard *real programs* than from prose about style.

1. Pick **one representative, correct program per task archetype** the app actually has — e.g. a
   file-maintenance form (`*fm`), a report (`*p`), a batch update, an EDI translate/load, a
   menu/dispatch, a keyed-read utility. Aim for **10–20** total.
2. Copy each into `app\exemplars\` (or reference it) and add a short header comment:
   *"Blessed pattern for X. Note: the error-handling idiom, the naming convention, FileIO-vs-raw-OPEN
   choice, screen handling."*
3. Choose files that are **minimal but complete** and genuinely typical — not the biggest or most
   clever. These are few-shot examples; their style is what the model will imitate.

### STEP 5 — Conventions sheet (derived, not guessed)
A 1–2 page `app\conventions.md` that **names** the rules the exemplars embody, so the model can
apply them to code it hasn't seen.

- Cover: naming (subscript constants, file prefixes), FileIO vs. raw `OPEN` preference, the house
  error-handling form, line-numbering / Lexi usage, screen conventions, module placement.
- **Derive the dominant idiom from the app's own source**, don't assert from habit: read a
  representative sample across modules and record which form actually dominates (FileIO adoption
  rate, the prevailing error-handling pattern, the naming shape), then state that as the convention
  with a pointer to an exemplar that shows it.

> **⚠️ Describe shape, don't fabricate an API.** `conventions.md` documents the *shape* of code;
> `exemplars\` are *deliberately chosen* whole files. Do **not** scrape the app's user-defined or
> library function names into a "standard API" list — that manufactures a surface the model will
> call incorrectly. Teach usage by whole-file exemplar instead.

### STEP 6 — Architecture map
`app\architecture.md` — the directory taxonomy, entry points, and 2–3 **core data flows**
(e.g. order → allocation → ship → EDI). Make them short, like a module table in 
your AI agent's memory file (`CLAUDE.md`).

### STEP 7 — Wire the app layer into the entry point
Make the app layer **discoverable** — through `APP-DEV-GUIDE.md`, not by overloading the keyword router.
The two routers stay single-responsibility: `topics.json` = "what does this BR statement mean";
`APP-DEV-GUIDE.md` = "how this app is built."

1. In `dev\APP-DEV-GUIDE.md` (the app entry point) add a terse pointer row for each app doc — in the
   "Start here" table and the §2 reference map. Mark **`conventions.md` and `toolset.md` as
   always-load** when writing app code; **`data-model.md` (by file), `exemplars\` (by archetype), and
   `architecture.md` as on-demand** lookups. Full detail stays in the `app\` docs (progressive
   restatement).
2. Leave `dev\topics.json` as the **language** keyword→`statement-semantics.md` router. It is keyed by
   BR lexemes, so app conventions/architecture — which aren't keyword-addressable — do **not** belong
   in it. *(Optional: a single pointer to `data-model.md` if you want schema reachable from the router,
   but the per-file index belongs in `data-model.md`'s own contents, not the keyword index.)*

---

## Done criteria

- [ ] `app\data-model.md` regenerates cleanly from `filelay\` (0 unparsed files).
- [ ] Source currency audited (STEP 3): every `.br`/`.wb` has an as-new-or-newer source file; any
      stale `.brs` was refreshed before exemplars/conventions were derived.
- [ ] `app\exemplars\` holds ≥10 annotated, representative programs across task archetypes.
- [ ] `app\conventions.md` states each rule and points to an exemplar that shows it.
- [ ] `app\toolset.md` lets a newcomer build, run, test, and deploy without asking.
- [ ] `app\architecture.md` names entry points and the core data flows.
- [ ] `APP-DEV-GUIDE.md` has terse pointer rows to every app doc (conventions/toolset marked
      always-load; data-model/exemplars/architecture on-demand); `topics.json` left as the language router.
- [ ] `br_tree\` and `dev\` (except the `APP-DEV-GUIDE.md` pointer rows) are **unchanged**.

## The feedback loop (why this works)
With STEP 1 (real schema) plus a compile pass in BR itself (`.brs` → `.br`), generated code is
**verifiable**: it can be checked against the actual files and the grammar before it ships. "Style"
then includes "compiles against our data model," not just "looks right."

## Maintenance
- Re-run STEP 1 after any `filelay\` change.
- Re-run the STEP 3 audit after recompiling; decompile any program whose `.brs` is now older than its
  `.br` before you re-derive exemplars or conventions.
- Refresh exemplars when the house pattern for an archetype changes.
- Language corrections go to `br_tree\` and flow to **every** app — never fork them into `app\`.

---

# Appendix A — the `filelay` file format

STEP 1 consumes a **`filelay\`** directory: one plain-text layout file per data file, describing its
keys and field record layout. If your application's data dictionary is in some other form, convert it
to this format and place the results in `filelay\`. This appendix is the complete spec.
(Source: FileIO Library, `br_tree\50-libraries\fileio\`.)

## Anatomy

Each layout file has three parts in order: a **header** (data file + keys + optional `recl`), a
**divider**, then the **field definitions**. Columns on every line are comma-separated; extra spacing
is cosmetic and ignored.

```
 price.dat, PR_, 1                         ← data file, subscript prefix, version
 price.key, FARM                           ← key 1
 price.ky2, ITEM                           ← key 2
 price.ky3, FARM/ITEM/GRADE                ← key 3 (composite)
 price.ky4, DESCRIPTION-U/COST             ← key 4 (DESCRIPTION segment case-insensitive)
 recl=127                                  ← optional record length
 ===================================================   ← divider (ignored)
 FARM$,          Farm Code (or blank),        C    4
 ITEM$,          Item Code,                   C    4
 GRADE$,         Quality,                     C    4
 X,              Empty,                       X   37
 PRICE,          Default Price,               BH 3.2
 ! comment lines start with ! and are ignored anywhere
 COST,           Default Cost,                BH 3.2
 DESCRIPTION$,   Description of Price Rule,   C   30
 #eof#                                         ← optional; everything after is ignored
 additional comments...
```

## Header lines

**Line 1 — `<data-file>, <PREFIX_>, <version>`**
- `<data-file>` — the data file name on disk (e.g. `price.dat`).
- `<PREFIX_>` — a short string prefixing every field's subscript name, so identically-named fields in
  different files stay distinct (`PR_PRICE` vs. `RT_PRICE`). Chosen per file.
- `<version>` — integer file-layout version. **Start at 0; increment by 1 on every layout change.**
  FileIO compares this to the on-disk file's version and auto-migrates data when yours is higher
  (backing up the old layout to `filelay\version\<name>.<n>`). Field data is copied by subscript name,
  so **never rename an existing subscript** — a rename reads as drop-old + add-new and loses that
  field's data. Rearranging fields, adding/removing fields or keys, and changing `recl` are all safe.

**Key lines — `<key-file>, <keydef>`** (zero or more, one per index)
- `<key-file>` — the index file name on disk (e.g. `price.key`, `price.ky2`).
- `<keydef>` — the key's composing field(s), given as **subscript names from this layout**:
  - A single field → simple key.
  - Multiple fields joined by **`/`** → composite key, concatenated in the given order. FileIO derives
    the BR `KPS=`/`KLN=` (position/length) from the fields' positions, so order matters.
  - Suffix **`-U`** on a field name → that segment is **case-insensitive** (BR's `U` key modifier).
- As many keys as you like; parsing stops at the first non-key header line.

**`recl=<n>`** (optional) — record length used when a file is created or upgraded. If omitted, it is
computed from the field FORM specs.

## Divider

A line of `=` characters separates the header from the fields. It is skipped entirely — purely for
readability.

## Field definition lines

One line per field, in **on-disk order**. Comma-separated columns:

| Col | Meaning | Rules |
|----:|---------|-------|
| 1 | **Subscript name** | Append `$` for string fields; nothing for numeric. Gets the header `PREFIX_` in code. Must be unique and stable (see versioning). |
| 2 | **Description** | Human label; also DataCrawler column heading and ScreenIO default caption. Keep ≤ ~80 chars. |
| 3 | **FORM spec** | A BR FORM type + size, e.g. `C 4`, `BH 3.2`, `PD 5`, `N 6`. Type **`X`** = filler: the field is ignored except that its length still advances the disk position of later fields. Full FORM type list: `br_tree\30-io-file\form-spec\`. |
| 4 | **Disk date format** *(optional)* | `DATE(Julian)`, `DATE(cymd)`, `DATE(ymd)`, `DATE(mdy)`, etc. — marks the field as a date in that storage format (enables DataCrawler/ScreenIO/CSV date handling; your program still unpacks it). **Any col-4 text that isn't `DATE(...)` is treated as a comment and ignored.** |
| 5+ | **Comments** | Ignored. |

## Comments, blanks, and end-of-file

- A line whose first non-space character is **`!`** is a comment — allowed anywhere, ignored.
- **Blank lines** are ignored.
- An optional **`#eof#`** line after the last field ends parsing; anything below it is ignored (free
  space for notes).

## Conversion checklist (other dictionary → filelay)

1. One file per data file, in a `filelay\` directory; header first.
2. Line 1: data-file name, a unique `PREFIX_`, version `0`.
3. One key line per index; join composite fields with `/` in physical order; add `-U` to
   case-insensitive segments; use the layout's subscript names, not raw positions.
4. Add `recl=` if you know it (else let FileIO compute it).
5. `====` divider.
6. One field line per field **in disk order**: `NAME[$], description, FORM-type size [, DATE(...)]`.
   Represent gaps/reserved bytes as `X <length>` so positions stay correct.
7. Keep subscript names stable across versions forever.
