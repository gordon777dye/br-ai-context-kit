# Kit Errors

Please record any context kit errors here that are found in the course of its use.
---

## 2026-10-20 — `FREE` has no `FR` abbreviation (br_tree/70-commands/file-directory/spec.md)

The BNF line `FREE <file-ref> [-ANPV] ... -- FR; deletes the file` says `FR` abbreviates
`FREE`. In BR 5.0 it does not: the command table (`tblcmd.cpp`, `table1k`) holds an entry
`FRE` whose only purpose is to refuse `F`, `FR` and `FRE` — `commandc.cpp`, `case
FRE_FORCE_CMD`: "force the full FREE command to be entered", error
`BREUNIDENTIFIEDSRC`. `F` and `FR` are ambiguous between `FRE` and `FREE` in `tokensub`,
and `FRE` matches the blocking entry exactly. `FREE` must be typed in full.
Found from the interpreter source while adding Tab completion.

**Confirmed and corrected, 2026-10-20.** Run headless, `FR <file>` and `fr <file>` stopped with
error 1000 and left the file; `FREE <file>` deleted it. `FR` had reached that error only by
falling through to calculator mode (a bare `FR` printed a variable named `FR`), so BR 5.0 now
sends `FR` to the same refusal as `FRE` (special case in `cmd()`, `command.cpp`). The spec's BNF
line now says "no abbreviation", recorded in its `corrections:` frontmatter.

## 2026-10-20 — `DIR` has no `DI` abbreviation (br_tree/70-commands/file-directory/spec.md)

The BNF line for `DIR` ends `-- DI`. In BR 5.0 (and in the 4.32 source it was imported
from) the command table `table1k` holds `DIR` followed by `DISPLAY`, and `tokensub`
returns 0 when the typed prefix matches two consecutive entries, so `DI` is ambiguous
and is not taken as `DIR`. There is no special case for it in `cmd()` (there are for
`PROC`, `REN`, `CD` and `FOR`). `DIR` must be typed in full. Found from the source;
not yet confirmed at a live `READY` prompt.
