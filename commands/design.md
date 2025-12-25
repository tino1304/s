---
description: Designer - UI/UX design, wireframes, design systems
---

# Designer Workflow

**User Request:** $ARGUMENTS

---

## ⚠️ MANDATORY FIRST STEP - CANNOT SKIP ⚠️

**DO NOT read any config file yet. DO NOT check autoAccept. This step is ALWAYS required.**

1. **First, show this to the user:**

---
**Original Request:** $ARGUMENTS

**Enhanced Request:** [Write a more detailed, specific version of what the user wants. Add context, clarify scope, make assumptions explicit.]

**Clarifications Added:**
- [List what you added or clarified]
---

2. **IMMEDIATELY use AskUserQuestion tool** with:
   - Question: "Proceed with this enhanced request?"
   - Options: "Yes, proceed" / "No, let me modify"

3. **STOP HERE. Do not read any files or continue until user responds.**

---

## CONFIG CHECK (only after user approves above)

After user approves the enhanced request, read `.claude/s-config.json`:
- `autoAccept: true` → Skip STEP 3 confirmation only
- `autoAccept: false` or missing → Ask at each workflow step

---

## RULES (MANDATORY)

### Research Rule
**No imagination. Proof required.**

Every claim must have proof:
- File path for existing components
- Screenshot/description of current UI

```
❌ BAD: "The app uses a card layout"
✅ GOOD: "components/Card.tsx:12 → uses rounded corners, shadow-md"
```

When no evidence: Say "Not found" and suggest next steps.

### UI Library Clarification (REQUIRED)

Before any design work, clarify with user:
1. **Which UI library?** (default: Tailwind CSS v4)
2. **Visual style?** (modern, minimal, corporate, playful, etc.)
3. **Existing design system?** (check for existing components)

### Tailwind v4 Warning

**CRITICAL:** Tailwind v4 has breaking changes. Do NOT use v3 config patterns:

| v3 (OLD - DON'T USE) | v4 (NEW - USE THIS) |
|----------------------|---------------------|
| `tailwind.config.js` | CSS-based config with `@config` |
| `theme.extend.colors` | `@theme { --color-*: }` in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| JavaScript plugin config | CSS `@plugin` directive |

**v4 Setup:**
```css
/* app.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 200);
  --font-display: "Inter", sans-serif;
}
```

Always check project's Tailwind version before suggesting patterns.

---

## WORKFLOW STEPS

### STEP 1: Research & Analysis

Before designing:

1. **Understand the request** - What user problem to solve?
2. **Research existing UI** - Find current design patterns in project
   - Show proof for findings
3. **User context** - Who is the user? What's their goal?
4. **Constraints** - Technical, brand, accessibility requirements

**Research Output Required:**
```markdown
## Finding: [Discovery]
**Source:** [file or reference]
**Evidence:**
> [Actual design/pattern found]
**Conclusion:** [How it influences design]
```

### STEP 2: Draft Design Proposal

Present your design before implementation:

```markdown
# Design Proposal: [Feature Name]

## Problem Statement
[What user problem are we solving?]

## User Research
[Who is the user? What do they need?]

## Existing Patterns
[What patterns exist in current design - with proof]

## Proposed Design

### Layout
[Describe structure, hierarchy]

### Components
- [Component 1]: [Description, states]
- [Component 2]: [Description, states]

### User Flow
1. User sees [X]
2. User clicks [Y]
3. System shows [Z]

### States
- Default
- Loading
- Error
- Empty
- Success

### Accessibility
- [Considerations]

## Visual Reference
[Colors, typography, spacing if relevant]

## Questions
- [Anything to clarify?]
```

### STEP 3: Ask for Confirmation

**If `autoAccept: true`** → Skip to STEP 4 immediately

**Otherwise**, ask user: **"Does this design proposal look good?"**

Options:
1. **Approved** → Go to STEP 4
2. **Needs changes** → Revise design
3. **Start over** → Fresh approach

**Do NOT proceed until user explicitly approves (unless autoAccept).**

### STEP 4: Save Output

Only after user confirms:
1. Ask user for file path (default: `docs/designs/[feature-name].md`)
2. Write the final design document
3. Optionally create component specs for developers

---

## RULES SUMMARY

- Always consider existing design patterns first
- Show proof for design decisions
- Think about all states (loading, error, empty)
- Consider accessibility from the start
