# BR 5.03 Release Notes

What changed in BR 5.03 that a user, an administrator or a support engineer needs to know about.
Entries that can change how an existing program behaves come first, because those are the ones worth
reading before an upgrade rather than after. For BR 5.02, see
[BR 5.02 Release Notes](old/BR502%20Release_Notes.md); for BR 5.01, see
[BR 5.01 Release Notes](old/BR501%20Release_Notes.md); for BR 5.0, see
[BR 5.0 Release Notes](old/BR50%20Release_Notes.md).

## Contents

- [1. Behaviour changes](#behaviour-changes)
  - [1.1 F1 on an empty command line](#f1-empty-line)
- [2. New features](#new-features)
  - [2.1 Selecting, copying and pasting at the console with the mouse](#console-mouse)
  - [2.2 Help opens in your web browser](#help-browser)
  - [2.3 COPY, MOVE, RENAME and TYPE take several names](#several-names)
  - [2.4 SEARCH shows the lines of files that match](#search)
  - [2.5 PgDn and digits at the -P pause](#pgdn)
- [3. Fixes](#fixes)
  - [3.1 TYPE with a wildcard types every file into a redirect](#type-wildcard)
  - [3.2 A failed load from source reports its line](#load-failure-line)
  - [3.3 Memory used by a debugger connection is released](#debugger-log-leak)

<a id="behaviour-changes"></a>
## 1. Behaviour changes

<a id="f1-empty-line"></a>
### 1.1 F1 on an empty command line

F1 on an empty command line, with nothing selected, types `HELP` and presses Tab, so the list of what
`HELP` covers comes up and Tab, Space and the arrow keys work through it as usual. Anywhere else F1
is the help key as before: help for the word under the cursor at the command line, or for the error
at an ERROR halt.

<a id="new-features"></a>
## 2. New features

<a id="console-mouse"></a>
### 2.1 Selecting, copying and pasting at the console with the mouse

Text on the console can be selected and copied to the clipboard with the mouse at the command
line (READY, ATTN, ERROR and LIST), on a HELP page, and in the
[console history](old/BR50%20Release_Notes.md#console-history) (HIST). All three take the same
gestures:

| Gesture | Does |
|---|---|
| Drag with the left button | Selects the text dragged over |
| Double-click | Selects the word under the pointer: letters, digits, `_` and `$`. Off a word it does nothing |
| Click while something is selected | Copies the selection to the clipboard and clears it |
| Click with nothing selected | Points Ctrl+Shift+Up/Down at the word clicked |
| Ctrl-C or Ctrl-Ins | Copies the selection and leaves it selected |
| Right-click | Pastes the clipboard into the command line, as Ctrl-V does |

A copy has one line per screen row, without trailing blanks.

The selection is cleared by any key other than Ctrl-C, Ctrl-Ins and F1, and when the text under it
changes or the screen scrolls or is cleared.

**Clicking a word to search for it.** After a click, Ctrl+Shift+Up and Ctrl+Shift+Down look for
the word clicked instead of the word at the cursor:

- **At the command line, on a HELP page and in HIST** they search the console history and the
  screen.
- **In LIST** they search the program. A click on a listed line searches on from that line.

A click points the search once; pressing the keys again goes on to the next match.

**What changes for clicks in these places:**

- **A click is no longer sent to BR.** On a HELP page it does not turn the page; the keys do.
- **A double-click at the command line no longer enters the line.**
- **A right-click at the command line pastes.** It is no longer the help key there; F1 and Ctrl-Y
  still are.
- **In HIST, a right-click** returns to the live screen and pastes into the command line. While a
  program is running it does nothing.
- **On a HELP page, a right-click does nothing.** There is nothing to paste into, and it does not
  turn the page.

**Running programs are not affected.** A program's screen and its input fields get every mouse event
as before, and in `INPUT FIELDS` a right-click is still the field's help key. That includes a
statement such as `INPUT FIELDS` typed at READY: the gestures apply only while the command line
itself is waiting for input.

<a id="help-browser"></a>
### 2.2 Help opens in your web browser

With `OPTION 85` off (the default), F1, Ctrl-Y and the `HELP` command show the br_tree topic in the
person's own web browser, from br_tree2, the HTML edition of br_tree, with its links, layout and
dark mode. The console is not painted over, and the status line says *Help is open in your browser*.

- **One help tab.** The first topic opens a tab; later ones move that tab to the new topic. If the
  tab has been closed, the next topic opens a new one. A browser does not let a page bring its own
  window forward, so a help tab behind other windows changes page without coming to the front.
- **The pages come from the BR server**, through a small web server inside the BR client that only
  this computer can reach. A client on another machine works the same, and nothing is copied to it.
  The server sends a page even while a program is busy in a long statement, so links in the help
  tab keep working while BR runs. No certificate is involved: the browser talks to the client on
  this computer only.
- **Where br_tree2 is.** BR looks for it with `CONFIG HELPTREE2 <folder>`, then `ENV$("BR_TREE2")`,
  then beside br_tree. `CONFIG HELPTREE2 CLEAR` puts back the search. br_tree's configuration
  section describes both `HELPTREE` and `HELPTREE2`.
- **Without br_tree2**, or with a client that cannot open a browser, help pages the topic on the
  console: 23 rows, the arrow keys, Page Up/Down and Home/End to move, F2 or Esc to leave.
- **From a program**, `HELP$(folder$, anchor$, "BROWSE")` shows a topic the same way and returns
  where it is, as `HELP$(folder$, anchor$)` does. Any other third argument is error 410; a third
  argument with `OPTION 85` on is error 9505.

A program's own field help (`INPUT FIELDS … HELP`) is unchanged.

<a id="several-names"></a>
### 2.3 COPY, MOVE, RENAME and TYPE take several names

`COPY`, `MOVE` and `RENAME` take more than one `<from>`, and `TYPE` more than one `<file>`, separated by
commas or blanks. Each may be a pattern. The last name of `COPY`, `MOVE` and `RENAME` is where they go;
`TYPE` has no target and types every name, in order, into the one redirect:

```
COPY a.txt,data\*.dat,notes\ bak
MOVE old1 old2 archive\
RENAME a,b *.bak
TYPE head.txt,body.txt >all.txt
```

- **A folder, unless the target has a wildcard.** With several names the target must be an existing
  folder, or the command is error 4203. A target with `*` or `?` still makes each file's own name.
- **A file that more than one name matches is handled once**, at the first. The overwrite question, or
  error 4150 where none can be asked, still appears when different files would be given one name.
- **A name that matches nothing is skipped**, if another matches. If none do, the command is error 4152, as
  for one name that matches nothing.
- **`RENAME -D`** renames one folder, so several names with it are a syntax error. An error, or Esc or
  Ctrl-A at a question, stops the whole command.

A blank is a separator, so `COPY a b c` now copies `a` and `b` to `c`; it used to be a syntax error. With
one name before the target, every command is as it was. See br_tree, 70-commands/file-directory/filename-patterns.md, section 1.7.

<a id="search"></a>
### 2.4 SEARCH shows the lines of files that match

`SEARCH` (`SE`) is a new file command, a small BR form of `grep`. It shows each line that contains a
pattern as `name:line: text`:

```
SEARCH apple notes.txt
SEARCH -I "apple pie" data\*.txt,old\*.txt >hits.txt
SEARCH /^ *PRINT/ src\**\*.brs >lines$
SEARCH -IWR print src\ -L
```

- **The pattern** is a word, a quoted literal, or a regular expression between slashes (ECMAScript
  syntax). `-I`, before the pattern, ignores case. A regular expression that does not compile is the new
  error 1009, *invalid regular expression*, and at the command line the cursor goes to the fault.
  The syntax, including what other regex languages have that BR's does not, is in br_tree,
  70-commands/file-directory/ECMA_REGEX.md, which `HELP COMMANDS REGEX` (or `HELP REGEX`) shows. A
  regular expression may hold a `!`, as in `/(?!x)/`; elsewhere on the line `!` still starts a remark.
- **Attributes**, before the pattern: `-I` ignores case, `-~` selects the lines that do not match, `-W`
  matches whole words only, `-B` lets a run of blanks and tabs match one blank, and `-R` searches a
  folder whole. They combine: `-I~WB`.
- **Options**, after the file names: `-C` shows a count per file, `-L` the names of the files with a
  match, and `-N` the lines without the `name:line:` prefix. An attribute after the names, or an
  option before the pattern, is error 1006.
- **The files** are named as for `TYPE`: several names, each of which may be a pattern, with the rules of
  2.3. The file the output is redirected to is never searched.
- **Each line is cleaned** before it is compared and shown: only displayable ASCII and tabs are kept, so a
  binary file can be searched without sending stray bytes anywhere.
- **An internal file** is searched record by record, numbered by record, with deleted records left out.
- **Output** goes to the screen, a file (`>`, `>>`), the printer (`PRINT`) or a string array (`>name$`).
  `-P` pauses after each screenful; at the pause a digit 2 to 9 shows that many more lines, and PgDn the
  next screen starting with the last line shown.

**Tab completes every file name** of `DIR`, `COPY`, `MOVE`, `RENAME`, `TYPE` and `SEARCH`, not only the 
first one. For `SEARCH`, completion starts after the pattern.

<a id="pgdn"></a>
### 2.5 PgDn and digits at the -P pause

At the pause that `-P` makes after each screenful of `DIR`, `COPY`, `MOVE`, `RENAME`, `DROP`, `FREE`,
`TYPE` and `SEARCH`, PgDn shows the next screen starting with the last line shown, so one line carries
over and nothing scrolls past unread. A digit 2 to 9 shows that many more lines before pausing again,
as it already did for `TYPE`. Any other key still shows the next screenful and the break key still ends
the command. `LIST -P` is unchanged.

<a id="fixes"></a>
## 3. Fixes

<a id="type-wildcard"></a>
### 3.1 TYPE with a wildcard types every file into a redirect

`TYPE *.txt > out` wrote only the first file to `out`: the redirect was closed after one file. A
plain wildcard such as `a*.dat` or `a?.dat` did not work at all; it was opened as a literal name
and failed with error 600, *bad wb file name*, with or without a redirect. `TYPE` now types every
file a wildcard names, one after the other, into the one redirect, so `>` and `>>` give the files
joined end to end.

Written to a file, the bytes are copied as they are, so a file that holds a blob comes through whole.
Trailing nulls and Ctrl-Z, which `TYPE >>` used to trim from each file, are now trimmed only when the
file is typed to the screen. This also applies to `TYPE oldfile >> out` for an old text file that ends
in Ctrl-Z: the Ctrl-Z now stays in `out`.

<a id="load-failure-line"></a>
### 3.2 A failed load from source reports its line

When a program is loaded from source and a line cannot be accepted, an unattended session logged
*Unattended processing terminated by error … while loading a program from source* with **line 0**.
It now names the line of the source file that failed, for example *error 1020 … line 2. missing
parenthesis*. A load that succeeds, or one that fails before any line is read because the file cannot
be opened, still reports line 0.

<a id="debugger-log-leak"></a>
### 3.3 Memory used by a debugger connection is released

While a debugger was attached (`DEBUG LISTEN`), each log message BR forwarded to it, which includes
every command entered, kept a little memory that was never released. The amount was small, a few dozen
bytes for each message, but it grew for as long as the session ran. It is now released as soon as the
message is sent.
