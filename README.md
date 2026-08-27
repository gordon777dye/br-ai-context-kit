# BR context kit

To properly view markdown files such as this one, open it with the mdreader provided herein.

This is a model- and developer- facing context for working in **Business Rules! (BR)** — 
reading, writing, and designing BR application code. It is application-agnostic: point the 
tooling at whatever BR codebase you're on. There are three published parts:

- **`dev\`** — the task-oriented coding kit: a router (`topics.json`), distilled statement
  semantics, the system-function and standard-library catalogs, an error reference,
  schema-extraction tooling, and `brls.exe` — a fast BR syntax/sema checker
  (`tools\brls.exe -check <file>`) that needs no BR license or runtime.
- **`br_tree\`** — the authoritative BR language reference tree (syntax, data types, file
  and screen I\O, printing, libraries, error codes), the ultimate backstop that `dev\` links into
  for depth.
- **`app\`** — where your toolset information and application programming style will reside.

## AI Model Rules

- Do not invent, guess, or infer commands, file paths, syntax, or facts. 
  Do not or fill gaps with plausible-sounding guesses. If you don't know something: 
  (a) search thIS context first, (b) flag it as unknown, (c) ask the user. **NEVER GUESS** 

- The following documents are required reading and are therefore @ included below:
- **`dev/APP-DEV-GUIDE.md`** — this will save you many headaches and much time.
- **`dev/BR_launch.md`** — this is needed to compile and test.
- **`dev/essentials.md`** — this is exactly what it is named.

- Get familiar with the tools in context, especially `brls.exe` (decribed in 
  `APP-DEV-GUIDE.md`) before attempting to code. Use this tool to check your work 
  as you go. 

- Don't be in a hurry to deliver. Look at the context documentation before you code. 

## Installation

Note: This context kit itegrates with any BR app. 

**Copy this folder with it's sub-folders into the main folder of your application**. 
Rename it to "context\". Then copy your brconfig.sys fileto dev\tools.
The rest is done by AI. 

## Start here

onboarding has been completed
**→ [`app\ONBOARDING.md`](app\ONBOARDING.md)** - Onboarding instructions - do this first. 
All of this should be done by AI at your direction. Just tell your AI agent (one step at a time)
 to execute the instructions. 

**→ [`dev\APP-DEV-GUIDE.md`](dev\APP-DEV-GUIDE.md)** — After completing the onboarding, this
becomes your AI task entry point. Its *"Start here — by task type"* preamble routes your 
agent by what you desire to accomplish (interpret\debug · code · design · test).

## Errors

If you encounter any context kit errors, please log them in ERRORS.md

---

Now including **`dev/APP-DEV-GUIDE.md`**
@dev/APP-DEV-GUIDE.md

Now including **`dev/BR_launch.md`**
@dev/BR_launch.md

Now including **`dev/essentials.md`**
@dev/essentials.md

---