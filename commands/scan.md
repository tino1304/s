---
description: Analyze source code and document project structure
---

1. Warn user: "This scans your entire codebase. It may consume significant tokens." Confirm or STOP.
2. Check `CLAUDE.md` exists. If missing → tell user to run `/init` first, STOP.
3. Check `.claude/s/` exists. If missing → tell user to run `/s:init` first, STOP.
4. Read `CLAUDE.md` + project config files (`package.json`, `pubspec.yaml`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `tsconfig.json`, `vite.config.*`, `next.config.*`, `tailwind.config.*`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `mix.exs`, `Dockerfile`, `docker-compose.*`) to detect tech stack.
5. **Ask user if they want to generate project skills.** If `.claude/s/skills/` already has skill files (besides `mapper.md`), list them and ask: **regenerate** or **keep current**. If declined → set `SKIP_SKILLS=true`.

---

**Single-pass codebase scan (steps 6–7)**

6. Scan source code file by file. Skip generated files, node_modules, build output, lock files, config-only files. While scanning, collect ALL of the following in one pass:
   - **Structure:** group files into logical areas (auth, database, routing, UI, API, config, etc.)
   - **Patterns** (if `SKIP_SKILLS=false`): note architecture patterns, code style, conventions, naming, how handlers/components/data access/tests are written
   - **Reusables:** functions in utils/, helpers/, shared/, lib/, common/, hooks/, composables/, pkg/, internal/common/ and functions imported across many files
   - **TODOs:** lines matching `// TODO`, `# TODO`, `/* TODO`, `<!-- TODO`, `-- TODO`

7. After scanning, write all outputs:

**7a. Skills** (skip if `SKIP_SKILLS=true`):

Generate `.claude/s/skills/[topic].md` per relevant topic. Only topics that apply to this project. Each file 20-50 lines:
```
# [Topic Title]
[1-2 sentence summary for THIS project.]
## [Pattern]
  [code example using THIS project's real types/files/functions]
## Rules
- [prescriptive rules from this project's conventions]
```
Rules: use real code from this project, not generic templates. Be specific to actual libraries used. Prescriptive ("Use X", "Never Y"), not descriptive.

**7b. Mapper** — update `.claude/s/skills/mapper.md`:
```
# Skill Map
## Stack
| Language | Framework | Styling | State | Build | Test | Other |
## Skills
| Skill | File | Keywords | Description |
## Note for Agents
Read relevant skill files from `.claude/s/skills/` before writing code.
Also read `.claude/s/mapper.json` for reusable code locations.
```

**7c. Reusables** — update `.claude/s/mapper.json`:
```json
{"reusable": [{"name": "fn", "path": "src/utils/file.ts:42", "description": "What it does", "keywords": ["k1"]}]}
```

**7d. Backlog** — update `.claude/s/backlog.md` with TODO table (`| # | File | Line | TODO |`). If none found, write "No TODOs found."

**7e. Project overview** — create `.claude/s/docs/overview.md`:
```
# [Project Name]
## What It Does — 2-3 sentences explaining the project's purpose and who it's for
## Tech Stack — language, framework, key libraries, database, etc.
## Architecture — high-level architecture pattern (e.g. monolith, microservices, serverless) and how the main pieces fit together. Include a Mermaid diagram showing the top-level components and their relationships.
## Directory Structure — annotated tree of the top-level directories and what each contains
## Entry Points — where the app starts, main routes/commands, key config files
## Data Flow — how data moves through the system (request → handler → service → DB, etc.)
## Key Concepts — domain-specific terms or patterns a new developer needs to know
```

**7f. Structure docs** — create `.claude/s/docs/` with one `.md` per logical area:
```
# [Area Name]
## Purpose — one sentence
## Files — `path` — what it does
## How It Works — plain English walkthrough, numbered steps
## Key Functions — `fn()` in `file` — what it does
## Diagram — Mermaid, <15 nodes
## Depends On — [Other Area] — why
```
Create `.claude/s/docs/README.md` with overview Mermaid diagram + area list.

8. Show summary: stack, skills generated, areas found, file counts, output paths.

**Rules:** Write for humans. Short sentences. No jargon. Skip generated/build/lock files. For large projects, prioritize important areas first, note skipped sections. Do NOT modify source code.
