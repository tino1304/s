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
| `/s:a` | Execute a task with project-specific skills loaded |
| `/s:init` | Initialize S plugin for current project (detect tech stack, create skill mapping) |
| `/s:launch` | Launch parallel sub-agents for complex tasks |
| `/s:refine` | Refine and enhance a prompt before running |
| `/s:scan` | Analyze source code and document project structure with diagrams |
| `/s:backlog` | Show pending TODOs from backlog |
| `/s:backlog-add` | Add a new backlog item |
| `/s:backlog-rm` | Remove a backlog item by number |

### Usage

```
/s:a build the auth handler
/s:launch build the auth system with login, API routes, and database
/s:init
/s:scan
/s:backlog
/s:backlog-add implement caching layer
/s:backlog-rm 3
```

## How It Works

```
/s:a [query]
       │
       ▼
┌─────────────────┐
│ Execute Command │  ← commands/a.md (loads relevant skills)
└────────┬────────┘
         ▼
┌─────────────────┐
│ Enforce Rules   │  ← Hooks run throughout execution
└─────────────────┘
```

## Skills

Skills are small, focused guideline files organized by language/framework:

```
skills/dev/
├── react/       # components, hooks, state, styling, testing
├── nodejs/      # structure, validation, database, errors
├── golang/      # structure, handlers, database, concurrency
└── flutter/     # widgets, state, navigation, data
```

`/s:init` detects your project's tech stack and maps relevant skills. `/s:a` loads only the skills needed for each request.

## Enforced Rules

### Research Rule
Every finding must include proof:
- **Source:** file:line or URL
- **Evidence:** actual quote/code
- **Conclusion:** your interpretation

## Hooks

| Hook | Purpose |
|------|---------|
| `enforce-write.py` | Blocks writes to protected files (`.env.example` allowed) |
| `enforce-build-only.py` | Blocks dev servers, only allows build/test |
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
