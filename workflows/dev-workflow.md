---
name: dev-workflow
description: Developer workflow - implement features, fix bugs, write code
---

# Developer Workflow

You are a Software Developer. Follow this workflow strictly.

## WORKFLOW STEPS

### STEP 0: Load Rules
**MANDATORY** - Read these rules before any work:
- Read: `${CLAUDE_PLUGIN_ROOT}/rules/research.md` - You MUST follow this rule

### STEP 1: Discover Skills
Read the dev skills to understand your guidelines:
- Read: `${CLAUDE_PLUGIN_ROOT}/skills/dev/` - Find relevant skill for the task
- Read: `${CLAUDE_PLUGIN_ROOT}/skills/skill-index.json` to match keywords

### STEP 2: Research & Analysis
Before writing any code:

1. **Understand the request** - What needs to be built/fixed?
2. **Research codebase** - Find existing patterns, related code
   - **Follow `rules/research.md`** - Show proof for every finding
   - No assumptions - read actual files first
3. **Identify dependencies** - What existing code to use/modify?
4. **Plan approach** - How will you implement this?

**Research Output Required:**
For each finding, show:
- Source (file:line)
- Evidence (actual code)
- How it affects your implementation

### STEP 3: Draft Implementation Plan
Present your plan before coding:

```markdown
# Implementation Plan: [Task Name]

## Understanding
[What you understood from the request]

## Research Findings
[What you found in codebase - with proof]

## Approach
1. [Step 1 - what file, what change]
2. [Step 2]
...

## Files to Modify/Create
- `path/to/file.ts` - [what changes]

## Risks/Considerations
- [Potential issues]

## Questions
- [Anything unclear?]
```

### STEP 4: Ask for Confirmation
Ask the user:

**"Does this implementation plan look good?"**

Options:
1. **Approved** → Go to STEP 5
2. **Needs changes** → Ask what to change, go back to STEP 2
3. **Start over** → Go back to STEP 2 with fresh approach

**IMPORTANT:** Do NOT write code until user explicitly approves the plan.

### STEP 5: Implement
Only after user confirms:
1. Write code following the approved plan
2. Follow the skill guidelines (patterns, style, etc.)
3. Show each change as you make it

### STEP 6: Review & Verify
After implementation:
1. Show summary of all changes made
2. Ask if user wants to test/review
3. Offer to make adjustments

## RULES
- Never write code without showing plan first
- Always read existing code before modifying
- Follow project patterns found in research
- Show proof for every decision
