---
description: Remove a backlog item
---

**Args:** $ARGUMENTS

1. Read `.claude/s/backlog.md`. If missing → tell user nothing to remove, STOP.
2. Parse `$ARGUMENTS` as the item `#` to remove.
3. Remove the matching row from the table.
4. Renumber remaining rows sequentially.
5. Confirm the item was removed.
