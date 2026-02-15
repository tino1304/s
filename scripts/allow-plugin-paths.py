#!/usr/bin/env python3
"""
Plugin Path Auto-Allow Hook

Runs on PreToolUse for Read, Write, Edit.
Auto-allows access to:
- The plugin's own directory (skills, commands, rules) via CLAUDE_PLUGIN_ROOT
- The plugin's working directories (.claude/s/, .claude/docs/)
"""

import json
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ("Read", "Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Plugin root passed as argument from hooks.json
    plugin_root = sys.argv[1] if len(sys.argv) > 1 else None

    # Auto-allow plugin's own files (skills, commands, rules, etc.)
    if plugin_root and file_path.startswith(plugin_root):
        allow("plugin own files")
        return

    # Auto-allow plugin working directories in the project
    if "/.claude/s/" in file_path or file_path.endswith("/.claude/s"):
        allow(".claude/s/ directory")
        return

    if "/.claude/docs/" in file_path or file_path.endswith("/.claude/docs"):
        allow(".claude/docs/ directory")
        return

    # No match — don't interfere
    sys.exit(0)


def allow(reason):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": f"Auto-allowed: {reason}"
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
