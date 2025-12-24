---
description: Start Tech Lead workflow - manage dev agents, break down requirements, review code
allowed-tools: Read, Glob, Task, AskUserQuestion
---

# Tech Lead Workflow Execution

**User Request:** $ARGUMENTS

## Instructions

1. First, read the workflow definition:
   - Read: `${CLAUDE_PLUGIN_ROOT}/workflows/tech-lead-workflow.md`

2. Then, read the tech lead skills:
   - Read: `${CLAUDE_PLUGIN_ROOT}/skills/tech-lead/SKILL.md`

3. Execute the workflow steps exactly as defined.

4. Tool permissions:
   - Read-only tools are allowed by default
   - Write, Edit require user confirmation
   - Task tool for spawning dev agents (with confirmation)

5. Remember:
   - All dev agent communication through .md files
   - Break down requirements into atomic tasks
   - Review all code changes
   - Track progress in TRACKER.md
   - Report to user with proof
