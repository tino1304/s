---
description: Quick introduction and usage guide for S plugin
---

Display this guide exactly:

---

**S Plugin** — Agent-based development workflows with enforced rules.

## Quick Start

1. **`/s:init`** — Run this first. Detects your tech stack and maps relevant skills.
2. **`/s:a [task]`** — Execute a task with matched skill guidelines loaded.
3. **`/s:launch [task]`** — Split a complex task into parallel sub-agents.

## All Commands

| Command | What it does |
|---------|-------------|
| `/s:a [task]` | Execute task with project skills |
| `/s:launch [task]` | Decompose into 2-5 parallel sub-agents |
| `/s:refine [task]` | Enhance a prompt before running it |
| `/s:init` | Detect tech stack, create skill mapping |
| `/s:scan` | Analyze codebase, generate structure docs |
| `/s:backlog` | Show pending TODOs |
| `/s:backlog-add [item]` | Add a TODO item |
| `/s:backlog-rm [#]` | Remove a TODO by number |
| `/s:help` | This guide |

## How It Works

```
/s:a build the auth handler
      │
      ▼
  Load .claude/s/skills.md → pick relevant skills → execute with guidelines
      │
      ▼
  Hooks enforce rules throughout (write protection, research proof, no dev servers)
```

## Skills Available

React (components, hooks, state, styling, testing) · Node.js (structure, validation, database, errors) · Go (structure, handlers, database, concurrency) · Flutter (widgets, state, navigation, data)

## Tips

- Run `/s:init` once per project. Re-run to refresh after stack changes.
- Use `/s:launch` for tasks that touch multiple areas (e.g. "build auth with API, UI, and tests").
- Use `/s:refine` when your prompt is vague — it clarifies before executing.
- `/s:scan` generates docs in `.claude/docs/structures/` with Mermaid diagrams.

---
