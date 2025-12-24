#!/usr/bin/env python3
"""
Session Start Rules Loader

Injects mandatory rules at the start of every session.
These rules cannot be bypassed.
"""

import sys
import os
from pathlib import Path

def main():
    # Get plugin root
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT', '')

    if plugin_root:
        rules_path = Path(plugin_root) / "rules" / "research.md"
    else:
        # Fallback
        rules_path = Path(__file__).parent.parent / "rules" / "research.md"

    rules = """
╔══════════════════════════════════════════════════════════════╗
║                    COZE TOOLKIT ACTIVE                       ║
║                  MANDATORY RULES LOADED                      ║
╚══════════════════════════════════════════════════════════════╝

RULE 1: RESEARCH PROOF REQUIRED
- Every claim needs SOURCE + EVIDENCE + CONCLUSION
- Never say "probably" or "likely" without proof
- If you didn't find it, say "Not found" - don't imagine

RULE 2: CONFIRMATION BEFORE ACTION
- Show plan before writing code
- Present options before deep diving
- Ask before modifying files

RULE 3: PROTECTED FILES BLOCKED
- .env, credentials, secrets → Always blocked
- User must explicitly confirm protected file changes

These rules are ENFORCED by hooks and cannot be bypassed.
"""

    # Also load research.md if exists
    if rules_path.exists():
        with open(rules_path) as f:
            research_content = f.read()
        rules += f"\n--- FULL RESEARCH RULE ---\n{research_content}"

    print(rules)
    sys.exit(0)

if __name__ == "__main__":
    main()
