---
title: SPAWN_RESTRICTED
file: SPAWN_RESTRICTED.md
category: 10-language
subcategory: 10-language/data-manipulation/system-functions
kind: function
since: BR 5.0
related: [internal function, restricted session, PROC, SLEEP, WSID$, SESSION$, DEBUG_STR, LOGGING, audit log, 4154, 4155, 4156, 4157]
---
`SPAWN_RESTRICTED(command$ [, config$ [, wait [, label$]]])`

Starts a **new BR session on this workstation ID** — the next free session number — restricted from
its first moment, and runs `command$` as that session's startup command, typically `PROC <file>`.

This is how a session runs something it does not trust **without restricting itself**: the new
session is restricted and disposable; the one that called it is neither.

## Arguments

| Argument | Meaning |
|---|---|
| `command$` | the new session's startup command, e.g. `"PROC report.prc"` |
| `config$` | its configuration file; defaults to **this session's** |
| `wait` | seconds to wait for it to finish; omitted or `0` means do not wait |
| `label$` | what the session is for, in a few words. It opens the new session's audit log and is in this session's own record of starting it, so a reader can tell several children apart. Control characters become spaces, a double quote becomes a single one, and it is cut to 200 characters |

## What it returns

- **Without a `wait`, or with `0`:** the new process's **id**, at once.
- **With a `wait`:** the session's **exit code**. The wait yields the way [`SLEEP`](spec.md#system-info)
  does, so the screen keeps repainting and ATTN still works while the child runs.
- A session still running when the wait runs out **is ended**, and the call raises **4157**. A
  disposable session nobody is waiting for has no reason to keep holding a session number.
- Pressing a key that takes the caller elsewhere stops the waiting, raises `BRETRAPSLEEPKEY`, and
  **leaves the child running** to finish its own work.

## Errors

| Code | When |
|---|---|
| `4154` | a **restricted** session called it. Nothing in the child could be less restricted than its parent; the refusal is because a program generated for a user has no business spending the WSID's sessions |
| `4155` | no session is free. **One session per workstation ID is always kept back**, so a spawn can never take the last one a person might need — with eight of nine in use, this is raised |
| `4156` | not local Windows. It is available in local mode on Windows and raises this elsewhere for now |
| `4157` | the session did not finish within `wait` and was ended |

Every refusal is logged as a security event.

## The restriction holds before the configuration is read

The new session is latched **before it reads its configuration file**, and the ordering is the whole
point: `config$` is the *caller's* choice, so the configuration operations a restricted session
refuses are refused **in that file**, not applied and then locked.

Since `LOGGING` and `WBSERVER` are among them, the new session is handed the **current session's**
`wbserver.dat`, and the **folder** of the current session's log. It writes its own audit log there,
`restricted-<SESSION$>.log` (for example `restricted-012.log` for WSID 01, session 2), at level 8;
when the current session is not logging, it goes in `%LOCALAPPDATA%\ADS`. The log's first entry
says why the session is restricted and, when `label$` was given, what it was started for:

```text
Restricted-session audit log for session 012, started for "C1 order check": this session may ...
```

The new session can add notes of its own with [`DEBUG_STR`](spec.md#debug_str). In a restricted
session they are written as `Program note: <text>`, on one line, at level 5 or above, so they cannot
pass for BR's own entries.

## Example

```text
00100    LET PID = SPAWN_RESTRICTED("PROC "&REPORT$)           ! start it, carry on
00110    LET RC  = SPAWN_RESTRICTED("PROC "&REPORT$, "", 300)  ! or wait 5 minutes
00115    LET RC  = SPAWN_RESTRICTED("PROC "&REPORT$, "", 300, "month-end report")  ! labelled
00120    IF RC <> 0 THEN PRINT "the report ended with "; RC
```

## See also

- [system-functions](spec.md#system-info) — `WSID$`, `SESSION$`, `SLEEP`
- [LOGGING in a restricted session](../../../00-configuration/config-directives/LOGGING.md#restricted-session) — the audit log, its name, its level and the program's notes
- [90-reference/error-codes](../../../90-reference/error-codes/_index.md) — 4154 to 4157
- [BRRESTRICT.SYS](../../../00-configuration/config-directives/BRRESTRICT.SYS.md) — the file list, which bounds the new session as it bounds every session
