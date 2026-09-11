# Kit Errors

Please record any context kit errors here that are found in the course of its use.
---

## 2026-09-11 — brls.exe does not parse Lexi preprocessor syntax; false positives on Lexi-authored source

**Where:** `dev/tools/brls.exe -check`, against any source written for **Lexi** (see
`dev/BR_launch.md`'s "The Lexi preprocessor" section and `dev/essentials.md` §1) — a preprocessor
some BR shops use that base BR and `brls` don't understand on their own.

**Confirmed directly against this kit's own `brls.exe`** (piped one line at a time, not inferred):

```
$ printf '00010 /* this is a lexi comment */\n' | dev/tools/brls.exe -check -
<stdin>:1:7: this is not a statement: a statement starts with a keyword, or is an assignment
<stdin>:1:15: unexpected "is" after the end of this statement

$ printf '00020 LET X$&="hello"\n' | dev/tools/brls.exe -check -
<stdin>:1:11: unexpected "X$"; expected an expression

$ printf '00030 #Select# X #Case# 1\n' | dev/tools/brls.exe -check -
<stdin>:1:8: unexpected "Select" after the end of this statement
```

**Issue:** `/* ... */` comments, the `X$&="..."` compound-append shorthand, and
`#Select#/#Case#/#End Select#` are real Lexi syntax, not base BR — they compile and run correctly
once Lexi has translated them, but `brls -check` has no notion of Lexi and reports each as a hard
syntax error. This is a **false-positive class** on any Lexi-using app, not isolated typos — QSMRP
itself doesn't use Lexi (its `.br.brs` source has none of this syntax), so it doesn't bite this
app's own code, but it will bite this kit's coding loop (`APP-DEV-GUIDE.md` §6.1) on any future
app onboarded with it that does use Lexi.

**Impact:** the kit's recommended coding loop treats a clean `brls -check` as the fast pre-check
before the authoritative real-BR `LOAD ... source` gate. For a Lexi-based app, that pre-check
rejects valid source outright unless the source is run through Lexi first.

**Fix applied:** documented, not patched into `brls` itself — `dev/BR_launch.md` now has a full
"Lexi preprocessor" section (mechanism, and a `dev/tools/lexi-compile.ps1` script that runs Lexi
headlessly), `dev/essentials.md` §1 documents Lexi's actual syntax, `dev/APP-DEV-GUIDE.md` §6.1
and §8 point to the Lexi-aware loop, and `app/ONBOARDING.md` STEP 1 now asks whether an app being
onboarded uses Lexi. Teaching `brls` an optional Lexi-syntax mode remains open — recorded here
since it isn't a `brls` bug in the general case, it's a gap in Lexi support.
