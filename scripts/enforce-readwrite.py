#!/usr/bin/env python3
"""
Read & Write Protection Enforcer

Runs on PreToolUse for Read, Write, Edit, Bash.
Asks user for confirmation when accessing or modifying protected files.
"""

import json
import sys


def ask_user(reason):
    """Ask user for permission instead of blocking."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Allowed exceptions — always pass through
    allowed_patterns = [
        ".env.example",
    ]

    # Protected paths that need user confirmation
    protected_patterns = [
        ".env",
        "credentials",
        "secret",
        "password",
        "api_key",
        "token",
        ".git/",
        "node_modules/",
        "package-lock.json"
    ]

    # Read, Write, Edit — check file_path
    if tool_name in ["Read", "Write", "Edit"]:
        file_path = tool_input.get("file_path", "")
        file_lower = file_path.lower()

        if any(ap in file_lower for ap in allowed_patterns):
            sys.exit(0)

        for pattern in protected_patterns:
            if pattern.lower() in file_lower:
                action = "read from" if tool_name == "Read" else "write to"
                ask_user(f"⚠️  Protected file: agent wants to {action} '{file_path}' (matched: {pattern}). Allow?")

    # Bash — check for dangerous patterns
    if tool_name == "Bash":
        command = tool_input.get("command", "")

        dangerous_patterns = [
            "rm -rf",
            "rm -r /",
            "> /dev/",
            "dd if=",
            "mkfs",
            ":(){",
            "chmod 777",
            "curl | sh",
            "curl | bash",
            "wget | sh",
            "wget | bash"
        ]

        for pattern in dangerous_patterns:
            if pattern in command:
                ask_user(f"⚠️  Dangerous command pattern '{pattern}' detected. Allow?")

    # Allow if passes all checks
    sys.exit(0)


if __name__ == "__main__":
    main()
