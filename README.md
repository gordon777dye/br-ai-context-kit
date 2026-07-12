# BR context kit

This is a model- and developer- facing context for working in **Business Rules! (BR)** — reading, writing,
and designing BR application code. It is application-agnostic: point the tooling at whatever BR
codebase you're on. There are three published parts:

- **[`dev\`](dev\)** — the task-oriented coding kit: a router (`topics.json`), distilled statement
  semantics, the system-function and standard-library catalogs, an error reference, and
  schema-extraction tooling.
- **[`br_tree\`](br_tree\)** — the authoritative BR language reference tree (syntax, data types, file
  and screen I\O, printing, libraries, error codes), the ultimate backstop that `dev\` links into
  for depth.
- **[`app\`](app\)** — where your toolset information and application programming style will reside.

## Rules

- Do not invent, guess, or infer commands, file paths, syntax, or facts. If you don't know something: (a) search the context first, (b) flag it as unknown, (c) ask the user. **Never guess** or fill gaps with plausible-sounding guesses.

## Installation

**Copy this `context` folder with it's sub-folders into the main folder of your application**. Then proceed to configure it for your app and toolset as 
described in app\INSTRUCTIONS.md. You will need to specify BR and config paths. The rest can be 
done by your favorite AI model. 

## Start here

**→ [`app\INSTRUCTIONS.md`](app\INSTRUCTIONS.md)** - Onboarding instructions - do this first. 
Nearly all of this should be done by AI at your direction. Just modify toolset.md 
(see INSTRUCTIONS step 2) and tell your AI agent to execute the instructions one step at a time.

**→ [`dev\APP-DEV-GUIDE.md`](dev\APP-DEV-GUIDE.md)** — After completing the onboarding this is 
your task entry point. Its *"Start here — by task type"* preamble routes your agent by what you 
desire to accomplish (interpret\debug · code · design · test).
