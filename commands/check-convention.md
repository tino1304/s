---
description: Check if project code follows skill conventions
---

**Target:** $ARGUMENTS

1. Check `.claude/s/skills/` exists and has at least one `.md` file (besides `mapper.md`). If not → "No skill files found. Run `/s:scan` to generate skills first." STOP.
2. If **Target** is empty → warn user: "This will scan your entire codebase against skill conventions. It may consume significant tokens." Confirm or STOP.
3. If **Target** is provided → verify the path exists. If not → "Path not found: [target]." STOP.

4. Read all skill files from `.claude/s/skills/` (exclude `mapper.md`). Extract every rule and convention.

5. Scan source code against loaded skill rules. If **Target** is a file, check that file only. If **Target** is a folder, check all files in it recursively. If no target, check entire project. Skip: node_modules, build output, generated files, lock files, test fixtures.

   Track:
   - **Violations** — code contradicts a skill rule
   - **Inconsistencies** — code uses a different pattern than the skill describes
   - **Missing patterns** — places where a skill pattern should apply but doesn't

6. Write `.claude/s/convention-report.md`:

```markdown
# Convention Report

Scope: [target path or "entire project"]

## Summary
| Files scanned | Violations | Inconsistencies | Compliance |
|---------------|------------|-----------------|------------|

## Violations
| # | File | Line | Skill | Rule | Issue |
|---|------|------|-------|------|-------|

## Inconsistencies
| # | File | Line | Skill | Expected | Found |
|---|------|------|-------|----------|-------|

## Suggestions
- [Actionable fix for common violations]
```

If no issues → write "All code follows skill conventions."

7. Show summary: scope, files scanned, violation count, compliance percentage.
