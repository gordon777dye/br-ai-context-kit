# brsafe — editing BR source that holds CP437 bytes

`*.br.brs` / `*.wbs` source is stored as **CP437**. A few files carry single‑byte high‑bit
characters (box‑drawing / window‑frame `data` tables). `Edit` / `Write` / `MultiEdit` re‑encode
the whole file as UTF‑8 and corrupt those bytes — **even when your edit is ASCII and nowhere
near them**. `brsafe` (`context/dev/tools/brsafe.exe`) edits such files at the byte level.

## Rule

Before editing any `*.br.brs` / `*.wbs` source file, run `brsafe check <file>`:

- **exit 0** — pure ASCII → use `Edit` / `Write` normally.
- **exit 1** — has CP437 bytes → **do not** use `Edit` / `Write` / `MultiEdit`. Read with
  `brsafe view`, edit with `brsafe replace`.

A `PreToolUse` hook may already enforce this by blocking `Edit`/`Write` on such files.

## Commands

### `brsafe view <file> [a:b]`
Prints the file (or a line range) to **stdout** as UTF‑8, so frame characters are legible
(`Read` shows `<?>` for them). Use it to get line numbers for `replace`.
`a:b` is **physical, 1‑based, inclusive**: `a` = one line, `a:` = a→EOF, `:b` = start→b.

### `brsafe replace <file> <a:b> [--old <prefix>] --new <text>|@file|- [--dry-run]`
Replaces physical lines `a`–`b` with `--new` (any resulting line count, including 0).

| element | rule |
|---|---|
| `<a:b>` | physical, 1‑based, inclusive — the numbers `brsafe view` prints |
| `--old <prefix>` | must be a **prefix of line `a`**. Mismatch → abort, nothing written. **Pass it on every call** as an ASCII anchor, e.g. the BR line number: `--old '07080'`. |
| `--new` | **required.** `-` = stdin (heredoc), `@file`, or an inline string. **Empty value deletes `a:b`.** Read as UTF‑8, written as CP437; a character with no CP437 mapping is a hard error and nothing is written. |
| `--dry-run` | print the old/new blocks to **stderr**; write nothing |

Lines outside `a:b` are byte‑copied untouched. CRLF and the file's trailing‑newline state are
preserved. Success prints one line to stdout:
`replaced 147:147 (1 line) -> 1 line; encoding still CP437`.

### `brsafe check <file>` — exit 0 = ASCII, exit 1 = has CP437 bytes.
### `brsafe scan [dir]` — list `*.brs` / `*.wbs` under `dir` that carry CP437 bytes.

## Do / don't

- **Do** take line numbers from `brsafe view`, not `Read`.
- **Do** pass `--old` on every `replace`.
- **Do** verify after an edit: `file <path>` must still report `ISO-8859`, not `UTF-8`.
- **Don't** copy box‑drawing characters out of `view` output into `--old` / `--new`. Edit ASCII
  code regions only — the static frame `data` tables never need editing.
- **Don't** `brsafe view f > f`.

## Exit codes

`0` ok · `1` `check` "has bytes" **or** `replace` semantic failure (`--old` mismatch,
unmappable character, bad range) · `2` usage / I/O error · `3` internal invariant (file left
untouched).

Full CLI: `brsafe -h`. Source: `context/dev/tools/brsafe.go`.

## Example

```bash
brsafe check  glp/accountp.br.brs            # exit 1 → route through brsafe
brsafe view   glp/accountp.br.brs 260:300    # read the frame tables; note line numbers

brsafe replace oap/shipperx.br.brs 147 \
      --old '07080' \
      --new '07080             let _ASN_OK= FNCOMM(SHIP$(2),SHIP$(4))  !xmit'
# → replaced 147:147 (1 line) -> 1 line; encoding still CP437

brsafe replace oap/shipperx.br.brs 200:204 --old '07540' --new - <<'EOF'
07540             print #PRINTER: "done" !:
                  let DONE = 1
EOF

brsafe replace oap/shipperx.br.brs 200:204 --old '07540' --new ''   # delete the range
```
