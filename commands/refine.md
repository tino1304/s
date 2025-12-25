---
description: Refine and enhance a user prompt
---

# Prompt Refinement

**User Request:** $ARGUMENTS

Your job is to refine and enhance the user's prompt. Do NOT execute any task - only improve the prompt.

## Instructions

1. **Analyze the prompt** and identify:
   - Main intent/goal
   - Any ambiguities or missing details
   - Implicit requirements
   - Technical terms that need clarification

2. **Create an enhanced version** that:
   - Corrects grammar/spelling issues
   - Adds specific details and context
   - Clarifies scope and expected output
   - Makes implicit requirements explicit

3. **Present to user:**

```
## Original Prompt
[User's original prompt]

## Enhanced Prompt
[Your refined, detailed version]

## Clarifications Added
- [What you added/clarified]
- [Assumptions made explicit]
- [Scope defined]

## Suggested Command
Based on this request, you might want to run:
- `/s:dev` - for implementation tasks
- `/s:ba` - for requirements analysis
- `/s:design` - for UI/UX work
- `/s:tech-lead` - for breaking down into tasks
```

4. **Ask user** which command to run with the enhanced prompt, or if they want to modify further.

## Rules

- Do NOT execute any code or make changes
- Do NOT start any workflow
- ONLY refine the prompt and present options
- Let user decide next step
