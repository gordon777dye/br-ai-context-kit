# Kit Errors

Please record any context kit errors here that are found in the course of its use.

## Broken paths (found 2026-08-26)

- `context\README.md` (AI Model Rules section) referenced `essentials.md` at the kit root; the
  file actually lives at `context\dev\essentials.md`. Fixed — README now reads `dev\essentials.md`.
- `context\dev\APP-DEV-GUIDE.md` (top of file) instructed logging errors to `dev\ERRORS.md`; the
  file actually lives at `context\ERRORS.md` (one level up from `dev\`). Fixed — now reads
  `..\ERRORS.md`.
