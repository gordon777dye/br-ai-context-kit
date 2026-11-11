# BR 5.02 Release Notes

What changed in BR 5.02 that a user, an administrator or a support engineer needs to know about.
Entries that can change how an existing program behaves come first, because those are the ones worth
reading before an upgrade rather than after. For BR 5.01, see
[BR 5.01 Release Notes](old/BR501%20Release_Notes.md); for BR 5.0, see
[BR 5.0 Release Notes](old/BR50%20Release_Notes.md).

## Contents

- [1. Behaviour changes](#behaviour-changes)
  - [1.1 Searching a program ](#searching-a-program)
  - [1.2 Searching the console history ](#searching-the-console-history)
  - [1.3 The help key and HELP$ read br_tree](#the-help-key-and-help-read-br_tree)
  - [1.4 Matching brackets](#matching-brackets)
  - [1.5 Tab completion at the READY prompt](#tab-completion)
  - [1.6 The HELP command](#the-help-command)
  - [1.7 MSGBOX: the new message box, and Don't ask again](#msgbox-the-new-message-box)
  - [1.8 An attached assistant can type at the READY prompt](#assistant-can-type-at-ready)
  - [1.9 WORK trees in brrestrict.sys](#work-trees)
  - [1.10 brrestrict.sys limits every session](#brrestrict-every-session)
- [2. Fixes](#fixes)
  - [2.1 Buttons are drawn plainly and centred](#buttons-are-drawn-plainly-and-centred)
  - [2.2 HTTP=SERVER reports exactly what is wrong](#http-server-reports-exactly-what-is-wrong)
  - [2.3 HTTP=SERVER fixes](#http-server-fixes)
  - [2.4 Memory-safety corrections](#memory-safety-corrections)
  - [2.5 MSGBOX fixes](#msgbox-fixes)

<a id="behaviour-changes"></a>
## 1. Behaviour changes

<a id="searching-a-program"></a>
### 1.1 Searching a program

**Searching the program from LIST.** While `LIST` is on the status line, **Ctrl+Shift+Up** and
**Ctrl+Shift+Down** search the loaded program's source for the word at
the cursor on, on the command line, and ignores case:

- With a listed line made the command line (the arrows put you on it), the search starts from the
  cursor's place in that line. With a word typed at the prompt, it starts from the bottom of the
  listing.
- The match is found ignoring case, in the lines as LIST shows them, going up or down and wrapping
  at both ends of the program.
- BR then lists a screenful ending with the line that matched, as `LIST -nnnnn` does, and
  highlights the match in that line. Near the start of the program, where there is not a screen's
  worth above it, the screen begins at the first line and the line is further up it; the highlight
  is still on that line.
- Pressed again on the empty prompt that leaves - or with the cursor on the highlighted match -
  the search goes on to the next occurrence of the same text, at the same length, as it does in
  the history.
- When nothing matches, BR sounds the bell and leaves the line as it was.

This is the arrows' counterpart to `LIST 'text'`, which lists every matching line at once.

<a id="searching-the-console-history"></a>
### 1.2 Searching the console history

The [console history](old/BR50%20Release_Notes.md#console-history) can be searched. The search
covers everything the history holds and the live screen below it, as one list, and ignores case.
A match is highlighted, and its line is brought into view about a third of the way down the
console, so that what led up to it shows above it.

**Ctrl+F** while you are reading the history (the status line says `HIST`) opens a **Search
History** box. It is a window of its own, so it can be moved anywhere, off the BR window included,
and it opens where you last left it.

| Key in the box | Does |
|---|---|
| **Enter** | searches up from the bottom of what is showing, then goes on to the next match up |
| **F3** | the next match up |
| **Shift+F3** | the next match down |
| **Esc** | closes the box; you are still reading the history |

Both directions wrap: past the oldest line the search goes on from the bottom of the live screen,
and past that back to the oldest. When a search wraps, the box's title says **wrapped**; when
nothing matches it says **not found**. Either one also sounds the bell.

**Ctrl+Shift+Up** and **Ctrl+Shift+Down** find the next occurrence, up or down, of the word at the
cursor, with or without the box open:

- On the live screen, the word is the one under BR's text cursor. Pressed at the live prompt, the
  keys also open the history, as Shift+Up does - except while BR is ready to draw more program
  lines (`LIST` on the status line), when they search the program instead; see
  [below](#searching-the-program-from-list).
- While the history is scrolled back, the word is the one you last clicked.
- Pressed again, they go on to the next occurrence of the same text, at the same length: searching
  for `aabb` highlights the `aabb` in `aabbcc` and then moves on, rather than searching for
  `aabbcc`.
- With the box open, the word is put into it, so F3 and Shift+F3 carry on with it.

A word is letters, digits, `_` and `$`.

All of this belongs to the history. Outside it, Ctrl+F goes to the program as any other key does,
and any key that leaves the history closes the box.

<a id="the-help-key-and-help-read-br_tree"></a>
### 1.3 The help key and HELP$ read br_tree

**The help key (F1) and `HELP$` now read the `br_tree` reference** - the BR language reference that
ships with the context kit as `context\br_tree` - instead of the `.wbh` help file. **`OPTION 85 ON`
puts back the old behaviour**, for an application that depends on it; see
[Compatibility](#help-compatibility) below.

**F1 at the READY prompt** shows the page for what the cursor is on:

- **The word under the cursor.** If the cursor is not on a word, it is the first word of the
  statement (after a line number or a label).
- **An error halt.** F1 on an empty line shows the page for the error code, for example the page
  for error 57.
- **What the word is.** A word that is several things is shown as the one it is on that line: the
  first word of the line is the statement or the command BR read it as (`DROP` typed at READY is
  the command; `OPEN` is a statement). A word written `rec=` is a clause of the statement, and
  one written `rec(` is a function. Each system function has its page row to itself, so
  `EXISTS` opens at the `EXISTS` row, not at the table of file functions.
- **On the empty prompt** with no error, the index of the commands.

**Where `br_tree` is** is found the first time it is needed and remembered until BR ends (a failure
too). BR looks in this order and takes the first folder that holds the tree:

1. `CONFIG HELPTREE <path>` - the folder, or the folder that holds `br_tree`. `CONFIG HELPTREE CLEAR`
   puts the search back.
2. `ENV$("BR_TREE")` - a `SETENV BR_TREE <path>` in the configuration file or a program, or the
   operating system's variable of that name.
3. `br_tree` or `context\br_tree` in BR's current folder, then checked in each of the two folders above it
   - then the same from the folder BR was started in, and from the folder the BR executable is in.

If it is not found F1 says so on the command line, `Help: br_tree not found [ CONFIG HELPTREE, or
ENV$(BR_TREE) ]`, and `HELP$` fails with error 9503. `STATUS` shows `HELPTREE` and `OPTION 85`.
`CONFIG HELPTREE` is refused in a restricted session.

**`HELP$(folder$[,anchor$])`** now returns where in `br_tree` a topic is, as the full path of the
file, followed by `#anchor` when one was given. It does not display anything.

- *folder$* is a folder of `br_tree` (`70-commands/program-management`), or simply (`program-management`), 
  or an error number (`57`, `ERR0057`), which gives the page for that error.
- *anchor$* names a section of that folder's `spec.md`, by its anchor or its heading, or a file in
  the folder. A name that begins two anchors is not enough: that is error 9504.
- A folder, section or file that is not there is **NOKEY**, error 4273, as `HELP$` has always
  reported a topic it could not find, and is trapped with `NOKEY`. A name that would leave the tree
  (`..`, a drive, an absolute path) is treated as not there.

```
LET PRG_MGT$ = HELP$("program-management", "go")
! C:\ADS\qsmrp\context\br_tree\70-commands\program-management\spec.md#go
```

<a id="help-compatibility"></a>
**Compatibility.** An application that calls `HELP$` with a `.wbh` keyword - `HELP$("topic", 1)` - or
depends on F1 opening `wbcmd.wbh`, or on `CONFIG HELPDFLT`, needs `OPTION 85 ON` in its
configuration; without it `HELP$` takes a string as its second parameter and a number is error 9505.
With `OPTION 85 ON` all of that works as it did, and a string second parameter is error 9505 instead.
F1 inside a running program - at an `INPUT` or a field - is not changed by this.

The error numbers 9503 to 9505 are provisional.

<a id="matching-brackets"></a>
### 1.4 Matching brackets

With the cursor on a bracket - `(` `)` `[` `]` `{` or `}` - BR shows the bracket that goes with it.
This works wherever you are typing at the console: the command line, an `INPUT` or `LINPUT`, and a
console field, whether or not the text is a program line.

- **A match** is shown in reverse.
- **No match** - the bracket is never closed, or never opened - shows the bracket under the cursor
  white on red.
- Brackets inside a string constant (`"..."` or `'...'`) are not counted, and a cursor on one shows
  nothing.
- The marks follow the cursor and come off when it moves, when the text changes and when the input
  ends. They are display only: the text is not changed.

**In the console history** the same is done for the bracket you last clicked. The match is looked for
in the rows on the screen, so a pair that reaches past them shows as unmatched until you scroll it into
view.

<a id="tab-completion"></a>
### 1.5 Tab completion at the READY prompt

Tab at the READY prompt lists the file names, or the HELP words, that fit what you have typed, and
a few keys then choose from the list. It works the same way in both places.

**Where it works.** After the file-name commands (`COPY`, `RENAME`, `MOVE`, `FREE`, `TYPE`, `LOAD`,
`DROP`, `DIR`, `RUN`, `SAVE`, `REPLACE`, `MERGE`, `PROC`, `SUBPROC`, `RMDIR` and `CHDIR`/`CD`, or an
abbreviation of one), in the file after `>` or `>>` on a command that redirects its output (and after
`<` on `LIST`), and after [`HELP`](#the-help-command). `RMDIR` and `CHDIR` offer folders only.

**The keys:**

| Key | Does |
|---|---|
| **Tab** | lists the names or words that fit what is typed, and leaves the line as it is. If only one fits it is completed (a folder gets its slash). Tab with a folder name on the line lists what is in that folder |
| **Right arrow** | puts the next name from the list on the line. With none chosen yet, the first one |
| **Left arrow** | puts the prior name on the line. With none chosen yet, the last one |
| **Space** | shows the next group of a long list. When there is no more, it is an ordinary blank |
| **Backspace** | when at the end of a word, takes away the whole word - otherwise normal backspace |
| **Enter** | accepts the line as it is |

- Right and left choose from the list, and wrap round at both ends. As soon as any other key is
  pressed they are the ordinary cursor keys again. **Up and down** always recall commands, as before.
- A letter typed after a name that was put on the line is added to it, and Tab lists again for what
  is now typed.
- **Tab straight after the command word** - even an abbreviation such as `HEL` or `LO` - puts in the
  blank for you and then lists, as if you had typed the blank and hit Tab.
- The first name of a command that takes two parameters (`COPY`, `RENAME`, `MOVE`) gets a blank after 
  it when it is completed. A name with a blank or comma in it is put in quotes. Options (`-S`) and the 
  words after the names (`TYPE`'s `PRINT`, `LOAD`'s `SOURCE`) are not completed.

**Long lists** show as many names as fit, then a line saying what can be done next:
`... 178 more - space for more | left/right to choose | type a letter, then Tab`. When the whole list
is showing it reads `left/right to choose or type a letter, then Tab`. The first list scrolls away
like any other output.

<a id="the-help-command"></a>
### 1.6 The HELP command

The new HELP command is a work in progress. Eventaully it will work with a new wiki when it is built. 
For now it works with br_tree documentation.

**`HELP` at the READY prompt** shows the `br_tree` page for a keyword, and **Tab completes what you
give it**, as it does for a file name after `DIR`; the keys are in
[1.5](#tab-completion). It reads `br_tree` like F1 does, so `OPTION 85 ON` puts back the old
behaviour; see [1.3](#the-help-key-and-help-read-br_tree).

- **`HELP word`** shows the page for that word (`HELP SORT`, `HELP OPEN`). Abbreviations work, as they do
  for any command.
- **`HELP` and Tab** lists the sets: `COMMANDS`, `STATEMENTS`, `FUNCTIONS`, `LIBRARIES` and `LEXI`.
- **A set is a folder.** Tab with a set on the line goes into it - `HELP FUN` and Tab gives
  `HELP FUNCTIONS ` and lists the functions - and so does Tab on a statement that has secondary
  keywords (`HELP STATEMENTS CLOSE` and Tab lists them, as below). `LEXI`, and a word with
  nothing inside it, stays as it is.
- **Enter on a set** lists its words, and leaves the set on the line: `HELP FUNCTIONS` lists the
  functions, and `HELP FUNCTIONS ABS` shows the page for `ABS`. A list shown this way is paged with
  Enter: `... 48 more - enter for next or [ bksp & type a letter, then ] Tab for more`.

What each set holds:

- **COMMANDS** - the commands, such as `DIR`, `MOVE` and `SORT`.
- **STATEMENTS** - the primary statements only. Choose one and Tab offers its secondary keywords:
  `HELP STATEMENTS, CLOSE` offers `DROP`, `FREE`, `RELEASE` and `WAITEQ`. `RETRY` and `CONTINUE` are
  statements; `GROW`, `IGNORE` and `SYSTEM` are secondary keywords (`ON ERROR SYSTEM`).
- **FUNCTIONS** - the functions that are not deprecated.
- **LIBRARIES** - the library topics (`FILEIO`, `FNFM`, `SCREENIO` and so on). `BRLIBS`, `LOAD`,
  `RELEASE` and `NOFILES` are left out of the list; `HELP LOAD` and `HELP RELEASE` still show their pages.
- **LEXI** - the Lexi page.

F1 follows the same rules: F1 on `SYSTEM` in `ON ERROR SYSTEM` now shows the secondary keyword, not the
`SYSTEM` command.

<a id="msgbox-the-new-message-box"></a>
### 1.7 MSGBOX: the new message box, and Don't ask again

On Windows, `MSGBOX` now shows the Windows **task dialog**, the message box Windows itself uses,
instead of the older classic box. The question, the buttons and the answers are the same, but the
box looks different:

- **`QST` shows no icon.** The task dialog has no question-mark icon, following Microsoft's
  guidance that routine questions carry none. `INF`, `ERR` and `EXCL` show their icons as before.
- **`YNAC` reads Yes, No, All, Cancel**, with Cancel at the far right.
- **BR's own permission question** (asked while an assistant is attached) reads
  "Yes, this once", "All this turn", "While connected", "No", with the safe answer, No, at the
  far right. Escape still answers No.
- **Other dialogs may look different too.** BR now uses the current Windows common controls
  throughout, so its file, print and font dialogs take the current Windows style.

**`^` in the buttons string adds a "Don't ask again" checkbox**, anywhere in the string: `"YN^"`,
`"YNC^"`, or `"^"` alone for an OK box. A ticked checkbox **adds 10 to the answer**: OK `11`, Yes
`12`, No `13`, Cancel `14`, All `15`. A program that does not use `^` never sees a value over 5.

```business-rules
00100 LET ANSWER=MSGBOX("Print the labels now?","Labels","YN^","QST")
00110 IF ANSWER>10 THEN LET SKIPASK=1 : LET ANSWER-=10
```

What BR does with the answer is up to the program: BR does not remember it.

<a id="assistant-can-type-at-ready"></a>
### 1.8 An attached assistant can type at the READY prompt

An assistant holding a grant now types at the `READY` prompt, and at BR's error prompt, in every
session, not only one whose channel was opened in `DEVELOP` mode. A line it types there runs as a
command, as the person's own would, and goes through the same checks: a restricted session's
command list and file limits, the refusals for lines that came from an assistant, and the
question BR asks before a shell command. The grant is the limit, and only the person gives it.

This is what lets a test, or an assistant, end a session cleanly, with `CLEAR PROC` and then
`SYSTEM`, rather than leaving BR running or killing it. `DEVELOP` mode still decides whether
other BR sessions started while the assistant is connected run restricted.

<a id="work-trees"></a>
### 1.9 WORK trees in brrestrict.sys

A `WORK` line in `brrestrict.sys` names a tree where a session may change files it did not
create - a site's test data, for an assistant to work on freely:

```
Q:\data
WORK Q:\data\test
!Q:\data\test\keys
```

- **In a restricted session,** a file under a `WORK` tree may be rewritten, emptied, renamed or
  deleted, and a directory under it removed, as if the session had created it. The tree's own
  root may not be removed or renamed.
- **In permission mode,** an AI turn does not ask about a change under a `WORK` tree.
- **It frees changing, not reaching.** Where the list names any area, a `WORK` tree must be inside
  one. A list of `WORK` lines alone names no area, so it does not limit where a session may be.
- **An exclusion still wins**, inside a `WORK` tree as anywhere.

Name test data only. A `WORK` tree lets an assistant overwrite what is in it without anybody being
asked. See `AI-Restricted-Operations.md`, *`WORK` trees: where changing is free*.

<a id="brrestrict-every-session"></a>
### 1.10 brrestrict.sys limits every session

The areas listed in `brrestrict.sys` bound **every** BR session, restricted or not: an ordinary
user's session, a `DEVELOP` session and a session with an assistant attached may read, create,
change, rename, delete and list only what the list permits, less what it excludes. Anything else
is refused with error **4165**, *brrestrict.sys does not permit this file*.

- **Inside the list,** a session that is not restricted may change any file, whoever created it.
  Only a restricted session is also held to the files it created (4153).
- **A file the list refuses is not asked about.** In an AI turn the list is tested before
  permission mode, so an excluded file is refused rather than put to the person.
- **Name everything BR uses.** Program and procedure directories, and the work, spool and print
  directories, have to be in the list as well as the data.
- **The configuration file and its `INCLUDE`s are read before the list applies,** in every
  session. The client reads its own list, beside the client executable, when the session starts.
- **No list, no limit.** Without `brrestrict.sys` nothing changes.
- **Operating-system commands are outside it.** What a shell command run from an unrestricted
  session does is not governed by the list.

See `AI-Restricted-Operations.md`, *Files: where the session may be*.

<a id="fixes"></a>
## 2. Fixes

<a id="buttons-are-drawn-plainly-and-centred"></a>
### 2.1 Buttons are drawn plainly and centred

A button field, such as a hot field shown as a button under `OPTION 40`, has a clear frame and a
label centred in the full height of its row, whether or not Windows themes are in use.

- **Label alignment.** The label is centred unless the field spec asks for right alignment, which
  is honoured.
- **`OPTION 50` applies to buttons**, as it does to text fields and combo boxes: a button is drawn
  with the classic raised 3D frame instead of the Windows theme. The same is true under
  `WINDOWS_THEMES OFF` and for a field whose attributes turn themes off. Note that this does not 
   change the functionality of OPTION 50, except to extend it.
- **With themes in use** (`OPTION 50` off), a button is drawn flat, as the Windows 11 theme draws
  it. It fills its row exactly as a classic button does, has a dark outline, and its face is a
  lighter shade of the field's colour so that it stands out from the window behind it. While the
  mouse is over it, the button takes the theme's own highlight.

<a id="http-server-reports-exactly-what-is-wrong"></a>
### 2.2 HTTP=SERVER reports exactly what is wrong

Each fault in setting up the web server has its own error, 0763 to 0797. `BRERR$` says what
is wrong and `SYSERR$` names the file, port or word concerned, so a certificate problem no longer
needs a log to diagnose:

```
ERR = 788   HTTPS private key file not found - <base>.key must sit beside <base>.crt
SYSERR$ =   C:\site\certs\server.key
```

| Codes | Cover |
|---|---|
| 0763-0768 | The `OPEN` string, and no HTTP licence. 9990 now means only a build without HTTP |
| 0770-0777 | `CONFIG HTTP` and `HTTPS`: keyword, port, range, missing value, `THREADS=`, `BIND=`, `PROXY=`, bad value. These replace 1006 |
| 0778-0781 | `LOG=` and `URL_BASE=` |
| 0782-0795 | The certificate, key and passphrase |
| 0796-0797 | The port is denied, or `BIND=` is not on this machine. 752 means only that the port is in use |

- **A wrong `URL_BASE=` now fails the `OPEN`.** No `URL_BASE=` and no `web` folder is a warning.
- **A `CONFIG HTTP` line with a fault changes nothing**, and a bad HTTP line in `brconfig.sys` is
  raised by the first `HTTP=SERVER` `OPEN`.
- **`CONFIG HTTP 0` and ports over 65535 are refused** (0771), and `PROXY=` takes only numeric
  addresses (0776).
- **`HTTP=SERVER` must be opened `DISPLAY, OUTIN`** (0764, 0765).
- **An expired certificate still starts the server**, with a warning, because renewing it needs the
  server answering on port 80.
- **The server log always records** a start-up failure, the start-up lines, and every refusal, with
  no `LOGGING` statement needed.
- **`FILE$(n,"HTTP-REFUSED")`** reports requests turned away, licence refusals first:
  `3,1,799,192.168.1.40,14:03:22`. Use it to see that clients are being refused for lack of HTTP
  licences. **`FILE$(n,"UPLOAD-ERROR")`** gives `769,<reason>` if the current request's upload could
  not be stored, otherwise `0`.
- **After error 4145, `SYSERR$`** says why the read ended: `no request in 15 seconds`, the same with
  `, 2 refused`, or `interrupted by a function key`.

<a id="http-server-fixes"></a>
### 2.3 HTTP=SERVER fixes

- **A refused second `OPEN` leaves `AUTH` as it was.** It could turn authentication mode off on the
  running server, so that static files were served without the program's login check.
- **A response contains only what the program printed.** Without `EOL=NONE`, it could also carry
  the rest of the request's body, to the same client.
- **The passphrase stays out of the BR log**, which recorded it in the `CONFIG` command.

<a id="memory-safety-corrections"></a>
### 2.4 Memory-safety corrections

- **A corrupt or over-deep index can no longer overrun memory.** Searching and inserting into an
  index kept the path from the root in a table of 12 levels, and stepped one past the end of it
  before noticing the index was too deep. That could overwrite the neighbouring field, and lock
  and read a node chosen from the overwritten value. The check is now made before the table is
  used, and such an index is refused with the bad-index error instead. An index of up to 12 levels
  behaves as before.
- **The console client no longer crashes clearing or closing the first screen.** `CLR_WINDOW`
  (clearing the current window) and closing a screen used the screen's list of linked controls
  before the screen had one, which crashed the client on Linux. Both now skip the step when there
  is no list. The wx client has the same guards, added for consistency; no crash has been seen
  there.

<a id="msgbox-fixes"></a>
### 2.5 MSGBOX fixes

- **All in a `YNAC` box works.** The fourth button showed "Help", and pressing it did nothing, so
  All could not be answered. It now reads All, closes the box, and returns `5`.
- **Ctrl-A works on a Yes/No box.** On a `YN` box, Ctrl-A did nothing. It now closes any message
  box without answering it and halts the program with ATTN at the `MSGBOX`; `GO` shows the box
  again. An `ON ATTN` handler takes the halt as usual.
- **An attached assistant keeps working while a box is up.** BR stopped answering the AI harness
  for as long as a message box was on the screen, so an assistant or a screen test went silent
  until somebody answered it. The harness now goes on answering, and a Break sent by the
  assistant interrupts the box as Ctrl-A does.
