# Onboarding the BR Context Kit to a New Application

**Purpose.** This document is a procedure **for teaching an AI Large Language Model (LLM)** the *coding style, 
data model, and toolset* of *your particular BR application*. Let your favorite AI model perform it once. 

When onboarding is complete, the reader may be a human or an AI model.

Please document any errors in ERRORS.md. This includes any inaccuracies *or ambiguities* found during the onboarding process.

---

## Prerequisite - The only thing YOU have to do

**The user should place a copy** of the application's `brconfig.sys` into `dev/tools/`. The resulting 
file should be named `context/dev/tools/brconfig.sys`. It is best to copy any include files along with 
it that could be needed for AI processing. User specific statements are not needed for AI processing. 
Also remove any SUBSTITUTE and EXECUTE statements in include files. If SUBSTITUTES are fundamental 
to the app (it won't run without them) then keep those in. There is no need for a license file. 

Onboardiong STEP 1 derives everything else from this one file. The remainder of this procedure is 
best done by an AI model.

---

## Instructions to AI -The principle: add a layer, don't edit the language

`context/` ships in three layers. **Only the third is app-specific; leave the other two alone.**

| Layer | Path | Scope | Edit during onboarding? |
|---|---|---|---|
| Language truth | `br_tree/` | BR syntax/semantics (37 verified `2b` specs) | ❌ Never — it is app-independent |
| Generic coding kit | `dev/` | Router, semantics, catalogs, tools | ◐ Only `APP-DEV-GUIDE.md` (add app pointer rows) |
| **App layer** | **`app/`** | **This** application's data model, style, and tools | ✅ This is what you build |

Onboarding adds an **app axis** beside the existing **language axis**; keep them distinct:
- **Language axis** — two parallel keyword entry points into the same reference, reached from a token
  you're about to read or write:
  - `topics.json` (statement/clause keyword) → `statement-semantics.md` → `br_tree/` — a *lexical*
    router with line ranges + the reserved-word `lexicon`.
  - `brtree-index.json` (any BR keyword — config, screen, printing, functions, commands) →
    `br_tree/<spec>#<anchor>` — a concept→spec router over *all* leaves; use it for non-statement
    tokens or to reach the authoritative spec directly. Complements `topics.json`, doesn't replace it.
- **App axis** (new): `dev/APP-DEV-GUIDE.md` → always-load `conventions.md` + `BR_launch.md`; on-demand
  `data-model.md` (by file), `exemplars/` (by archetype), `architecture.md`.

The app axis links *into* the language axis for statement detail — it does not live inside it.
`topics.json` stays a keyword→semantics index and is **not** where app conventions/architecture live
(they aren't keyword-addressable).

As you add layer 3 keep the kit's **progressive restatement** discipline: state each app fact in full
in the `app/` docs and as a terse pointer in `dev/APP-DEV-GUIDE.md` (the app entry point) — increasing
brevity as it ascends. (Language facts still ascend into `topics.json`; app facts do not.)

---

## Target shape when finished

```
context/app/
  ONBOARDING.md         # this sheet (stays)
  data-model.md         # STEP 3 — generated from the app's filelay/ folder
  data-model-index.json
  exemplars/            # STEP 5 — ~10–20 blessed real programs, annotated
  conventions.md        # STEP 6 — house style, derived from the app's own source
  architecture.md       # STEP 7 — module map + core data flows
  BR_test.md            # STEP 9 — real-BR LOAD/SAVE survey of this app's tree
  BRLS_test.md          # STEP 9 — brls's own parse/sema survey of the same tree
```

`context/dev/BR_launch.md` (referenced by STEP 1 — BR launch env, canonical invocations, run/build commands) is a
static, application-agnostic kit file. 

`dev/APP-DEV-GUIDE.md` holds pointers to the generated app docs (STEP 8); `topics.json` is the
language keyword router. 

---

## Procedure

Do them in order. STEP 1 (BR launch) and STEP 2 (locate/create `filelay/`) are prerequisites —
nothing else can run BR or read data layouts without them. After that, ROI is highest at the top:
the data model (STEP 3) and exemplars (STEP 5) alone deliver most of the value (correct file I/O +
demonstrated style) — but STEP 4 (audit source currency, using the BR runtime STEP 1 configured)
comes first so the source used to create those exemplars is current. STEP 2 gates STEP 3:
`extract-schema.exe` only parses `filelay/`, so STEP 3 has nothing to read until STEP 2 confirms or
creates it.

### STEP 1 — BR launch entries (fully automated) and AI init root
Create 2 of the 4 files to be used by AI for application development.

**Fixed locations:** - files used to compile and test BR programs

| Role | Path |
|---|---|
| BR executable | `dev/tools/brserver-433c-Win32-Debug-2026-08-27.exe` |
| Existing app startup config | `dev/tools/brconfig.sys` |
| AI Utility config (headless) | `dev/tools/brconfig.ai_util` |
| AI User config (interactive) | `dev/tools/brconfig.ai_user` |

**Generate `dev/tools/brconfig.ai_user`** from `dev/tools/brconfig.sys`:
1. Copy `brconfig.sys`. If `dev/tools/brconfig.sys` doesn't exist, request the user
   to place it there. Don't proceed without it.
2. Remove every line that is an `EXECUTE` or `SUBSTITUTE` statement — matched on the 
    line's leading token (case-insensitive, ignoring leading whitespace); don't touch 
    commented-out (`REM`/`!`) lines.
3. Remove every line that is a `LOGGING` statement, matched the same way.
4. Prepend, as the new first line of the file:
   ```
   LOGGING 10, context\app\startlog.txt
   ```

**Generate `dev/tools/brconfig.ai_util`** from the `brconfig.ai_user` just produced:
1. Copy `brconfig.ai_user`.
2. Replace its `LOGGING` line with:
   ```
   LOGGING 10, context\app\startlog.txt, unattended
   ```

The UNATTENDED keyword lets AI run BR in a headless (no user prompts) mode.

Both are regenerated whenever `brconfig.sys` changes — generated, never hand-edited (same
convention as `data-model.md`/`topics.json`).

### STEP 2 — Locate or create `filelay/` ◆ prerequisite for STEP 3
STEP 3 does **not** inspect the app's actual data files to learn their layout. `extract-schema.exe`
only parses the plain-text **`filelay/`** directory (described in Appendix A): one 
hand-declared layout file per data file, giving the FORM spec, disk position, and 
key composition of every field. If `filelay/`doesn't exist, STEP 3 has nothing to read.

1. **Search the app tree for an existing `filelay/` directory** — check case variants too, and don't
   assume it sits directly under the app root: FileIO's `DefaultFileLayoutPath$` setting (in
   `fileio.ini`) can relocate it anywhere, so a real app's dictionary may live elsewhere in the
   tree. If found and it holds one layout file per data file in the Appendix A format, note its
   actual path as `<filelay-path>` and skip to STEP 3.
2. **If none exists, synthesize one — from authoritative sources only, never by guessing at record
   shape:**
   - **Best source: the app's own data dictionary**, if one exists. It need not be a text file — a
     dictionary can just as easily be stored as a BR `INTERNAL` (binary) file, since BR reads its
     own internal formats most conveniently. If it's in `INTERNAL` format, write a short BR program
     to read it and export its contents into `app/filelay/` in the Appendix A format.
   - If no dictionary — text or `INTERNAL` — can be located, ask the user where it lives and in
     what format, rather than guessing.
   - **Cross-check against the app's own BR source once a draft layout exists**: named `FORM`
     declarations and the `OPEN`/`DIM` statements that reference them describe the real on-disk
     field order. Treat this as **confirmation only, not the primary source** — `FORM` specs can
     jump position (`POS n`), skip bytes (`X n`), and be partial, so they don't reliably reconstruct
     a complete layout on their own.
   - **Do not derive a field layout from the raw `.dat` bytes.** A record's field boundaries aren't
     recoverable from binary data without the FORM spec — reverse-engineering a plausible-looking
     layout that way is exactly the kind of guess [README.md's rule](../README.md) forbids.
   - Write each confirmed layout into `app/filelay/`, in the exact format given in **Appendix A**:
     header line (data file, prefix, version `0`), key lines, optional `recl=`, `====` divider, then
     one field line per field in on-disk order. Appendix A's "Conversion checklist" is the
     step-by-step for this. Note this path as `<filelay-path>` (`app/filelay/`) for STEP 3.
3. **Sanity-check before moving on:** every layout file has a header line, a divider, and at least
   one field line; if `recl=` is given, be sure it's consistent with the sum of field sizes. If not,
   stop and report the discrepancy to the user. A solid `filelay/` folder is required to proceed. If
   the user tells you to ignore the discrepancy then do so.

### STEP 3 — Data model (automated) ◆ highest ROI
The LLM cannot write valid `OPEN` / `READ…USING` / `KEY=` without the real field layouts and key
composition. This step is deterministic.

```
dev/tools/extract-schema.exe <filelay-path> context/app
dev/tools/gen_datamodel_index.exe
```

`<filelay-path>` is the directory STEP 2 resolved — not necessarily `<app>/filelay`; use whatever
path STEP 2 found or created.

- **Produces:** `app/data-model.md` (readable) — per file: data path, record length, key indexes
  **with their composing fields in order**, and every field's FORM type/position. Each file section
  carries an `<a id="…">` anchor.
- **Index:** `gen_datamodel_index.exe` then builds `app/data-model-index.json` — a per-file map to
  1-based inclusive line ranges (like `dev/topics.json` for statement-semantics). Load one file's
  slice instead of the whole (large) `data-model.md`.
- **Verify:** the extractor prints `layouts: N, total fields: M`; the indexer prints `files: N …`.
- **Re-run both** whenever `filelay/` changes — they are generated, never hand-edited.

### STEP 4 — Audit source currency (`.brs` vs `.br`) ◆ automated; no user decision
Typically AI models have trouble with this one because they don't understand how BR DRIVE statements work. 
Get familiar with the DRIVE statement, examine the first drive statement and thereby learn what 
folder is current (present working directory) when BR starts. Note, BR uses backslashes in 
pathnames like Windows Command Prompts, and forward slashes mean something legacy - 
so don't use them. 

STEPS 5–6 learn the house style by reading the app's **`.brs` source**. Because BR can edit a program
while it is compiled (*incremental compilation*), the `.brs` on disk may be **stale or absent**. A
timestamp audit settles this mechanically — no need to ask which copy is authoritative:

Before proceeding with this step, ask the user whether the program masters are kept in source or
compiled form. Record the answer in context/README.md at the end of the Rules section. If the 
program masters are stored in source format decompiling is prohibited. 

> **Audit every compiled `.br`/`.wb`: confirm a corresponding source file (e.g. `prog.br.brs` or 
`prog.brs` for `prog.br`) exists whose modification date-time is the *same as or later than* the compiled file.**

- **Pass** (source exists and is ≥ its `.br`) → that source is current; nothing to do.
- **Fail** (source missing, or older than its `.br`) → the compiled file was changed more recently, so
  the `.brs` is genuinely stale. **if program masters are stored in compiled form** decompile just 
  those programs to refresh the source. Otherwise report the stale source in app/STALE_SOURCE.md.

If decompiling: After identifying a missing or stale .brs file refresh it by running BR with the command: 
> `LIST < <path\program-name> > <path\program-name.br.brs> : EXECUTE "system"` 

Or put the LIST commands into a procedure (batch) file and execute it with "PROC <batch-file-pathname>". 

### STEP 5 — Blessed exemplars ◆ the real way style is learned
An LLM learns style far better from a few gold-standard *real programs* than from prose about style.

1. Pick **one representative, correct program per task archetype** the app actually has — e.g. a
   file-maintenance form (`*fm`), a report (`*p`), a batch update, an EDI translate/load, a
   menu/dispatch, a keyed-read utility. Aim for **10–20** total.
2. Copy each into `app/exemplars/` (or reference it) and add a short header comment:
   *"Blessed pattern for X. Note: the error-handling idiom, the naming convention, FileIO-vs-raw-OPEN
   choice, screen handling."*
3. Choose files that are **minimal but complete** and genuinely typical — not the biggest or most
   clever. These are few-shot examples; their style is what the model will imitate.

### STEP 6 — Conventions sheet (derived, not guessed)
A 1–2 page `app/conventions.md` that **names** the rules the exemplars embody, so the model can
apply them to code it hasn't seen.

- Cover: naming (subscript constants, file prefixes), FileIO vs. raw `OPEN` preference, the house
  error-handling form, line-numbering / Lexi usage, screen conventions, module placement.
- **Derive the dominant idiom from the app's own source**, don't assert from habit: read a
  representative sample across modules and record which form actually dominates (FileIO adoption
  rate, the prevailing error-handling pattern, the naming shape), then state that as the convention
  with a pointer to an exemplar that shows it.

> **⚠️ Describe shape, don't fabricate an API.** `conventions.md` documents the *shape* of code;
> `exemplars/` are *deliberately chosen* whole files. Do **not** scrape the app's user-defined or
> library function names into a "standard API" list — that manufactures a surface the model will
> call incorrectly. Teach usage by whole-file exemplar instead.

### STEP 7 — Architecture map/res
`app/architecture.md` — the directory taxonomy, entry points, and 2–3 **core data flows**
(e.g. order → allocation → ship → EDI). Make them short, like a module table in 
your AI agent's memory file (`CLAUDE.md` or `AGENTS.md`).

### STEP 8 — Wire the app layer into the entry point and update either CLAUDE.md or AGENTS.md

1. If you haven't done so already, go to the app root and run the /init command to be sure either 
  a CLAUDE.md or AGENTS.md file is placed in the app root.
2. Insert `@context/README.md` at the end of any CLAUDE.md or AGENTS.md files in the app root folder. 
3. Modify context/README.md as follows: - State "onboarding has been completed" just ahead of 
  the onboarding paragraph.
4. If you are operating in vscode chat mode stop and use another service with more than 200k of 
  context capacity. This kit only uses around 30k but it requires better intelligence than vscode chat provides. 
5. If you are operating in cursor: - Follow the instructions in context/app/onboarding/context-kit-always-load.md. 
  This will create necessary initialization rules for this repo. 
6. Advise the user that the first prompt after onboarding and restarting should be: 
  "Which documents did you read in full during initialization?"

### STEP 9 — Survey brls vs real BR ⏱ typically long-running (30–60 minutes)

brls's own diagnostic rejections (which findings mean "BR will actually reject this") are calibrated
against BR itself, not asserted — but that calibration was checked against the programs brls was
developed on, not necessarily against *your* application's source. We need to check each app-specific 
construct BR happens to tolerate, or reject, to be sure our language server handles all code patterns. 
STEP 9 checks that calibration for your app specifically. 

`context/dev/tools/loadsave.exe` and `context/dev/tools/lscheck.exe` are two independent survey
programs, prebuilt and deployed the same way `brls.exe` is (`context/lsp/brls/build.ps1`) — nothing to
build on-site, run them directly, the same as `extract-schema.exe`/`gen_datamodel_index.exe` in STEP 3.

**Run both from the app root** — the directory the kit (`context/`) was installed into, one level above
`context/` itself — **not from inside `context/dev/tools/`.**

`-root` is the only location flag either tool takes: the directory to recursively scan for `.brs`
program source (where the suite of BR programs live), which both tools also assume `context/` is
installed directly inside of — it's how each locates the BR executable/`brconfig.ai_util` (`loadsave`
only) and how every file path in the report gets made relative. `-root .` means "the app root is the
current directory," which is exactly why these must be run from there.

**Run `lscheck` first** — fast, pure brls, no real BR involved; gives an immediate baseline:

```
context/dev/tools/lscheck.exe -root . -out context/app/BRLS_test.md
```

**Then run `loadsave`** — drives the real BR executable one process per batch of files, whole-file
`LOAD`/`SAVE`. This is the long-running half: **budget 30–60 minutes** for an application-sized tree
(QSMRP's ~1,100 files took ~24 minutes; scale roughly linearly, and confirm with the user before
running against a much larger tree — see `context/app/second-corpus-load-validation.md` for why a
flat multi-thousand-file harvest needs a different, sampled approach instead of this whole-file sweep).

```
context/dev/tools/loadsave.exe -root . -out context/app/BR_test.md
```

**Compare the two reports' Summary tables.** `BR_test.md`'s "Load and save clean" count should match
(or come very close to) `BRLS_test.md`'s "Clean + advisory only" count — the two are meant to describe
the same thing, real BR's own opinion and brls's opinion of the identical file set. See
`context/app/br-load-save-validation.md` for a worked example of a clean match and how it was verified
file-for-file, not just by comparing the two totals.

**If the two counts disagree, do not silently accept it and do not try to fix brls's rules yourself as
part of onboarding** — a miscalibrated brls rule is a `brls` repo change, not an app-code change, and
fixing it requires the same real-BR confirmation discipline `br-load-save-validation.md` Instead, 
**append a discrepancy report to `context/ERRORS.md`**, covering:

- The two summary counts (BR's "Load and save clean" vs brls's "Clean + advisory only") and the gap.
- The file-level diff between the two reports' failing-file lists: which files brls flags that BR
  loads/saves clean (candidate brls false positives), and which files BR fails that brls calls
  clean/advisory (candidate brls blind spots) — group by the rule/error each side cites, the same
  grouping both reports already carry.
- For each group, a first-pass guess at cause: a genuine brls miscalibration worth reporting upstream,
  or app-specific noise (non-production scratch files, dev tools, misfiled non-BR text) that belongs in
  this app's own excluded-files list instead — see `br-load-save-validation.md`'s "Excluded —
  non-production files" section for the shape of that judgment call.

If the counts already match, no `ERRORS.md` entry is needed for this step.

---

## Done criteria

- [ ] `filelay/` exists (found or synthesized per STEP 2), one layout file per data file, in
      Appendix A format — no guessed field layouts; any file without a locatable FORM/DIM source
      was flagged to the user instead.
- [ ] `app/data-model.md` regenerates cleanly from `filelay/` (0 unparsed files).
- [ ] Source currency audited (STEP 4): every `.br`/`.wb` has an as-new-or-newer source file; any
      stale `.brs` was refreshed before exemplars/conventions were derived.
- [ ] `app/exemplars/` holds ≥10 annotated, representative programs across task archetypes.
- [ ] `app/conventions.md` states each rule and points to an exemplar that shows it.
- [ ] `dev/BR_launch.md` lets a newcomer build, run, test, and deploy without asking.
- [ ] `app/architecture.md` names entry points and the core data flows.
- [ ] `APP-DEV-GUIDE.md` has terse pointer rows to every app doc (conventions/BR_launch marked
      always-load; data-model/exemplars/architecture on-demand); `topics.json` left as the language router.
- [ ] `br_tree/` and `dev/` (except the `APP-DEV-GUIDE.md` pointer rows) are **unchanged**.
- [ ] STEP 9 ran to completion: `app/BR_test.md` and `app/BRLS_test.md` both exist; their summary
      counts were compared, and any discrepancy is recorded in `context/ERRORS.md` (not silently
      fixed or ignored).

## The feedback loop (why this works)
With STEP 3 (real schema) plus a compile pass in BR itself (`.brs` → `.br`), generated code is
**verifiable**: it can be checked against the actual files and the grammar before it ships. "Style"
then includes "compiles against our data model," not just "looks right."

## Maintenance
- If a data file is added or its layout changes, update `filelay/` (STEP 2) first, then re-run STEP 3.
- Re-run STEP 3 after any `filelay/` change.
- Re-run the STEP 4 audit after recompiling; decompile any program whose `.brs` is now older than its
  `.br` before you re-derive exemplars or conventions.
- Refresh exemplars when the house pattern for an archetype changes.
- Language corrections go to `br_tree/` and flow to **every** app — never fork them into `app/`.

---

# Appendix A — the `filelay` file format

STEP 3 consumes a **`filelay/`** directory: one plain-text layout file per data file, describing its
keys and field record layout. If your application's data dictionary is in some other form, convert it
to this format and place the results in `filelay/`. This appendix is the complete spec.
(Source: FileIO Library, `br_tree/50-libraries/fileio/`.)

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
  (backing up the old layout to `filelay/version/<name>.<n>`). Field data is copied by subscript name,
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
| 3 | **FORM spec** | A BR FORM type + size, e.g. `C 4`, `BH 3.2`, `PD 5`, `N 6`. Type **`X`** = filler: the field is ignored except that its length still advances the disk position of later fields. Full FORM type list: `br_tree/30-io-file/form-spec/`. |
| 4 | **Disk date format** *(optional)* | `DATE(Julian)`, `DATE(cymd)`, `DATE(ymd)`, `DATE(mdy)`, etc. — marks the field as a date in that storage format (enables DataCrawler/ScreenIO/CSV date handling; your program still unpacks it). **Any col-4 text that isn't `DATE(...)` is treated as a comment and ignored.** |
| 5+ | **Comments** | Ignored. |

## Comments, blanks, and end-of-file

- A line whose first non-space character is **`!`** is a comment — allowed anywhere, ignored.
- **Blank lines** are ignored.
- An optional **`#eof#`** line after the last field ends parsing; anything below it is ignored (free
  space for notes).

## Conversion checklist (other dictionary → filelay)

1. One file per data file, in a `filelay/` directory; header first.
2. Line 1: data-file name, a unique `PREFIX_`, version `0`.
3. One key line per index; join composite fields with `/` in physical order; add `-U` to
   case-insensitive segments; use the layout's subscript names, not raw positions.
4. Add `recl=` if you know it (else let FileIO compute it).
5. `====` divider.
6. One field line per field **in disk order**: `NAME[$], description, FORM-type size [, DATE(...)]`.
   Represent gaps/reserved bytes as `X <length>` so positions stay correct.
7. Keep subscript names stable across versions forever.
