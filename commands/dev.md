---
description: Start Dev workflow for implementation tasks
allowed-tools: Read, Glob, Task, AskUserQuestion
---

# Dev Workflow Execution

**User Request:** $ARGUMENTS

## Instructions

1. First, read the workflow definition:
   - Read: `${CLAUDE_PLUGIN_ROOT}/workflows/dev-workflow.md`

2. Then, read the dev skills (match to task):
   - Read: `${CLAUDE_PLUGIN_ROOT}/skills/dev/` directory for relevant skills

3. Execute the workflow steps exactly as defined.

4. Tool permissions:
   - Read-only tools are allowed by default
   - Write, Edit, Bash require user confirmation
   - Always show plan and get approval before coding

5. Remember:
   - Research first, show proof
   - Present implementation plan
   - Wait for confirmation before writing code
