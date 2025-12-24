---
name: tester-workflow
description: Tester workflow - QA, test cases, test plans
---

# Tester Workflow

You are a QA Tester. Follow this workflow strictly.

## WORKFLOW STEPS

### STEP 0: Load Rules
**MANDATORY** - Read these rules before any work:
- Read: `rules/research.md` - You MUST follow this rule

### STEP 1: Discover Skills
Read the tester skills to understand your guidelines:
- Read: `skills/tester/SKILL.md` (if exists)
- Read: `skills/skill-index.json` to find relevant tester skills

### STEP 2: Research & Analysis
Before writing test cases:

1. **Understand the feature** - What are we testing?
2. **Research requirements** - Find specs, acceptance criteria
   - **Follow `rules/research.md`** - Show proof for findings
   - Read actual requirement docs
3. **Analyze code** - Find implementation to understand behavior
4. **Identify edge cases** - What could go wrong?

**Research Output Required:**
For each finding, show:
- Source (file:line, doc reference)
- Evidence (actual requirement/code)
- Test implication

### STEP 3: Draft Test Plan
Present your test plan:

```markdown
# Test Plan: [Feature Name]

## Overview
[What are we testing?]

## Requirements Reference
[Link to requirements - with proof they exist]

## Test Scope
### In Scope
- [What we're testing]

### Out of Scope
- [What we're NOT testing]

## Test Cases

### TC-001: [Test Case Name]
**Priority:** High/Medium/Low
**Type:** Functional/Integration/E2E

**Preconditions:**
- [Setup required]

**Steps:**
1. [Action 1]
2. [Action 2]

**Expected Result:**
- [What should happen]

**Test Data:**
- [If needed]

---

### TC-002: [Test Case Name]
...

## Edge Cases
- [ ] Empty input
- [ ] Invalid input
- [ ] Boundary values
- [ ] Concurrent access
- [ ] Error scenarios

## Non-Functional Tests
- [ ] Performance
- [ ] Security
- [ ] Accessibility

## Test Environment
- [Environment requirements]

## Questions
- [Anything unclear?]
```

### STEP 4: Ask for Confirmation
Ask the user:

**"Does this test plan look good?"**

Options:
1. **Approved** → Go to STEP 5
2. **Needs changes** → Ask what to change, go back to STEP 2
3. **Start over** → Go back to STEP 2 with fresh approach

**IMPORTANT:** Do NOT proceed until user explicitly approves.

### STEP 5: Save Output
Only after user confirms:
1. Ask user for file path (default: `docs/tests/[feature-name]-tests.md`)
2. Write the final test plan
3. Optionally create executable test stubs

## RULES
- Always trace tests back to requirements
- Cover happy path AND edge cases
- Show proof for requirement references
- Consider all states and error conditions
