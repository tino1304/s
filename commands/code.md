---
description: Execute task with project skills
---

**Request:** $ARGUMENTS

1. Read `.claude/s/skills/mapper.md`. If missing → tell user to run `/s:init` first, STOP.
2. Based on the request, pick only the relevant skill(s) from the Skills table. Read only those skill files from `.claude/s/skills/[file]`.
3. Execute the request following loaded skill guidelines and project CLAUDE.md.

**Rule:** Always break code into small, focused files. Extract reusable logic into shared modules. No large monolithic files.
