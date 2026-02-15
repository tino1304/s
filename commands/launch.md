---
description: Launch parallel sub-agents for complex tasks
---

**Request:** $ARGUMENTS

1. Read `.claude/s/skills.md`. If missing → tell user to run `/s:init` first, STOP.
2. Decompose into **2-5 independent subtasks**. Present per agent: focus, files, deliverable.
3. Ask user to confirm before launching.
4. **Spawn ALL subtasks in a SINGLE message** using Task tool (parallel). Use "general-purpose" for code, "Explore" for research. Each agent prompt MUST start with: "First, read `.claude/s/skills.md` and follow the matched skill guidelines." followed by the subtask details.
5. After all complete: review outputs, resolve conflicts, run build/test.
6. Show summary.
