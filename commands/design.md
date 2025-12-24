---
description: Start Design workflow for UI/UX tasks
allowed-tools: Read, Glob, Task, AskUserQuestion
---

# Design Workflow Execution

**User Request:** $ARGUMENTS

## Instructions

1. First, read the workflow definition:
   - Read: `${CLAUDE_PLUGIN_ROOT}/workflows/design-workflow.md`

2. Then, read the design skills (if available):
   - Read: `${CLAUDE_PLUGIN_ROOT}/skills/design/SKILL.md`

3. Execute the workflow steps exactly as defined.

4. Tool permissions:
   - Read-only tools are allowed by default
   - Write, Edit require user confirmation

5. Remember:
   - Research existing patterns first
   - Present design proposal with all states
   - Wait for confirmation before finalizing
