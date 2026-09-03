# Kit Errors

Please record any context kit errors here that are found in the course of its use.

---

## 2026-09-02 — AI configs still contain `SUBSTITUTE` lines (ONBOARDING STEP 1 not fully applied)

`context/dev/tools/brconfig.ai_util` and `brconfig.ai_user` were generated from
`brconfig.sys` with the `EXECUTE` and `LOGGING` lines handled per STEP 1, but the
`SUBSTITUTE` lines were **not** stripped (STEP 1 §2 and the Prerequisite both say to remove
`SUBSTITUTE`). Lines still present in both configs:

```
substitute reports\ reports\ads\
substitute prn:/10 preview:10/default   (… through prn:/70)
```

Impact hit during a STEP 4 rerun: `substitute reports\ reports\ads\` silently rewrites every
`reports\...` path, so `LOAD "reports\mtr\shipperp.wb"` (headless, `ai_util`) resolved to a
non-existent `reports\ads\mtr\shipperp.wb` and aborted with BR error 4203. 9 of 57
decompiles failed until re-run with a `SUBSTITUTE`-free copy of the config.

**Fix:** regenerate both AI configs per STEP 1, removing every `EXECUTE`, `SUBSTITUTE`, and
`LOGGING` line from the `brconfig.sys` copy before prepending the AI `LOGGING` directive.
**Kit doc gap (minor):** STEP 1's "Generate `brconfig.ai_user`" list should probably also
call out the `printer.landscape.sys` INCLUDE, which is absent from `dev/tools/` and logs a
`4152 / not found` on every headless start (non-fatal, but noisy).
