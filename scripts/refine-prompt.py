#!/usr/bin/env python3
"""
Prompt Refinement Hook for Coze Toolkit

Refines user prompts before LLM execution.
Triggers for /coze-* commands and general prompts.
"""

import json
import sys
import re

# Commands that need LLM actions (trigger refinement)
# Plugin name is "s", commands are "dev", "ba", etc.
# When installed: /s:dev, /s:ba, /s:design, /s:tech-lead
COZE_LLM_COMMANDS = [
    "s:ba",
    "s:dev",
    "s:design",
    "s:tech-lead"
]

# Commands to skip refinement (they do their own refinement)
SKIP_COMMANDS = [
    "s:refine",
    "s:config"
]

# Skip refinement for these patterns
SKIP_PATTERNS = [
    "yes", "no", "ok", "approved", "confirm", "cancel",
    "y", "n", "done", "skip", "continue", "stop",
    "proceed", "looks good", "lgtm"
]

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        hook_input = json.loads(input_data)
        prompt = hook_input.get("prompt", "").strip()

        if not prompt:
            sys.exit(0)

        prompt_lower = prompt.lower().strip()

        # Skip short confirmations
        if prompt_lower in SKIP_PATTERNS or len(prompt_lower) < 5:
            sys.exit(0)

        # Check if it's a /s:* command (e.g., /s:dev, /s:tech-lead)
        coze_match = re.match(r'^/(s:[a-z-]+)\s*(.*)', prompt, re.DOTALL | re.IGNORECASE)

        if coze_match:
            command = coze_match.group(1).lower()
            args = coze_match.group(2).strip()

            # Skip commands that handle their own refinement
            if command in SKIP_COMMANDS:
                sys.exit(0)

            # Only refine s:* LLM commands
            if command in COZE_LLM_COMMANDS:
                if not args or len(args) < 5:
                    sys.exit(0)  # No args to refine

                output = f"""[COZE PROMPT REFINEMENT]

**Command detected:** /{command}
**Arguments:** {args}

Before executing, you MUST:

1. **Analyze the arguments** and identify:
   - Main intent/goal
   - Any ambiguities or missing details
   - Implicit requirements

2. **Create enhanced arguments** that:
   - Correct any grammar/spelling issues
   - Add specific details and context
   - Clarify scope and expected output

3. **Present to user**:

---
**Command:** /{command}

**Original:** {args}

**Enhanced:**
[Your refined, detailed version of the arguments]

**Added clarifications:**
- [What you added/clarified]
---

4. **Ask confirmation** using AskUserQuestion:
   - "Proceed with this enhanced request?"
   - Options: "Yes, proceed" / "No, let me modify"

5. **Only execute** the /{command} workflow AFTER user confirms.

[END REFINEMENT]
"""
                print(output)
        # Non-matching commands - skip refinement
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Refinement error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
