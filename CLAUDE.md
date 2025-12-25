# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Coze

Coze is a Claude Code plugin that provides agent-based development workflows with enforced rules. It manages agents (BA, Dev, Design, Tech Lead) through structured workflows, skills, and hooks.

## Architecture

```
coze/
├── commands/           # Slash commands (/s:ba, /s:dev, /s:tech-lead)
├── workflows/          # Workflow definitions (steps each agent follows)
├── skills/             # Agent-specific guidelines and patterns
│   ├── {agent}/SKILL.md
│   └── skill-index.json  # Keyword → skill mapping
├── rules/              # Mandatory rules (enforced by hooks)
├── hooks/hooks.json    # Hook configurations
├── scripts/            # Python scripts for hooks
└── .claude-plugin/     # Plugin manifest
```

## Flow: Command → Workflow → Skills → Rules

1. User runs `/s:{agent} [query]` (e.g., `/s:dev fix the login bug`)
2. `refine-prompt.py` enhances the request, asks confirmation
3. Command loads `workflows/{agent}-workflow.md`
4. Workflow reads `skills/{agent}/SKILL.md`
5. Rules enforced via hooks throughout execution

## Hooks (Enforced, Cannot Bypass)

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `session-rules.py` | Loads mandatory rules |
| UserPromptSubmit | `refine-prompt.py` | Asks if user wants prompt enhancement |
| UserPromptSubmit | `discover-skills.py` | Loads skills for @role prompts |
| PreToolUse | `enforce-write.py` | BLOCKS protected file writes |
| PreToolUse | `enforce-task-files.py` | Enforces task files in `.claude/tasks/` |
| PreToolUse | `enforce-build-only.py` | BLOCKS dev servers, only allows build/test |
| PreToolUse | `enforce-delegation.py` | BLOCKS code edits unless `.claude/.dev-mode` exists |
| PostToolUse | `enforce-research.py` | Reminds to show proof after research |

## Dev Mode (Code Editing)

Code editing is controlled by `.claude/.dev-mode` marker file:
- **Without marker:** Edit/Write to code files is BLOCKED
- **With marker:** Code editing is allowed

This ensures:
- Tech-lead cannot edit code directly (must spawn dev agents)
- Dev agents create the marker file first, then can edit code

**Flow:**
1. Tech-lead spawns dev agent with Task tool
2. Dev agent creates `.claude/.dev-mode`
3. Dev agent can now edit code files
4. Tech-lead reviews the work

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

1. Create `skills/{agent}/SKILL.md`
2. Create `workflows/{agent}-workflow.md`
3. Create `commands/{agent}.md`
4. Add to `skills/skill-index.json`
5. Add to `COZE_LLM_COMMANDS` in `scripts/refine-prompt.py`

## Workflow Structure (All Agents Follow)

```
STEP 0: Load Rules (rules/research.md)
STEP 1: Discover Skills
STEP 2: Research & Analysis (with proof)
STEP 3: Present Options/Draft
STEP 4: User Confirmation (loop if needed)
STEP 5+: Execute & Save
```

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
