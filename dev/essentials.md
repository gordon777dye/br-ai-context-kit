---
title: BR Language Essentials
file: essentials.md
category: dev
alwaysApply: true
status: 1a
description: The language rules that bite newcomers (and LLMs trained on other BASICs), plus runtime gotchas confirmed empirically while building and RUN-testing a real BR program end to end.
---

# BR Language Essentials

Two kinds of content, both load-bearing:

1. **§1 — core language rules.** Things that read as surprising if you're coming from another
   BASIC or from Python/C-family languages. Most are stated plainly in the written spec; a
   handful were **not written down anywhere** until they were recovered from BR's own tables and
   parser while building the language server, and those are flagged as such where the distinction
   matters. Per-statement detail is in [`statement-semantics.md`](statement-semantics.md) (indexed
   by [`topics.json`](topics.json)); full detail is in [`../br_tree/`](../br_tree/).
2. **§2 onward — runtime gotchas found empirically, not written down anywhere.** These came from
   actually developing and testing programs. **Treat these as "confirmed in at least one BR
   build/config, verify before assuming universal"** — but treat them as real: each was isolated
   with a minimal reproduction before being written down here.

---

## 1. Core language rules

- **Every line is numbered**; labels go right after the number (`00050 LOOP1: …`).
- **`=` is context-sensitive.** Inside `IF`/`WHILE`/`UNTIL` it means *compare*; elsewhere it
  *assigns*. Use **`:=`** to force assignment inside a condition (must be parenthesized).
- **Operators aren't C/Python.** `&` is **string concatenation**, not bitwise-AND. Exponentiation is
  **`**` only — `^` is *not* an operator at all and raises error 1026.** BR has **no working
  bitwise or shift operators**. **`MOD` is a function only — `MOD(a, b)`, never infix `a MOD b`**
  (`REM(a, b)` is an alias). Precedence (tight → loose): 1 `()`/`[]` · 2 `~`/unary `-` ·
  3 `**` · 4 `*`/`/` · 5 `+`/`-` · 6 `&` (concat) · 7 comparison (`==`/`<`/`>`/…) ·
  8 bare `=` (is-equal) · 9 `NOT` · 10 `AND`/`&&`/`OR`/`||` (one level, left to right) ·
  11 `=` assignment · 12 `:=` forced. (Full detail:
  [expressions](../br_tree/10-language/data-manipulation/expressions/spec.md).)
- **`AND` does NOT bind tighter than `OR`.** They are one precedence level, evaluated strictly
  **left to right** — unlike C, Python, SQL and VB. Evaluation also **stops the moment the running
  value settles the answer** (true meeting `OR`, false meeting `AND`), and the rest is never
  evaluated, so a function call in the abandoned branch never runs. `1 OR 0 AND 0` is **1**
  (nothing after `1 OR` is seen); `(1 OR 0) AND 0` is **0**; `0 OR 1 AND 0` is **0**.
  **Rule: whenever a condition mixes `AND` and `OR`, always parenthesise** — not only when it looks
  ambiguous. Unparenthesised, it is legal BR that nearly every reader will group the wrong way.
- **`~` and `NOT` are not synonyms**, though both negate. `~` binds *tighter* than comparison and
  `NOT` binds *looser*, so `~ 0==5` is `(~0)==5` → **0** while `NOT 0==5` is `NOT (0==5)` → **1**.
  Use `NOT` for conditions; parenthesise if you use `~`.
- **Six spellings compile or look valid and are not operators.** `^`, and `&`/`|` between numbers,
  raise **error 1026**. Worse, **`%`, `<<` and `>>` compile silently and always evaluate to `0`** —
  `PRINT 17%5` prints `0`, with no error and no warning, because BR's compiler emits an opcode its
  runtime has no evaluator for. Treat all six as non-existent.
- **Everything associates left — `**` included — and unary binds *tighter* than `**`.** Two
  groupings where BR parts company with C, Python and most calculators:

  ```
  00010 PRINT 2**3**2      ! 64, not 512   — groups (2**3)**2
  00020 PRINT -2**2        ! 4,  not -4    — groups (-2)**2
  ```

  Both confirmed against a running BR. Exponentiation chains left like subtraction does, and a
  sign attaches to the base before the exponent applies. Neither is a special case: BR's precedence
  table puts `~` and unary `-` *above* `**`, and its operator stacker treats only that unary level
  as right-associative. Parenthesise whenever either could be meant.
- **Assignment binds looser than every operator, so it takes the whole right-hand side.**
  `LET X = A OR B AND C` assigns the entire condition, which is what you want and worth knowing
  why: BR never consults a precedence for `=` at all, it pushes an implied open parenthesis after
  it, so nothing on the right can bind past it. That is also what makes chained assignment work —
  `LET SUMA = SUMB = SUMC = 0` sets all three.
- **`NOT` cannot be repeated.** `NOT NOT X` is a compile error, not a double negation: BR stacks
  the operator once and rejects a second. Use `~ ~ X`, or drop both.
- **String variables end in `$`**; size is declared `DIM NAME$*30`. Arrays are 1-based. Default
  string max (un-`DIM`'d) is **18 characters** — see §2, this is the single biggest source of
  silent runtime failure in practice.
- **What a token *is* is decided by arity, not by a symbol table.** Meeting a name that matches a
  keyword or intrinsic, BR checks whether the **mandatory operands that name requires are
  present**. Present ⇒ it *is* that keyword/function. Absent ⇒ BR moves on and the token ends up a
  variable. This is the machinery behind BR's positional lexicon, and it does **not** work the way
  a C/Python/JS-trained instinct expects — *declaring a name does not shadow anything.* Only the
  126 names in `table6k`/`table7k` are reserved; five intrinsics resolved outside those tables
  (`ABS`, `INT`, `SGN`, `AIDX`, `DIDX`) are not, so all of this is true at once:

  ```
  00010 DIM ABS          ! legal: no argument supplied, so it is a name
  00020 LET ABS = 7
  00030 PRINT ABS        ! 7  — the variable
  00040 PRINT ABS(3)     ! 3  — the intrinsic, same program, same spelling
  ```

  and `DIM ABS(3)` is **rejected** — `ABS(3)` supplies ABS's required argument, so it reads as a
  call and no subscript reading survives. Hence: such a variable can never be subscripted, and
  `X(3)` vs `SIN(3)` is settled by *what the name requires*, never by whether it was `DIM`'d.
  Legal, and a trap worth avoiding in code you want read. **All of this is about keywords and
  *system* functions** — user/library `FN…` functions never enter the contest, since a variable
  never starts `FN`, and their signature rules are their own (see the `DEF`/`FNEND` bullet below).
  (Full rule:
  [10-language/syntax#name-resolution](../br_tree/10-language/syntax/spec.md#name-resolution).)
- You will never read abbreviations in source files; BR expands abbreviations.
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
  **`END DEF` is accepted as a synonym for `FNEND`** — BR's compiler checks the word after `END`
  and rewrites `END DEF` to behave exactly like `FNEND` on the spot (verified against BR's own
  source, `command5.cpp`'s `END_PRI` case), so a function closed either way is closed correctly.
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
- **A required colon is required at the end of the line too.** `00120 CLOSE #1` does not compile;
  it is `CLOSE #1:`. There is no end-of-line exemption — the colon is part of the statement, not a
  separator you may drop when nothing follows. `CLOSE`, `DELETE`, `RELEASE` and `RESERVE` always
  need it; the file forms of `READ`, `WRITE`, `REREAD`, `REWRITE`, `RESTORE`, `PRINT`, `INPUT`,
  `LINPUT`, `RINPUT` and `OPEN` carry it before their operand list.
- **A statement whose own syntax ends in a required colon needs a *second* colon to chain another
  statement on the same physical line.** `CLOSE #n:` terminates the `CLOSE`; `CLOSE #n: STOP` on
  one line mis-parses `STOP` as part of the `CLOSE`. Write `CLOSE #n: : STOP` (two colons) instead.
- **The colon belongs to the *branch*, not to the statement name — and `RESTORE` is where that
  bites.** `RESTORE` is two statements sharing a spelling, and only one of them takes a colon:

  ```
  00100 RESTORE                        ! DATA-table pointer to the top      — NO colon
  00110 RESTORE 900                    ! DATA-table pointer to line 900     — NO colon
  00120 RESTORE #1:                    ! file #1 back to its first record   — colon REQUIRED
  00130 RESTORE #1, KEY=CUST$: NOKEY 800
  ```

  With no `#channel` it repositions the compiled-in `DATA` table and ends there; with a `#channel`
  it is the file statement and its syntax ends in a required colon. So "does `RESTORE` need a
  colon?" has no single answer — *`RESTORE #n` does, bare `RESTORE` does not*, and writing either
  one the other way is a compile error. `READ` splits exactly the same way (`READ A$, B$` reads the
  `DATA` table with no colon; `READ #1: A$, B$` reads a record), which is the same trap seen twice.
  (The two statements are documented separately:
  [RESTORE (file)](statement-semantics.md#restore) and
  [DATA / READ / RESTORE](statement-semantics.md#data-read-restore).)
- **A `!` comment ends only at `!:`, never at a bare `:`.** Everything after the `!` is prose to the
  end of the line unless a `!:` closes it, so `! Convert H:M:S to seconds` is one comment and the
  colons in it are text. (`!:` is not a special marker: it is an empty comment followed by an
  ordinary statement separator, which is exactly why it doubles as the sub-line continuation.) A
  `REM` is stronger still — nothing but the end of the line closes it.
- **`DATA` items are not expressions, and the ordinary lexical rules do not apply inside one.** An
  item that does not open with a quote runs **verbatim to the next comma**, so a backslash, an
  apostrophe, a stray double quote, an operator or a space are all just data:

  ```
  00010 DATA "Scanning Program",bcp\scanser
  00020 DATA "340 HENRY FORD II",3001 MILLER ROAD"
  ```

  Both compile. `DATA` must also be the **first statement on its line** and owns the rest of it.
- **`MAT A(n)` with no `=` is a statement, not an unfinished one.** It **redimensions** the array at
  runtime. `MAT A = (0)` assigns, `MAT A(50)` resizes, and `MAT A(50) = B` does both.
- **A `(…)` may follow a `(…)`, and a slice may follow anything that yields a string.** `FILE$(0)(1:3)`
  subscripts and then slices; `CONTEXT$(C_DISK)(1:2)` is idiomatic. Only a *name* can be subscripted
  or called, so a second `(…)` in a chain must be a `start:end` slice.
- **In a `DIM`, `*length` goes after the subscript and sizes each element.** `DIM FUNCTION$(27)*18`
  is 27 strings of 18 characters — not `DIM FUNCTION$*18(27)`. The same `*length` on a scalar is
  `DIM NAME$*30`, and in either position it is a declaration, not a multiplication.
- **`EXIT DO` leaves a `DO` loop and is not the `EXIT` statement.** BR reads the word after `EXIT`
  and treats it as a loop exit only when it is `DO` (or `FOR`, or `SELECT`). Bare `EXIT` naming an
  error-exit group is a different statement and must be alone on its line.
- **`ELSE` terminates the statement before it**, like `:` and `,` do — you never need a colon in
  front of it. It also stands alone at the head of a statement, which is what the multi-line form
  is built from:

  ```
  00100 IF X>0 THEN !:
           PRINT "positive" !:
        ELSE !:
           PRINT "zero or less"
  ```
- **`FORM` and `USING` are a sub-language with their own rules.** Inside one, a comma does not
  always separate: `PIC(ZZZ,ZZZ.##)` and `DATE(mm/dd/yy)` run **verbatim to their closing `)`**, so
  the comma and the `#`s are part of the picture. A field width may be a **variable** rather than a
  literal — `FORM POS POSITION, C LENGTH` is ordinary BR — and a `n*` prefix repeats a
  specification, where `n` may also be a variable (`ROWS*C COLUMNS`). Spellings are matched
  longest-first, so `DATE(` is not read as `D`.
- **`LIBRARY "name":` with a library name but no function list LOADS that library immediately —
  it does not detach a linkage.** The only way to fully detach a library linkage is to end the main
  program. Don't infer a "no functions ⇒ unlink" meaning from the empty list.
_ **OS utility use** BR has no regex, grep or find. However it has full access to such OS commands
  via `EXECUTE system <string>`.

---

## 2. Sizing discipline — the #1 source of silent runtime failure

BR's default string length (18 chars, when nothing is `DIM`'d) doesn't just apply to plain scalar
variables — it applies everywhere a string can implicitly size itself, and overflowing it doesn't
raise a clean, catchable error if ON SOFLOW IGNORE has been executed. Instead, an untrapped
overflow (and several other untrapped runtime error classes — see §3) manifests as the runtime
sitting at what looks like a keyboard-input wait — under `UNATTENDED` logging this shows up as
`Input attempted in unattended mode ... line N:S`, which is actually the tell that *something*
overflowed or errored upstream, not that the program is genuinely waiting on the keyboard.

- **Un-`DIM`'d scalars default to 18 chars.** A channel-less `READ` into an
  un-`DIM`'d string, or a `LINPUT #n:` into one, silently hits the input-wait fallback instead of a
  clean `SOFLOW` once the source data exceeds 18 chars. **Explicitly `DIM` every scalar that
  receives file or `DATA`-table input**, sized to the real data — not "seems long enough": an array
  sized exactly to an expected item count still overflowed when it was one short of the actual count.

- **`DEF FN` string parameters default to 18 chars too, if the signature doesn't size them.**
  `DEF FNX$(P$)` with no `*n` on `P$` silently caps it at 18 chars regardless of the function's own
  declared return size (`DEF FNX$*500(...)` sizes the *return value*, not the parameters — each
  parameter needs its own `*n`). **Rule: size every `DEF FN` string parameter explicitly** 
  (`DEF FNX$*500(P$*500)`), to the largest value any caller will ever pass - OR - pass values by reference. 

- **`DEF FN` strings passed by value cannot exceed 32,767 bytes. If you need to pass strings 
  longer than that pass them by reference. e.g. `DEF FNA$*500(&BIG_STR$)` But if you 
  pass by reference keep in mind that any changes to the passed values change the original variables. 

- **A config-level ceiling can override the documented string-length limit entirely.**
  `BRConfig.sys`/startup-config `OPTION 60` selects the **legacy BR internal program-save format**,
  which caps every variable (including strings) at **32767 bytes** — regardless of the
  99,999,999-byte `DIM` limit documented for the current format (4.30+). 
  **If a program needs string buffers in the tens/hundreds of KB, check the target config for
  `OPTION 60` first** — remove it, or keep every `DIM`'d string under 32767 bytes if it must stay.

- **`MAT arr(n)` resizing a shared/reusable scratch array is sticky.** A generic subroutine 
  (e.g. a sort/dedupe helper) that does `MAT WORK$(n)` to resize a shared array before
  processing **reshapes it for every subsequent caller**. This also applies to arrays 
  passed as parameters. If a later call reuses that same array for a *larger* batch without 
  re-growing it first, writing past the now-too-small bound 
  silently manifests as the same input-wait symptom (`ERR 122`, "illegal array element" —
  [`../br_tree/90-reference/error-codes/0122.md`](../br_tree/90-reference/error-codes/0122.md)).
  **`MAT arr(neededsize)` immediately before every write into a shared scratch array**.

---

## 3. Control-flow footguns

- **Never name a label a numeric value (e.g `06340 4520:`); while BR allows this, it converts 
  it to a LET statement (e.g. `LET 4520: !`); use a descriptive text label (`DONE:`, `SKIPBT:`) 
  for every `GOTO` target**. 
- **No CONTINUE statement** Only GOTO. However EXIT DO is supported.
- **`DIR` only wildcards its *last* path segment — never a middle one, and there is no recursive
  form.** `DIR` is `FindFirstFile`-based, so a pattern like `DIR br_tree\*\spec.md` (wildcard
  directory, literal file after it) fails outright. To walk a multi-level tree,
  descend one real, known directory name at a time; see 
  [program-management](../br_tree/70-commands/program-management/spec.md#command-vs-statement)).

---

## 4. Built-ins that didn't behave as documented (environment-specific — verify before trusting)

- **`DEF` lets you declare a by-value string parameter larger than 32,767 — and then fails at the
  call, not at the `DEF`.** The oversized declaration is accepted silently: `DEF FNX(B$*400000)`
  compiles and loads without complaint. But pass a string longer than **32,767** bytes into it and you
  get **error 4 — string overflow**
  ([`0004`](../br_tree/90-reference/error-codes/0004.md)) at the point of call. **The declared `*n`
  therefore lies**: 32,767 is the hard by-value ceiling no matter what size you specify in the `DEF`. 
  The boundary itself is clean — a `*32767` parameter takes a full 32,767-byte string with no trouble.
  **To pass more than 32,767 bytes, pass by reference** (`DEF FNX(&BIG$)`) — see §2, and remember a
  by-reference parameter means the callee's writes mutate the caller's variable.

- **`HEX$` values must be given in pairs; `HEX$("ABC")` is invalid; `HEX$("ABCD")` is valid. 

- **`HEX$` and `UNHEX$` go the opposite direction from what the name suggests.** (The
  system-functions table used to gloss both as "hex notation ↔ characters", which disambiguated
  neither; it now spells out each direction separately.) Empirically confirmed: `UNHEX$(binary$)`
  is binary→hex-text (e.g. turns a 20-byte
  `ENCRYPT$(...,"SHA-1")` digest into its familiar 40-char hex string — verified against
  `hashlib.sha1(b"hello world").hexdigest()`, matched exactly case-insensitively). `HEX$(hextext$)`
  is the reverse, hex-text→binary (`HEX$("ABCD")` → 2 raw bytes `0xAB 0xCD`) — consistent with the
  gotcha above it (hex text must come in digit pairs). **Calling `HEX$` on a string that is not
  valid hex-digit text — e.g. accidentally passing it a raw binary digest instead of `UNHEX$`'s
  output — does not raise a catchable BR error. It segfaults the entire `br432g-32.exe` process**
  (confirmed reproducible on this build/config). Never call `HEX$` on data you haven't confirmed is
  hex-digit text; if in doubt which conversion you need, `UNHEX$` is binary→readable-hex.

- **`ENCRYPT$` has no SHA-256 — hash with SHA-1.** `ENCRYPT$(s$,"","SHA-256")` fails with error
  **2022** ("the given encryption method does not exist"). This build's `STATUS ENCRYPTION` reports
  message digests `MD5 SHA SHA-1 DSS DSS-1 MDC-2 RIPEMD-160`, which matches
  [`Encryption.md`](../br_tree/10-language/data-manipulation/system-functions/Encryption.md) — it
  lists SHA-256 under *Wishlist: Future Encryption Types* ("supported by OpenSSL but not currently
  exposed in BR"). **`STATUS ENCRYPTION` is the authoritative list for the executable you are actually
  running** — check it rather than assuming an algorithm exists. Hash via the 3-argument null-key form,
  `ENCRYPT$(data$,"","SHA-1")`, which returns a **20-byte binary** digest — pass it through `UNHEX$`
  to get the familiar 40-character hex string (see the `HEX$`/`UNHEX$` entry above; the digest is not
  hex until you convert it).

- **No documented trap clause for channel-less `READ`/`DATA` exhaustion.**
  [`statement-semantics.md`](statement-semantics.md) and `br_tree`'s DATA/READ/RESTORE coverage
  list "out of data" only as a common error, with no dedicated clause keyword (unlike file `READ`,
  which has `EOF <line-ref>`). Don't assume one exists. The READ / DATA combination is not designed 
  for loading unknown data quantities.

- **On an `EXTERNAL` file, clean end-of-file does *not* fire the `READ` statement's own `EOF
  <line-ref>` clause — it arrives as `ERR 4270`. **Don't trust the `EOF` clause
  alone on an `EXTERNAL` sequential read; give it an `IOERR` handler that treats `ERR=4270` as normal
  completion** (and still special-case `4271` for a short final record, per the OPEN spec).

- **`EXTERNAL` file `RECL=` is capped at `32767`, untrapped.** `RECL=32768` (or higher) on an
  `EXTERNAL OPEN` fails outright at the `OPEN` statement.  `RECL=32767` works; `32768` doesn't. 
  This is a **different** ceiling from the
  documented `OPTION 60` 32767-byte *string* limit ([[br-option60-string-limit-gotcha]]) — it bites
  even with `OPTION 60` absent, and it's on the *file record* size, not any string variable's `DIM`.
  **To read a large `EXTERNAL` file, chunk it in a loop at ≤32767 bytes/record**, not one giant
  `RECL`.

- **`DIR -C`'s columnar layout  truncates long names.** a name like `installation-tooling` 
  was truncated mid-word to
  `installation-tooli` to fit the fixed column width — `-C` is unsafe for programmatically
  enumerating real file/directory names. Plain (no-option) `DIR` is worse: it renders 8.3 short
  names (`00-CON~1`). **`DIR ... -B` gives full, untruncated long names, one per line** (still
  including literal `.`/`..` pseudo-entries and a trailing `" N Files, ... Kilobytes Used, ..."`
  summary line to skip) but does **not** itself mark which entries are directories — a program
  walking a tree via `-B` output needs its own convention (e.g. this corpus's directories never
  contain a `.`, so "no dot in the name" is a safe file/dir heuristic *for this specific tree*, not
  a general BR mechanism).

- **A plain `READ #n: STRINGVAR$` (no `USING`) on an `EXTERNAL` file does not reliably read `RECL`
  raw bytes.** Empirically it returns small, inconsistent, content-dependent lengths. 
  **Always give the `READ` (and any `REREAD`) an explicit `USING <form-line>: STRINGVAR$` with a
  `FORM C <len>` item** (`<len>` may be the same numeric value as `RECL=`) to force a true
  fixed-length raw read. 

- **Repeated growing self-concatenation (`X$ = X$ & Y$` in a loop) silently corrupts once the
  cumulative result crosses roughly 120,000 bytes** — no error, no hang; `LEN(X$)` afterward is some
  small, wrong, content-scrambled value (bytes from many different appends interleaved). Confirmed
  the exact neighborhood: 1200×100-byte appends (120,000 total) breaks, 1199× (119,900) is fine.
  A **single** concatenation straight to a large size (e.g. 130,000 bytes in one `A$ = B$ & C$`) is
  fine — it's specifically *iterated* growth via `=` concatenation that's unsafe past that point.
  **Fix: use the substring-assignment append idiom instead — `X$(INF:0) = Y$`** — which grew the
  same content past 120,000 bytes (tested to 130,000) with no corruption at all. Prefer `X$(INF:0) =`
  over `X$ = X$ &` for any string built incrementally in a loop, not just ones you expect to get big.

- **A substring-*extraction* expression (`X$(a:b)` read as a value — a function argument, or the
  right side of an assignment to a different variable) fails outright once the extracted length
  exceeds roughly 119,000–120,000 bytes** — same "input attempted" symptom, confirmed at the
  statement itself (`Y$ = X$(1:120000)` alone, no function call involved). **Passing the plain full
  variable (however long) works fine** — confirmed `ENCRYPT$(BIGVAR$, ...)` succeeds at 214,670
  bytes when `BIGVAR$` is passed whole, but `ENCRYPT$(BIGVAR$(1:N), ...)` fails once `N` crosses the
  same ~120,000 threshold. So treat "any expression whose *computed* string value exceeds ~120KB"
  as generally unsafe, not just DEF FN arguments. **If you need only part of a large string, either
  keep the whole thing in one variable and pass it whole, or build the trimmed copy via `(INF:0)`
  append in a loop** rather than a single big slice expression.

---

## 5. Output/I/O gotchas

- **`DRIVE` statements establish virtual drives** BR programs operate on virtual drives. When BR 
  OPENs a file, the drive letter in the  file path (default is "current" drive) must be mapped with a 
  configuration DRIVE statement. This letter can be entirely different from the OS drive letter and 
  folder location. This makes applications portable without code changes but coders need to 
  be aware of it when creating an `OPEN` statement.

- **A `DISPLAY OUTPUT` file with no `RECL=` wraps output at a 132 byte default width** — inserting a
  mid-line CRLF that silently splits one `PRINT`'d line into two physical lines on disk. This
  produced no error at all; it just corrupted a generated JSON file (a long string value cut across
  two lines, breaking the JSON). **Specify `EOL=NONE` when opening a json DISPLAY file for OUTPUT.**

- **Minor:** a string built in memory ending `... & CHR$(10)` carries that trailing newline, but
  printing it to a file and re-reading the same content back from disk using LINPUT will drop 
  newline characters.

- **NO argv capability** BR invokation doesn't accept argv style arguments. However, it does 
  support arguments provided by a procedure (batch) file. So, if you need to pass arguments to a 
  BR invokation, create a procedure file that runs the program or proc you desire to run followed 
  by parameter values, each on a separate line. The command is **`RUN PROC`** (two words)
  Then in the program LINPUT each parameter as if the operator were keying them. Note that 
  multiple values are easily passed between BR programs and this limitation only pertains to 
  BR invokation. 

- **`DIR <path>\* -B >file` output's first line is `Directory of <resolved-path>\*`**, not a
  filename — a program parsing this output to enumerate entries must skip that header line
  explicitly (it has no `.`/`..`-style marker and, if the path happens to contain no `.` character,
  it also survives a naive "no dot = directory" filter and gets mistaken for a real subdirectory
  name). Confirmed on every `DIR -B` redirect regardless of target directory.


- **`CNT` is a reserved BR system pseudo-variable** ("I/O items successfully processed" — see
  [flow-control/error-handling](../br_tree/10-language/flow-control/error-handling/spec.md), which
  documents "any I/O resets it"), **not an ordinary name available for `LET`/loop-counter use.**
  Using `LET CNT = 0` / `LET CNT = CNT + 1` as a plain counter compiles and runs *most* individual
  statements without a runtime error, but CNT will get reset by the system under a wide range 
  of conditions, thereby making it useless as a working variable.
  **check any small failing program for a variable named `CNT` first**; renaming it to anything else
  (`FCOUNT`, `XCOUNT`, etc.) fixes it immediately, no other change needed. The project's VS Code BR
  linter independently flags bare `CNT` assignment as a parse error, confirming this is a real
  reserved-word collision, not an environment fluke.

---

## 6. When something silently fails: how to actually debug it

Moved to [`APP-DEV-GUIDE.md`](APP-DEV-GUIDE.md#when-something-silently-fails-how-to-actually-debug-it)
(§6, *Running BR*) — the debugging loop is about *running* BR, so it lives beside the headless
invocation, `UNATTENDED` logging, and the operational hazards it depends on. Read it before chasing
any gotcha in this file: several of them cost real time only because the failing construct looked
like a logic error when it was a runtime limitation.
