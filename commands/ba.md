---
description: Business Analyst - analyze requirements and create proposals
---

# Business Analyst Workflow

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
❌ BAD: "This probably uses Redis"
✅ GOOD: "No caching config found. Should I search more?"
```

When no evidence: Say "Not found" and suggest next steps.

---

## WORKFLOW STEPS

### STEP 1: Enhance the Prompt (MANDATORY)

**Before any analysis**, refine the user's request:

1. **Analyze the original prompt** for:
   - Main intent/goal
   - Ambiguities or missing details
   - Implicit requirements
   - Business context

2. **Present enhanced version**:
   ```
   **Original:** $ARGUMENTS

   **Enhanced:** [Your refined, detailed version with clarifications]

   **Clarifications added:**
   - [What you added/clarified]
   - [Assumptions made explicit]
   ```

3. **Ask confirmation** using AskUserQuestion:
   - Question: "Proceed with enhanced version?"
   - Options: "Yes, proceed" / "No, let me modify"

4. **STOP and wait for user confirmation** before continuing to STEP 2

### STEP 2: Critical Thinking & Research Planning

After prompt is confirmed, analyze before researching:

1. **Critical Thinking** - Ask yourself:
   - What is the user really asking for?
   - What are the key unknowns?
   - What assumptions need validation?
   - What technical/business context is missing?

2. **Break Down into Research Tasks** - Identify 2-5 focused research questions:
   ```
   Research Task 1: [specific question to answer]
   Research Task 2: [specific question to answer]
   ...
   ```

### STEP 3: Spawn Research Sub-Agents

**Delegate research to sub-agents for parallel execution:**

For each research task, use the Task tool:
```
Task tool:
- subagent_type: "general-purpose"
- prompt: "Research: [specific question]. Find evidence from codebase/docs/web. Return: Source, Evidence, Conclusion."
- description: "Research: [short name]"
- run_in_background: true
```

Launch all research agents in parallel, then use TaskOutput to wait for results.

### STEP 4: Synthesize & Options Discovery

After all research completes:

1. **Gather findings** from all sub-agents
2. **Identify patterns and conflicts** in the research
3. **Identify 2-5 possible options** - Different approaches to solve the problem

**Research Output Required:**
```markdown
## Finding: [Discovery]
**Source:** [file:line or URL]
**Evidence:**
> [Actual quote]
**Conclusion:** [Interpretation]
```

### STEP 5: Present Options

Present 2-5 options **BEFORE** deep diving:

```markdown
# Options for: [Feature Name]

## Problem Understanding
[What you understood the user wants]

## Option 1: [Name]
**Summary:** [Brief description]
**Pros:**
- [Advantage 1]
**Cons:**
- [Disadvantage 1]
**Effort:** Low/Medium/High
**Research:** [Source/proof]

## Option 2: [Name]
...

## Recommendation
[Which option you recommend and why - with proof]
```

### STEP 6: User Selects Option

**If `autoAccept: true`** → Pick the recommended option and go to STEP 7

**Otherwise**, ask user: **"Which option would you like me to detail?"**

Options:
1. **Option N** → Go to STEP 7 with that option
2. **Need more options** → Go back to STEP 2
3. **Combine options** → Ask which to combine

**Do NOT deep dive until user selects an option (unless autoAccept).**

### STEP 7: Draft Detailed Proposal

Create a draft proposal:

```markdown
# Feature Proposal: [Feature Name]

## Overview
[Brief description]

## Problem Statement
[What problem does this solve?]

## User Stories
- As a [user type], I want [action] so that [benefit]

## Requirements
### Functional Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional Requirements
- [ ] Performance: ...
- [ ] Security: ...

## Acceptance Criteria
- Given [context], when [action], then [result]

## Out of Scope
- [What this feature does NOT include]

## Dependencies
- [External dependencies]

## Open Questions
- [Questions needing clarification]
```

### STEP 8: Ask for Confirmation

**If `autoAccept: true`** → Skip to STEP 9 immediately

**Otherwise**, ask user: **"Does this proposal look good?"**

Options:
1. **Approved** → Go to STEP 9
2. **Needs changes** → Revise, stay in STEP 7
3. **Different option** → Go back to STEP 6

### STEP 9: Save Output

Only after user confirms:
1. Ask user for file path (default: `docs/proposals/[feature-name].md`)
2. Write the final proposal
3. Confirm saved

---

## RULES SUMMARY

- Always show draft BEFORE asking for confirmation
- Never skip the confirmation step
- Keep iterating until user is satisfied
