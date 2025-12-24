# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Coze

Coze is a Claude Code plugin/toolkit that provides role-based development workflows with enforced rules. It manages agents (BA, Dev, Design, PM, Tester, Tech Lead) through structured workflows, skills, and hooks.

## Architecture

```
coze/
├── commands/           # Slash commands (/coze-ba, /coze-dev, etc.)
├── workflows/          # Workflow definitions (steps each role follows)
├── skills/             # Role-specific guidelines and patterns
│   ├── {role}/SKILL.md
│   └── skill-index.json  # Keyword → skill mapping
├── rules/              # Mandatory rules (enforced by hooks)
├── hooks/hooks.json    # Hook configurations
├── scripts/            # Python scripts for hooks
└── .claude-plugin/     # Plugin manifest
```

## Flow: Command → Workflow → Skills → Rules

1. User runs `/coze-{role} [request]`
2. `refine-prompt.py` enhances the request, asks confirmation
3. Command loads `workflows/{role}-workflow.md`
4. Workflow reads `skills/{role}/SKILL.md`
5. Rules enforced via hooks throughout execution

## Hooks (Enforced, Cannot Bypass)

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `session-rules.py` | Loads mandatory rules |
| UserPromptSubmit | `refine-prompt.py` | Enhances prompts before execution |
| UserPromptSubmit | `discover-skills.py` | Loads skills for @role prompts |
| PreToolUse | `enforce-write.py` | BLOCKS protected file writes |
| PostToolUse | `enforce-research.py` | Reminds to show proof after research |

## Research Rule (MANDATORY)

Every research finding must include:
- **Source:** file:line or URL
- **Evidence:** actual quote/code
- **Conclusion:** interpretation

Never say "probably" or "likely" without evidence. If not found, say "Not found."

## Adding New Roles

1. Create `skills/{role}/SKILL.md`
2. Create `workflows/{role}-workflow.md`
3. Create `commands/coze-{role}.md`
4. Add to `skills/skill-index.json`
5. Add to `COZE_LLM_COMMANDS` in `scripts/refine-prompt.py`

## Workflow Structure (All Roles Follow)

```
STEP 0: Load Rules (rules/research.md)
STEP 1: Discover Skills
STEP 2: Research & Analysis (with proof)
STEP 3: Present Options/Draft
STEP 4: User Confirmation (loop if needed)
STEP 5+: Execute & Save
```

## Tech Lead Special Flow

Tech Lead manages dev agents via `.md` files in `docs/tasks/`:
- `task-XXX-name.md` - Task assignment
- `task-XXX-report.md` - Dev agent's report
- `task-XXX-review.md` - Tech lead's review
- `TRACKER.md` - Master status
