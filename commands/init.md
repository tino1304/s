---
description: Initialize S plugin for current project
---

1. Check `CLAUDE.md` exists. If missing → tell user to run `/init` first, STOP.
2. Read `CLAUDE.md` + project config files (`package.json`, `pubspec.yaml`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `tsconfig.json`, `vite.config.*`, `next.config.*`, `tailwind.config.*`) to detect tech stack.
3. Read `${CLAUDE_PLUGIN_ROOT}/skills/skill-index.json`. Match project tech against skill keywords.
4. Create `.claude/s/skills.md`:

```markdown
# Project Skills

## Matched
- **[name]** → `[skill path]` (matched: [keywords])

## Stack
Language | Framework | Styling | State | Build | Test | Other
```

5. Show summary. Do NOT modify CLAUDE.md.
