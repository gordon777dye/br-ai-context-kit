# Kit Errors

Please record any context kit errors here that are found in the course of its use.
---

## 2026-09-26 — ScreenIO API docs described a superseded build (16 exports; now 21)

**Where:** `br_tree/50-libraries/screenio/` (`ScreenIO_Function_Reference.md`, `spec.md`,
`ScreenIO_Library.md`, `ScreenIO_Data_Model.md`, `_index.md`), `dev/library-catalog.md` §2,
`dev/screenio-guide.md`.

**What was wrong:** every page said ScreenIO has "exactly 16 `DEF LIBRARY` exports", taken from a
2020 `screenio.brs`. The currently shipped ScreenIO (v2.95, `FNVERSION=2.95`) has 21. The five
added exports (`fnDesignScreen`, `fnMakeScreen`, `fnCompileScreen`, `fnCheckScreenErrors`,
`fnListSpec$`) had no Function Reference entry. `ScreenIO_Library.md` stated `fnListSpec$` and
`fnDesignScreen` were *not* exports. `Fnfm$`'s new 16th parameter `SaveDontAsk` was undocumented,
which made `run.brs`'s 16-argument `fnfm$` call look like a bug. The wiki manual's description of
`fnListSpec$` ("build a listview column spec from width/justification/type") does not match the
v2.95 source, which only truncates its argument before the third comma. `screenio-guide.md`'s
`fnCompileScreen` example also said a return of `1` meant "compiled", but the compile runs in a
separate BR process.

**Fixed:** all of the above updated from the v2.95 source listing (`screenio.br.brs`).

**Still unverified:** `Fnfm` and `Fndisplayscreen` are absent from the v2.95 source listing
(probably hidden by `DEL … source`), though both names are in the compiled `screenio.br` and in
the `LIBRARY` line ScreenIO writes into every helper library. Their documented signatures are from
the 2020 build. The internal `FNWARNMESSAGE` that `fnMakeScreen` checks first is also not in the
listing, so what makes `fnMakeScreen` exit BR is unknown.
