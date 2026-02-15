# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Coze

Coze is a Claude Code plugin that provides agent-based development workflows with enforced rules. It manages agents through structured workflows, skills, and hooks.

## Architecture

```
coze/
├── commands/           # Slash commands (/s:go, /s:init, /s:launch, /s:refine)
├── skills/             # Additional guidelines for @role prompts
│   ├── {agent}/SKILL.md
│   └── skill-index.json  # Keyword → skill mapping
├── rules/              # Mandatory rules (enforced by hooks)
├── hooks/hooks.json    # Hook configurations
├── scripts/            # Python scripts for hooks
└── .claude-plugin/     # Plugin manifest
```

## Flow

**Option 1: `/s:{agent}` commands**
1. User runs `/s:{agent} [query]` (e.g., `/s:launch build the auth system`)
2. Command file (`commands/{agent}.md`) executes with embedded workflow
3. Rules enforced via hooks throughout execution

## Hooks (Enforced, Cannot Bypass)

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `session-rules.py` | Loads mandatory rules |
| PreToolUse | `enforce-write.py` | BLOCKS protected file writes (`.env.example` allowed) |
| PreToolUse | `enforce-task-files.py` | Enforces task files in `.claude/tasks/` |
| PreToolUse | `enforce-build-only.py` | BLOCKS dev servers, only allows build/test |
| PostToolUse | `enforce-research.py` | Reminds to show proof after research |

## Rules (MANDATORY)

### Research Rule
Every research finding must include:
- **Source:** file:line or URL
- **Evidence:** actual quote/code
- **Conclusion:** interpretation

Never say "probably" or "likely" without evidence. If not found, say "Not found."

## Adding New Agents

1. Create `commands/{agent}.md` with embedded workflow

## Agent Communication

All agents communicate via `.md` files in target project's `.claude/tasks/`:

```
.claude/tasks/
├── task-001-feature.md   # Single file: Assignment + Report + Review
├── task-002-bugfix.md
└── TRACKER.md            # Master status
```

Hook `enforce-task-files.py` enforces:
- Task files must be in `.claude/tasks/`
- Task files must have `## Assignment`, `## Report`, `## Review` sections
- Auto-creates `.claude/tasks/` directory
