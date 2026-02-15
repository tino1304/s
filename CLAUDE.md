# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Coze

Coze is a Claude Code plugin that provides agent-based development workflows with enforced rules. It manages agents through structured workflows, skills, and hooks.

## Architecture

```
coze/
├── commands/           # Slash commands (/s:a, /s:init, /s:launch, /s:refine, /s:scan, /s:backlog, /s:backlog-add, /s:backlog-rm)
├── skills/             # Skill guidelines per language/framework
│   ├── dev/{lang}/*.md
│   └── skill-index.json  # Keyword → skill mapping
├── rules/              # Mandatory rules (enforced by hooks)
├── hooks/hooks.json    # Hook configurations
├── scripts/            # Python scripts for hooks
└── .claude-plugin/     # Plugin manifest
```

## Flow

1. User runs `/s:a [query]` or other commands (`/s:launch`, `/s:init`, `/s:refine`, `/s:scan`, `/s:backlog`)
2. Command file (`commands/*.md`) executes with embedded workflow
3. Rules enforced via hooks throughout execution

## Hooks (Enforced, Cannot Bypass)

| Hook | Script | Purpose |
|------|--------|---------|
| PreToolUse | `enforce-write.py` | BLOCKS protected file writes (`.env.example` allowed) |
| PreToolUse | `enforce-build-only.py` | BLOCKS dev servers, only allows build/test |
| PostToolUse | `enforce-research.py` | Reminds to show proof after research |

## Rules (MANDATORY)

### Research Rule
Every research finding must include:
- **Source:** file:line or URL
- **Evidence:** actual quote/code
- **Conclusion:** interpretation

Never say "probably" or "likely" without evidence. If not found, say "Not found."

## Adding New Skills

1. Create skill file in `skills/dev/{lang}/`
2. Add entry to `skills/skill-index.json` with keywords
