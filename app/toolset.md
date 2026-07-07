# Toolset — QSMRP

> **Sample.** This is a filled-in example for the QSMRP application, written to the STEP 2 spec in
> [`INSTRUCTIONS.md`](INSTRUCTIONS.md). Adapt every value to your app; the **BR launch environment**
> and **canonical invocations** sections are required, the rest are as-needed.

---

## BR launch environment

AI models need to know how to invoke Business Rules for compilation and testing. Here is where you tell it how it can do that from a terminal command line (e.g. cmd.exe or PowerShell). 

**If your standard brconfig.sys includes an EXECUTE statement (recommended) then you will need to create another config file for simple AI access.** Note- you can use a standard set of configuration statements in a config file that you INCLUDE into each config variant.

| Fact | Value | Nature |
|---|---|---|
| **BR executable** | `$BR_EXE` — default `C:\BRnative\brnative.exe` | Server-specific - your existing BR pathname
| **`brconfig.sys`** | `$BR_CONFIG` — default `C:\ads\qsmrp\brconfig.sys` | App startup |
| **`brconfig.sys`** | `$BR_CONFIG` — default `C:\ads\qsmrp\br_test.sys` | AI utility |
| **BR version/flavor** | BR **native** 4.3x (Windows) | Config directives & behavior differ across versions |

Set the machine-specific path once per box (PowerShell):

```powershell
$env:BR_EXE = "C:\ADS\sys\br.d\br432g-32.exe"
$env:BR_CONFIG = "C:\ads\sys\br.d\brconfig.sys"
$env:BR_TEST = "C:\ads\sys\br.d\br_test.sys"
```

## AI Canonical invocations

Copy these verbatim (the STEP 1 compile check uses the same form).

```
"$BR_EXE" -"$BR_CONFIG"                          # start BR into the app (interactive)
"$BR_EXE" "RUN cnp\menu" -"$BR_TEST"           # run a statement/command at startup
```

- **`-<config-file>`** names an alternate config file — a dash **immediately followed** by the
  path/filename (e.g. `-"$BR_CONFIG"`), no space. With none given, BR looks for `brconfig.sys`, then
  `wbconfig.sys`.
- The **first quoted argument** is a BR statement/command to run the instant BR starts (e.g.
  `"RUN cnp\menu"`, `"PROC start"`); a workstation id is `-<wsid>`, a login is `@<name>`. Note that your default startup command is best placed in the configuration file using an EXECUTE configuration statement.
- Syntax reference: [br_tree — Startup command line](../br_tree/00-configuration/platform/spec.md).
- Startup sequence baked into config: `cnp\startup.br` runs after login; `cnp\initfile.br` creates DB
  files on a fresh install. Main menu entry point is `cnp\menu.bro`.

---

## Development commands

### Compile / syntax-check
Sources auto-compile `.br.brs` → `.br` on modification. To force a compile-check of one source
(the STEP 1 feedback loop):

```
"$BR_EXE" "LOAD program.brs source" -"$BR_CONFIG"   # parses; reports first error + line
```

The **`source`** keyword is required to load a `.brs` as source — `LOAD` defaults to object mode and
will not infer source from the extension ([LOAD](../br_tree/70-commands/program-management/spec.md#loading)).

### Run a program from the console
```
"$BR_EXE" -"$BR_CONFIG"
> RUN "cop\xlate850"                           # or: EXECUTE "program_name" from code
```

### EDI (in `cop\`)
```
> RUN "cop\xlate850"     # translate inbound 850
> RUN "cop\load850"      # load translated 850
> RUN "cop\send856"      # transmit 856
```
X12 sets in use: 810, 820, 830, 850, 856, 860, 862, 997.

### File / DB maintenance
```
> RUN "cnp\reorg<file>"  # reorganize a data file (cnp\reorg*.br)
> RUN "cnp\histpurg"     # purge history
> RUN "cnp\initfile"     # (re)create DB files from filelay\ — new installs only
```

### Reindex
Rebuild indexes after bulk operations. `invent` and `oed\orderl` are large — expect ~10–20 s per 10k
records.

---

## Utilities & entry points

| Task | Program |
|---|---|
| Main menu / dispatch | `cnp\menu.bro` |
| Post-login startup | `cnp\startup.br` |
| Create DB files | `cnp\initfile.br` |
| Conversions (upgrades) | `cvt\*` |

## Deploy notes

- Deploy = copy compiled `.br` (+ any changed `.brs`) into the app tree; no build server.
- ScreenIO event-code changes require recompiling the **screen**, not just the program.
- Security/permissions live in `cnd\security`; menu & program access is permission-gated.

---

## Prerequisites recap

- **Node.js** (v14+) — only to (re)generate `app\data-model.*` via `dev\tools\extract-schema.js`.
- **BR runtime** — the values above; used to run the app and compile-check generated code.

Both are build/run-time tools, not part of the delivered `context\`.
