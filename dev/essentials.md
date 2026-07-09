---
title: BR Language Essentials
file: essentials.md
category: dev
kind: reference
status: 1a
description: The language rules that bite newcomers (and LLMs trained on other BASICs), plus runtime gotchas confirmed empirically while building and RUN-testing a real BR program end to end.
---

# BR Language Essentials

Two kinds of content, both load-bearing:

1. **§1 — core language rules.** Things the written spec states clearly but that read as
   surprising if you're coming from another BASIC or from Python/C-family languages. Per-statement
   detail is in [`statement-semantics.md`](statement-semantics.md) (indexed by
   [`topics.json`](topics.json)); full detail is in [`../br_tree/`](../br_tree/).
2. **§2 onward — runtime gotchas found empirically, not written down anywhere.** These came from
   actually driving a real BR program ([`gen_topics.brs`](gen_topics.brs)) headlessly from
   "compiles clean" to "produces correct output," under `br432g-32.exe` + a `gui off` config with
   `UNATTENDED` logging. Several **documented, spec-correct constructs silently misbehaved** in
   that environment — not because the spec was wrong, but because an unstated size limit or
   line-numbering trap was crossed. **Treat these as "confirmed in at least one BR
   build/config, verify before assuming universal"** — but treat them as real: each was isolated
   with a minimal reproduction before being written down here, not inferred from a single failure.

---

## 1. Core language rules

- **Every line is numbered**; labels go right after the number (`00050 LOOP1: …`).
- **`=` is context-sensitive.** Inside `IF`/`WHILE`/`UNTIL` it means *compare*; elsewhere it
  *assigns*. Use **`:=`** to force assignment inside a condition (must be parenthesized).
- **Operators aren't C/Python.** `&` is **string concatenation**, not bitwise-AND. `^` and `**` are
  **both exponentiation**, not XOR. BR has **no source-level bitwise operators** at all — a
  runtime-internal table once listed `<< >> & | ^`, but those aren't reachable as base-BR source
  operators. **`MOD` is a function only — `MOD(a, b)`, never infix `a MOD b`** (`REM(a, b)` is an
  alias). Full 12-level precedence (tight → loose): 1 `()`/`[]` · 2 `^`/`**` · 3 `*`/`/`/`MOD` ·
  4 `+`/`-` · 5 `&` (concat) · 6 comparison (`=`/`<`/`>`/…) · 7 bare `=` (is-equal) · 8 `NOT`/`~` ·
  9 `AND`/`&&` · 10 `OR`/`||` · 11 `=` assignment · 12 `:=` forced. (Full detail:
  [expressions](../br_tree/10-language/data-manipulation/expressions/spec.md).)
- **String variables end in `$`**; size is declared `DIM NAME$*30`. Arrays are 1-based. Default
  string max (un-`DIM`'d) is **18 characters** — see §2, this is the single biggest source of
  silent runtime failure in practice.
- **Keywords abbreviate on entry** (shortest-unique-prefix; functions and clause words need full
  spelling), but BR **expands them when a program is LISTed** — so `.brs` source always shows full
  keywords. You never read or write abbreviations in source files.
- **I/O carries trailing error clauses**, not exceptions: `READ #1,…: A$ NOKEY L900 EOF L990`.
  Handle `EOF`, `NOKEY`, `IOERR`, `CONV`, `LOCKED` explicitly.
- **`[WSID]`-style substitutions** appear in file names for per-workstation temp files
  (`"SORTCTL.Z[WSID]"`).
- **`DEF`/`FNEND` functions** can have a typed/sized return (`DEF FNX$*255(...)`), optional
  parameters after `;` (which double as the **local-variable idiom** — trailing params the caller
  never passes are fresh 0/null scratch locals each call; an unpassed by-reference optional
  defaults an array to dim 1 and a string to length 18 — the 18-char default again, see §2), and
  by-reference parameters marked `&`. A function name is capped at **30 characters including the
  `FN` prefix**. Two traps: `FN<name>` in a mid-body expression is a
  *recursive call*, not the value-so-far — build an incremental result in a scratch variable, never
  by reading `FN<name>` back (you *may* assign it more than once — last write wins — just never
  read it back); and a function has **one exit** — no early return, `GOTO` a label before `FNEND`.
  **BR skips over `DEF…FNEND` blocks in normal top-to-bottom execution flow** — unlike some other
  BASICs, you do **not** need a `STOP`/`GOTO` guard before a function definition to keep execution
  from falling into it with unset parameters. **See §2 for two more `DEF FN` traps not in the
  written spec at all.**
- **`SELECT CASE … END SELECT` is Lexi-preprocessor syntax, not base BR.** If your program is
  plain `.brs` (not run through the Lexi preprocessor), `SELECT CASE` won't compile — this isn't a
  bug, it's simply unsupported outside Lexi. Use `ON expr GOTO`/`ON expr GOSUB` or chained
  `IF`/`ELSE IF` instead.
- **Plain `INPUT` takes NO prompt argument.** `INPUT "X", A$` does not compile — emit the prompt
  with a separate `PRINT "X"` first, then `INPUT A$` on its own. A lesser-known third form, **plain
  `RINPUT <var>`** (a single variable, not a list, no `FIELDS`), *is* valid: it prints the
  variable's current value and prompts for a replacement.
- **A statement whose own syntax ends in a required colon needs a *second* colon to chain another
  statement on the same physical line.** `CLOSE #n:` terminates the `CLOSE`; `CLOSE #n: STOP` on
  one line mis-parses `STOP` as part of the `CLOSE`. Write `CLOSE #n: : STOP` (two colons) instead.
- **`LIBRARY "name":` with a library name but no function list LOADS that library immediately —
  it does not detach a linkage.** The only way to fully detach a library linkage is to end the main
  program. Don't infer a "no functions ⇒ unlink" meaning from the empty list.

---

## 2. Sizing discipline — the #1 source of silent runtime failure

BR's default string length (18 chars, when nothing is `DIM`'d) doesn't just apply to plain scalar
variables — it applies everywhere a string can implicitly size itself, and overflowing it doesn't
raise a clean, catchable error in at least one observed BR build/config. Instead, an untrapped
overflow (and several other untrapped runtime error classes — see §3) manifests as the runtime
sitting at what looks like a keyboard-input wait — under `UNATTENDED` logging this shows up as
`Input attempted in unattended mode ... line N:S`, which is actually the tell that *something*
overflowed or errored upstream, not that the program is genuinely waiting on the keyboard.

- **Un-`DIM`'d scalar `READ`/`LINPUT` targets default to 18 chars.** A channel-less `READ` into an
  un-`DIM`'d string, or a `LINPUT #n:` into one, silently hits the input-wait fallback instead of a
  clean `SOFLOW` once the source data exceeds 18 chars. **Explicitly `DIM` every scalar that
  receives file or `DATA`-table input**, sized to the real data — not "seems long enough": an array
  sized exactly to an expected item count still overflowed once, one short of the actual count.

- **`DEF FN` string parameters default to 18 chars too, if the signature doesn't size them.**
  `DEF FNX$(P$)` with no `*n` on `P$` silently caps it at 18 chars regardless of the function's own
  declared return size (`DEF FNX$*500(...)` sizes the *return value*, not the parameters — each
  parameter needs its own `*n`). This was, empirically, the most expensive single gotcha to
  diagnose: symptoms that looked like "substring extraction on a parameter breaks with
  backslashes" or "`SREP$` mishandles multi-backslash replacement inside a `DEF FN`" were both red
  herrings — the real cause was always an unsized parameter, and every "fix" that happened to route
  the value through an adequately-`DIM`'d intermediate variable first just masked it. **Rule: size
  every `DEF FN` string parameter explicitly** (`DEF FNX$*500(P$*500)`), to the largest value any
  caller will ever pass.

- **`DEF FN` parameters have a further real-world size ceiling well below any declared `*n`, for
  genuinely large strings.** Even with a parameter explicitly sized `*400000`, passing a realistic
  ~27,000-byte string into it hit the same input-wait failure — reproduced with a bare whole-copy
  body (`LET FNX$ = TEXT$`, no substring, no concatenation). The identical logic at top level, or
  in a `GOSUB` reading/writing shared globals, handled the same string with no issue. The exact
  threshold was never pinned down (somewhere between a few hundred bytes and ~27KB) because the fix
  is simple and general: **route anything that might be more than a few KB through a `GOSUB`
  operating on shared global variables, not through a `DEF FN` parameter.**

- **A config-level ceiling can override the documented string-length limit entirely.**
  `BRConfig.sys`/startup-config `OPTION 60` selects the **legacy BR internal program-save format**,
  which caps every variable (including strings) at **32767 bytes** — regardless of the
  99,999,999-byte `DIM` limit documented for the current format (4.30+). The failure mode is the
  same "looks like nothing's wrong at the `DIM` line" silent misbehavior/hang described above.
  **If a program needs string buffers in the tens/hundreds of KB, check the target config for
  `OPTION 60` first** — remove it, or keep every `DIM`'d string under 32767 bytes if it must stay.

---

## 3. Control-flow footguns

- **A numeric `GOTO`/`GOSUB` target always resolves to the line NUMBER — never to a same-spelled
  text label placed on a different line.** Writing `GOTO 6260` to reach a label written as
  `6260: !` fails silently if line number 6260 is actually a *different*, unrelated statement (e.g.
  an inner loop's `LOOP`) and the intended label sits a few lines later at, say, line number 6265.
  This doesn't error — it silently executes the wrong statement with whatever stale state happens
  to be lying around, and can corrupt output with no diagnostic at all. **Never name a label the
  same as a nearby line number; use a descriptive text label (`DONE:`, `SKIPBT:`) for every
  non-sequential `GOTO` target**, and double-check the *label's own line number*, not just where
  the label text visually appears in the source.

- **`MAT arr(n)` resizing a shared/reusable scratch array is destructive and sticky.** A generic
  subroutine (e.g. a sort/dedupe helper) that does `MAT WORK$(n)` to size a shared `WORK$` before
  processing **permanently reshapes it** for every subsequent caller. If a later call reuses that
  same array for a *larger* batch without re-growing it first, writing past the now-too-small bound
  silently manifests as the same input-wait symptom (`ERR 122`, "illegal array element" —
  [`../br_tree/90-reference/error-codes/0122.md`](../br_tree/90-reference/error-codes/0122.md)).
  **`MAT arr(neededsize)` immediately before every write into a shared scratch array**, not only
  inside whichever subroutine happens to also resize it.

---

## 4. Built-ins that didn't behave as documented (environment-specific — verify before trusting)

- **`HEX$` did not work at all** in one observed `br432g-32.exe` build/config — confirmed on a
  plain ASCII literal with no other function involved (`HEX$("ABC")` alone triggered the input-wait
  failure). `ENCRYPT$(data$,"","SHA-1")` itself worked fine and produced a correct, verified
  digest — it was specifically `HEX$` that was broken. Worked around with a hand-rolled hex
  encoder (`ORD`/`INT`/`MOD` against a 16-char lookup string — no bitwise ops needed, matching §1's
  "no bitwise operators" rule). **If `HEX$` matters to you, smoke-test it in your target
  environment before depending on it.**

- **`br-lsp`'s built-in signature for `ENCRYPT$` is stale.** `/br-check` flags the 3-argument
  one-way-hash form (`ENCRYPT$(data$, "", "SHA-1")`) as "expects 1-2 parameters, but 3 provided".
  That form is directly documented in
  [`Encryption.md`](../br_tree/10-language/data-manipulation/system-functions/Encryption.md) and
  works at real BR runtime. Treat an `ENCRYPT$` arg-count warning from `br-check` as a possible
  false positive, not proof the call is wrong.

- **No documented trap clause for channel-less `READ`/`DATA` exhaustion.**
  [`statement-semantics.md`](statement-semantics.md) and `br_tree`'s DATA/READ/RESTORE coverage
  list "out of data" only as a common error, with no dedicated clause keyword (unlike file `READ`,
  which has `EOF <line-ref>`). Don't assume one exists (e.g. an invented `EOD` clause) — it isn't
  in `br_tree`, and a fabricated keyword may pass a syntax checker without being real at runtime.
  Read a known, fixed row count instead of looping to exhaustion when the count is known ahead of
  time.

---

## 5. Output/I/O gotchas

- **A `DISPLAY OUTPUT` file with no `RECL=` wraps output at a short default width** — inserting a
  mid-line CRLF that silently splits one `PRINT`'d line into two physical lines on disk. This
  produced no error at all; it just corrupted a generated JSON file (a long string value cut across
  two lines, breaking the JSON). **Always specify a generous `RECL=` when writing any line that
  might exceed roughly 130 characters**: `OPEN #n: "NAME="&f$&",REPLACE,RECL=4000", DISPLAY, OUTPUT`.

- **Minor:** a string built in memory ending `... & CHR$(10)` carries that trailing newline, but
  re-reading the same content back from disk (line-by-line, rejoined with the same separator) will
  not reproduce a final trailing blank line that was never actually printed as its own output line.
  Not a data bug — just a one-byte trap for "regenerate and diff against on-disk" comparison logic;
  trim the trailing separator from the in-memory side before comparing.

---

## 6. When something silently fails: how to actually debug it

- Run headless with a `gui off` config and **`UNATTENDED`** logging (§6 of
  [`APP-DEV-GUIDE.md`](APP-DEV-GUIDE.md#6-running-br-headless-via-procedures)). This turns an
  otherwise-indefinite hang into a fast, logged abort with the offending program and line number —
  the difference between one diagnostic pass and manually killing a stuck process every time.
- Don't assume the reported line number is the *root cause* line — it's where the symptom
  surfaced. Trace backward from there; the actual defect (an un-sized variable, a bad `GOTO`
  target) is often several statements upstream.
- When a documented, spec-correct construct still fails, **isolate it** with a minimal `mini*.brs`
  probe — a handful of lines, one `OPEN`/`PRINT`/`CLOSE` to a debug file — before assuming your own
  program logic is the bug. Several of the gotchas above cost real time specifically because the
  failing construct *looked* like it must be a logic error in the larger program, when it was
  actually a runtime limitation unrelated to the surrounding code.
