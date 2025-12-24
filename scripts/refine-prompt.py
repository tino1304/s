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
COZE_LLM_COMMANDS = [
    "coze-ba",
    "coze-dev",
    "coze-design",
    "coze-pm",
    "coze-tester",
    "coze-tech-lead"
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

        # Check if it's a /coze-* command
        coze_match = re.match(r'^/(\w+[-\w]*)\s*(.*)', prompt, re.DOTALL)

        if coze_match:
            command = coze_match.group(1).lower()
            args = coze_match.group(2).strip()

            # Only refine coze LLM commands
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
            # Other slash commands - skip refinement
            sys.exit(0)

        # General prompts (not slash commands) - also refine
        else:
            output = f"""[COZE PROMPT REFINEMENT]

Before executing this request, you MUST:

1. **Analyze the prompt** and identify:
   - Main intent/goal
   - Any ambiguities or missing details
   - Implicit requirements

2. **Create an enhanced prompt** that:
   - Corrects any grammar/spelling issues
   - Adds specific details and context
   - Clarifies scope and expected output

3. **Present to user**:

---
**Original:** {prompt}

**Enhanced:**
[Your refined, detailed version]

**Added clarifications:**
- [What you added/clarified]
---

4. **Ask confirmation** using AskUserQuestion:
   - "Proceed with this enhanced prompt?"
   - Options: "Yes, proceed" / "No, let me modify"

5. **Only proceed** AFTER user confirms.

[END REFINEMENT]
"""
            print(output)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Refinement error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
