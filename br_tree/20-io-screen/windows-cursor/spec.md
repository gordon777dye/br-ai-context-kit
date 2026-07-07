---
title: Windows & cursor
file: spec.md
source: §Screen Operations → Window Operations, Navigation
category: 20-io-screen
subcategory: 20-io-screen/windows-cursor
kind: spec
status: 2b           # reference base + br_tree enrichment (CMDKEY/FKEY/CURFLD, cursor shape, GUIMODE, borders); no conflicts
recovered-fold: CURFLD, CURWINDOW, EROW, FNKEY, GUI_Console, GUI_Mode, Parent=None folded+pruned; FKEY retained (scancode tables). 8 redirect-collision pages re-fetched; verbatim retained on the BR wiki
related: [input-output, fields-attributes, controls]
canonical: window-open   # canonical home for the window OPEN spec (printing guide links here)
---

# Windows & cursor

Opening bordered windows (mini-screens) as DISPLAY channels, drawing borders, and locating the
cursor. FIELDS I/O *inside* a window uses `PRINT #w, FIELDS …` — see
[input-output](../input-output/spec.md). **This is the canonical home for the window OPEN spec**;
the printing guide links here rather than redefining it.

<a id="open-window"></a>
## Syntax — OPEN window

```bnf
<border-spec> ::= { 'B' | 'D' | 'S' | <corners> } [ <display-attr> ]   -- B=blank D=double S=single
<window-open-string> ::=
  '"' '{ROWS|SROW}=' <int> ',' '{COLS|SCOL}=' <int> ','
      '{ROWS|EROW}=' <int> ',' '{COLS|ECOL}=' <int>
      [ ',' 'ABSOLUTE' | ',' 'RELATIVE' ]
      [ ',' 'CAPTION=' ['<'|'>'] <title> ]
      [ ',' 'BORDER=' <border-spec> ]
      [ ',' 'N=' <display-attr> ] [ ',' 'FKEY=' <int> ]
      [ ',' 'FONT[.TEXT|.LABELS|.BUTTONS]=' <font> ] [ ',' 'FONTSIZE=' <int>'x'<int> ] '"'
    | <string-expression>

OPEN '#'<channel> ':' <window-open-string> ',' 'DISPLAY' ',' 'OUTIN'

PRINT '#'<window> ',' BORDER [<border-spec>] [ ':' <caption> ]
```

<a id="semantics"></a>
## Semantics

- A window is opened on a user channel as `DISPLAY, OUTIN`; `SROW/SCOL`/`EROW/ECOL` give the
  corners. **#0** is always the main console (GUI console if GUI mode is on, else character-mode).
- **Border types**: `S` single, `D` double, `B` blank, `NONE`; or supply two custom corner
  characters (BR derives the rest). `PRINT BORDER` (re)draws the border / sets a caption.
- **Positioning**: `RELATIVE` (default) — coordinates from the parent window `#0`'s top-left
  (negatives allowed, placing the window above/left of the parent); `ABSOLUTE` — from the
  screen's top-left. When a `BORDER` is specified, `EROW`/`ECOL` must be **one short** of the desired
  edge to leave room for the one-cell border, and the end values may not precede the start values.
- **Hot windows**: `FKEY=<n>` in an OPEN WINDOW string (4.2+) makes the *whole window* hot — clicking
  anywhere in it fires that FKEY interrupt (typically to switch focus). The value is inherited by child
  windows (but **not** independent ones) unless a child sets its own `FKEY=` (or `-1`).
- **Cursor**: `CURROW`/`CURCOL` give the current row/column (within a 2-D control when one is
  active); `CURPOS` positions the cursor. The **`CURSOR SSEE`** config (BRConfig.sys / `CONFIG` /
  `EXECUTE`) sets the block-cursor *shape* — `SS`/`EE` are hex start/end scan lines `00`–`0D`
  (e.g. `CONFIG CURSOR 080D` = lower-half block). **GUI mode**: `ENV$("GUIMODE")` returns `ON`/`OFF`.

<a id="keyboard-results"></a>
### Keyboard-result functions
After an `INPUT`/`RINPUT`/`INPUT FIELDS`/`INPUT SELECT`, these report how and where input ended:

- **`CMDKEY`** — the command/function key that terminated input (`0` = Enter or any non-command key;
  `-1` before first input; `90`/`91` = PgUp/PgDn). Assignable: `LET CMDKEY(x)` presets it (handy with
  `KSTAT$` / unattended runs).
- **`FKEY`** — the newer, more capable equivalent of `CMDKEY` (preferred in new code): it reports *how*
  a field was exited and is set by clickable controls, buttons and hot windows. `LET FKEY(x)` sets both
  `FKEY` and `CMDKEY` (but if `x>91`, `CMDKEY` becomes 0); `LET CMDKEY(x)` sets both to `x`. A **HotKey**
  is just an assigned FKEY value — attach one to a control (via `PRINT FIELDS`/`INPUT FIELDS`) to make it
  clickable, or to a whole window to make it *hot* (see below). FKEY values **>100 do not terminate
  `INPUT FIELDS`** but can be read afterward; **`OPTION 48`** makes Enter leave `FKEY=0` rather than
  firing a field's FKEY. (As of **4.20** the old name **`FNKEY` is just `FKEY`**.) The full
  scancode↔FKEY/CMDKEY tables (per key; per GRID/LIST/TextBox attribute set; KSTAT-only codes) are the
  retained references — [FKEY](FKEY.md) and [CMDKEY](CMDKEY.md).
- **`CURFLD`** — the 1-based field/control the cursor was on after the last `INPUT FIELDS` (pre-4.2 also
  `RINPUT FIELDS`/`INPUT SELECT`/`RINPUT SELECT`; **4.2+ limited to `INPUT FIELDS`**); `RUN` initializes
  it to `-1`. It pairs with `FKEY` to know *what* was chosen and *which key* chose it, and serves as the
  "mark" in `HELP$` for field-specific help. **With parameters** it also *sets* the next input's
  starting field and attributes:
  - `CURFLD(nn)` — returns the current item's subscript within the 2D control (LIST/GRID) at field `nn`.
  - `CURFLD(field [,attr$] [,fkey])` — set the starting field (= the `C` control attribute), optionally
    add field attributes (`AEP`/`#` etc., *added* to the field's own and overriding a floating `ATTR`),
    and optionally replay an `fkey` keystroke before input. CURFLD **ignores fkey ≤100 or ≥114**; the
    added attributes apply only to the *next* `INPUT FIELDS`/`INPUT SELECT`.
  - `CURFLD(field, row|cell)` — for a 2D control, position into a LIST **row** / GRID **cell** / TOOLBAR
    icon on entry (a mouse click into the control overrides it).
  - **The BRC-standard validate-and-replay idiom**: after `AE` field-exit interrupts, verify the data
    then `IF FKEY>100 THEN LET CURFLD(CURFLD,FKEY) : GOTO <input>` re-enacts the operator's exit key.
    (Comboboxes with the `x` attribute return FKEY **209**; loop with `LET CURFLD(CURFLD,FKEY)` to stop
    blinking.) `CURROW`/`CURCOL` give the ending row/column; **`OPTION 43`** restores old INPUT SELECT
    `NXTFLD`/CURFLD behavior.
- **`CURWINDOW(<n>)`** — returns the window currently in focus **when it was opened `PARENT=NONE`** (`-1`
  if no PARENT=NONE window is active); passing `<n>` raises/focuses that window. Used with PARENT=NONE
  windows and FKEY 93.

<a id="borders"></a>
### Borders & captions
`BORDER=` (in OPEN WINDOW) / `PRINT [#w,] BORDER` take `S` (single/sunken), `D` (double), `B`
(blank), or two custom **corner** characters, optionally followed by display `<attributes>`. As of
4.2, `D`/`H`/8-char specs require **`OPTION 62`** (`BORDER=S|D|B|H|8-chars[:attributes]`). `PRINT
BORDER` accepts the `S` (drop-shadow) attribute only if the window was opened with `S` (else error
0868). `CAPTION=` sets the top-border title; lead with `<` (flush left) or `>` (flush right), else
centered. The `GRAPHIC_LINEDRAW {ON|RAISED|SUNKEN|OFF}` BRConfig.sys directive controls border
*rendering* (with `CONFIG GUI OFF`, RAISED/SUNKEN need `DRAWLINE.BMP`/`DRAWSUNK.BMP` in the
executable folder to avoid dotted lines). Extra modes **`THIN`** (BR's default sunken thin line) and
**`THINRAISED`** (Windows thin line) need no bitmaps; `RAISED`(=`ON`, the default)/`SUNKEN` do. The
change takes effect on the next OPEN of window #0. You can draw lines directly by typing linedraw
characters (numeric-keypad `0`–`9` in **linedraw mode**, toggled with **`Ctrl-\`**); `GRAPHIC_LINEDRAW
OFF` makes such source readable while editing.

<a id="gui-console"></a>
### GUI vs non-GUI console
The console runs in **GUI** mode (`CONFIG GUI ON`, the modern Windows-object console) or **non-GUI**
("old console") mode (`CONFIG GUI OFF`), and a program may switch between them at runtime — every switch
**closes all windows and reopens the main console** (do `PRINT NEWPAGE` after toggling).
`ENV$("GUIMODE")` returns `ON`/`OFF`.

| behavior | `GUI OFF` (old console) | `GUI ON` (new console) |
|---|---|---|
| window bleed-through | allowed | **none** — an overlapping field deletes the field it overlaps |
| `PRINT` to screen/window | allowed, scrolls | not allowed — must reference a `FIELD` |
| `LINPUT` | allowed | not allowed |
| fonts | fixed only | fixed **and** proportional (`STATUS FONTS` lists both) |

In GUI mode `PRINT` with no window number goes to the command console only, while `PRINT FIELDS` with no
window number goes to **window #0**. The new console extends graphical controls (buttons, text fields)
by **3 px on each side**, so leave one blank between controls to avoid overlap; a proportional label that
outgrows its fixed-width slot extends the control, and a later label on that area lands *under* the
extension. While the new console is up the command console hides — **Ctrl-A** interrupts and brings it
back. Related: **`CONFIG CONSOLE {ON|OFF|OFF ALWAYS}`** controls whether the BR console stays visible
behind VB/Delphi `Project=` forms (`OFF ALWAYS` pops a "now processing" box if no form appears for 3 s),
and **`CONFIG GUI SUPPRESS {ON|OFF}`** makes BR ignore `Project=` keywords in OPEN strings (independent
of `GUI ON|OFF`).

<a id="parent-none"></a>
### Independent & modal windows (PARENT=NONE)
`OPEN #ch: "…,PARENT=NONE,…", DISPLAY, …` creates an **independent** top-level window rather than a child
clipped to window #0 — **Windows and Client-Server only**, and **GUI mode must be ON** (`PARENT=NONE`
under `GUI OFF` raises **error 0877**). The new window inherits any unspecified attributes from the main
console but is **not** itself a main console; after a GUI mode switch (which closes all windows) output to
a stale PARENT=NONE window without reopening it raises **error 0704** (file not open).
- **Positioning** uses the same `RELATIVE` (default, from window #0 — negatives allowed) / `ABSOLUTE`
  (screen) keywords; under `ABSOLUTE`, `SROW`/`SCOL` are measured in character cells of the window's
  `FONTSIZE`.
- **`NAME=<window-name>`** persists the window's size/position (and font size) at close and restores it
  on the next open — **even across sessions** — after which `ROW=`/`COL=` are ignored in favor of the
  stored values. (Window #0's geometry is likewise remembered in the registry.)
- **`MODAL`** blocks interaction with window #0 until the window closes (and shows no taskbar icon);
  **`NO_TASK_BAR`** just suppresses the taskbar icon. `CURWINDOW` reports/raises the focused PARENT=NONE
  window; `DISPLAY #window,MENU` finds the corresponding top window automatically.

<a id="help-facility"></a>
## Help facility

Context-sensitive help from READY mode (F1/Ctrl-Y) and during programs (Ctrl-Y = `<HELP>`).
Help text lives in compiled `.wbh` files (built with `wbhelp`); a config `HELPDFLT <topic>[,<file>]`
sets the default.
```bnf
HELP$([*]<keyword>[,<filename>][,<mark>])     -- enter HELP mode / show a topic; returns a scancode or selection
ON HELP {GOTO <line-ref> | SYSTEM | IGNORE}    -- SYSTEM=HELPDFLT (default), IGNORE disables the key
```
- The **`HELP` error condition** on `INPUT`/`RINPUT FIELDS … HELP <line-ref>` traps the Help key
  for field-level help (often using `CURFLD` for context); see
  [controls](../controls/spec.md#help) and [error-handling](../../10-language/flow-control/error-handling/spec.md).
- Help-text file topics use `:topic menu-desc` / `::related-topic` / body / `:topic`; display
  attributes via `|U…|`; topics can return a scancode or a `*program` menu selection.
```business-rules
00400 INPUT FIELDS MAT FLD$: HRS, OT, DT HELP 900
00900 LET X$ = HELP$("HOURS.ENTRY", CURFLD): RETRY
```

<a id="examples"></a>
## Examples

```business-rules
00110 OPEN #1: "SROW=5,SCOL=10,EROW=15,ECOL=60,BORDER=S,CAPTION=Data Entry", DISPLAY, OUTIN
00120 PRINT #1: NEWPAGE
00130 INPUT #1, FIELDS "2,5,C 20": NAME$
00140 CLOSE #1:

! Scrollable text box inside a window
00110 OPEN #10: "SROW=10,SCOL=10,ROWS=5,COLS=40", DISPLAY, OUTIN
00130 RINPUT #10, FIELDS "1,1,100/C 2000,N/W:W": TEXT$
```

<a id="see-also"></a>
## See also

- [input-output](../input-output/spec.md) — FIELDS I/O directed at a window channel
- [controls](../controls/spec.md) — controls placed inside windows
- [fields-attributes](../fields-attributes/spec.md) — border/caption display attributes
- Printer/display OPEN of non-window channels → [30-io-file/statements](../../30-io-file/statements/spec.md#open)
- Backing keyword pages (deep detail retained): [OPEN_WINDOW](OPEN_WINDOW.md) (all open params),
  [Help_Facility](Help_Facility.md) (full help-system reference), [CMDKEY](CMDKEY.md) and
  [FKEY](FKEY.md) (full key-code / scancode tables — `FKEY` re-fetched and retained in 2b).
  Other pages folded into this spec and pruned. The 2b
  redirect-collision pages `CurFld`, `CurWindow`, `EROW`, `FNKEY`, `GUI_Console`, `GUI_Mode` and
  `Parent=None` were folded here and pruned; verbatim wikitext remains on the BR wiki.
