# Initial Prompt Guide

## Model Recommendation

We recommend using models that are **Sonnet and above**. If you are not using Anthropic models, you may need to keep the reins tighter than you would for Anthropic models (see below).

---

## Necessary AI Prompts

### Start a new conversation
```
/clear
```

### Onboarding (required first)
```
Read context/README.md and do what it says before I provide product specifications.
```

### Understand the tooling
```
What does brls.exe do and how should it be applied during coding?
```

---

## Standard Workflow

### Step 1: Design Phase

**Prompt:**
```
First design the program and show me the plan.
```

Provide the product requirements document or tell the AI what you want it to do.

### Step 2: Implementation Phase

**Prompt:**
```
Please proceed with step 1.
```

Continue through remaining steps (step 2, 3, etc.).

---

## If the AI Model Has Difficulty

**Stop the session and restart:**

```
/clear
```

Then, instead of "Please proceed with step 1," give this alternative directive:

```
Build the product incrementally as follows:
Create the BR program following APP-DEV-GUIDE.md section 6.1's brls.exe workflow.
After writing each subroutine (or every ~50 lines):

Run: ./dev/tools/brls.exe -check dev/gen_brtree_index.br.brs
Show me the brls JSON output
Fix any errors - see APP-DEV-GUIDE 6.1 Required AI Coding loop
Do not proceed to the next section until brls returns clean: true,
and you show me the evidence.
```

---

## During Development

**Pay attention to the comments made by the agent (AI model) as it works.** Sometimes you will want to stop it and give it advice or question its conclusions.

---

## After the Session

### Feedback

Ask the AI:

> Is there anything in the way of documentation that could have better prepared you for this assignment?

### Documentation

Please record observations in `ERRORS.md` for forwarding to ADS.
