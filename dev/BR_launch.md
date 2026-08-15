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
$env:BR_EXE     = "context\dev\tools\brserver-433a-Win32-Debug-2026-08-12.exe"
$env:BR_CONFIG  = "context\dev\tools\brconfig.sys"
$env:BR_AI_UTIL = "context\dev\tools\brconfig.ai_util"
$env:BR_AI_USER = "context\dev\tools\brconfig.ai_user"
$env:BRLS_EXE   = "context\dev\tools\brls.exe"
```

```bash
export BR_EXE="context/dev/tools/brserver-433a-Win32-Debug-2026-08-12.exe"
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

## Deploy notes

- Deploy = copy compiled `.br` and `.brs` into the app tree; no further build required.
- ScreenIO event-code changes require recompiling the **screen**, not just the program.

