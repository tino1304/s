---
description: Start Tester workflow for QA and test planning
allowed-tools: Read, Glob, Task, AskUserQuestion
---

# Tester Workflow Execution

**User Request:** $ARGUMENTS

## Instructions

1. First, read the workflow definition:
   - Read: `workflows/tester-workflow.md`

2. Then, read the tester skills (if available):
   - Read: `skills/tester/SKILL.md`

3. Execute the workflow steps exactly as defined.

4. Tool permissions:
   - Read-only tools are allowed by default
   - Write, Edit, Bash require user confirmation

5. Remember:
   - Trace tests back to requirements
   - Cover edge cases and error states
   - Wait for confirmation before finalizing
