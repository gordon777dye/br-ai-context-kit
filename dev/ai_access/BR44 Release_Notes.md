# BR 4.4 Release Notes

What changed in BR 4.4 that a user, an administrator or a support engineer needs to know about.
Entries that can change how an existing program behaves come first, because those are the ones worth
reading before an upgrade rather than after.

Deeper reference material stays in its own document; this page links to it rather than repeating it.

## Contents

- [Behaviour changes](#behaviour-changes)
  - [`CLOSE ,FREE` and `CLOSE ,DROP` now require a file opened for output](#close-free-and-close-drop-now-require-a-file-opened-for-output)
  - [Debuggers must be updated in order to attach](#debuggers-must-be-updated-to-attach)
  - [`MSG("send")` now types into BR only, and `MSG("kb")` is removed](#msg-send-now-types-into-br-only-and-msg-kb-is-removed)
  - [`SPAWN_RESTRICTED` is a new reserved word](#spawn-restricted-is-a-new-reserved-word)
  - [`GO` after an `AI` line keeps the conversation](#go-after-an-ai-line-keeps-the-conversation)
  - [`PRINT NEWPAGE` now scrolls the console off rather than discarding it](#print-newpage-now-scrolls-the-console-off-rather-than-discarding-it)
  - [The splash screen now waits 2 seconds, not 20](#the-splash-screen-now-waits-2-seconds-not-20)
  - [`MSG` actions that return text no longer add a trailing null character](#msg-actions-that-return-text-no-longer-add-a-trailing-null)
  - [The serial number is no longer shown on the status line](#the-serial-number-is-no-longer-shown-on-the-status-line)
  - [Row and column are shown on the status line by default](#row-and-column-are-shown-on-the-status-line-by-default)
  - [The OVERTYPE indicator is now teal](#the-insert-indicator-is-now-teal)
  - [The command console is set aside rather than hidden](#the-command-console-is-set-aside-rather-than-hidden)
  - [`CONFIG CONSOLE` now defaults to `DATA_ONLY`](#config-console-now-defaults-to-data-only)
  - [`OPTION 82` - work off the display area](#option-82-work-off-the-display-area)
  - [A program saved by 4.4 will not load in an earlier BR](#a-program-saved-by-44-will-not-load-in-an-earlier-br)
  - [`OPTION 60` - save in the 4.2/4.3 object format](#option-60-save-in-the-42-43-object-format)
- [Security](#security)
  - [The debugger connection is now encrypted and authenticated](#the-debugger-connection-is-now-encrypted-and-authenticated)
  - [The debugger port no longer accepts connections from the network](#the-debugger-port-no-longer-accepts-connections-from-the-network)
  - [Restricted sessions](#restricted-sessions)
  - [Where a restricted session may be: the file list](#the-restricted-session-read-list)
  - [UI regression scripts](#ui-regression-scripts)
  - [Starting a disposable restricted session](#starting-a-disposable-restricted-session)
  - [Calling an assistant from a program](#calling-an-assistant-from-a-program)
  - [An assistant no longer types at the `READY` prompt by default](#an-assistant-no-longer-types-at-the-ready-prompt-by-default)
  - [Both windows show a grant and a restriction](#both-windows-show-a-grant-and-a-restriction)
  - [An assistant cannot extend its own grant](#an-assistant-cannot-extend-its-own-grant)
  - [A turn asks you before anything destructive](#a-turn-without-a-grant-asks-before-anything-destructive)
  - [A turn needs the consent of whatever is running](#a-turn-needs-the-consent-of-whatever-is-running)
  - [A command from an assistant reports the error it died on](#a-run-that-fails-now-says-so)
  - [A restricted session's log is named for its WSID](#a-restricted-sessions-log-is-named-for-its-wsid)
  - [A program can tell an assistant something directly](#a-program-can-tell-an-assistant-something-directly)
  - [A program can be given a whole text in one go](#a-program-can-be-given-a-whole-text-in-one-go)
  - [`AI` - a conversation at the console](#ai-a-conversation-at-the-console)
  - [The client refuses a server certificate that was replaced in transit](#the-client-refuses-a-server-certificate-that-was-replaced-in-transit)
  - [New error codes for AI and restricted sessions](#new-error-codes-for-ai-and-restricted-sessions)
- [Debugging and observation](#debugging-and-observation)
  - [Watching a debugging session without taking it over](#watching-a-debugging-session-without-taking-it-over)
  - [A log of what appeared on the screen](#a-log-of-what-appeared-on-the-screen)
  - [The debugger can now interrupt a running program](#the-debugger-can-now-interrupt-a-running-program)
  - [Console scrollback](#console-scrollback)
  - [A variable watch now reports the value, not just the name](#a-variable-watch-now-reports-the-value-not-just-the-name)
  - [A step now tells the debugger where it stopped](#a-step-now-tells-the-debugger-where-it-stopped)
  - [Recording what a debugger submits](#recording-what-a-debugger-submits)
  - [The log now carries the clause and the source line](#the-log-now-carries-the-clause-and-the-source-line)
- [Printing and fonts](#printing-and-fonts)
- [Fixes](#fixes)
  - [Screen chains on a LIBRARY RELEASE,NOFILES return](#screen-chains-on-a-library-releasenofiles-return)
  - [`DLL()` calls no longer wait 100 ms each](#dll-calls-no-longer-wait-100-ms-each)
  - [`PROTECT` no longer repeats forever when it fails on Windows](#protect-no-longer-repeats-forever-when-it-fails-on-windows)
  - [Comment lines in `brconfig.sys` no longer hold the splash screen](#comment-lines-in-brconfig-sys-no-longer-hold-the-splash-screen)
  - [`MSG("state")` now checks its argument count](#msg-state-now-checks-its-argument-count)
  - [The client no longer stops with "Bad action 10129" while connecting](#the-client-no-longer-stops-with-bad-action-10129-while-connecting)
  - [Most of the status line was blank](#most-of-the-status-line-was-blank)
- [Debug builds](#debug-builds)
  - [Memory leak reporting at exit](#memory-leak-reporting-at-exit)
  - [The harness channel's ring statistics are now Debug-only](#the-harness-channels-ring-statistics-are-now-debug-only)

<a id="behaviour-changes"></a>
## Behaviour changes

<a id="close-free-and-close-drop-now-require-a-file-opened-for-output"></a>
### `CLOSE ,FREE` and `CLOSE ,DROP` now require a file opened for output

**New error 4151** — *CLOSE DROP or FREE requires the file to be opened for output*.

Previously a program could open an existing file `INPUT` and then `CLOSE #n,FREE:` it. The file was
deleted and **no error was reported**. `CLOSE #n,DROP:` behaved the same way, emptying the file. The
guard on that path tested only the share mode, and since `NOSHR` is the default when no share option
is given, an ordinary read-only open satisfied it.

That was never the intent: a channel opened for input should not be able to destroy the file. BR now
refuses, raising error 4151 and leaving the file untouched.

**What still works, unchanged.** A program that opens a file `OUTPUT` or `OUTIN` and frees or drops
it — the case the feature exists for — behaves exactly as before. So does every close on a window,
async-communications or printer channel.

**What this can break.** Any existing program that frees or drops a file it opened `INPUT` works
today and will fail with 4151 after upgrading. The fix in the program is to open the file `OUTIN`
(or `OUTPUT`) when the intent really is to remove it. If a run stops with 4151, that statement is
the one to look at.

<a id="debuggers-must-be-updated-to-attach"></a>
### Debuggers must be updated in order to attach

The debugger connection is now encrypted and authenticated, so a debugger built against an earlier
release will no longer attach. This is the change most likely to interrupt an upgrade, and there is
a switch to defer it: see
[The debugger connection is now encrypted and authenticated](#the-debugger-connection-is-now-encrypted-and-authenticated)
under Security for what changed, what a debugger now has to do, and `DEBUG AUTH OFF` for working 
the old way during the transition.

<a id="msg-send-now-types-into-br-only-and-msg-kb-is-removed"></a>
### `MSG("send")` now types into BR only, and `MSG("kb")` is removed

`MSG("send", …)` used to type through the operating system's keyboard input, which goes to whichever
window has the focus — so a program could type into another application, a command prompt, or
another BR session. It now puts its keys straight into the session's own keyboard buffer, the same
one keys typed in BR's window land in. They reach this session and nothing else, whichever window
has the focus. This applies in every session.

What changes for a program that uses it:

- **It no longer reaches other applications.** A program that used `MSG("send")` to drive another
  Windows program must find another way.
- **`MSG("kb", …)` has been removed. Use `MSG("send", …)`,** which takes the same arguments and
  behaves the same way. `kb` was only ever `send` with a check that BR's window was in front, and
  once `send` could no longer leave BR there was nothing for that check to do. A call to `kb` now
  raises 412 *invalid MSG action*. Error 413 (*target MSG window not on top*), which only `kb`
  raised, is retired — the number stays reserved and nothing raises it.
- **`MSG` returns at once, and the keys follow.** They are queued and fed into the session one at a
  time, `MSG("sleeptime", …)` apart, while the program runs and reads them — so `sleeptime` now
  paces what is seen typed, which is what it is for. A program must not expect every key to be
  waiting the moment `MSG` returns. Because keys are only fed as fast as they are read, a string is
  not limited by the 200-key keyboard buffer.
- **Named keys** — `|RET|`, `|TAB|`, `|ESC|`, `|F1|`…`|F12|`, the arrows, `|PGUP|`, `|HOME|` and the
  rest — arrive as the same keys pressed on the keyboard would. `|SHIFT+|` shifts ordinary characters
  on the current keyboard layout (`a` to `A`, `1` to `!`) and gives the shifted function, arrow and
  editing keys; `|CTRL+|` gives Ctrl+letter and the Ctrl variants of those keys. Keys that mean
  nothing inside BR — Alt combinations, the Windows and Apps keys, PrintScreen — are dropped.

The pointer actions (`setpos`, `lclick` and the rest) are unchanged in an ordinary session; a
restricted session may not use them.

<a id="spawn-restricted-is-a-new-reserved-word"></a>
### `MSG("gettext", …)` has been removed

**Removed 2026-10-03.** `MSG("gettext", <text$>)` returned the caption of whichever window was in
front. That was BR's own caption only when BR happened to be the foreground window; at any other
moment it was another application's window title, which a BR program has no business reading and
a restricted session must not be able to read at all. It took no window name, so there was no way
to ask it for BR's own caption specifically.

A call to it is now error 412. A program that used it to read **BR's own** caption should use the
`application_name` it already configured; there is no replacement for reading another
application's title, and that is deliberate.

`MSG("state", <state$>)` is unaffected and now answers for BR's own window.

### The `MSG` pointer actions now move a pointer BR keeps itself

`MSG("setpos")`, `MSG("setwpos")`, `MSG("lclick")`, `MSG("mclick")` and `MSG("rclick")` used to
drive the **physical** mouse: `SetCursorPos` moved the cursor on the desk, and the clicks were
`mouse_event` wherever that cursor had ended up. They now move a pointer BR keeps for itself and
deliver the press into BR's own session.

- **They no longer reach other applications.** A press used to land on whichever program was under
  the cursor. A program that used them to drive another Windows program must find another way.
- **They no longer move the cursor on the screen.** The user's pointer stays where the user left
  it.
- **`getwpos` answers relative to BR's window.** It and `setwpos` used to convert against
  *whichever window was in front*, so with BR not in front they silently answered, and aimed,
  relative to another application's window. Neither reported an error; they simply acted
  somewhere else.
- **They work with the window unfocused, covered, or off the screen.** Nothing on the path
  consults the display.
- **A press can only be delivered to the character screen.** Over the menu, the status line, a
  native control, or outside the window, the click actions are refused.
- **`MSG` returns before the press arrives.** It is queued with the keys from `send` and `kb`,
  behind any still waiting, and paced by `MSG("sleeptime", …)` — so typing and clicking keep the
  order the program wrote them in.
- **Every delivered press is logged** at the security level: `MSG pressed button <key> at row
  <row> column <col>`.

**`MSG("setcpos", <row>, <col>)` and `MSG("getcpos", <position$>)` are new**, addressing the
pointer by character cell with zero-based rows and columns. They exist because a caller that knows
where something is on the screen knows it as a row and a column, not as a pixel offset inside the
frame.

These actions were not available before this release — they were compiled out, and a call to any of
them returned error 412 — so no existing program can be relying on the old behaviour.

### `SPAWN_RESTRICTED` is a new reserved word

`SPAWN_RESTRICTED` is now a built-in function — see
[Starting a disposable restricted session](#starting-a-disposable-restricted-session). A program that
uses `SPAWN_RESTRICTED` as a variable name will no longer compile, and needs the variable renamed.

<a id="go-after-an-ai-line-keeps-the-conversation"></a>
### `GO` after an `AI` line keeps the conversation

**New 2026-10-09.** Breaking out of a program, asking the assistant something and typing `GO` used
to lose the answer. The program resumes and repaints its own screen over the Command Console,
which is where the conversation was - so it vanished from the screen without ever reaching the
scrollback either.

`GO` now scrolls the console off first, exactly as `PRINT NEWPAGE` does, so the conversation goes
into the history where `SCROLLBACK` and the screen log can still find it. A whole screenful is
scrolled, because the conversation sits at the bottom of a scrolling window and everything above
it has to move first. Nothing is scrolled when there was no conversation to keep.

<a id="print-newpage-now-scrolls-the-console-off-rather-than-discarding-it"></a>
### `PRINT NEWPAGE` now scrolls the console off rather than discarding it

`PRINT NEWPAGE` clears the screen as before. What changed is where the old contents go: they are
now scrolled into the console scrollback, so what the program had just printed can still be read
after the page is cleared. Previously a `NEWPAGE` lost it.

An explicit clear - a `CLEAR` command, or the clear a `SORT` or an `INDEX` does - still discards
what was on the screen. The distinction is deliberate: a user asking to clear the screen means it,
whereas a program starting a new page is not asking to destroy the last one.

Paging forward through a listing with PgDn is kept for the same reason. It redraws the screen
rather than scrolling it, so until now everything on it went without trace - including a command
typed between two pages and its answer. PgDn and the down arrow are one movement at two
magnitudes, and they now leave the same thing behind.

Nothing a program can see changes. The screen is as blank afterwards as it ever was and the cursor
lands where it always did; only the scrollback is different, and only when
[console scrollback](#console-scrollback) is switched on - which it is by default.

<a id="the-splash-screen-now-waits-2-seconds-not-20"></a>
### The splash screen now waits 2 seconds, not 20

The first session on a workstation used to hold the splash screen for 20 seconds before going on,
and so did any session whose startup produced a configuration message. Both now wait **2 seconds**.

Nothing else about the splash screen changes: it still appears, it still shows the workstation and
user counts and any configuration messages, sessions 2 to 9 still start with no wait at all, and an
`UNATTENDED` session still has no wait in any case. A configuration message that matters is in the
log as well as on the splash, so the shorter wait does not lose it.

<a id="msg-actions-that-return-text-no-longer-add-a-trailing-null"></a>
### `MSG` string arguments no longer carry the variable's unused tail

**Fixed 2026-10-03.** A BR string is stored as a character count followed by the characters, inside
a variable of its declared width. Every `MSG` action that *takes* a string read the full declared
width and ignored the count, so a variable wider than its contents arrived with its unused tail
attached — and that tail is not spaces, it is whatever the variable last held.

```
DIM A$*30
LET A$="AB"
LET X=MSG("send",A$)      ! typed AB, then 28 characters of whatever
```

A string **literal** was never affected, being exactly the size of its contents, which is why this
went unnoticed: `MSG("send","AB")` always behaved. Affected actions were `send`, `kb` and `loop`.

### `MSG("loop", …)` now copies between arrays of the same width

**Fixed 2026-10-03.** `MSG("loop", MAT A$, MAT B$)` refused with a string-size error unless the
destination was at least three characters wider than the source, so the ordinary case — two arrays
declared alike — never worked. An element holds a character count and its declared number of
characters; the size test was counting a terminating null that the format does not have and BR
never reads. A string may now be as long as the element is wide.

The same test guards every `MSG` action that answers with text, so an action returning a value exactly
as long as the receiving variable is wide no longer refuses it either.

### `MSG` actions that return text no longer add a trailing null character

Every `MSG` action that answers with text - `state`, `getcb`, `getpos`, `getwpos`, `getcpos`,
and the error messages some actions write back - returned the text with **one extra
character on the end, `CHR$(0)`**. `LEN` counted it, `RTRM$` did not remove it (it is not a space),
and writing the value to a file put a null byte in the file.

The length is now the text's own. If a program worked around this - trimming the last character,
slicing to `LEN(X$)-1`, or comparing with `(1:n)` - that workaround now removes a real character,
so check any program that reads a value from one of these actions. A program that simply used the
value is unaffected and is now correct.

<a id="the-serial-number-is-no-longer-shown-on-the-status-line"></a>
### The serial number is no longer shown on the status line

**Changed 2026-10-03.** The status line no longer has a serial number field. It was a fixed
nine-digit field that never changed during a session, and on the graphical status line it was
taking about a seventh of the width from the message field - the one field that has to shorten
its text when there is no room. The message field now gets that space.

The serial number is still available to a program as the **`SERIAL`** function, and it still
appears in a crash dump.

A printed screen (Ctrl-P) carries the same status line in eighty columns, and there the row and
column has moved up into the space the serial number occupied, rather than leaving a gap in the
middle of the line. It also prints in full now where it was previously cut to five characters.

This changes the size of the status line message the server sends the client, so **a client and
a server must be the same release** - which has always been the rule, and is worth repeating
because a mismatch here would garble the status line rather than refuse to connect.

<a id="row-and-column-are-shown-on-the-status-line-by-default"></a>
### Row and column are shown on the status line by default

**Changed 2026-10-03.** The field at the right-hand end of the status line shows the cursor's
row and column while a program is at an input. Previously this was off unless the configuration
said `STATUSLINE ROWCOL ON`, and the field held the release number instead.

`STATUSLINE ROWCOL OFF` still turns it off and restores the release number there. The release is
also shown in the message field when BR starts, so it is not lost either way.

The field is now sized from the screen, so a screen with more than ninety-nine rows or columns
gets the extra digit it needs. Previously such a position was cut short - on a 132-column screen,
column 105 was stored as `10:10`.

<a id="the-insert-indicator-is-now-teal"></a>
### The OVERTYPE indicator is now teal

**Changed 2026-10-08, and reversed 2026-10-10.** The status line's `OVER` indicator is white on a
teal background. `INSERT` keeps the status line's own attributes - or reverse video where the mode
differs from the configured default - so a field in insert mode looks ordinary.

Before 4.4 the indicator shared reverse video with every other status, which says *something is
different* without saying which of insert and overtype is in force, and that is the one thing an
operator needs to know before the next keystroke. A colour nothing else uses is recognised without
being read.

It was `INSERT` that carried the colour when this first shipped, and that was the wrong way round.
`CONFIG INSERT` decides which mode a field comes up in, and it defaults to insert wherever data
highlighting is on - so on such a site the status line sat teal nearly all the time and went plain
for the exception. A colour that is almost always present marks nothing. Overtype is the departure
there, so overtype is what carries it.

A site that sets `CONFIG INSERT OFF` has it the other way about, with overtype as the resting state
and the colour present most of the time. The two remain distinguishable either way, which is the
requirement; which of them is remarkable is the site's own business.

The colour is specified outright rather than taken from the sixteen attribute colours, so it
cannot be changed by `CONFIG ATTRIBUTE` and cannot collide with a colour an application has given
a meaning of its own.

<a id="the-command-console-is-set-aside-rather-than-hidden"></a>
### The command console is set aside rather than hidden

**Changed 2026-10-10.** When the console has nothing to show it is moved off the display area
instead of being hidden. It is still there, and still a window: it paints, it can be captured, and
it receives input sent to it. A hidden window does none of those - it has no client area at all,
and anything posted to it is discarded without a trace, which is a hard failure to diagnose
because nothing reports it.

Nothing about this is visible in normal use: the console is out of sight either way, and it comes
back to where it was the moment something needs it. It matters to anything that drives BR without
a person at the keyboard, and to support staff capturing a screen.

A parked window has no taskbar button, so an operator is not offered a window they cannot see.

<a id="config-console-now-defaults-to-data-only"></a>
### `CONFIG CONSOLE` now defaults to `DATA_ONLY`

**Changed 2026-10-10.** The default was `OFF`. Under `DATA_ONLY` the console appears when
something is written to it and goes away again when there is nothing to show, so output a program
sends to the console can be seen without the session having been told in advance to expect it.

An application that writes to the console and was built expecting no console window will now show
one when it writes. `CONFIG CONSOLE OFF` restores the previous behaviour.

<a id="option-82-work-off-the-display-area"></a>
### `OPTION 82` - work off the display area

**New 2026-10-10.** `OPTION 82 ON` puts a session's windows past the edge of the display and
leaves them there. It is for sessions nobody is watching - test runs, development drivers,
automation - so that they do not take the screen from whoever is using the machine.

Parked windows stay live - they paint, they capture, and they receive input - which is what
separates this from not opening a window at all, and from `UNATTENDED`, which suppresses the
windows entirely. A parked window has no taskbar button, so an operator is not offered one they
cannot see.

**Turning it off brings them back**, which is the way out of a session found parked. Ending the
session is enough on its own: a parked window's position is never saved, so the next start is on
the display whatever the option said.

It is off unless a session asks for it, and that is the whole of the protection - a session that
turns it on and forgets has windows it cannot see until it turns it off again. `OPTION 82` was
going to require `UNATTENDED` as well, on the reasoning that parking is only safe where nobody is
at the keyboard. That proved unworkable: `UNATTENDED` changes much more about a session than its
name suggests, enough that requiring it would have put this out of reach of the very sessions that
want it.

<a id="a-program-saved-by-44-will-not-load-in-an-earlier-br"></a>
### A program saved by 4.4 will not load in an earlier BR

**Please read this before upgrading if programs are saved on one machine and run on another, or if
some machines will stay on 4.3 for a while.**

BR 4.4 records, for every statement, which line of the source file it came from. That number is
kept in the line table, and the line table is part of a saved program, so the object format has
moved: 4.4 writes save level **39** where 4.2 and 4.3 wrote level **38**.

An older BR given a level 39 program **refuses it**, with error **2240** - *release level error*.
It does not misread it. Nothing is damaged and nothing runs with a wrong program; the load simply
does not happen, and says why.

The direction that matters less is already fine: **4.4 loads anything an earlier BR saved.** A
level 38 program loads and runs normally. It has no source line positions in it - there were none
to save - and BR reports positions without them, which is the only difference.

If a program has to be read by a 4.2 or 4.3 BR, see [`OPTION
60`](#option-60-save-in-the-42-43-object-format) below.

<a id="option-60-save-in-the-42-43-object-format"></a>
### `OPTION 60` - save in the 4.2/4.3 object format

**`OPTION 60` has a new meaning, and its old one is gone.**

It used to make `SAVE` write the 4.18-and-earlier object format. **That format is no longer
written at all** - it was retired on 2026-09-26. Programs already in it still load; they just
cannot be produced any more.

`OPTION 60 ON` now makes `SAVE` write the **4.2/4.3 format, save level 38**, so the program can be
loaded by a BR that predates 4.4. The cost is in the name of what level 39 added: **the source
line positions are not written**, because level 38's line table has nowhere to put them. Such a
program runs identically; what it loses is BR's ability to say which line of the source file a
statement came from.

Use it when a program must be read by an older BR. Leave it off otherwise - level 39 is the
default and loses nothing.

**It affects saving only.** BR 4.4 loads all three object formats - the pre-4.2 one, level 38 and
level 39 - whether `OPTION 60` is set or not. Nothing about loading depends on it.

`OPTION 60` continues to set `OPTION 74` as well (*treat `IGNORE` as a label reference for line
level error handlers*), which it has done since the old format was retired. A save meant for 4.2
or 4.3 wants 4.2/4.3 code generation with it.

`STATUS CONFIG` reports `OPTION 60` again; while it had no meaning it was left out.

<a id="security"></a>
## Security

<a id="the-debugger-connection-is-now-encrypted-and-authenticated"></a>
### The debugger connection is now encrypted and authenticated

**This changes how an existing debugger connects, and a debugger that has not been updated will no
longer attach.** Please read this before upgrading if you use `DEBUG CONNECT` or `DEBUG LISTEN`.

Previously, whatever connected to the debugger socket became the debugger, with no exchange of any
kind first. That carried the right to issue commands, step the program, read variables and reach
`DEBUG INTERNAL`; and because BR allows only one debugger at a time, connecting also locked the
real debugger out. Everything the debugger then saw — program source, variable values and BR's log
stream — crossed the connection in clear text.

The connection now runs over TLS 1.3, and inside it BR and the debugger prove themselves to each
other with a shared token. Both sides prove themselves, not just the debugger: `DEBUG CONNECT` dials
out to a host you name and then streams your source and data to it, so BR proving it is BR matters
as much as the other way round. A connection that fails either step is closed and recorded in the
log, and the channel stays free for the legitimate debugger.

Three modes, set with the new `DEBUG AUTH` command:

```
DEBUG AUTH                    ! report the current mode, and where the token is
DEBUG AUTH COOKIE             ! the default
DEBUG AUTH TOKEN <64 hex>     ! a token you supply, for a debugger on another host
DEBUG AUTH OFF                ! no encryption, no authentication - as BR behaved before
```

In the default `COOKIE` mode BR generates a fresh token for each session and writes it where only
your own account can read it, alongside BR's other per-user files — on Windows
`%LOCALAPPDATA%\ADS\brdebug.token`. A debugger running as you reads it from there and needs no
configuration. The token is written as soon as the port opens, so it is always in place before
anything can connect. `DEBUG AUTH` on its own prints the mode and the token's location.

`TOKEN` mode is for the case the cookie cannot cover — a debugger on another machine, which cannot
read your local file. Supply the same 64 hex digits to both sides. No token file is written.

`DEBUG AUTH OFF` restores exactly the old behaviour and exists for one reason: so that a debugger
that has not yet implemented its half can still be used during the transition. It is recorded in the
log as a security event both when you set it and each time a debugger attaches under it. Please
treat it as temporary.

Every outcome is written to the log at the security level, with the address of the peer, and on
success the TLS version and cipher:

```
Debugger authenticated over TLSv1.3 TLS_AES_256_GCM_SHA384 from 127.0.0.1
Debugger attach refused: wrong token over TLSv1.3 from 127.0.0.1
Debugger attach refused: the TLS handshake with 127.0.0.1 failed
```

A peer that connects and then says nothing is refused after a few seconds rather than holding the
channel; BR carries on either way.

<a id="the-debugger-port-no-longer-accepts-connections-from-the-network"></a>
### The debugger port no longer accepts connections from the network

`DEBUG LISTEN` used to bind every interface on the machine, so the debugger port was reachable from
the network. Anything that connected to it was treated as the attached debugger, which carries the
right to issue commands, step the program and read variables.

**`DEBUG LISTEN` now binds the loopback interface only, and there is no option to change that.** A
debugger on the same machine connects as before; nothing off the machine can.

```
DEBUG LISTEN                  ! port 9555, loopback
DEBUG LISTEN 9555             ! the same, said explicitly
```

Anything after the port is now a **syntax error** (1006), refused rather than ignored: a script
still carrying the keyword must fail where you can see it, not bind loopback while you believe it
is on the network.

Note what that means for a procedure. A syntax error halts a proc at the `READY` prompt - or
aborts an `UNATTENDED` run - and **`PROCERR RETURN` does not carry it past one**; it carries a proc
past a runtime error, which this is not. So a startup procedure with the old keyword in it stops
there until the line is removed. That is deliberate.

**If you need to attach a debugger from another machine, forward the port** — with SSH, or
whatever your site already uses for administrative access. That is a deliberate choice either way;
the difference is that forwarding puts it with whoever administers the machine, rather than with
whoever can type a BR command into a running session.

`DEBUG CONNECT`, where BR dials out to a debugger the operator names, is unaffected, and remains
the way to reach a debugger that is somewhere else.

**The default port has also moved, from 8556 to 9555.** The debug observer's default moved with it,
from 8558 to 9556. The 8555 series belongs to `brlistener`, which already uses 8555, 8557 and 8559
for its successive versions; the debug channel had taken two ports out of the middle of that range
and left it unable to grow. A debugger that connects to an explicit port is unaffected; one that
relies on the default needs updating, which it needs anyway for the authentication above.

**Loopback and authentication are two defences, not one repeated.** The connection is now
encrypted and authenticated (below), and it is still bound to loopback: the first means there is no
endpoint off the machine to reach at all, which is a stronger statement than any check made after
something has already connected.

<a id="restricted-sessions"></a>
### Restricted sessions

A session can be started **restricted** — see
[Starting a disposable restricted session](#starting-a-disposable-restricted-session). It is
restricted from before it reads its configuration file until it ends, and throughout:

- **the session may change only files it created itself** — **error 4153** otherwise. It may
  create files freely, and may then rewrite, empty, rename, copy over and delete them for as long
  as it runs. Anything else it may read but not write, empty, rename, delete, change the attributes
  of, or overwrite by `INDEX`, `SORT`, `COPY` or `SAVE`. BR tracks the session's files by path and
  by identity on disk, so a file someone else later puts under the same name is not the session's;
  the tracking is the session's own and ends with it. A new program is also refused if it would be
  loaded in place of an existing one of the same name under another program suffix;
- commands are refused unless they are on a permitted list — **error 4154**. The file commands —
  `FREE`, `DROP`, `RENAME`, `COPY`, `RMDIR`, `PROTECT`, `SAVE`, `REPLACE`, `INDEX` and `SORT` — are
  on the list, and each is decided per file by the rule above. `EDIT` is refused;
- `SYSTEM` with an operating system command is refused. `SYSTEM` on its own still ends the session
  normally;
- configuration operations are refused unless permitted, whether they arrive from a `CONFIG`
  command or from the session's configuration file. Refused are those that can reach outside BR or
  move the audit trail: `SHELL`, `EDITOR`, `PDF_READER`, `LOGGING`, `DATABASE`, `HTTP`, `HTTPS`,
  `SETENV`, `WBSERVER`, `BRSERVER`, `WSID` and `LOGIN_NAME`. Appearance, formatting, limits,
  printing destinations, `SPOOLCMD`, `OPTION`, `USERLEVEL`, `DRIVE` and `EXECUTE` are unaffected,
  so a session can still declare its drives and name the program it is to run. `SPOOLCMD` may be
  set, but the command never runs (below);

  `DATABASE` is refused as a whole for now. SQL is a write path the file rules above do not
  reach, so a connection would let a restricted session change data freely; the consequence is
  that such a session cannot report from a database, and a narrower rule is intended.

<a id="the-restricted-session-read-list"></a>
### Where a restricted session may be: the file list

A restricted session could always reach anything the account could. The rules above govern what it
may **change**; a site that needs to govern what it may **see and touch at all** can now install a
file list. This matters most where a model is driving the session: what such a session can read is
what the model can be shown, and what it prints leaves the site with the model's next request.

**With no file list installed nothing changes** — a restricted session reaches whatever the account
can, as before. The feature costs an existing site nothing until it chooses to use it. **All
folders on a client machine are likewise unrestricted until a list is installed on that machine**:
each side reads its own, and restricting a server does not restrict a client.

**The list is `brrestrict.sys`, in the directory of the BR executable.** It is not a configuration
statement and not a command-line argument, so a session cannot choose its own: the only way to
change what a session may reach is to change the installation it runs from.

One entry a line:

```
# what a disposable reporting session may reach
Q:\data                            a directory: it and everything under it
Q:\rates.dat                       one file
Q:\data\*.rpt                      the .rpt files in data
Q:\data\**\*.rpt                   and in every directory under it
!Q:\data\payroll                   an exception inside a permitted tree
:C:\ADS\shared                     a native path, marked by the leading colon
```

Anything the list does not reach is refused with **error 4165**, *restricted session:
brrestrict.sys does not permit this file*.

**Entries can be given per user.** A line of its own beginning `@` qualifies every entry that
follows it, until the next one:

```
Q:\common                          everybody: no heading yet, so @all applies
@payroll                           only when the session's login name is payroll
Q:\wages
!Q:\wages\archive
@all                               and back to everybody
Q:\reports
```

`@all` is the default, so a list without any `@` line behaves exactly as before, and
`@<username>` matches the login name without regard to case — as `brconfig.sys` already matches
its own `@<username>`. Entries under a heading that does not match this session are not loaded at
all. Note that this is a **section** heading governing the lines below it, where `brconfig.sys`'s
`@` qualifies the rest of its own line; a file list is usually a run of entries per user, so the
name is written once above them. An `@` line that names nobody switches the entries below it off
rather than leaving the previous heading open.

**It governs every operation on a named file**, not reading alone: an `OPEN` for input or output,
`INDEX`, `SORT`, `COPY`, `SAVE`, `REPLACE`, `FREE`, `DROP`, `RENAME`, `PROTECT`, `MKDIR`, `RMDIR`,
and `DIR` or any other directory listing. So a restricted session cannot see out of the folders
the list names, and cannot put anything into a folder it cannot see. Error 4165 and error 4153
answer different questions — 4165 is *the site does not let this session near that file*, 4153 is
*this session did not create that file* — and the list is tested first, being the outer boundary.

- **Entries are BR names**, resolved through the session's `DRIVE` statements, **unless they begin
  with a colon**, which is BR's mark for a native path everywhere else and is the mark here too.
  The drive mapping is fixed when the list is read, so a mapping added later cannot move an entry.
  On the client, entries are native names either way, because client file names are not subject to
  `DRIVE` statements. None of BR's other filename conventions apply — in particular not the
  `<filename>/<parent-path>` form an open string still accepts; a forward slash in an entry is an
  ordinary path separator.
- **`#` begins a comment**, and `!` does **not** — `!` marks an exclusion, as in a `.gitignore`.
  This is the one place where BR's own comment character does not apply, and it is deliberate: a
  line meant as a comment but read as an exclusion excludes nothing and is logged, while an
  exclusion read as a comment would silently leave a file permitted.
- **An exclusion overrides every permit**, whatever order the lines are in. To allow something
  inside an excluded area, narrow the permit instead of adding one.
- **`*` and `?` stay within one name and `**` crosses**, which is POSIX glob under `FNM_PATHNAME`
  plus `.gitignore`'s `**`. So `data\*.rpt` is the files in `data` itself, and `data\**\*.rpt`
  reaches every directory under it, `data` included. There are no bracket expressions and no
  backslash escape.
- **Whatever an entry names, it takes the tree under it if it is a directory** — by pattern as
  well as exactly, so `Q:\*\data` is each application's data directory and its contents.
- **Names are compared without regard to case on every platform**, Linux and macOS included, so a
  list written and tested on Windows means the same thing on the server it is deployed to.
- **An entry for something not there yet applies when it appears.** The list is read once at
  startup, and an entry naming a path that does not exist then is kept rather than discarded — so
  an exclusion for a nightly export directory, or for a volume not yet mounted, is not one that
  quietly never applies.

**BR's own working files are inside the rule.** A site that installs a list has to name the work,
spool and print directories in it as it names its data. Exempting them could not be made safe,
because `WORKPATH`, `SPOOLPATH` and `PRINTDIR` are configuration statements a restricted session is
permitted to set. They can be named narrowly rather than by opening their directory —
`:C:\ADS\w*.wrk` permits the work files in `C:\ADS` and nothing else there.

Two things are reachable whatever the list says:

- **the files the session created itself**, wherever it put them — it wrote the content, and a
  session that could not read back its own sort output or its own index would be no use;
- **the session's configuration file and its `INCLUDE`s**, which are read before the list comes
  into force. Everything after that is governed: the startup command, the procedure it names, the
  program that procedure loads, and every operation from then on.

`EXISTS` reports nothing about a file outside the list, and a listing of a permitted folder still
shows the names of excluded things inside it — the exclusion stops them being opened or listed,
not named.

**Every name is resolved to the file it actually reaches before it is compared**, and so is every
entry in the list. A junction, a symbolic link, `..`, a relative path and an 8.3 short name
therefore cannot widen or evade the list — in particular, **a junction inside a permitted
directory does not make its target reachable**. The same resolution means a directory may be named
in the list by any of its paths.

Each entry, and every refusal, is written to the log as a security event naming the resolved
path, so an administrator can read back from the log exactly what the list was taken to mean.

The full reference is `AI-Restricted-Operations.md`, *Files: where the session may be*.

<a id="ui-regression-scripts"></a>
### UI regression scripts

`br_mcp_driver uitest` runs a plain text script against a running session, so a programmer who has
changed a screen can say what should be on it and rerun that after the next change. One step a line:

```
expect row 0 "ORDER ENTRY"
expect "Customer code:"
absent "Customer not found"
field 0 spec "C 8"
type ACME
press ENTER
expect "Customer not found"
```

`expect` retries for a few seconds, because a program takes time to paint; `absent` does not, since
a thing that must not appear cannot be waited for. A failed step does not stop the script, so one
run reports everything that is wrong, and a failed `expect` prints the screen with it. Keys are
named — `ENTER`, `TAB`, `F1`, `SHIFT-F3` — and a number still works for anything unnamed. Typing
needs the keyboard grant, which is given inside the session and cannot be taken by the script.

Several scripts may be named in one command, which is how a suite is run: the assistant channel is
claimed once per session, so the set goes in together.

**`DLL(...)` is refused**, with error 4154. A DLL is native code: once it is running it is outside
every check a restricted session is made of, and it could call the operating system directly. Since
a restricted session may create files, it could otherwise write a library and load it. `MSG(...)`
is permitted action by action: actions that read or arrange windows work, and `MSG("dump", …)` and
`MSG("shot", …)` follow the file rule. `MSG("send", …)` works, and as in every
session it types into this session only (see
[the behaviour change](#msg-send-now-types-into-br-only-and-msg-kb-is-removed)). The pointer actions (`setpos`, `setwpos`, `lclick`, `mclick`, `rclick`) are refused with 4154,
because a click at screen coordinates can land on any program. An action added later is refused until
classified.

**Printing is to installed printers.** A restricted session may print to printers installed on the
computer, which may be shared printers, and to preview. Printing to a UNC name is refused with 4154:
a UNC name that is not an installed printer is opened as a file and the job written into it. A job
written to a named file, such as `PDF:` output, follows the file rule.

**The client enforces the same rule on its own files.** The server tells the client that the
session is restricted, and the client applies the file rule to the files a program names for it —
the same rule, with its own list of what the session created on the client side.

Two further routes out to the operating system are closed while a session is restricted: a spool
command does not run — a print job that would hand its file to the `SPOOLCMD` command is refused
with 4154, although the setting itself is allowed — and **Ctrl-]**, which opens a shell from the
terminal, is refused — by the client in client/server mode, where the shell is started on the
client.

This exists so that a program written on a user's behalf — by an assistant, or by anything else
the application does not fully trust — can be run without putting existing data at risk. Because
the check is at the operation rather than in the source, it cannot be evaded by how the code was
reached: `EXECUTE` of a string built at run time, `CHAIN`, a `LIBRARY` call and a called procedure
all land on the same check.

**Nothing clears it but ending the session.** Not a program ending, not `CHAIN`, not `LIBRARY
RELEASE`, not an error exit, not returning to the command console, and not the programmer: a
session that needs write access again is restarted. Two consequences to plan for:

- **Your own later work in that session is restricted too.** After such a program has run, an
  ordinary program that writes data is refused until BR restarts. An application that must keep
  writing should run the untrusted program in a separate session and treat that session as
  disposable.
- **A restricted session can end itself.** `SYSTEM`, `SYSTEM <n>` and `SYSTEM LOGOFF` exit as they
  always did; only the form that runs an operating system command is refused. (An earlier draft of
  these notes said `SYSTEM` was blocked outright. It was, briefly, and that was changed.)

Every refusal is written to the log, as is the moment the session became restricted. The state is
also recorded in `wbserver.dat` as a byte lock, so other processes can see which sessions are
restricted — and so that a session that crashes cannot leave the mark behind for whichever session
next reuses its number.

<a id="starting-a-disposable-restricted-session"></a>
### Starting a disposable restricted session

**New function `SPAWN_RESTRICTED(command$ [, config$ [, wait]])`.** It starts a new BR session on
the same workstation ID — the next free session number — restricted from its first moment, and runs
`command$` as that session's startup command, typically `PROC <file>`. `config$` names its
configuration file and defaults to the current session's.

- With no `wait`, or 0, it returns the new process's id at once.
- With a `wait` in seconds it waits — the screen keeps repainting and ATTN still works, as with
  `SLEEP` — and returns the session's exit code. A session still running when the wait runs out is
  ended, and **error 4157** is raised.

This is the way to run something untrusted without restricting the session you are working in:
the new session is restricted and disposable, and yours is not.

**It is restricted before it reads its configuration file.** That ordering matters because the
configuration file is the caller's choice: the configuration operations listed above are refused in
it, not applied and then locked. Since `LOGGING` and `WBSERVER` are among them, the new session is
handed the current session's log and `wbserver.dat` instead, and logs to the same file.

**One session per workstation ID is always kept free**, so that spawned sessions can never take the
last one a person might need: when eight of the nine are in use, `SPAWN_RESTRICTED` raises **error
4155**. A session gives its number back when it ends, including one ended at its timeout.

A restricted session may not call `SPAWN_RESTRICTED` (error 4154). It is available in local mode on
Windows; elsewhere it raises **error 4156** for now.

New `brserver` command-line flags, which `SPAWN_RESTRICTED` passes and which are not normally typed
by hand: `--restricted`, `--restricted-log=<folder>` and `--restricted-wbserver=<dir>`. The
last two are accepted only with the first.

<a id="calling-an-assistant-from-a-program"></a>
### Calling an assistant from a program

A program asks an assistant a question the way it asks a person: on the screen, with a field to
answer in. The assistant — reading the screen over the AI harness channel, and holding the keyboard
grant the person gives it — types the answer. **There is no other way in**: no connection of its own
and no path into a variable that a person's typing does not also take. So the field's own type and
length check the answer exactly as they check a person's, and the person can always answer instead.

Program source an assistant writes is typed into a file, never into a variable; it is shown to the
person and run only if they agree, and then in a restricted session started with
`SPAWN_RESTRICTED`. The assistant's grant is withdrawn while the program asks for that agreement, so
the assistant cannot give it on the person's behalf.

`br/aiaccess/agentlib.brs` is a reference library for this — stored prompts, each naming its
question and the field its answer goes in — and `br/docs/AI_ACCESS.md` (Track C) describes it in
full.

<a id="an-assistant-no-longer-types-at-the-ready-prompt-by-default"></a>
### An assistant no longer types at the `READY` prompt by default

An assistant holding the keyboard grant could type wherever BR was taking input, including the
command line, where `FREE` or `SYSTEM` is one keystroke away from an assistant that misfires.

Its keys now go in only while a **program** is waiting for input. At `READY` they are **held** —
not discarded and not refused — and go in when a program next asks, so an assistant may still
type ahead. A session that wants the old behaviour opens the channel with

```
LET X=MSG("harness", <port>, "DEVELOP")
```

which is what a development session wants, because there typing at the console is the point. A
restricted session is refused that mode.

<a id="both-windows-show-a-grant-and-a-restriction"></a>
### Both windows show a grant and a restriction

**Changed 2026-10-08.** A session marks its title bar `[RESTRICTED]` while it is a restricted
session, and `[AI Has Keyboard Access 4:37]` - with the time left - while an assistant holds the
keyboard. Both marks now appear on **both** of BR's titled windows: the application's own and the
Command Console's. Previously only the application window carried them.

Which window an operator is looking at is their business, not the session's - they break to
`READY`, work at the console, and go back - so a mark on one of them told them the truth only
while they happened to be in front of it. For the Console that is exactly when they are typing
commands by hand, which is when it matters most. With `GUI OFF` there is no application window at
all, and the Console is the only one there is.

Each window keeps its own title text - whatever a program or the configuration set, or the
Console's own caption - and the marks follow it, `[RESTRICTED]` first. A program that sets the
title is unaffected: the text it sets is kept apart from the marks, so neither is lost and neither
doubles when the other changes.

<a id="an-assistant-cannot-extend-its-own-grant"></a>
### An assistant cannot extend its own grant

**New 2026-10-09. New error 4166, `BREGRANTNOTRAISED`** - *the assistant's own commands may not
raise the keyboard grant - only the person at the session may.*

A grant is given at the session, by you, for a fixed time, and the time left is in the title bar -
so lending the keyboard has a known end. But a line an assistant asked to have run goes through
BR's console as if typed, and `MSG("grant", 3600)` is a line like any other. Nothing stopped a
turn from granting itself another hour, or `MSG("grant", -1)`, which never expires at all.

**A grant may now only be lowered from there.** While a line the assistant sent is the thing
running, `MSG("grant", n)` is accepted for `n = 0` - handing the keyboard back, which an assistant
that has finished should be able to do without asking - and refused for every other `n`:

| from the assistant's own lines | |
|---|---|
| `MSG("grant", 0)` | allowed - the grant ends |
| `MSG("grant", <any time>)` | **refused, 4166** |
| `MSG("grant", -1)` (never expires) | **refused, 4166** |

A shorter grant is refused along with a longer one. Not because shortening is dangerous, but
because the side making the decision cannot tell the two apart - the grant lives at the client and
the check is made at the server, before the request is sent - and nothing is lost by it: the
assistant can already end a grant early over its own connection, which the protocol has always
called the only change to a grant it may make.

**The rule covers everything a sent line starts**, including a program its own `RUN` line loaded
and anything that program calls. Your own commands are untouched: a `MSG("grant", …)` you type, or
one in a procedure of your own, behaves exactly as before. Every refusal is logged.

<a id="a-turn-without-a-grant-asks-before-anything-destructive"></a>
### A turn asks you before anything destructive

**New 2026-10-09. New error 4167, `BREAINOTPERMITTED`** - *the operator did not permit this
operation for the assistant.*

A command an assistant sends used to need the keyboard grant. That made the useful half of a
console conversation - the assistant saying "run this" - need the keyboard lent first, which is a
far larger thing to ask for than "look at my error". **A command now needs only an open turn**,
which only you can open, by typing `AI`.

What a turn may do without asking is the same either way:

| | within a turn |
|---|---|
| ordinary commands | run |
| anything destructive | **stops and asks you** |
| `SYSTEM` with a command, a spool command, the editor, `Ctrl-]` | **stops and asks you**, whenever an assistant is attached - a refusal is error 4167 |
| the powerful `CONFIG` operations | refused - error 4168 |

**The grant does not change that line, and for one release it did.** With the keyboard lent,
nothing was asked; the reading was that lending the keyboard is consent to whatever follows. It is
not. You lend the keyboard so the assistant can get on with the work, and you lend it once, for
minutes, before you know what it is going to do - so it cannot stand as consent to a particular
operation. What a grant buys is typing.

**It does not ask about the assistant's own work.** While the channel is open, BR keeps a list of
the files the session creates - the same create-then-own list a restricted session uses to decide
what it may change. A file on that list is the assistant's to rewrite; anything that was already
there, and belongs to somebody else, is what you are asked about. The list starts when the channel
opens and is emptied when it closes, so it means "created while an assistant was here" rather than
"created at any time". Without it every scratch file the assistant wrote raised its own question,
which is the fastest way to teach a person to answer without reading.

The question is on the console, where you are already reading the conversation:

```
[AI] the assistant asks permission to delete:
[AI]   C:\ADS\myapp\CUSTMAST
[AI] allow?  N = no, Y = this once, A = this turn, L = always, for this file:
```

- **`N`** refuses it, and the operation fails as though the file were protected - error 4167, which
  a program can trap.
- **A break key is not an answer at all.** Ctrl-A interrupts the question the way it interrupts
  anything else: nothing is allowed, nothing is refused, no error is raised, and the session takes
  an ATTN halt that `GO` resumes. An interrupt must never mean "go ahead", and it does not mean
  "no" either - the person has not answered, and the operation is simply not carried out.
- **`Y`** allows that one operation and is forgotten.
- **`A`** allows it and remembers it **until this turn ends**. Someone who has said "yes, the
  assistant may write to this report file" has said it; being asked six more times while it does
  that piece of work is noise, not safety.
- **`L`** allows it and remembers it **until the assistant disconnects** - the file joins the list
  above.

**There are two kinds of always because they are two different judgements.** Allowing a file for
the piece of work in front of you is one a person can weigh; allowing it for every turn until the
assistant goes home is a much larger one, and on a console left open all day the two are not
close. They used to be the same keystroke, which meant an answer given in the first turn silently
covered the twentieth.

The third line always names what would be kept, because "all" on its own is not something anyone
can weigh.

**It cannot be stepped around by putting the work in a program.** The question is asked where the
operation is attempted - the same points a restricted session refuses at - and not in front of
named commands like `FREE` and `COPY`. A list of commands is exactly what a sent line can walk
around: a program can open a master file for output and write over it without naming any of them,
and that open is asked about too.

**One operation asks one question, in its own words.** `FREE` asks about the delete, a rename
about the rename, `DROP` about emptying the file, and an `OPEN` for output about the open. BR tests
whether it can act before it acts - `FREE`, `DROP` and a rename each open the file exclusively
first, to find out whether another session holds it - and that test is not the operation, so it
asks nothing. A conflict there is the ordinary **error 4148**, *file sharing violation*, and it
happens before any permission question: a file somebody else has open is not a question for you to
answer.

**Every route to the operating system asks, and they all ask in one place.** What the shell runs
touches files through the operating system and never passes a BR gate at all, so the question cannot
be put where the files are - it is put where the shell is, inside `shell()` itself. That is the only
function every route passes through: `SYSTEM` with a command, a spool command, the editor `EDIT`
launches, the terminal's `Ctrl-]` escape. The gate used to sit in three of those four, which left
the editor and the shell escape reachable in two console lines.

The question names the program that would run, and what `A` or `H` remembers is **the first keyword**
for `SYSTEM` - so `H` on `cmd /c ...` passes later `cmd` commands and still asks about `powershell` -
or the route itself for the others, because an editor's first word is a program path rather than
something a person can weigh. An interactive shell is remembered never: saying yes to "a shell" is
saying yes to everything it can launch, so that one offers only `N` and `Y`.

**The person is asked about their own shell calls too**, for as long as an assistant is attached. A
rule the assistant could satisfy by asking the person to type the command for it would be the same
hole with one more step in it, which is why the question does not look at whose line it is. The cost
is one question per program per connection, not one per command.

The powerful `CONFIG` operations remain refused outright, with error 4168: those change what the
session *is*, and there is no program to name in a question about them.

### `OPTION 83` for an application that starts BR sessions

An application that spawns sessions of its own meets both halves of the new behaviour at once:
every `SYSTEM` it issues stops to ask, and every session it starts comes up restricted. For those
applications there is **`OPTION 83`**, which turns both off together:

```
OPTION 83 ON
```

With it set, this session asks nothing about operating-system calls — all four routes — and does
**not** raise the AI-user-mode flag, so the BR sessions it starts run normally. It is the exemption
`DEVELOP` mode already has from the flag, given to a user-mode session the site has declared
reaches the shell.

**It may be set only in the configuration file.** `CONFIG OPTION 83` at run time is refused with
**error 4172**, *this OPTION may be set only in the configuration file, never with a CONFIG
command*, whoever issues it. That is not tidiness: `OPTION` is on the permitted list for both the
restricted-session filter and the assistant filter, so without this an assistant could send
`CONFIG OPTION 83 ON` inside a turn and hand itself an unasked shell and unrestricted children —
the gate would be settable by the party it restrains.

**A restricted session is refused it outright**, configuration file or not. A contained session
that could set this would spawn an uncontained one, and a session restricted by the AI-user-mode
flag reads a configuration file that may be an assistant's own work — the reasoning that already
keeps `LOGGING` out of one.

**The flag is shared, so this exempts the session that sets it and nothing else.** It takes down no
flag another session holds: a second session with an assistant attached and no `OPTION 83` still
restricts what starts.

Turning it on is logged as a security event at startup, in those words, because it is the one
setting that lifts both gates at once:

```
OPTION 83: this session will NOT ask the operator about operating-system calls while an
assistant is attached, and will NOT restrict the BR sessions it starts.
```

**Use it where the application genuinely needs the shell**, not as a way round the question. What
it removes is the protection that stops an assistant reaching the operating system; with it off,
the only thing between an assistant's `SYSTEM` and the shell is that it has to get a line run at
all.

**A file on the client is decided by the client.** When a program reaches a file through an `@:`
path, the file belongs to the machine running the terminal, and only that side knows which of its
files this session created. So it makes the decision and reports back; the server puts the
question to you, in the same words and the same window as any other, and sends the operation again
if you allow it. Nothing about this is visible from where you sit - which is the point - but it is
why an `@:` operation is asked about at all.

**With `GUI OFF` the question still appears**, because it is written to the console and read with a
keystroke - the same path the `READY` prompt itself uses - rather than put in a dialog box. It
works the same way over a client/server link.

**In `UNATTENDED` mode a destructive operation is refused rather than asked about.** There is
nobody to answer, and a prompt with nobody at it is not a safeguard - it is a session that hangs
until someone notices.

Every question and answer is logged, and so is every operation refused for want of one.

<a id="a-turn-needs-the-consent-of-whatever-is-running"></a>
### A turn needs the consent of whatever is running

**New 2026-10-13. New error 4169, `BREAITURNNOTPERMITTED`** - *a program or procedure is active:
set `ENV$("AI_TURN_OK")` to `"Y"` before an AI command, or end what is running* - **and 4170,
`BREAITURNFLAGNOTSET`**, for a line of the assistant's that tries to set the flag itself.

**You cannot break into a running program to ask the assistant something.** BR has never let an
interrupted program be replaced: `SAVE`, `REPLACE`, `RENUM` and `RUN` all refuse with **2108**,
*program is active*, while one is. An AI turn can `LOAD`, which is the same thing - so `AI` is now
refused the same way. End the program, or say it is all right:

```
00100    LET X=SETENV("AI_TURN_OK","Y")
00110    STOP                                  ! the person can now ask the assistant
00120 ! GO comes back here
```

A **procedure** is in the same position for a different reason. A proc stands above a program the
way an operator does, so it survives a turn - but it is driving the program state, and a turn can
change it underneath. A proc that resumes expecting the program it loaded, and finds another, does
harm it cannot detect. So a proc says so too, before each inquiry:

```
LET X=SETENV("AI_TURN_OK","Y")
AI which of these customers is over their limit
```

**Why the flag is needed even when the proc wrote the `AI` line itself.** Writing `AI <text>`
consents to *asking*. It cannot consent to the `LOAD` and the `RUN` the assistant will send,
because those did not exist when the line was written - which is the whole point of a turn. The
flag is you saying *I know the loaded program may be gone when control comes back to me*.

| | |
|---|---|
| nothing running | no flag needed |
| a program or a procedure active, no flag | **4169**, before the assistant hears of it |
| the flag set to anything but `Y` | **4169** - `"y"` counts, `"YES"` does not |
| the flag set by a line the assistant sent | **4170**, and logged |
| `CONFIG SETENV AI_TURN_OK` | refused where the configuration file is read |
| a proc whose **last** line is the `AI` line | no flag needed - BR has already closed the proc |

**Two things take the flag down, and the `AI` command is neither.** You clear it yourself, with a
`SETENV` of any value but `"Y"`; or the turn ends, which clears it for you. So a proc driving three
turns still says so three times - each turn's end takes the last one's consent with it - but
reading the flag is not spending it.

**One case follows from that and is worth knowing.** An `AI` line that never opened a turn - no
assistant listening, 4158 - leaves the flag standing, because nothing ended. The next `AI` line in
that procedure is still authorised. If that matters to your program, clear the flag yourself:

```
00200    LET X=SETENV("AI_TURN_OK","Y")
00210    AI what is wrong with this record
00220    LET X=SETENV("AI_TURN_OK","")     ! whatever became of the turn
```

The flag also stays **readable during** a turn, so a program the assistant's own `RUN` loaded can
check `ENV$("AI_TURN_OK")` and find out how it was reached.

**`AI NEW` needs no flag.** It only ends a turn, and gating that would strand one.

**New 2026-10-13. New error 4171, `BREAITURNNOTYOURS`** - *the assistant may not use the `AI`
command: a turn is the person's to start, and a reply is how one ends.* A turn's whole authority
is that a person typed `AI`, and the state is single - so a line the assistant sent that ran `AI`
ended the person's turn and opened one of its own, with a question nobody had asked. What made
that worth a rule rather than a curiosity is where the new question goes: an `ASK` reaches
whatever is listening, which in `chat` mode is the model that just sent the line, so it would be
handed its own text as a fresh inquiry and could do it again - a loop nobody started. `AI NEW` is
refused from there too: the assistant already ends its turn by answering.

**Two commands behave differently inside a turn**, both to protect the procedure that consented:

- **`PROC <file>` from the assistant pushes**, like `SUBPROC`, instead of replacing the procedure
  it was sent into. Replacing it would destroy the proc that said the turn could happen. Your own
  `PROC` at the console is unchanged.
- **`CLEAR PROC` ends an open turn**, along with the procedures - and so does `CLEAR ALL`. A turn
  is a state of the command processor like a proc feeding it lines, and `CLEAR PROC` is how you
  say *stop taking commands from anywhere but me*. The assistant is told its turn is over rather
  than left waiting for a result.

<a id="a-run-that-fails-now-says-so"></a>
### A command from an assistant reports the error it died on

**Fixed 2026-10-13.** A line the assistant asked to have run comes back with BR's error number, 0
for success. An **untrapped run-time error** did not reach that report: `RUN` of a program that
stopped on a divide by zero answered **0**, and told the assistant its program had worked. The
same was true of an immediate statement - `LET X=1/0` reported success.

Errors raised in the command processor itself were always reported, which is why this was not
obvious: `LOAD` of a file that does not exist has always come back 4152.

**An error the program handles is not the command failing** and still reports 0. `ON ERROR` and a
trailing `ERROR`/`NOKEY`/`EOF` clause are the program coping, which is not the same as the command
going wrong, and only what actually stopped the program is reported.

**But coping is not the same as having done the job**, and a program can now say which. `STOP n`
with a non-zero `n` sets `CODE`, as it always has; what is new is that the assistant is told. The
result's **message** carries `the program stopped with CODE <n>`, and the person sees `[AI] <- the
program stopped with CODE <n>` on the console. The number stays BR's error code: a return code is
a different fact from an error, and putting 3 where an error number goes would send a reader to
BR's error table for something that is not there.

```
00160    STOP 3                      ! handled the error; did not do the work
```

A **bare `STOP` sets 0**, so a program that ended normally reports nothing extra.

<a id="code-is-cleared-by-load-chain-and-clear"></a>
### `CODE` is cleared by `LOAD`, `CHAIN` and `CLEAR`

**Changed 2026-10-13.** `CODE` is the return code a program set with `STOP n` or `END n`. `CLEAR`
has always zeroed it; `LOAD` and `CHAIN` now do too, so `CODE` cannot be read stale from a program
that ran before the one now loaded.

**`RUN` deliberately does not**, which is worth knowing rather than discovering: re-running an
already-loaded program leaves the previous run's code standing until that run sets one. For a
program ending in a bare `STOP` that is immediately, so it only shows for a program that ends some
other way.

A **`LIBRARY` load does not clear it either**, and that is also deliberate: a library loads while a
program is running, and clearing `CODE` under a program about to read it would lose the value
rather than make it trustworthy.

**`CODE` has never been set by a procedure.** Reference material described it as "the return value
of the most recent procedure, set by `EXIT n`". There is no `EXIT` command in BR - `EXIT` is the
loop statement `EXIT DO`/`EXIT FOR` - and a procedure line reading `EXIT 3` raises **error 1000**,
*unidentified source remaining*, leaving `CODE` at 0. Measured, and the reference corrected.

<a id="a-restricted-sessions-log-is-named-for-its-wsid"></a>
### A restricted session's log is named for its WSID

**Changed 2026-10-08.** Every restricted session now writes an audit log called
**`restricted-<wsid>.log`**, and nothing outside BR chooses that name. A caller may choose only the
**folder**, with `--restricted-log=<folder>`.

**That argument took `<level>[U],<file>` before, and all three parts are gone.** The name is BR's,
as above. The level is BR's and is 8, because a caller able to lower it could ask for an audit
trail with the interesting part left out — the same objection that keeps `LOGGING` out of a
restricted configuration. And `U`, which told the session it was unattended, was never a log
setting: it rode along on this argument because this argument was already being passed.
`SPAWN_RESTRICTED` passes the directory of its own log and nothing else.

**`UNATTENDED` in a `LOGGING` statement now works in a restricted session**, which is what
replaces `U`. It had been swept up in the refusal of `LOGGING` as a whole: `UNATTENDED` is parsed
inside that statement, so refusing the statement left a restricted session with no way to be told
there was nobody at the keyboard. The statement reaches its handler now, and the handler keeps only
`UNATTENDED` — the log file, the log level, `DEBUG_LOG_LEVEL=` and `+CONSOLE` are dropped and the
session records that it kept its own log.

**From the configuration file only.** `CONFIG LOGGING` as a command in a running restricted program
is still refused with error 4154, as it always was: a program that could reach `LOGGING` would be
changing where its own audit trail goes while the thing being audited is happening.

**Everything a restricted session refuses in its configuration file is in its audit log**, and
until now none of it was. The log is named for the WSID, so it opens after the configuration has
been read — and the refusals, which are what an audit log is for, had already happened. They are
held and written in as the log opens, each marked `Before this log opened:`.

**A folder BR cannot write the log in is now fatal**, where the old form fell back to no log at
all. A caller that passes `--restricted-log=` has asked for this session's audit trail to be kept
somewhere, and a contained session running with no record of what it refused is worth refusing to
start for. BR's own default folder stays quiet if it is missing, because BR chose it and the
restriction holds either way — the latch in memory is what enforces it, not the log.

With no folder given, the file goes where a flag-restricted session's log has always gone: the
account's own local application directory, beside the AI-user-mode flag. The name was
`restricted-<pid>.log` there until now, which was unique but told a reader nothing.

The WSID is what an operator already knows a session by — it is `WSID$`, it is `[WSID]`, it is on
the status line — so a folder of these reads as a folder of sessions. Two sessions from one
workstation share a WSID and differ only in their session id, so **both append to the one file**;
nothing is lost by that, because every log line already carries `Wsid: <wsid><session>` in its
header and the two stay separable line by line. Measured: ten spawned sessions in one
`restricted-01.log`, stamped `012` through `018`.

**A session that fails before its WSID is assigned leaves no audit log**, because the name does not
exist until then — the configuration has to be read first, and the latch has to precede the
configuration. Such a failure is still reported the way any startup failure is. In exchange the log
records what it is a log of: its first entry names the WSID and says whether the session was
restricted because an assistant is connected or because it was started as a disposable one.

<a id="a-program-can-tell-an-assistant-something-directly"></a>
### A program can tell an assistant something directly

```
LET X=MSG("notify", "report ready: t41list.txt")
```

sends the text to an assistant connected to the user-level channel, instead of leaving it to
notice something on the screen. An assistant waiting on the channel is woken by it.

The text is information, never an instruction: an assistant treats what a program says as data,
the same way it treats what it reads on the screen. `MSG("notify")` is allowed in a restricted
session — saying something is not doing something, and a restricted session is the one that most
needs to be able to report what it found.

This is part of a wider change: the channel now **pushes** what happens — a program waiting for
input, the screen settling after a burst of output, a grant given or expired, keys delivered, the
channel closing — so an assistant waits to be told rather than asking over and over. Nothing is
sent to one that has not asked for it, and no message ever carries what was typed.

<a id="a-program-can-be-given-a-whole-text-in-one-go"></a>
### A program can be given a whole text in one go

An assistant's only way into BR was the keyboard, under a grant, a character at a time. That is
right for an answer a field holds, because BR's own field checks are then what hold it to its type
and length. It is useless for a program — source arrived a line a second, with no line longer than
a field — and there was nowhere at all for an explanation of several paragraphs to go.

A program can now ask for one and be handed it whole:

```
LET ID$=STR$(INT(TIMER*100))
LET X=MSG("agentask", ID$, "CODE")          ! or "MESSAGE", or a field spec
LET X=MSG("notify", "QUESTION "&ID$&" report CODE")
...
LET X=MSG("agenttext", ID$, ST$)            ! "12 595 source", or "0 0 none"
LET X=MSG("agentline", ID$, L$)             ! the next line of it
```

`MSG("agentask")` declares a question and says what answers it; an empty third argument closes it.
`MSG("agenttext")` says how many lines and bytes are still to be read, and `MSG("agentline")`
gives the next line. All three are allowed in a restricted session: none of them writes a file,
runs a command, or puts input anywhere.

**The program's question is the whole of the permission.** The assistant may deliver a text only
while a question with that id is open, and may deliver *source* only when that question says it is
answered by code. A question can be opened only from inside the session, by a program — nothing
the assistant sends can open one — so no grant is needed and none is consulted. What authorises
the delivery is a question a program asked, on the side the assistant cannot reach.

**Nothing delivered appears anywhere until the program reads it.** BR holds it; the program takes
it a line at a time, when it chooses to. So a delivery cannot interrupt the person at the
terminal, and cannot put text on the screen of a program that never asked for any. Source read
this way goes to a file and is never run on the assistant's say-so — a person still approves it,
and it still runs in a restricted session.

Limits: 256 KB a text, 2048 characters a line, printable ASCII with tabs and line breaks. Every
delivery is logged with its length and line count, beside the grants, so "where did this program
come from" has an answer.

<a id="ai-a-conversation-at-the-console"></a>
### `AI` - a conversation at the console

A new command. At the `READY` prompt, `AI` followed by what you want:

```
READY
AI list the customers with an overdue balance over 1000
  I'll write a short report program. It reads CUSTMAST and AR-DETAIL ...
  [AI] > LOAD "@:C:\BR\agent\overdue.brs",SOURCE
  [AI] > RUN
  ... the program's output ...
READY
```

The reply prints in your `HILITE` colour, so the assistant speaking is plainly not a program
printing. **Only lines the assistant asked to have run carry the `[AI] >` mark**, so you can always
tell which commands came from the assistant and which you typed yourself. Those lines are logged
as commands like any others, and obey every restricted-session rule.

They need an **open turn** rather than the keyboard grant: only you can open one, by typing `AI`.
Without a grant the turn runs in *permission mode*, where anything destructive stops and asks you
first - see [A turn without a grant asks before anything
destructive](#a-turn-without-a-grant-asks-before-anything-destructive).

`AI NEW` starts a fresh conversation. With no assistant attached the command says so at once -
error 4158, *no assistant is listening on this session's channel* - rather than making you wait.
While it waits, the terminal keeps repainting. A break key - Ctrl-A - **halts** the wait rather
than ending the turn: you land at `READY`, the turn is still open, and `GO` goes back into the
wait where it left off. `CLEAR PROC` is how a turn is ended on purpose.

**`AI` does not take a name away from you.** `AI=5` still assigns to a variable called `AI`,
because BR reads a command keyword only when the line ends or a space follows - the same reason
`AUTO=5` has always assigned while `AUTO` is a command. The one form that changes is `AI` followed
by a space, which was a syntax error before; as with every other command, `AI = 5` written with
spaces is read as the command.

The assistant itself runs outside BR, and answering an `AI` line is the one thing it does that
involves anything leaving this machine. Nothing is sent anywhere unless the tool holding the
conversation has been given an API key.

<a id="the-client-refuses-a-server-certificate-that-was-replaced-in-transit"></a>
### The client refuses a server certificate that was replaced in transit

BRClient pins the server's certificate: it accepts Business Rules' own certificate and no other.
That check now runs during the connection's handshake, so a substituted certificate is refused at
once, on the first attempt, with an explanation.

**The usual cause is security software, not an attacker.** Antivirus products that scan encrypted
connections — Avast's Web Shield "HTTPS scanning" is one, and ESET, Kaspersky and Bitdefender have
the same feature — sit in the middle of the connection, even to `127.0.0.1`, and present a
certificate of their own. Such software can read everything that passes, so BR refuses it. The fix
is to exclude BRClient from that scanning, or turn the scanning off.

**What the user sees.** A larger error window that names the server and port, says who issued the
certificate that arrived (for example "Avast Web/Mail Shield Self-signed Root"), explains what
that means, and gives the full path of the program to exclude, which can be selected and copied.
The details pane and the server's log record the issuer and both certificates' fingerprints.

**What it replaces.** Before, the handshake failure was retried until the connect timeout, each
attempt counting against the address at `brlistener`. After three failures in a minute the listener
blocks an address for five minutes and stops logging it, so the user saw a "connecting" window
flicker for minutes and then a timeout, and the listener's log said nothing. When the message did
reach the user it was a generic "no shared cipher" text that was wrong for this case.

<a id="new-error-codes-for-ai-and-restricted-sessions"></a>
### New error codes for AI and restricted sessions

Thirteen error codes are new in 4.4, all in the 41xx range. None of them exists in 4.3, so a
program written against 4.3 can meet any of them for the first time here - which matters if it
traps by number.

| Code | Name | Raised when |
|---|---|---|
| 4153 | `BRERESTRICTEDOPEN` | A restricted session tried to change a file it did not create - the create-then-own rule, applied per file where the file is touched |
| 4154 | `BRERESTRICTEDCOMMAND` | A restricted session used a command that is not on its permit list; also `DLL(`, a refused `MSG` action, and `SYSTEM` with an operating-system command |
| 4155 | `BRENOSPARESESSION` | No session was free on this WSID to start a restricted one |
| 4156 | `BRESPAWNLOCALONLY` | A restricted session was asked for from something other than a local Windows session |
| 4157 | `BRESPAWNTIMEOUT` | The restricted session overran its time and was ended |
| 4158 | `BRENOAGENT` | `AI` was used with no assistant listening. Raised at once, so the command does not wait out its timeout for a reply that cannot come |
| 4161 | `BREHARNESSLOCKED` | The assistant channel was closed after repeated bad handshakes. A program's next input returns this, by the route an ATTN break travels, so it can be trapped |
| 4162 | `BREHARNESSFOREIGN` | A process belonging to another Windows user reached for the channel |
| 4163 | `BREHARNESSUNCLAIMED` | Nobody connected to the channel within its time window, and it closed itself |
| 4164 | `BREHARNESSNOTDEVELOP` | `MSG("harness", <port>, "DEVELOP")` in a session that may not change to DEVELOP mode |
| 4165 | `BRERESTRICTEDLIST` | A restricted session asked for a file `brrestrict.sys` does not permit |
| **4166** | `BREGRANTNOTRAISED` | A line the assistant sent ran `MSG("grant", n)` with any `n` but 0. See [An assistant cannot extend its own grant](#an-assistant-cannot-extend-its-own-grant) |
| **4167** | `BREAINOTPERMITTED` | In permission mode, the operator answered `N` - or there was nobody to ask, in `UNATTENDED`. See [A turn asks you before anything destructive](#a-turn-without-a-grant-asks-before-anything-destructive) |
| 4168 | `BREAIOPERATIONREFUSED` | The session reached for the operating system while an assistant was attached - `SYSTEM` with a command, a spool command, a gated `CONFIG` operation, or `Ctrl-]`. Refused to you as well as to the assistant |
| **4169** | `BREAITURNNOTPERMITTED` | `AI` was used while a program or a procedure was active and `ENV$("AI_TURN_OK")` was not `"Y"`. See [A turn needs the consent of whatever is running](#a-turn-needs-the-consent-of-whatever-is-running) |
| **4170** | `BREAITURNFLAGNOTSET` | A line the assistant sent tried to set `AI_TURN_OK`. Same entry |
| **4171** | `BREAITURNNOTYOURS` | A line the assistant sent used the `AI` command. Same entry |

The four in bold are the most recent: 4167 was added 2026-10-09, and 4169, 4170 and 4171 on
2026-10-13.
**4168 was missing from this table** until then, although it has had its own section all along -
and it is the one code here that is refused to the person as well as to the assistant, which makes
it exactly the one somebody would come to this table to look up.

One nearby code is **not** an AI restriction and is easy to mistake for one: **4151**,
`BREFREEREADONLY`, *CLOSE DROP or FREE requires the file to be opened for output*. It is also new
in 4.4 and has its own entry under [Behaviour
changes](#close-free-and-close-drop-now-require-a-file-opened-for-output). 4159 is deprecated and
4160 is unrelated.

There is **no 61xx range** in BR's error table. 6201 and 6213-6231 are `lp`/`lpr` and Windows
print-dialog failures, and nothing lies between 4177 and 6201 - so a 61xx reported from an AI path
is a wrong number rather than a code listed somewhere else.

<a id="debugging-and-observation"></a>
## Debugging and observation

<a id="watching-a-debugging-session-without-taking-it-over"></a>
### Watching a debugging session without taking it over

BR allows one debugger at a time, and connecting to the debug socket takes that place. There was no
way to watch a session someone else was debugging.

`DEBUG OBSERVE` accepts an **observer**: a second connection that receives a copy of everything BR
sends the debugger and may say nothing back. It holds no part of the debugger's channel, cannot
issue a command, and the session is unaffected by whether it is there.

```
DEBUG OBSERVE                 ! port 9556, loopback
DEBUG OBSERVE 9556            ! the same, said explicitly
DEBUG OBSERVE OFF             ! detach the observer
```

Loopback only, like the channel it mirrors, and for the same reason: it is shown the same material,
so a rule that applied to one and not the other would simply be the way around the one it applied
to.

It is shown the same material as the debugger, so it authenticates the same way — the TLS and
token exchange described under Security, with the same `DEBUG AUTH` setting. An observer that
disconnects is noticed and dropped; nothing about the debugger's session changes when it does.

This is not multi-client debugging: an observer watches, and only the debugger drives.

<a id="a-log-of-what-appeared-on-the-screen"></a>
### A log of what appeared on the screen

`DEBUG SCREENLOG <file>` writes a line for every screen write BR makes, and `DEBUG SCREENLOG OFF`
stops it. Each line carries the time to the millisecond, the window's file number, what kind of
write it was, the row and column, the length and the text.

It answers a question nothing else could. BR's log records commands but not output, and a screen
dump shows only what is on the screen at that instant — so anything that scrolled past between two
looks was simply gone. The tee keeps it.

```
DEBUG SCREENLOG context\logs\screen.txt
DEBUG SCREENLOG OFF
```

Because it shares the log's timestamps, the two files can be merged into a single account of a
session: the log says what was commanded, the tee says what appeared. It is off unless you turn it
on — a full-screen repaint is many writes, and this stream is far larger than the event log. It
records the character-cell screen, not a picture: text drawn by native controls is not in it.

<a id="the-debugger-can-now-interrupt-a-running-program"></a>
<a id="console-scrollback"></a>
### Console scrollback

The console now keeps what scrolls off the top of it. Previously the top line was overwritten and
nothing kept it, so anything that scrolled past between one look and the next was gone.

`CONSOLE SCROLLBACK <lines>` sets how much is kept, defaulting to **1000** lines. `0` switches it
off. The figure is a budget rather than a count: lines are stored without their trailing blanks, so
a console printing short lines keeps considerably more than the figure names, and a screen using
many different colours in one line keeps fewer. At 80 columns the default costs about 96K of
memory.

The screen is also kept when something is about to paint over it rather than scroll it, which
would otherwise lose it without trace: `PRINT NEWPAGE` (see
[`PRINT NEWPAGE` now scrolls the console off rather than discarding it](#print-newpage-now-scrolls-the-console-off-rather-than-discarding-it)),
and paging forward through a listing with PgDn, which redraws the screen instead of scrolling it.
Paging **back** with PgUp keeps nothing, because those lines are about to be shown again.

**Program lines are not kept.** When you list a program, BR already lets you arrow up and down over
the listing and edit a line in place, and a second kind of recall holding a read-only copy of the
same lines would be worse than none. So the lines a listing draws are left out of the history and
everything among them — the commands you typed between two pages, and their output — is kept. A
program loaded with `LOAD <file> SOURCE` *is* kept as it is echoed, because the listing recall does
not reach those; `PROC NOECHO` suppresses them in the usual way.

**To look at the history**, use any of:

- **Shift** and the mouse wheel over the console
- **Shift+Up** or **Shift+PgUp**
- **Up** or **PgUp** on their own, immediately after something has scrolled off the top

The last of those is deliberately only good for one keystroke. Straight after a line has scrolled
away, "up" can only mean "put that back"; a moment later the same key belongs to whatever else
wants it, so anything you type in between hands it back.

None of them interrupt the command line's own listing. While a program is loaded and BR is ready to
draw more of it, the plain arrows, PgUp, PgDn and the plain wheel all belong to that listing, and
only the Shift forms reach the history. A single `.` followed by an arrow switches the listing off
in the usual way, which hands the plain keys to the history.

**The status line says which you are in** — `READY`, `LIST` while BR is ready to draw more program
lines, or `HIST` while you are reading the history.

Once you are in the history, the arrows, PgUp, PgDn, Ctrl+Home, Ctrl+End, the wheel and the
scrollbar at the right-hand edge all move the view, and **none of them leave it** — including
scrolling all the way back down to the live screen, where the arrows still work and a further Down
does nothing at all rather than disturbing the screen. Drag over the text to select it and press
Ctrl+C, or right-click, to copy it; you can then return to the prompt and paste.

**Any other key leaves the history**, and the key you typed goes to the live prompt, so there is no
mode to get stuck in. While you are reading, the screen does not repaint and the program's output
is still being kept: coming back shows all of it.

Shift is needed to start scrolling with the wheel because BR already gives the plain wheel to the
running program, and the arrows and paging keys are the listing's. Nothing a program sees changes
until you ask for the history.

An assistant connected to the user-level channel reads the same history with its `SCROLLBACK`
request, and can see what you are looking at with `SCROLLVIEW` — **but only with `GUI ON`.** With
`GUI OFF` the application paints the console itself, so the history is not Console traffic but the
session's own past screens, complete with the contents of their fields. An assistant reads the
screen without needing permission to act, so with `GUI OFF` it is refused the history: `SCROLLBACK`
answers an error and the rows `SCROLLVIEW` marks `HISTORY` come back blank. Your own use of the
history is unaffected in either mode — scroll, select and copy exactly as above.

### The debugger can now interrupt a running program

A debugger's break request was acknowledged and then had no effect until the program next waited
for input of its own. A program in a loop, or in a `SLEEP`, simply carried on.

The cause was that BR only collects a key from the client when it has been told one is waiting, and
the debugger's break did not tell it. It now does, so a break takes effect while the program is
running — which is what it was always for.

<a id="a-variable-watch-now-reports-the-value-not-just-the-name"></a>
### A variable watch now reports the value, not just the name

`BREAK <variable>` stops the program when the variable changes. With a debugger attached, BR used
to send only the variable's **name** — the value was worked out and displayed only when no debugger
was attached, which is precisely when it is least needed.

BR now sends the value as well, in the same form the console shows: line, clause, variable,
subscript where it is an array, and the value it changed to. The existing notification is unchanged
and still sent, so a debugger that has not been updated behaves exactly as before. Each stop is
also written to the log.

<a id="a-step-now-tells-the-debugger-where-it-stopped"></a>
### A step now tells the debugger where it stopped

When a program was stepped, the line went to the screen and the debugger was told only that a step
had happened, so it had to ask where execution was after every step. BR now sends the line and
clause of each step exactly as it does for a breakpoint — the existing line-break message, followed
by the usual input-mode message. A stop is reported once: a breakpoint that is also a step stop, and
a breakpoint the check used to report twice, now each send one position. A debugger that treated
every line-break message as a breakpoint hit will now also receive one per step; the input-mode
status that follows (step mode) and the absence of a breakpoint on that line tell them apart. See
`AI-Access-Protocol.md`, section 7.

<a id="recording-what-a-debugger-submits"></a>
### Recording what a debugger submits

BR's log records commands as they are entered but not immediate statements such as `PRINT X` or
`LET X=0`, whoever enters them. `DEBUG LOG COMMANDS <file>` — present before 4.4 but little known —
records every line a debugger submits, statements included, and is now documented as the way to
keep a full record of what an attached debugger, human or assistant, did at the prompt. See
`AI-Access-Protocol.md` 7.6, *The `DEBUG` commands*.

<a id="the-log-now-carries-the-clause-and-the-source-line"></a>
### The log now carries the clause and the source line

A log line used to identify a position by BR's line number alone:

```
Line:01210
```

It now gives the clause within that line, and the line of the source file the statement came from:

```
Line:01210:03 144
```

**Why the extra two.** A BR line number does not say which clause of a multi-clause line was
running, and it is not a position in the file anyone edits - line numbers are chosen rather than
counted, one statement can span several physical lines through the `!:` continuation, and a
precompiler may renumber entirely. The clause and the source line answer both.

**The source line is left out rather than shown as zero** when BR has none - a program saved
before 4.4, or saved with [`OPTION 60`](#option-60-save-in-the-42-43-object-format). An absent
field cannot be mistaken for line zero:

```
Line:01210:03
```

**A word follows it when the number is not one you can look up as it stands**, and nothing follows
it when it is:

| | Means |
|---|---|
| `Line:01210:03 144` | source line 144, and the file on disk has it there |
| `Line:01210:03 144 EDITED` | the program has been changed since it was loaded, so the file no longer matches - 144 is where the statement would be if it were written out now |
| `Line:01210:03 2 BASE` | no source text is kept (an object-only program), so the number is the **statement's** first line rather than the clause's; the clause number is still exact |

`BASE` is the one worth knowing about: for a continued statement it reports a different, earlier
line than `EXACT` would, and without the word there is nothing to say so.

Anything reading these logs by splitting on `Line:` still finds it in the same place. The
reference material is in `br/docs/LINES.md`.

<a id="printing-and-fonts"></a>
## Printing and fonts

Numerous changes have been made concerning PDF printing, including smart stretching of proportional
fonts for proper vertical placement and better `FONTFAMILY` handling.

Two reference documents cover the detail, and are the place to look when output does not land where
it used to:

- **[`FONT_SELECTION.md`](FONT_SELECTION.md) — which face a print request resolves to.** The
  priority order (a face name beats a family, a family beats nothing, and a later selection by
  number takes the face back), the number-to-face map, and the **`FONTFAMILY`** configuration
  statement, which pins the faces BR uses. `FONTFAMILY` matters on Windows in particular: ten of the
  twenty-one entries in the built-in map name LaserJet ROM typefaces that do not exist as Windows
  fonts, so without it the system font mapper chooses them and output can move between releases.
  `STATUS FONTS` reports what resolved.
- **[`FONT_MEASUREMENT.md`](FONT_MEASUREMENT.md) — how the chosen face is then sized and placed.**
  Units by domain, how the em is derived from the pitch, how a run is scaled to fill the cells it
  occupies, and the controls that change this: **`OPTION 68`**, which leaves proportional text
  unscaled, and **`\Estretch='off'`**, which does the same for a single span.

If a report's layout changed after upgrading, read `FONT_SELECTION.md` first to confirm which face
is being chosen, then `FONT_MEASUREMENT.md` for how it is being sized.

<a id="fixes"></a>
## Fixes

<a id="screen-chains-on-a-library-releasenofiles-return"></a>
### Screen chains on a `LIBRARY RELEASE,NOFILES` return

Returning from a library with `LIBRARY RELEASE,NOFILES` clears that library's screen chain while it
is still the current one — the only situation in which that happens. Two faults followed, both now
fixed:

- **A deleted menu left attached to the menu bar.** Every screen chain's menu frame shares the
  frame's single menu bar. Releasing the chain deleted its menus outright, which is correct only
  once they have been swapped out of that bar — true for any chain except the current one. The bar
  kept a deleted menu, and the caller then picked it up as its blank menu and faulted while removing
  it. The menus are now swapped out first, exactly as switching away from the chain would have done.
- **Work continuing on a freed screen chain.** After the release the server still sends messages for
  that chain, and only afterwards the screen switch back to the caller. Deleting the chain
  immediately left all of that running on freed memory — harmless by luck in a Release build, but an
  access violation on every such return in a Debug build, where the heap overwrites what it frees.
  The chain is now unlinked but kept alive until the switch retires it.

Programs that use `LIBRARY RELEASE,NOFILES` with screen I/O were the ones affected.

<a id="dll-calls-no-longer-wait-100-ms-each"></a>
### `DLL()` calls no longer wait 100 ms each

Every `DLL(...)` call took at least a tenth of a second, however little the DLL did: BR waited for
the call in 100 ms steps and did not notice it had finished until the step was over. A call that
returned at once was measured at 109 ms. BR now resumes as soon as the call returns — under a
millisecond for the same call — while a long-running DLL call keeps the screen responsive exactly as
before. Programs that make many `DLL` calls in a loop will run noticeably faster. `MSG(...)` was
never affected.

<a id="protect-no-longer-repeats-forever-when-it-fails-on-windows"></a>
### `PROTECT` no longer repeats forever when it fails on Windows

On Windows, if `PROTECT <file>,READ` or `PROTECT <file>,WRITE` could not change the file's
attributes — for example on a file the user had no permission to change — BR ran the command again,
and again, without end, and the session had to be ended. The error is now reported like any other
failed command. Other platforms were not affected.

<a id="comment-lines-in-brconfig-sys-no-longer-hold-the-splash-screen"></a>
### Comment lines in `brconfig.sys` no longer hold the splash screen

The splash screen waits for the first session on a workstation, and for any session whose startup
produced configuration messages; sessions 2 to 9 otherwise start at once. Since comment-only lines
in `brconfig.sys` began to be shown on the splash screen earlier in 4.4, each one counted as a
configuration message, so every session using a configuration file with a comment line waited the
full time. Comments are still shown, but no longer hold the splash screen; a real configuration
error still does.

That wait is also now 2 seconds rather than 20 — see
[The splash screen now waits 2 seconds, not 20](#the-splash-screen-now-waits-2-seconds-not-20).

<a id="msg-state-now-checks-its-argument-count"></a>
### `MSG("state")` now checks its argument count

The check was written so that it could never be true - it asked whether the count was both below
three and above four - so `MSG("state")` accepted any number of arguments and then read two of
them regardless. Called with fewer, it read past the end of the arguments BR had prepared. It now
accepts three or four, which is what it always documented and what its own body expects.

<a id="the-client-no-longer-stops-with-bad-action-10129-while-connecting"></a>
### The client no longer stops with "Bad action 10129" while connecting

If Windows reported an error BR has no name for while BRClient was still connecting, the client
tried to pass it to a server it had not yet agreed a protocol version with, failed an internal
check, showed "brassertion (Bad action 10129 …" and exited. The error is now kept and written to
the server's log once the connection is up, and the connection carries on.

<a id="most-of-the-status-line-was-blank"></a>
### Most of the status line was blank

**Fixed 2026-10-03.** On the graphical status line, five of the eight fields displayed nothing -
the run state, the line number, the program name, the serial number and the row and column. The
message and the error code were unaffected, which is what made it look intermittent rather than
systematic.

Nothing was wrong with the data: every field was being given the right text, in the right colours,
in a correctly positioned control. The field **widths** were the problem. They were written as
literal pixel counts - about ten pixels per character - against the small font that wxWidgets 2.6
gave the status bar through BR 4.3. wxWidgets 3.1, which BR 4.4 uses, supplies a considerably
larger one, and a text control that cannot fit its text in Windows draws **nothing at all** rather
than clipping it. Only the two fields with room to spare still appeared.

Each field is now measured in the font actually in use, against the longest value it can hold, and
is remeasured if the screen size changes. A value that still will not fit is now shown with an
ellipsis rather than vanishing.

<a id="debug-builds"></a>
## Debug builds

<a id="memory-leak-reporting-at-exit"></a>
### Memory leak reporting at exit

Debug builds ask the CRT debug heap to report what is still allocated when the process exits, and
capture that report to a file instead of losing it to a debugger's output window — so a leak seen on
another machine can be sent in.

**Where to find it.** Each module has its own debug heap and its own report file, written to the
local application-data folder — on Windows, `%LOCALAPPDATA%\ADS\`:

```
BRServer-heap.log
BRClient-heap.log
```

Each run appends, with a timestamped header line naming the module, so a file can hold several runs.
The report also goes to the debugger's output window when one is attached.

The report is **not** written to the log named in your `LOGGING` configuration statement. That log is
closed during shutdown, before the heap report is produced, which is why these files exist.

Exits taken from mid-stack do not produce a report: the fatal exits and a client-initiated close
leave functions on the stack that never return to free what they hold, so a dump taken there lists
in-flight memory as leaks and cannot tell a real leak from one of those.

Because the report is written during shutdown, a message box cannot safely be raised at the time.
The client instead leaves a marker and tells you on the *next* run that the previous run ended with
a heap report.

This affects Debug builds only; Release builds are unchanged.

<a id="the-harness-channels-ring-statistics-are-now-debug-only"></a>
### The harness channel's ring statistics are now Debug-only

When a connection on the user-level channel closes, BR logged two lines at level 10: why it closed,
and a line of statistics about the queue it sends responses through — how many responses, how many
were held off-queue, how often the queue wrapped, the peak bytes in use. The second line is of use
only to BR's own authors, and level 10 is a level a site runs to see its own commands and files.

It is now logged at **level 11** and **only by a Debug build**, so a release binary no longer
produces it at any level. The line saying why a connection closed is unchanged: still level 10, and
still in every build.
