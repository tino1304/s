#!/usr/bin/env python3
"""
Prompt Refinement Hook for S Plugin

Applies to ALL user prompts. Asks user if they want enhancement before proceeding.
"""

import json
import sys
import re

# Skip refinement for these exact patterns (confirmations, short responses)
SKIP_PATTERNS = [
    "yes", "no", "ok", "approved", "confirm", "cancel",
    "y", "n", "done", "skip", "continue", "stop",
    "proceed", "looks good", "lgtm", "go ahead",
    "yes, proceed", "no, let me modify",
    "enhance", "don't enhance", "original"
]

# Skip refinement for commands that handle their own flow
SKIP_COMMAND_PATTERNS = [
    r'^/s:config',
    r'^/help',
    r'^/clear',
    r'^/compact',
    r'^/cost',
    r'^/doctor',
    r'^/init',
    r'^/login',
    r'^/logout',
    r'^/memory',
    r'^/model',
    r'^/permissions',
    r'^/review',
    r'^/status',
    r'^/terminal-setup',
    r'^/vim',
]

def should_skip(prompt: str) -> bool:
    """Check if prompt should skip refinement."""
    prompt_lower = prompt.lower().strip()

    # Skip short prompts
    if len(prompt_lower) < 10:
        return True

    # Skip exact confirmation patterns
    if prompt_lower in SKIP_PATTERNS:
        return True

    # Skip built-in commands
    for pattern in SKIP_COMMAND_PATTERNS:
        if re.match(pattern, prompt, re.IGNORECASE):
            return True

    return False

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        hook_input = json.loads(input_data)
        prompt = hook_input.get("prompt", "").strip()

        if not prompt:
            sys.exit(0)

        # Check if should skip
        if should_skip(prompt):
            sys.exit(0)

        # For all other prompts, ask user if they want enhancement
        output = f"""<prompt-refinement>
Before proceeding with the user's request, you MUST ask if they want prompt enhancement.

**User's Original Prompt:**
{prompt}

**Your Action:**
Use AskUserQuestion tool NOW with:
- Question: "Would you like me to enhance this prompt with more detail and clarity?"
- Options:
  1. "Enhance" - You will analyze and improve the prompt, then ask for confirmation
  2. "Original" - Proceed with the original prompt as-is

**If user selects "Enhance":**
1. Analyze the prompt for:
   - Main intent/goal
   - Ambiguities or missing details
   - Implicit requirements
2. Present:
   ---
   **Original:** {prompt}

   **Enhanced:** [Your refined, detailed version]

   **Clarifications added:**
   - [What you added/clarified]
   ---
3. Use AskUserQuestion with:
   - Question: "Proceed with this enhanced version?"
   - Options:
     1. "Yes, proceed" - Execute the enhanced prompt
     2. "No, let me modify" - User will provide changes

4. **CRITICAL LOOP:**
   - If "Yes, proceed" → Execute the task
   - If "No, let me modify" → Wait for user's changes, then:
     a. Update the enhanced prompt based on their feedback
     b. Present the NEW enhanced version
     c. Ask confirmation AGAIN using AskUserQuestion
     d. REPEAT until user selects "Yes, proceed"

   **NEVER execute until user explicitly selects "Yes, proceed"**

**If user selects "Original":**
Proceed with the original prompt immediately.

</prompt-refinement>"""
        print(output)
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Refinement error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
