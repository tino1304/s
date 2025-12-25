#!/usr/bin/env python3
"""
Enforce Build Only Hook

Blocks dev server commands. Only allows build/test/typecheck commands.
This prevents agents from running long-running dev servers.
"""

import json
import sys
import re

# Patterns for DEV commands (BLOCKED)
DEV_PATTERNS = [
    # Node.js / JavaScript
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

    # Python
    r'\bpython.*\s+runserver\b',
    r'\bpython.*\s+run\b',
    r'\bflask\s+run\b',
    r'\buvicorn\b(?!.*--help)',
    r'\bgunicorn\b(?!.*--help)',
    r'\bdjango-admin\s+runserver\b',
    r'\bmanage\.py\s+runserver\b',

    # Go
    r'\bgo\s+run\b',
    r'\bair\b',  # Go live reload

    # Ruby
    r'\brails\s+server\b',
    r'\brails\s+s\b',
    r'\bbundle\s+exec\s+rails\s+s',

    # PHP
    r'\bphp\s+artisan\s+serve\b',
    r'\bphp\s+-S\b',

    # Rust
    r'\bcargo\s+run\b(?!\s+--release)',
    r'\bcargo\s+watch\b',

    # General
    r'\bserve\b',
    r'\b--watch\b',
    r'\b-w\b(?=.*\bnode\b)',
    r'\bnodemon\b',
    r'\bts-node-dev\b',
    r'\btsx\s+watch\b',
]

# Patterns for BUILD commands (ALLOWED)
BUILD_PATTERNS = [
    r'\bnpm\s+run\s+build\b',
    r'\bnpm\s+run\s+typecheck\b',
    r'\bnpm\s+run\s+type-check\b',
    r'\bnpm\s+run\s+lint\b',
    r'\bnpm\s+run\s+test\b',
    r'\bnpm\s+test\b',
    r'\byarn\s+build\b',
    r'\byarn\s+typecheck\b',
    r'\byarn\s+test\b',
    r'\bpnpm\s+build\b',
    r'\bpnpm\s+typecheck\b',
    r'\bpnpm\s+test\b',
    r'\bbun\s+run\s+build\b',
    r'\bnpx\s+tsc\b',
    r'\bnpx\s+next\s+build\b',
    r'\bnpx\s+vite\s+build\b',
    r'\bgo\s+build\b',
    r'\bgo\s+test\b',
    r'\bcargo\s+build\b',
    r'\bcargo\s+test\b',
    r'\bpytest\b',
    r'\bmypy\b',
    r'\bruff\b',
    r'\bblack\b',
    r'\bmake\s+build\b',
    r'\bmake\s+test\b',
]

def is_dev_command(command: str) -> bool:
    """Check if command is a blocked dev server command."""
    for pattern in DEV_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def is_build_command(command: str) -> bool:
    """Check if command is an allowed build command."""
    for pattern in BUILD_PATTERNS:
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

        # Check if it's a dev command
        if is_dev_command(command):
            # Output block decision
            result = {
                "decision": "block",
                "reason": f"""BLOCKED: Dev server commands are not allowed.

Command: {command}

Use build/test commands instead:
- npm run build / pnpm build / yarn build
- npm run typecheck / npx tsc --noEmit
- npm test / go test / pytest
- npm run lint

Dev servers (npm run dev, go run, etc.) are blocked because:
1. They run indefinitely and block the agent
2. Verification should use build commands, not runtime testing
3. Build errors catch most issues without running a server"""
            }
            print(json.dumps(result))
            sys.exit(0)

        # Allow everything else
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Build check error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
