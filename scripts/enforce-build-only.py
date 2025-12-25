#!/usr/bin/env python3
"""
Block Dev Server Commands Hook

Blocks dev server commands (npm run dev, go run, etc.) that run indefinitely.
Use build/test commands to validate code instead.
"""

import json
import sys
import re

# DEV SERVER patterns to BLOCK (these run indefinitely)
BLOCKED_PATTERNS = [
    # Node.js / JavaScript dev servers
    r'\bnpm\s+run\s+dev\b',
    r'\bnpm\s+start\b',
    r'\bnpx\s+next\s+dev\b',
    r'\bnpx\s+vite\b(?!\s+build)',
    r'\bnpx\s+nuxt\s+dev\b',
    r'\byarn\s+dev\b',
    r'\byarn\s+start\b',
    r'\bpnpm\s+dev\b',
    r'\bpnpm\s+start\b',
    r'\bbun\s+dev\b',
    r'\bbun\s+run\s+dev\b',

    # Python dev servers
    r'\bpython.*\s+runserver\b',
    r'\bflask\s+run\b',
    r'\buvicorn\b(?!.*--help)',
    r'\bgunicorn\b(?!.*--help)',
    r'\bmanage\.py\s+runserver\b',

    # Go
    r'\bgo\s+run\b',
    r'\bair\b',

    # Ruby
    r'\brails\s+server\b',
    r'\brails\s+s\b',

    # PHP
    r'\bphp\s+artisan\s+serve\b',
    r'\bphp\s+-S\b',

    # Rust
    r'\bcargo\s+run\b(?!\s+--release)',
    r'\bcargo\s+watch\b',

    # General watch/dev patterns
    r'\bnodemon\b',
    r'\bts-node-dev\b',
    r'\btsx\s+watch\b',
]

def is_dev_server_command(command: str) -> bool:
    """Check if command is a blocked dev server command."""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        hook_input = json.loads(input_data)
        tool_name = hook_input.get("tool_name", "")
        tool_input = hook_input.get("tool_input", {})

        # Only check Bash commands
        if tool_name != "Bash":
            sys.exit(0)

        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        # Check if it's a dev server command
        if is_dev_server_command(command):
            result = {
                "decision": "block",
                "reason": f"""BLOCKED: Dev server commands are not allowed.

Command: {command}

Dev servers run indefinitely and cannot validate code.
Use build/test commands instead:
- npm run build
- npm run typecheck / npx tsc --noEmit
- npm test / go test / pytest"""
            }
            print(json.dumps(result))
            sys.exit(0)

        # Allow all other commands
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Command check error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
