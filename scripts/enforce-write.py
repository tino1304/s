#!/usr/bin/env python3
"""
Write Confirmation Enforcer

Runs on PreToolUse for Write, Edit, Bash.
Blocks writes if plan wasn't confirmed first (for coze workflows).
"""

import json
import sys
import os

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Tools that modify files
    write_tools = ["Write", "Edit"]

    if tool_name in write_tools:
        file_path = tool_input.get("file_path", "")

        # Protected paths that always need confirmation
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

        for pattern in protected_patterns:
            if pattern.lower() in file_path.lower():
                # BLOCK - protected file
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"🚫 BLOCKED: Cannot modify '{pattern}' files. This is a protected path. Ask user for explicit permission first."
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

    # Bash commands - check for dangerous patterns
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
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"🚫 BLOCKED: Dangerous command pattern '{pattern}' detected. This requires explicit user confirmation."
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

    # Allow if passes all checks
    sys.exit(0)

if __name__ == "__main__":
    main()
