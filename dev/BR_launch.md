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

## The Lexi preprocessor

Some BR shops write source for **Lexi**, a preprocessor that adds a handful of constructs base BR
doesn't have (`/* ... */` comments, `X$&=` compound append, `#Select#/#Case#`, `#Autonumber#`,
`#Define#`, and line-number-free editing) and rewrites them into plain, correctly line-numbered BR
text before real BR ever compiles it. 

- **Lexi's syntax** (what each construct does): [`essentials.md`](essentials.md#1-core-language-rules).
- **The full reference** — what Lexi is, both known distributions, how the VS Code extension
  invokes it, and every directive in detail:
  [`br_tree` — Lexi](../br_tree/00-configuration/installation-tooling/Lexi.md).
- **How this fits into the actual coding loop**:
  [`APP-DEV-GUIDE.md`](APP-DEV-GUIDE.md#lexi-aware-coding-loop).

### Running `lexi-compile.ps1`

[`dev/tools/lexi-compile.ps1`](tools/lexi-compile.ps1) translates (and optionally compiles) a
Lexi-authored `.brs` file headlessly — no editor or VS Code window involved — running under
`UNATTENDED` logging so a bad input aborts fast instead of hanging the shell.

```powershell
# Translate only (default) — produces <source>.lexiout.brs next to the source
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs

# Translate AND compile to a real .br object
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs -Compile

# Explicit output paths
context\dev\tools\lexi-compile.ps1 -Source path\to\file.brs -OutFile path\to\translated.brs -Compile -OutObject path\to\file.br
```

| Parameter | Default | Meaning |
|---|---|---|
| `-Source` | *(required)* | The `.brs` file to translate. |
| `-OutFile` | `<Source>.lexiout.brs` | Where the translated, plain-BR output goes. |
| `-Compile` | off (switch) | Also compile the translated output to a `.br` object (`LOAD`/`SAVE` or `REPLACE`, whichever applies), via the same bundled runtime. |
| `-OutObject` | `<Source>` with its extension replaced by `.br` | Where the compiled `.br` goes, when `-Compile` is given. |
| `-LexiPath` | auto-detected under `$env:USERPROFILE\.vscode\extensions\crs-dev.vslang-br-*\Lexi` | The Lexi install folder (`lexi.brs`, `lexionly.brs`, `linenum.brs`, `brnative.exe`, `wbconfig.sys`). Pass explicitly if that extension isn't installed, or to compile through a different Lexi install (e.g. this app's own root-level `lexi.brs`, if it has one — confirm byte-identity with the extension's copy before assuming they're the same engine; see `../app/conventions.md`). |
| `-BrExe` | `<LexiPath>\brnative.exe` | The BR executable to run Lexi with. |
| `-WbConfig` | `<LexiPath>\wbconfig.sys` | The config to run Lexi with (Lexi's own — separate from this app's `brconfig.sys`). |
| `-KeepTemp` | off (switch) | Keep the generated proc/config/log temp files afterward — useful for debugging a failure. |
| `-TimeoutSec` | `30` | Kill the BR process if it hasn't exited after this many seconds. A safety net only — unattended mode should abort on its own well before this. |

See `Get-Help -Full dev\tools\lexi-compile.ps1` for the complete parameter help and examples.

---

## Deploy notes

- Deploy = copy compiled `.br` and `.brs` into the app tree; no further build required.
- ScreenIO event-code changes require recompiling the **screen**, not just the program.

