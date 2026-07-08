---
title: File & directory commands
file: spec.md
source: §Commands → File System / File Management Commands
category: 70-commands
subcategory: 70-commands/file-directory
kind: spec
status: 2b           # reference base + br_tree fold (full -options, TYPE/PROTECT, CHDIR nav, client-server @:, abbreviations); no conflicts
recovered-fold: MkDir, RENAME (2 redirect-collision pages folded from re-fetched source — RENAME full -NPVF options + PRINT/redirect, MKDIR naming rules; verbatim retained on the BR wiki)
related: [program-management, information]
keywords: [DIR, COPY, RENAME, MKDIR, RMDIR, CHDIR, FREE, PROTECT, DROP]
---

# File & directory commands

OS-level file and directory operations, runnable interactively or from a procedure / `EXECUTE`.
For opening files inside a program see
[30-io-file/statements](../../30-io-file/statements/spec.md). Each command has a short abbreviation
(in parentheses below). Options follow a leading dash and may be combined (`-AW`); a `-<n>` record
length, when combined, must come **last**.

<a id="syntax"></a>
## Syntax

```bnf
CHDIR [<drive>':'] ['\']<path> [-N]     -- CD / CH; no arg = show current dir
MKDIR [<drive>':']<path>                -- MK
RMDIR [<drive>':']<path>                -- RM; directory must be empty
DIR  [<drive>':'][<path>][<filename>] [-AOLPWUCB] [PRINT | '>'['>'] <file>]   -- DI
COPY   <from> { <to> | PRN: | AUX: } [-ACDNPSV] [-<new_recl>] [PRINT | '>'['>'] <file>]  -- COP
RENAME <from> <to> [-NPVF] [PRINT | '>'['>'] <file>]   -- REN; renames or moves (wildcards ok)
TYPE   <file> [PRINT | '>'['>'] <file>] -- TY; dump a file to screen/printer/file
DROP <file-ref> [-ANPV] [PRINT | '>'['>'] <file>]   -- DR; empties contents, keeps the name (size→0)
FREE <file-ref> [-ANPV] [PRINT | '>'['>'] <file>]   -- FR; deletes the file (unrecoverable)
PROTECT <file-ref> ',' { RESERVE | RELEASE }        -- PROT; reserve a path to one workstation
```

<a id="semantics"></a>
## Semantics

<a id="chdir"></a>**CHDIR / MKDIR / RMDIR** navigate/create/remove directories.
`CHDIR` with no path just *shows* the current directory. A leading `\` means an absolute path from
the root; without it the path is appended to the current directory. `drive:` **alone** changes the
current drive; `drive:\path` changes the current directory *on* that drive without switching to it.
Relative forms work: `\` → root, `..` → parent, `..\..` → grandparent. `-N` suppresses the
"new directory" echo (useful under `PROC NOECHO`). An invalid path raises error **4152**.

<a id="dir"></a>**DIR** lists files (wildcards `*`/`?`), with file size, date and time. Options:
`-A` archive-bit files only (DOS; ignored on Linux), `-O` sort alphabetically, `-P` pause per
screen, `-W` wide four-column (sorted, long names; like `-C` but across not down), `-U` unadorned
(no extended names), `-C` columnar sorted with a trailing `/` on directories and `*` on
executables, `-L` long names + permissions (Linux), `-B` bare long name. `>file` redirects (`>>`
appends), `PRINT` to the printer (mutually exclusive with `>`).

<a id="copy"></a>**COPY** duplicates one or more files (same/different disk, or rename-in-place with
a new name), and can copy to a device. Options: `-A` archive-bit only then clears it (DOS), `-C`
prompt on full disk, `-D` omit deleted records (internal files — **rebuild indexes after**), `-N`
no action log, `-P` pause per screen, `-S` copy an **open** file (must be opened `SHR`/`SHRI` else
error **4148**), `-V` verify each action, `-<n>` set the new internal-file record length
(space-padded; must be the last option). Device targets `PRN:`/`AUX:`/`COM1:`/`LPT1:`… send to a
printer (on Linux these need a `SUBSTITUTE` mapping in [BRConfig.sys](../../00-configuration/config-directives/spec.md));
copying *to* `PRN:`/`WIN:` is illegal — use `TYPE` with redirection. As of 4.2 a print file copies
unaltered to a `DIRECT:` device. **Destination wildcards truncate**: `COPY src\* dest\*` strips the
extension, `dest\*.*` keeps one dot, `dest\*.*.*` keeps two — prefer a bare `dest`.
*Client/server:* `@:` denotes the client (`COPY file @:file` sends to the client's current
directory; `@:file file` pulls from it; `@::` for client absolute paths).

<a id="rename"></a>**RENAME** renames or moves one or more files (wildcards ok — `RENAME C:*.*
C:\DIR\*.*` moves a whole group keeping each original name). Options: `-N` (no action log), `-P`
(pause per screen), `-V` (verify each rename), **`-F`** (force-delete an existing target when needed to
complete the rename); `PRINT` / `>` / `>>` redirect the log. **TYPE** sends a file's contents to the
screen, a printer, or another file. **MKDIR** subdirectory names follow file-name rules, and the same
name may exist under different parent directories.

<a id="drop-free"></a>**DROP** empties a file's contents — freeing all allocated space and leaving
only the header record for internal files — but keeps the name (size→0). **FREE** deletes the
file(s) outright (unrecoverable). Both take `-A`/`-N`/`-P`/`-V` and accept wildcards (use `-V` to
verify). A procedure can `FREE` itself as its last line; a `.$$$`-named procedure self-deletes
after running. *(The same-named `DROP`/`FREE` **CLOSE parameters** inside a program are a separate
file operation — [30-io-file/statements](../../30-io-file/statements/spec.md#close).)*

<a id="protect"></a>**PROTECT … RESERVE/RELEASE** reserves a full path name for one workstation's
exclusive use (and releases it) — the multi-user purge idiom; see
[30-io-file/file-model](../../30-io-file/file-model/spec.md).

<a id="examples"></a>
## Examples

```text
CHDIR \DATA\REPORTS
DIR *.BR -C
COPY CUST.FIL TEMP[WSID].FIL -D     ! copy omitting deleted records
RENAME TEMP[WSID].FIL CUST.FIL
COPY A:SAMPLE.* B: -DC              ! copy group; drop deleted recs; prompt on full disk
FREE *.BAK -V
TYPE README.TXT PRINT
```

<a id="see-also"></a>
## See also

- [program-management](../program-management/spec.md) — these commands inside procedures / `EXECUTE`
- [30-io-file/statements](../../30-io-file/statements/spec.md) — in-program `OPEN`/`CLOSE … FREE/DROP`
- [30-io-file/file-model](../../30-io-file/file-model/spec.md) — `[WSID]` per-workstation names, `PROTECT`
- Client-side **OPEN/SAVE file browser** (`OPEN #99: "NAME=OPEN|SAVE:dir[mask],…"`) →
  [30-io-file/statements](../../30-io-file/statements/spec.md)

*(Backing keyword pages — `CHDIR`, `COPY`, `Copy_option`, `DIR`, `Dir_option`,
`Directory_Management_Commands`, `Drop`, `Drop_options`, `FREE`, `Free_option`,
`File_Management_Commands`, `File_Browser`, and the misfiled `Delete_(command)` — were folded into
this spec and pruned. The 2b redirect-collision pages `MkDir` and
`Rename` were likewise folded here and pruned; verbatim wikitext remains on the BR wiki.)*
