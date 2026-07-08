---
title: Installation & tooling
file: spec.md
source: §External Editors (incl. Lexi), §Configuration (EDITOR); br_tree tool pages folded in & pruned (2b) — MyEdit / ODBC / Profiler_File_Layout retained for deep detail
category: 00-configuration
subcategory: 00-configuration/installation-tooling
kind: spec
status: 2b           # reference base + br_tree enrichment
recovered-fold: AutoIt, BRListenerInstaller.exe, BRSerial.dat (3 redirect-collision pages folded from re-fetched source — AutoIt automation note + EditNN/R99C999, installer service-register, brserial.dat license/UserID$/version-rename; verbatim retained on the BR wiki)
related: [config-directives, platform]
keywords: [ODBC, PDF, Lexi, DLL, PEM, AutoIt]
---

# Installation & tooling

External tools around BR: source editors, the Lexi preprocessor, installers, runtimes, DLLs and
diagnostic utilities used to deploy and support it. **Setup, not coding.** Most pieces ship from
`ftp.brulescorp.com` (`/Dll_Distr/…`).

<a id="editors"></a>
## External editors

Edit programs as **source** (`.brs`/`.wbs`, via `SAVE … SOURCE` / `LOAD … SOURCE`) in a real
editor. Configure one in `BRConfig.sys` with the
[`EDITOR`](../config-directives/spec.md#behavior) directive:
```
EDITOR "C:\Program Files (x86)\Mills Enterprise\MyEditBR\MyEditBR.exe"
EDITOR "/usr/bin/vim"
```
The **`EDIT`** command lists the program to a source file, opens the editor, and merges changes back
on close.

- **MyEditBR** (MyEdit – BR Edition) — the BR-specific editor (4.18+): syntax highlighting, code
  completion, refactoring of variables/labels/named-forms, line renumbering, and a visual debugger
  with watches and breakpoints. **Free** vs **Supported** licensed builds (one program; a support
  license unlocks features such as direct `.BR`/`.WB` editing+compile, conditional breakpoints,
  unlimited open files). `/forceportable` on the `EDITOR` line runs it from a USB install. Settings
  live in `MyEditBR.*` files (`.actbindings`, `.broptions`, `.desktop`, …) — copy these to migrate
  setups. Deep detail in [MyEdit_(BR_Edition)](MyEdit_(BR_Edition).md).
- **Notepad++** — generic editor; usable for BR via a **User-Defined Language** file and a *run
  command* that searches the BR Wiki for the word at the cursor
  (`http://brwiki.ads.net/index.php?title=Special:Search&search=$(CURRENT_WORD)`). Also hosts Lexi.

<a id="lexi"></a>
## Lexi preprocessor

**Lexi** lets you edit `.BRS` source **without line numbers**, managing numbering automatically on
compile, and adds preprocessor directives:
- **`#AutoNumber# <start>,<incr>`** — controls regenerated line numbers per program section (must be
  ascending, with room for the lines between directives).
- **`#Define# [[name]] = text`** — text-substitution constants expanded at preprocess time.
- **SELECT CASE** — preprocessor switch construct.

Before stripping numbers Lexi runs **`RENUM LABELS_ONLY`** so hard-coded `GOTO`/`GOSUB` line targets
become `L#####` labels (safe to edit number-free; re-added numbers reuse them as hints). It runs the
compile under `PROC NOECHO` for speed (press **F2** to see a compile-error line), and **you must save
the source before invoking a Lexi tool** or it operates on the stale on-disk copy.

Install (into MyEditBR): download Lexi from SageAX, unzip to **`C:\Lexi`** (the path is required for
auto-install), copy your `brserial.dat` there, then in MyEditBR use *Tools → Configure User Tools →
Import Tools* and select `Lexi.mut` (it adds Compile/Extract-Source/Add-or-Strip-Line-Numbers/Run/
Debug tools — `DebugBR` needs a matching `brnative.exe`). Lexi also integrates with Notepad++ and
Sublime, and supports [ScreenIO](../../50-libraries/screenio/spec.md) development. Full tool tables
and directive examples: [Lexi](Lexi.md).

<a id="catalog"></a>
## Tool & DLL catalog

| Tool / file | Kind | Purpose / key usage |
|---|---|---|
| **INNO Setup** | installer builder | jrsoftware.org; advanced steps via embedded Pascal scripts |
| **NSIS** | installer builder | Nullsoft Scriptable Install System |
| `BRODBC32.dll` | DLL | required for [ODBC](#odbc) access; use the latest from the FTP site |
| `PDFLIB.DLL` | DLL | required to create [PDFs](#pdf) (32-bit only — see below) |
| `pemnet.dll`, `brconvert.dll`, `vcdlltest.exe` | DLL/util | [.NET / PEM controls](#dotnet) support (BR directory) |
| `Dotnetfx20.exe`/`Dotnetfx35.exe`, `vcredist_x86.exe` | runtime installers | install/upgrade .NET (Win2000 / WinXP+) and VC++ libs for PEM |
| **Profiler** | diagnostic | line/timing profiler (see [#diagnostics](#diagnostics)) |
| `Printlocks.exe` | diagnostic | dumps the lock area; requires a filename as 1st parameter |
| **REGCLEAN** | diagnostic | fixes BR SDK / SQL Mod DCOM registration (see [#diagnostics](#diagnostics)) |
| `CheckSerial.exe` | license util | reads the licence info in a `brserial.dat` (BRC utility) |
| `brserial.dat` | license file | holds the BR licence (`UserID$` returns the licensee); inspect with `CheckSerial.exe`; may be named `BRSerial.<version>` (e.g. `BRSerial.43`) |
| `BRListenerInstaller.exe` | installer | registers `BRListener.exe` as a Windows service (admin; `.exe` in `System32`, `BRListener.conf` in `C:\Windows`; `/Release` to remove) — see [client-server](../client-server/spec.md#service-install) |
| **AutoIt** | automation tool | free Windows keyboard/GUI-automation scripting language — drive BR screens, read spreadsheets, enter data (see [#automation](#automation)) |
| `Color.exe` | util | colour utility (Western Canadian Software) |
| **cURL** | external util | fetch URLs from BR via a `sy` shell call (see [#diagnostics](#diagnostics)) |

<a id="odbc"></a>
## ODBC (database connectivity)

Needs the latest `BRODBC32.dll`. Setup distinguishes **virtual** paths (BR logical, e.g. *Data
Path* — what `CD` reports inside BR) from **actual** OS paths (BR location, the BRConfig.sys file).
DSNs can be generated from the Context with the `CREATE_INI.BR` program; client install can run from
a command line (no interaction). For query diagnostics set
[`LOGGING`](../config-directives/spec.md#behavior) to level 6 (`LOGGING 6, C:\ODBC-LOG.TXT`); the
`@ODBC LOGGING` form overrides BR's level for ODBC only (levels 6/8/10/13 give increasing detail).
Licensing is per ODBC workstation or per BR WSID (WSID-based is half price; brserial.dat then
reports 999 users); an **"ODBC registration problem"** message almost always means too few licences
— contact BRC to upgrade `brserial.dat`. Full config-field meanings, the licence-enforcement scheme,
and the MS-Access middleware technique are in [ODBC](ODBC.md).

<a id="pdf"></a>
## PDF

`PDFLIB.DLL` is required for PDF creation (used by the [printing](../../40-io-printing/pcl-pdf/spec.md)
side). **There is no 64-bit PDFLib** (`Pdflib4-x64.dll` does not exist) — BR's PDF capability is
**32-bit only**.

<a id="dotnet"></a>
## .NET / PEM controls

Properties-Events-Methods (PEM) and .NET controls need two DLL groups: the **VC++ shared libraries**
(test with `vcdlltest.exe`, install with `vcredist_x86.exe`) and the **.NET framework**
(`dotnetfx20.exe` on Win2000, `dotnetfx35.exe` on WinXP/Vista). BR ships `pemnet.dll`, `brconvert.dll`
and `vcdlltest.exe` in its directory.

<a id="diagnostics"></a>
## Diagnostics & utilities

- **Profiler** (Luis Gomez / Vertican; `/Dll_Distr/profiler` on the FTP site). Capture with
  `DEBUG PROFILE SAMPLED <file>` / `DEBUG PROFILE TIMED <file>` / `DEBUG PROFILE STOP`
  (see [70-commands/information](../../70-commands/information/spec.md)), then render the log with
  `profiler.exe <file> [raw]`. The binary output format (network byte order; record types for
  module mapping, current line, time-in-line, backtrace, function name, GOSUB, …) is in
  [Profiler_File_Layout](Profiler_File_Layout.md).
- **REGCLEAN** (`regclean.exe`) — repairs BR SDK DCOM (311) errors, e.g. an unregistered SQL Mod.
  `regclean -q all` lists registered projects + paths; `regclean -d <project|all>` removes entries;
  re-register by running the project exe (`dcomkey`, `sql`). The `fix.cmd` batch
  (`regclean -d all` / `dcomkey` / `sql` / `regclean -q all`) automates the full reset.
- **Printlocks.exe** — dumps the lock area; pass a filename as the first parameter.
- **CheckSerial.exe** — inspects the licence in a `brserial.dat`; a `CheckSerial.cmd` wrapper lets you
  open a `.dat` by double-click.
- **cURL** — called from BR via a shell-out, e.g.
  `EXECUTE 'sy -M curl <url> -A "Mozilla/4.0" -o page.html -s'`, then read the saved file — a simple
  web-fetch/scrape pattern (related to [60-integration/web](../../60-integration/web/spec.md)).

<a id="automation"></a>
## Automation (AutoIt)
**AutoIt** is a free Windows scripting language for GUI automation (keystrokes, clicks, COM, even its own
GUIs) — useful for automated testing or unattended data entry against BR screens, and for reading
spreadsheets or writing display files. BR cooperates with it: a `R99C999` row/column tag appears in the
text of BR labels (4.3+), and individual BR input fields are addressable in AutoIt as **`EditNN`**, where
`NN` is the field's `INPUT FIELDS` subscript ([`CURFLD`](../../20-io-screen/windows-cursor/spec.md#keyboard-results)).
Its bundled Window Info utility shows what AutoIt "sees" on screen.

<a id="see-also"></a>
## See also

- [config-directives](../config-directives/spec.md#behavior) — the `EDITOR` and `LOGGING` directives
- [platform](../platform/spec.md) — per-OS executables & runtimes
- [40-io-printing/pcl-pdf](../../40-io-printing/pcl-pdf/spec.md) — where `PDFLIB.DLL` is used
- [50-libraries/screenio](../../50-libraries/screenio/spec.md) — Lexi also supports ScreenIO development
- Backing keyword pages (deep detail retained): [MyEdit_(BR_Edition)](MyEdit_(BR_Edition).md),
  [ODBC](ODBC.md), [Profiler_File_Layout](Profiler_File_Layout.md), [Lexi](Lexi.md) (preprocessor
  tool tables + directive examples — relocated here from 50-libraries/screenio)

*(3 redirect-collision pages re-fetched in 2b — `AutoIt`, `BRListenerInstaller.exe`, `BRSerial.dat` —
were folded into this spec and pruned; verbatim wikitext remains on the BR wiki.)*
