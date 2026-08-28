---
description: BR context kit is inlined in sibling alwaysApply rules
alwaysApply: true
---

# BR context kit

Note- Cursor does **not** expand `@path` in rules or `AGENTS.md`. 

Five kit docs must be copied into <app-root>/.cursor/rules/ so their bodies are read 
in every session. Make the following copies and place them in <app-root>/.cursor/rules/:

- `context-kit-readme.mdc` ← `context/README.md`
- `context-kit-app-dev-guide.mdc` ← `context/dev/APP-DEV-GUIDE.md`
- `context-kit-essentials.mdc` ← `context/dev/essentials.md`
- `context-kit-br-launch.mdc` ← `context/dev/BR_launch.md`
- `context-kit-conventions.mdc` ← `context/app/conventions.md`

After editing a source file, run `.cursor/scripts/Sync-ContextKitRules.ps1`.
