---
alwaysApply: true
---

# BR Launch

## BR launch environment

AI models need to know how to invoke Business Rules for compilation and testing. The executable and
all three config files are fixed, kit-relative paths — nothing here is machine-specific.
`brconfig.ai_util`/`brconfig.ai_user` are generated from `brconfig.sys` by ONBOARDING.md STEP 1, 
never hand-edited.

| Fact | Value | Nature |
|---|---|---|
| **BR executable** | `$BR_EXE` | Ships with the kit |
| **`brconfig.sys`** | `$BR_CONFIG` | Existing app startup config |
| **`brconfig.ai_util`** | `$BR_AI_UTIL` | AI Utility — headless (`UNATTENDED`) |
| **`brconfig.ai_user`** | `$BR_AI_USER` | AI User — interactive, for testing user interfaces |
| **`brls.exe`** | `$BRLS_EXE` | Standalone syntax pre-check (optional semantic pass via `-check -sema`) — does **not** invoke BR (§6.1) |

```powershell
$env:BR_EXE     = "context\dev\tools\brserver-433c-Win32-Debug-2026-08-27.exe"
$env:BR_CONFIG  = "context\dev\tools\brconfig.sys"
$env:BR_AI_UTIL = "context\dev\tools\brconfig.ai_util"
$env:BR_AI_USER = "context\dev\tools\brconfig.ai_user"
$env:BRLS_EXE   = "context\dev\tools\brls.exe"
```

```bash
export BR_EXE="context/dev/tools/brserver-433c-Win32-Debug-2026-08-27.exe"
export BR_CONFIG="context/dev/tools/brconfig.sys"
export BR_AI_UTIL="context/dev/tools/brconfig.ai_util"
export BR_AI_USER="context/dev/tools/brconfig.ai_user"
export BRLS_EXE="context/dev/tools/brls.exe"
```

**All paths above, and every invocation in this file and in §6.1, are relative to the kit root**
(the directory containing `context/` — Run from there, or resolve these paths against it first; 
`brls.exe` takes no config file and needs none of `$BR_CONFIG`/
`$BR_AI_UTIL`/`$BR_AI_USER` — it never launches BR.

## AI Canonical invocations

Copy these verbatim (the STEP 3 compile check uses the same form).

```
"$BR_EXE" -"$BR_CONFIG"                           # start BR into the app (interactive)
"$BR_EXE" "RUN glp\trial_bal" -"$BR_AI_UTIL"       # run a program, headless
"$BR_EXE" "RUN cnp\menu" -"$BR_AI_USER"            # run a statement/command, interactive
"$BR_EXE" "PROC cnp\batch.prc" -"$BR_AI_UTIL"      # run a procedure, headless
```

- **`-<config-file>`** names a config file — a dash **immediately followed** by the
  path/filename (e.g. `-"$BR_CONFIG"`), no space. With none given, BR looks for `brconfig.sys`, then
  `wbconfig.sys`.
- The **first quoted argument** is a BR statement/command to run the instant BR starts 
  (e.g. `"RUN cnp\menu"`, `"PROC start"`). 
- Syntax reference: [br_tree — Startup command line](../br_tree/00-configuration/platform/spec.md).

---

## Development commands

### Compile / syntax-check
Sources compile `.br.brs` → `.br` on modification. To force a compile-check of one source
(the STEP 3 feedback loop):

```
"$BR_EXE" "LOAD program.brs source" -"$BR_AI_UTIL"   # parses; reports first error + line
```

The **`source`** keyword is required to load a `.brs` as source — `LOAD` defaults to object mode and
will not infer source from the extension ([LOAD](../br_tree/70-commands/program-management/spec.md#loading)).

### Run a program with console input
```
"$BR_EXE" "RUN cop\xlate850" -"$BR_AI_USER"
```
---

## The Lexi preprocessor (if this app uses one)

Some BR shops write source for **Lexi**, a preprocessor that accepts a handful of constructs base
BR doesn't (`/* ... */` comments, `X$&="..."` compound append, `#Select#/#Case#/#End Select#`, and
others — full list in [`essentials.md`](essentials.md#1-core-language-rules)) and rewrites them
into plain, correctly line-numbered BR text before real BR ever compiles it. **QSMRP does not use
it** — its `.br.brs` source has none of the Lexi-only constructs (`/*`, `$&=`, `#Select#`) and
[`../app/conventions.md`](../app/conventions.md) doesn't mention it — so none of this section
applies to this app's own code. It's documented here anyway because a future app onboarded with
this same kit may use it: check `../app/conventions.md` if this app has been (re-)onboarded to a
different codebase, or grep its `.brs` source for the syntax above if not (a bare `SELECT
CASE`/`END SELECT` with no `#` is not a useful signal — see `essentials.md`, it isn't valid syntax
either way).

### What Lexi actually is

Lexi is itself a **BR library program**, not a separate compiler binary. Confirmed by reading the
bundled source directly (not guessed):

- `lexi.br`/`lexi.brs` — the library, exposing two functions: `fnApplyLexi(InFile$, OutFile$,
  Mode, SourceMapFile$)` and `fnUndoLexi(InFile$, OutFile$)`.
- `fnApplyLexi`'s `Mode` argument: `1` translates Lexi syntax only, keeping whatever line numbers
  the input already has; `0` assigns line numbers **and** translates Lexi syntax in one pass —
  this is the mode a file written with `#Autonumber#` (no baked-in numbers — the normal shape of
  hand-authored app code) needs.
- `fnUndoLexi` is the reverse: strips line numbers back out.

### A real, common Lexi distribution: the "BR Language Server" VS Code extension

One confirmed real-world packaging of Lexi (there may be others) is bundled inside the VS Code
extension `crs-dev.vslang-br` ("BR Language Server"), under `<extension-install-dir>/Lexi/`:

| File | Role |
|---|---|
| `lexi.br` / `lexi.brs` | The Lexi library itself (see above) |
| `lexionly.brs` | Thin driver: `fnApplyLexi(InFile$, OutFile$, 1, SourceMapFile$)` |
| `linenum.brs` | Thin driver: `fnApplyLexi(InFile$, OutFile$, 0, SourceMapFile$)` |
| `strip.brs` | Thin driver: `fnUndoLexi(InFile$, OutFile$)` |
| `brnative.exe` / `brnative.42.exe` / `brlinux` | Bundled BR runtimes (4.3 / 4.2 / Linux 4.3) used to actually run the above |
| `wbconfig.sys` | A config used only for this compile step — separate from the app's own `brconfig.sys` |

The extension's README confirms the user-facing behavior: **"Compile `.brs`/`.wbs` to `.br`/`.wb`
via the Lexi preprocessor"**, triggerable by `Ctrl+Shift+B` or automatically **on save** (a
per-file status-bar toggle). This is what "saving a `.brs` file in VS Code produces the matching
`.br`" means mechanically — it isn't the editor itself compiling anything, it's the extension
shelling out to run this same Lexi library through a bundled BR runtime. (Some apps ship their own
root-level copy of `lexi.brs` too — e.g. because a screen-compile step invokes it directly, see
that app's own `conventions.md` if so. A byte-for-byte diff against one such app-root copy, done
during a prior onboarding, found it identical to the extension's bundled copy aside from
CRLF-vs-LF line endings: same `fnApplyLexi` engine either way, just two separate physical
deployments — worth checking again if this app has its own copy, rather than assuming.)

**How the extension wires that up** (reverse-engineered by reading the extension's own bundled
`dist/extension.js`, not officially documented — the *translation* step below has since been
**verified independently** by actually running it outside VS Code; the surrounding copy-in/
compile-to-.br/copy-out steps are still as-read-from-the-code, not personally re-run end-to-end):

1. Copy the current source into a temp file the extension manages (under a `tmp/` folder next to
   the source).
2. Generate a small BR **proc** (same shape as this file's own procs) that:
   - `subproc lexionly.brs` or `subproc linenum.brs` (picked by whether the source already has
     line numbers),
   - **types two more numbered lines directly into the proc** — `Infile$="tmp\..."` /
     `Outfile$="tmp\..."` (and `SourceMapFile$=...`, if a source map was requested) — which BR
     inserts into the `lexionly.brs`/`linenum.brs` program now sitting in memory, between its
     existing `dim` and `library`/`fnApplyLexi` lines, exactly as if a human had typed new lines
     at the keyboard. This is how `Infile$`/`Outfile$` actually get set — not a command-line
     argument or an environment variable.
   - `run` (executes the now-patched Lexi driver against those files),
   - `clear`,
   - `subproc <the-now-translated-temp-file>` (loads the plain-BR result as the program to
     compile),
   - `skip PROGRAM_REPLACE if exists(...)` / `save "<target>.br"` **or** `replace "<target>.br"`
     (fresh compile vs. recompile over an existing object),
   - `system` (exit).
3. Run that proc through the bundled runtime with the bundled `wbconfig.sys` — the same
   `"$BR_EXE" "PROC <path>" -<config>` invocation shape already documented above in this file —
   and watch stdout for BR's own error patterns to report a compile failure back in the editor.

### Use `dev/tools/lexi-compile.ps1` — the ready-made, tested way to run this headlessly

This kit ships a PowerShell script that does the above for you — don't hand-build the proc
described in step 2 from scratch each time; use the script, which has already been debugged
(quoting, `ArgumentList` not existing in Windows PowerShell 5.1, path-with-spaces handling) so you
don't have to rediscover those problems:

```powershell
# Translate only (default) — produces <source>.lexiout.brs next to the source
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs

# Translate AND compile to a real .br object
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs -Compile

# Explicit output paths
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs -OutFile path\to\translated.brs -Compile -OutObject path\to\file.br
```

By default it auto-detects the Lexi install under
`$env:USERPROFILE\.vscode\extensions\crs-dev.vslang-br-*\Lexi` (the "BR Language Server" VS Code
extension's bundled copy) and uses its bundled `brnative.exe`/`wbconfig.sys`. **This means the
script depends on that extension being installed on the machine it runs on** — if it isn't, or
you'd rather compile through the app's own BR runtime, pass `-LexiPath`/`-BrExe`/`-WbConfig`
explicitly (see the script's own `Get-Help -Full` for all parameters; an app's own root-level
`lexi.brs`, if it has one — see that app's `conventions.md` — may be the *same* Lexi library, but
confirm byte-identity before relying on that; pointing `-LexiPath` at wherever it lives plus an
explicit `-BrExe`/`-WbConfig` for a real BR install works just as well). It runs everything under
unattended logging automatically, so a bad input aborts in seconds instead of hanging the shell —
see the operational hazards in [`APP-DEV-GUIDE.md`](APP-DEV-GUIDE.md#63-operational-hazards-of-a-headless-run)
for why that matters. Both the translate-only and `-Compile` paths were run end-to-end (not just
written from theory) as part of building this script — see its own `.NOTES`.

**Verified mechanism** this script (and the VS Code extension) both rely on:

```
proc noecho
subproc linenum.brs
00025 Infile$=":C:\full\path\to\source.brs"
00026 Outfile$=":C:\full\path\to\translated-output.brs"
run
clear
system
```

Run from inside the extension's `Lexi/` folder (so the bare `subproc linenum.brs` resolves), e.g.
`Lexi\brnative.exe "proc :C:\full\path\to\this.prc" -Lexi\wbconfig.sys`. The leading `:` on each
absolute path is required — without it BR applies its own `DRIVE`-letter substitution to `C:` and
resolves the path wrong; a bare `:` marks a literal OS path. This confirmed, live-tested:

- `/* multi-line comments */` translate to `!` comments (a comment spanning multiple source lines
  collapses — the closing fragment attaches to the *next* line as a trailing `!` comment rather
  than getting its own numbered line, so don't expect a strict 1:1 source-line-to-output-line
  mapping).
- `X$&="..."` becomes `X$(INF:0)="..."` — the safe append idiom, not naive self-concatenation.
- `#Select# expr #Case# value ... #End Select#` becomes `IF expr = value THEN ... ELSE IF ...
  END IF`, each original directive line preserved as a trailing comment.
- A bare `SELECT CASE ... END SELECT` (no `#`) passes through **completely untouched** by Lexi in
  both modes, and then fails to `LOAD` in real BR — confirming (see `essentials.md`) that spelling
  was never valid syntax at all, in Lexi or base BR.

**Practical consequence for this kit's own compile-check loop:** `"$BR_EXE" "LOAD program.brs
source"` (this file's own compile-check command, and what `brls -check` approximates) assumes
**plain BR text**. Handed a Lexi-flavored `.brs` directly, both will report false syntax errors on
every real Lexi construct present (see `essentials.md`). **Don't read that as a real bug in the
source.** `dev/tools/lexi-compile.ps1` (above) is the verified way to get a Lexi-authored file's
*syntax* translated to plain BR headlessly, and can also finish the job into a compiled `.br` in
the same step via `-Compile` — see "The Lexi-aware development loop" below for how this fits into
actually editing and checking code.

### The Lexi-aware development loop

For a file confirmed to use Lexi (`../app/conventions.md`, once onboarded, says so), adapt
`APP-DEV-GUIDE.md` §6.1's coding loop like this instead of running `brls -check` on the
Lexi-flavored source directly:

1. Edit the `.brs` file (Lexi syntax is fine — that's what it's written for).
2. Translate it: `dev\tools\lexi-compile.ps1 -Source <file.brs> -OutFile <tmp-translated.brs>`.
   A translation failure here (the script throws) means Lexi itself rejected something — e.g. a
   `#Select#` with no matching `#End Select#` — fix that before going further.
3. Run `brls -check` (and `-sema`) against the **translated** file, not the original — this is
   now plain BR, so `brls`'s diagnostics are meaningful again. Fix findings in the *original*
   `.brs`, then repeat from step 2 (translation is cheap; don't hand-edit the translated temp
   file, it'll just be regenerated).
4. Once clean, either let `-Compile` finish the job (`lexi-compile.ps1 -Source <file.brs>
   -Compile`), or save the file in VS Code with the "BR Language Server" extension installed — both
   run the identical underlying Lexi engine (confirmed byte-identical, see above), so either is a
   legitimate way to produce the final `.br`.
5. Close with real BR's own gate regardless: `LOAD <the-compiled-or-translated-file> source` (or
   just trust step 4's `-Compile`, which already does this) — same discipline as any other BR
   program, per `APP-DEV-GUIDE.md` §7.

---

## Deploy notes

- Deploy = copy compiled `.br` and `.brs` into the app tree; no further build required.
- ScreenIO event-code changes require recompiling the **screen**, not just the program.

