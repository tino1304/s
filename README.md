# S Plugin for Claude Code

Agent-based development workflows with enforced rules for Claude Code.

## Installation

```bash
# Add marketplace
/plugin marketplace add your-username/coze

# Install plugin
/plugin install s
```

Or test locally:
```bash
claude --plugin-dir /path/to/coze
```

## Commands

| Command | Description |
|---------|-------------|
| `/s:go` | Execute a task with project-specific skills loaded |
| `/s:init` | Initialize S plugin for current project (detect tech stack, create skill mapping) |
| `/s:launch` | Launch parallel sub-agents for complex tasks |
| `/s:refine` | Refine and enhance a prompt before running |

### Usage

```
/s:launch build the auth system with login, API routes, and database
```

## How It Works

```
/s:{agent} [query]
       │
       ▼
┌─────────────────┐
│ Execute Command │  ← commands/{agent}.md (has embedded workflow)
└────────┬────────┘
         ▼
┌─────────────────┐
│ Enforce Rules   │  ← Hooks run throughout execution
└─────────────────┘
```

## Agent Communication

Agents communicate via `.md` files in your project's `.claude/tasks/` folder:

```
your-project/
└── .claude/
    └── tasks/
        ├── task-001-feature.md   # Assignment + Report + Review
        ├── task-002-bugfix.md
        └── TRACKER.md            # Master status
```

### Task File Format

Each task file has three sections:

```markdown
# Task: TASK-001 Add login button

## Assignment
(Tech Lead fills: objective, requirements, acceptance criteria)

## Report
(Dev agent fills: changes made, decisions, deviations)

## Review
(Tech Lead fills: approved/changes requested, feedback)
```

## Enforced Rules

### Research Rule
Every finding must include proof:
- **Source:** file:line or URL
- **Evidence:** actual quote/code
- **Conclusion:** your interpretation

## Hooks

| Hook | Purpose |
|------|---------|
| `enforce-task-files.py` | Ensures task files go to `.claude/tasks/` |
| `enforce-write.py` | Blocks writes to protected files (`.env.example` allowed) |
| `enforce-research.py` | Reminds to show proof after research |

## Updating

```bash
# Update to latest version
/plugin update s

# Restart Claude to apply
exit
claude
```

## License

MIT
