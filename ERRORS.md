# Kit Errors

Please record any context kit errors here that are found in the course of its use.
---

## 2026-11-01: DISPLAY MENU and FKEY reference (found against BR 5.0 source, commit d21448a)

- `br_tree/20-io-screen/controls/display_menu.md` omits two status flags the runtime honours: `G`
  (radio item, implies checkable) and `K<spec>` (raise this key instead of FKEY 98, implies `E`;
  must come last, because flags after the `K` are not read). Source: `br/brs/menu.h` `processStatus`.
- The same page says `DISPLAY MENU` is Windows only, but the unix `guidll` build also compiles
  `menu.o`. Not run on unix.
- `br_tree/20-io-screen/windows-cursor/FKEY.md` line 103 gives "second right" as 101. In the field
  loop `KB_MOUSE_DBLRIGHT` does nothing (`br/brs/fieldin.cpp:1764`), and 101 is `FKEY_TIMEOUT`.
  From reading the source; not measured.
- `br_tree/90-reference/error-codes/0840.md` describes error 840 for bad menu indenting. Measured
  on BR 5.0: bad indentation and mismatched array sizes raise no error from `DISPLAY MENU`, because
  the client sends its reply before doing the work (`br/brs/remoteargs.cpp:761`). This is a BR bug
  rather than a page error, recorded here so that the page is not trusted meanwhile.

## 2026-11-01: HTTP_SERVER.md (measured on BR 5.0, commit d21448a)

- `br_tree/60-integration/web/HTTP_SERVER.md` line 89 says an OPEN on the same port by another BR
  session gives 740. Measured: 752. 740 comes only from a second OPEN in the same BR.
- §3.2 step 5 says a good start writes the certificate and `HTTP server started` lines to `LOG=`.
  Those are level 6 events: with no `LOGGING` line the log stayed at 0 bytes.
- §2.9 says the reason for 750 is in the server log, including `HTTPS` without `CERT=`. That case
  goes to the BR log only, and with no `LOGGING` line it is recorded nowhere.
- §3.2 step 3 says "Keep the keyword order (§1)", but §1 says the keywords may be in any order.
- §2.1 says `NAME=` is required syntax. Measured: `OPEN #1: "http=server"` opens.
- §2.1 shows `OUTIN`, but `DISPLAY, INPUT` and `DISPLAY, OUTPUT` also open; `PRINT` or `LINPUT`
  then fails 721.
- §1 says `BIND=` takes a numeric address. Measured: `BIND=localhost` works.
- §1 omits the port limits. `CONFIG HTTP 0` is accepted and opens on an unknown port, and a port
  over 65535 gives 752 at the OPEN.
- `br_tree/90-reference/error-codes/0746.md` and the §2.9 wording "not responding to active
  inquiry" hide what the code means: no current request.

## 2026-11-01: HTTP=SERVER error codes 0763-0799 (edited in place in this copy of the kit)

`br_tree/90-reference/error-codes` has new pages 0763-0799 and an updated `_index.md`. Pages 0716,
0740, 0742, 0744, 0746, 0750, 0752, 0754, 0756, 4145, 4270 and 9990 gained a "Setup documentation"
section. `br_tree/60-integration/web/HTTP_SERVER.md` was updated to match, which also corrects its
entries above. The upstream kit needs the same edits, or the next kit update will remove them.
