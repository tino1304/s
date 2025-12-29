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
| `/s:dev` | Developer - implementation tasks |
| `/s:ba` | Business Analyst - requirements & user stories |
| `/s:design` | Designer - UI/UX design tasks |
| `/s:tech-lead` | Tech Lead - manage dev agents, break down tasks |
| `/s:refine` | Refine and enhance a prompt before running |
| `/s:config` | Configure plugin settings |

## Configuration

Toggle auto-accept mode (skip confirmation prompts):

```bash
# Enable autonomous mode (no confirmations)
/s:config auto-accept true

# Disable autonomous mode (default, asks for confirmations)
/s:config auto-accept false

# Show current settings
/s:config show
```

Config is stored in `.claude/s-config.json` in your project.

### Usage

```
/s:dev fix the login button not responding on mobile

/s:ba analyze requirements for user checkout flow

/s:tech-lead break down the authentication feature into tasks
```

## How It Works

```
/s:{agent} [query]
       │
       ▼
┌─────────────────┐
│ Prompt Refinement│  ← Enhances your query, asks confirmation
└────────┬────────┘
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

### Atomic Tasks Rule (Tech Lead)
Tasks must be small and focused:
- One task = one responsibility
- Max 1-3 files per task
- If 4+ files → break it down

## Hooks

| Hook | Purpose |
|------|---------|
| `refine-prompt.py` | Enhances prompts before execution |
| `enforce-task-files.py` | Ensures task files go to `.claude/tasks/` |
| `enforce-write.py` | Blocks writes to protected files |
| `enforce-research.py` | Reminds to show proof after research |

## Workflow Steps

Each agent has its own workflow embedded in `commands/{agent}.md`. Example (BA):

1. **Enhance Prompt** - Refine user request, ask confirmation
2. **Critical Thinking** - Identify unknowns, plan research
3. **Spawn Research Agents** - Parallel research via sub-agents
4. **Synthesize & Present Options** - Show findings and options
5. **User Confirmation** - Get approval
6. **Execute & Save** - Create deliverable

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
