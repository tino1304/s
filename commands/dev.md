---
description: Developer - implement features, fix bugs, write code
---

# Developer Workflow

**User Request:** $ARGUMENTS

---

## CONFIG CHECK

Read `.claude/s-config.json` if it exists:
- `autoAccept: true` → Skip confirmations at workflow steps
- `autoAccept: false` or missing → Ask at each workflow step

---

## RULES (MANDATORY)

### Research Rule
**No imagination. Proof required.**

Every claim must have proof:
- File path + line number for code
- URL for web sources

```
❌ BAD: "The config has database settings"
✅ GOOD: "config/database.yml:15 → `host: localhost`"
```

When no evidence: Say "Not found" and suggest next steps.

### Tailwind v4 Warning (Frontend)

**CRITICAL:** If using Tailwind, check version first. v4 has breaking changes:

```bash
# Check version
npm list tailwindcss
```

| v3 (OLD) | v4 (NEW) |
|----------|----------|
| `tailwind.config.js` | CSS `@config` or `@theme` |
| `theme.extend.colors` | `@theme { --color-*: }` |
| `@tailwind base` | `@import "tailwindcss"` |

**v4 Example:**
```css
@import "tailwindcss";
@theme {
  --color-primary: oklch(0.7 0.15 200);
}
```

Do NOT mix v3 config patterns with v4.

---

## WORKFLOW STEPS

### STEP 1: Research & Analysis

Before writing any code:

1. **Understand the request** - What needs to be built/fixed?
2. **Research codebase** - Find existing patterns, related code
   - Show proof for every finding
   - No assumptions - read actual files first
3. **Identify dependencies** - What existing code to use/modify?
4. **Plan approach** - How will you implement this?

**Research Output Required:**
```markdown
## Finding: [Discovery]
**Source:** [file:line]
**Evidence:**
> [Actual code]
**Conclusion:** [How it affects implementation]
```

### STEP 2: Draft Implementation Plan

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

## Files to Modify/Create
- `path/to/file.ts` - [what changes]

## Risks/Considerations
- [Potential issues]

## Questions
- [Anything unclear?]
```

### STEP 3: Ask for Confirmation

**If `autoAccept: true`** → Skip to STEP 4 immediately

**Otherwise**, ask user: **"Does this implementation plan look good?"**

Options:
1. **Approved** → Go to STEP 4
2. **Needs changes** → Ask what to change, revise plan
3. **Start over** → Fresh approach

**Do NOT write code until user explicitly approves (unless autoAccept).**

### STEP 4: Implement

Only after user confirms:
1. Write code following the approved plan
2. Follow existing project patterns
3. Show each change as you make it

### STEP 5: Review & Verify

After implementation:
1. Show summary of all changes made
2. Ask if user wants to test/review
3. Offer to make adjustments

---

## RULES SUMMARY

- Never write code without showing plan first
- Always read existing code before modifying
- Follow project patterns found in research
- Show proof for every decision
