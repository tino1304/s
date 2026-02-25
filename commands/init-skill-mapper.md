---
description: Generate mapper.md from existing skill files
---

1. Read all `.md` files in `.claude/s/skills/` (exclude `mapper.md` itself). If no skill files found → tell user "No skill files found in `.claude/s/skills/`. Run `/s:scan` to generate skills first." STOP.

2. For each skill file, extract:
   - **Skill name** — derived from filename (e.g. `api-handlers.md` → `api-handlers`)
   - **Keywords** — identify 5-10 keywords an agent would encounter during coding that should trigger this skill. Think: what would the agent be working on when this skill applies? Include language names, framework names, function patterns, file types, library names, common terms from the skill's rules.
   - **When to use** — one clear sentence: "Use when [specific coding scenario]." This must be unambiguous so an agent selecting skills won't miss it.
   - **Key rules summary** — 2-3 most critical rules from the skill, condensed to short phrases.

3. Write `.claude/s/skills/mapper.md`:

```markdown
# Skill Map

> **How to use:** Before writing ANY code, scan this table. Match your task against the **When to Use** column. Load ALL matching skill files. When in doubt, load the skill — it's better to over-match than to miss a relevant guideline.

## Stack
| Language | Framework | Styling | State | Build | Test | Other |
|----------|-----------|---------|-------|-------|------|-------|
| [detect from skill contents] | | | | | | |

## Skills

| # | Skill | File | When to Use | Keywords | Key Rules |
|---|-------|------|-------------|----------|-----------|
| 1 | [name] | `[file].md` | [clear scenario] | [5-10 keywords] | [2-3 critical rules] |

## Quick Match Guide

Group skills by coding activity for fast lookup:

- **Building UI?** → [list relevant skill files]
- **Writing API/handlers?** → [list relevant skill files]
- **Working with data/DB?** → [list relevant skill files]
- **Writing tests?** → [list relevant skill files]
- **Styling?** → [list relevant skill files]
- **State management?** → [list relevant skill files]
- **Project structure?** → [list relevant skill files]

Only include groups that have matching skills. Add custom groups if skills don't fit the above.

## Note for Agents
1. Read this file FIRST before any coding task.
2. Match your task against **When to Use** and **Keywords**.
3. Load ALL matching `.md` files from `.claude/s/skills/`.
4. Also read `.claude/s/mapper.json` for reusable code locations.
```

4. Show summary: number of skills indexed, list of skill files mapped.
