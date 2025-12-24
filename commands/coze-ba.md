---
description: Start BA workflow for feature analysis and proposal creation
allowed-tools: Read, Glob, Task, AskUserQuestion
---

# BA Workflow Execution

**User Request:** $ARGUMENTS

## Instructions

1. First, read the workflow definition:
   - Read: `workflows/ba-workflow.md`

2. Then, read the BA skills (if available):
   - Read: `skills/ba/SKILL.md`

3. Execute the workflow steps exactly as defined.

4. Tool permissions:
   - Read-only tools are allowed by default
   - Write, Edit, Bash, WebSearch, WebFetch require user confirmation
   - Always ask before modifying files

5. Remember:
   - Show draft proposal and wait for user confirmation
   - Loop back if user wants changes
   - Only save to file after explicit approval
