# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Coze

Coze is a Claude Code plugin that provides agent-based development workflows with enforced rules. It manages agents (BA, Dev, Design, Tech Lead) through structured workflows, skills, and hooks.

## Architecture

```
coze/
├── commands/           # Slash commands with embedded workflows (/s:ba, /s:dev, /s:tech-lead)
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
1. User runs `/s:{agent} [query]` (e.g., `/s:dev fix the login bug`)
2. `refine-prompt.py` asks if user wants prompt enhancement
3. Command file (`commands/{agent}.md`) executes with embedded workflow
4. Rules enforced via hooks throughout execution

**Option 2: `@role` prompts**
1. User types `@dev some task` or `@ba analyze this`
2. `discover-skills.py` loads matching skills from `skills/{role}/`
3. Claude follows the skill guidelines

## Hooks (Enforced, Cannot Bypass)

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `session-rules.py` | Loads mandatory rules |
| UserPromptSubmit | `refine-prompt.py` | Asks if user wants prompt enhancement |
| UserPromptSubmit | `discover-skills.py` | Loads skills for @role prompts |
| PreToolUse | `enforce-write.py` | BLOCKS protected file writes |
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

### Atomic Tasks Rule (Tech Lead)
Tasks must be atomic - smallest unit of work that delivers value:
- One task = one focus (single responsibility)
- Max 1-3 files per task
- If 4+ files or description > 10 lines → break it down

## Adding New Agents

1. Create `commands/{agent}.md` with embedded workflow
2. (Optional) Create `skills/{agent}/SKILL.md` for @role prompts
3. (Optional) Add to `skills/skill-index.json` for keyword matching

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
