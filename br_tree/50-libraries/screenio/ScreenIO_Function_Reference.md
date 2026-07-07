---
title: ScreenIO Function Reference
file: ScreenIO_Function_Reference.md
source: screenio.brs (shipping library source) — signatures verified against every DEF LIBRARY export
category: 50-libraries
subcategory: 50-libraries/screenio
kind: reference
status: deep-reference          # source-derived; retained alongside spec.md (too detailed to fold)
related: [screenio, library-facility, fnsnap]
---

# ScreenIO Function Reference

The library's **public surface is exactly 16 `DEF LIBRARY` functions** (the rest of `screenio.brs`'s
~425 functions are internal to the engine and the designer). Every signature below is taken verbatim
from the shipping `screenio.brs` source, not the wiki (the ScreenIO wiki page is empty). Parameters
after the `;` are optional; `&` marks pass-by-reference; `Mat` marks array parameters.

All the screen-invocation calls are thin wrappers over one internal engine, `Fnmasterfm$` — so they
share the same parameter set and semantics.

<a id="invocation"></a>
## A. Screen invocation (the everyday surface)

```business-rules
Fnfm$ (Screenname$; Keyval$, Srow, Scol, Parent_Key$, Parent_Window, Display_Only,
       Dontredolistview, Recordval, Mat Passeddata$, Usemyf, Mat Myf$, Mat Myf,
       Path$, Selecting)                                   -- returns chosen/edited record key$ ("" if cancelled)

Fnfm  (Screenname$; …same params…, ___, Returnvalue)       -- returns 1 ok / 0 cancelled (or the screen's return value)

Fndisplayscreen (Screenname$; Keyval$, Srow, Scol, Parent_Key$,
                 Parent_Window, Recordval, Path$, Selecting)  -- read-only display of a screen (forces Display_Only)

Fncallscreen$ (Screen$; Keyval$, Parent_Key$, Display_Only, Parent_Window,
               Dontredolistview, Recordval, Mat Passeddata$, Usemyf, Mat Myf$,
               Mat Myf, Path$, Selecting)                   -- call by the bracket form; wraps name in [ … ] if absent
```

| Function | Returns | Use |
|---|---|---|
| `Fnfm$` | record key (string) | Run/edit a screen; the workhorse call. |
| `Fnfm` | numeric (1/0 or screen return value) | Same, when you want an ok/cancel or numeric result rather than the key. |
| `Fndisplayscreen` | numeric | Show a screen read-only (it sets `Display_Only`/`Selecting` for you). |
| `Fncallscreen$` | record key (string) | Programmatic equivalent of the in-screen `[SCRNNAME]` call syntax — adds the `[` `]` if you omit them. |

### Shared parameters

| Param | Meaning |
|---|---|
| `Screenname$` / `Screen$` | The screen **code** (key into `screenio.dat`; see [data model](ScreenIO_Data_Model.md)). |
| `Keyval$` | Record key to edit. **Blank = add a new record.** |
| `Srow`, `Scol` | Upper-left position for the screen window (0 = default/centred). |
| `Parent_Key$`, `Parent_Window` | Calling screen's key and window channel — establishes the parent/child relationship. |
| `Display_Only` | `1` = read-only (no edits / no Write event). |
| `Dontredolistview` | Suppress re-populating a listview when returning to it. |
| `Recordval` | Open by **record number** instead of key. |
| `Mat Passeddata$` | Arbitrary data handed to the screen; readable in its event code. |
| `Usemyf` + `Mat Myf$`, `Mat Myf` | Supply your **own** open file record arrays instead of letting ScreenIO open the file. |
| `Path$` | Override the data-file path. |
| `Selecting` | Listview is being used as a **picker** (return a selection rather than just browse). |

<a id="designer"></a>
## B. Event / designer support

```business-rules
Fnselectevent$ (&Current$; &Returnfkey)     -- opens the designer's "select event function" dialog
```
Presents the event-function picker used inside the ScreenIO designer; updates `Current$` (the chosen
function call) and `Returnfkey` **by reference** and returns the chosen function string. Used when wiring
a screen/control event to a `DEF FN…` (see [Event-callback contract](#events)).

<a id="helpers"></a>
## C. Helpers (callable from event code and the designer)

| Function | Signature | Returns / purpose |
|---|---|---|
| `Fnfindsubscript` | `(Mat Subscripts$, Prefix$, String$*40)` | Index of a field subscript by `Prefix$`+`String$` — resolves `FILE_FIELD` subscript constants at run time. |
| `fnGetUniqueName$` | `(Mat ControlName$, Control)` | A control name guaranteed not to collide with the existing names in `Mat ControlName$`. |
| `fnIsInputSpec` | `(type$)` | `1` if a control field-type code is an **input** control: `c`, `search`, `check`, `combo`, `filter`. |
| `fnIsOutputSpec` | `(type$)` | `1` if a code is **output/static**: `caption`, `button`, `p` (picture), `frame`, `screen`. |
| `fnDays` | `(String$*255; DateSpec$*255)` | The numeric `DAYS` value parsed from a date string; supports **relative** offsets (e.g. `-3w` = three weeks ago). |
| `fnFunctionBase` | *(no args)* | Base **FKEY** number for the current screen nesting level — `1500 + 200 × loaded-screen-count`. ScreenIO assigns each screen's buttons/controls function keys above this base, so nested screens never collide. |
| `fnBR42` | *(no args)* | `1` if running **BR ≥ 4.2** (feature detection on `WBVERSION$`). |
| `fnBR43` | *(no args)* | `1` if running **BR ≥ 4.3**. |

<a id="animation"></a>
## D. Wait animation

A small "please wait" animation for long operations.

| Function | Signature | Purpose |
|---|---|---|
| `fnPrepareAnimation` | *(no args)* | Initialise the animation (timing, speed defaults via `fnSettings`). |
| `fnAnimate` | `(; Text$*60)` | Render one animation frame, with an optional caption. Call repeatedly during the long task. |
| `fnCloseAnimation` | *(no args)* | Tear down the animation window. |

<a id="events"></a>
## Event-callback contract (how your code runs)

ScreenIO is **event-driven**, but events are **not** fixed-signature callbacks. The designer stores, per
screen and per control, a **BR statement string** (a function call you write); the engine `EXECUTE`s it
(`fnExecute`) at the right point in the screen lifecycle. So you "wire an event" by typing a **filename** of a custom function file (in .\function\\) such as
`{MyValidation}` (assumes .brs) into the event field.

**Screen-level events** (each is a field in the `screenio.dat` header — see data model):

| Event | Header field | Fires |
|---|---|---|
| Enter | `ENTERFN$` | when the screen is first displayed |
| Initialize | `INITFN$` | when the screen is called **without** a `key$` (add mode), if it has a data file |
| Read | `READFN$` | when the initial record is read; in a **listview**, also whenever the selection changes |
| Load | `LOADFN$` | as field values are loaded into controls |
| Write | `WRITEFN$` | when the user picks **Save**, just before the record is written to disk |
| Wait | `WAITFN$` | on keyboard idle, per the screen's `WAITTIME` timeout (`-1` disables) |
| Record Locked | `LOCKEDFN$` | when the record is locked by another user |
| Merge | `MERGEFN$` | during ScreenIO AutoMerge, before the record is written |
| Main Loop | `LOOPFN$` | every pass of the main `RINPUT FIELDS` statement |
| Nokey | `NOKEYFN$` | when a keyed read finds no record |
| Listview Prepopulate | `PRELISTVIEWFN$` | before a listview is filled (default `prelist.brs` if blank) |
| Listview Postpopulate | `POSTLISTVIEWFN$` | after a listview is filled (default `postlist.brs` if blank) |
| Exit | `EXITFN$` | last, as the screen closes |

**Control-level events** (the control's `FUNCTION$` field — see data model):
- **Validate** — input controls (`c`, `search`, `check`, `combo`, `filter`): decide whether the entered
  value is acceptable; may modify or reject it.
- **Click** — `button`, `caption`, `p` (picture): runs when the user clicks the control.
- **Filter** — listviews: decide whether the current record is added to the list (and its row colour).
  Example in [spec.md](spec.md#examples).

A `fnInit_…` / `fnFinal_…` function-name pair lets a control run initialization / finalization logic.

<a id="context"></a>
### Handler runtime context

The engine passes one large fixed parameter list into every event/helper function (so the same code can
run from any event); most are **by reference**, so assigning to them changes the screen. The
author-relevant ones:

| In scope | Meaning |
|---|---|
| `Mat F$` / `Mat F` | the screen's **file** record — fields by `FILE_FIELD` subscript constants |
| `Mat S$` | values of **non-file** controls (named controls not bound to a file field), by control name |
| `Key$` / `CurrentKey$` | current record key |
| `CurrentRec` | current record number |
| `ParentKey$` | the parent screen's key (child screens) |
| `FieldText$` / `FieldIndex` | value / index of the field being validated (Validate events) |
| `ControlIndex` | the control that fired (index into `Mat ControlName$`) |
| `ExitMode` | set this to exit the screen — see [constants](#exitmode) |
| `Mat PassedData$` | the `Mat passeddata$` handed to the screen at the call |
| `Path$`, `Selecting`, `DisplayOnly`, `Active` | call / mode context |
| `RepopulateListviews`, `RedrawListviews`, `RedrawScreens`, `RepopulateCombo` | set to force a UI refresh |
| `Window` | the screen's window channel |
| `Mat Disk_F$` / `Mat Disk_F` | the on-disk record (for Merge / compare) |

**Control properties** are addressable by a `ctl_<ControlName>` subscript into property arrays, e.g.
`let Invisible(ctl_MyField)=0` or `let BgColor$(ctl_MyField)="…"` — so a handler can show/hide and
recolour controls at run time.

<a id="exitmode"></a>
### ExitMode constants

A handler ends the screen by setting `ExitMode`; the engine keeps looping while it is `0`. From source
(`fnDefineExitModes`):

| Constant | Value | Meaning |
|---|---:|---|
| *(none)* | `0` | keep running (default) |
| `QuitOnly` | `1` | cancel / discard — the **ESC** default |
| `SaveAndQuit` | `2` | save the record, then exit |
| `SelectAndQuit` | `3` | select the record, then exit — the **ENTER** default in select mode |
| `QuitOther` | `4` | quit to another target |
| `AskSaveAndQuit` | `5` | prompt to save, then exit |
| `Reload` | `6` | reload the screen |
| `AutoReload` | `7` | reload automatically (no prompt) |

<a id="function-types"></a>
### Valid custom-function types

An event or control `FUNCTION$` field may hold any of:
- a **library function** call (your own `DEF FN…`) or a **custom screen function**;
- a **link to another screen** — the `[SCRNNAME]` form, optionally using `CurrentKey$` / `ThisParentKey$`;
- a **`CHAIN`** statement;
- **any single BR command**;
- (Conversion functions only) **any valid BR field spec**.

<a id="coverage"></a>
## Coverage check

This page documents **all 16** `DEF LIBRARY` exports in `screenio.brs`:
`fnPrepareAnimation`, `fnAnimate`, `fnCloseAnimation`, `fnBR42`, `fnBR43`, `Fnselectevent$`,
`Fndisplayscreen`, `Fnfm`, `Fnfm$`, `fnFunctionBase`, `fnGetUniqueName$`, `fnIsOutputSpec`,
`fnIsInputSpec`, `fnDays`, `Fncallscreen$`, `Fnfindsubscript`.

*(To regenerate the inventory: `grep -niE "^\s*def\s+library\s+fn" screenio.brs`.)*

## See also

- [spec.md](spec.md) — concepts, screen-function types, screen-to-screen call syntax
- [ScreenIO_Data_Model.md](ScreenIO_Data_Model.md) — the `screenio.dat` / `screenfld.dat` schema events and controls live in
- [fileio](../fileio/spec.md) — the FileIO library ScreenIO builds on
- [library-facility](../library-facility/spec.md) — linking the library (the BR `LIBRARY` statement)
