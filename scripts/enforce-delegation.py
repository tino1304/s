#!/usr/bin/env python3
"""
Enforce Delegation Hook (PreToolUse)

Blocks Edit/Write to code files unless dev mode is enabled.
- Tech-lead cannot edit code files (must spawn dev agents)
- Dev agents create .claude/.dev-mode to enable code editing
"""

import json
import sys
import os

# Marker file that enables code editing
DEV_MODE_FILE = ".claude/.dev-mode"

# File patterns that are always allowed (no marker needed)
ALWAYS_ALLOWED = [
    '.claude/tasks/',
    '.claude/s-config.json',
    '.claude/.dev-mode',
    'TRACKER.md',
    'CLAUDE.md',
    'README.md',
]

# File extensions that are code files (need dev mode)
CODE_EXTENSIONS = [
    '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
    '.py', '.pyw',
    '.go',
    '.rs',
    '.rb',
    '.java', '.kt', '.scala',
    '.c', '.cpp', '.h', '.hpp',
    '.cs',
    '.php',
    '.swift',
    '.vue', '.svelte',
    '.css', '.scss', '.sass', '.less',
    '.html', '.htm',
    '.json', '.yaml', '.yml', '.toml',
    '.sql',
    '.sh', '.bash', '.zsh',
]

def is_always_allowed(file_path: str) -> bool:
    """Check if file is always allowed to edit."""
    for pattern in ALWAYS_ALLOWED:
        if pattern in file_path:
            return True
    return False

def is_code_file(file_path: str) -> bool:
    """Check if file is a code file."""
    _, ext = os.path.splitext(file_path.lower())
    return ext in CODE_EXTENSIONS

def find_project_root() -> str:
    """Find project root by looking for .claude/ or .git/ directory."""
    current = os.getcwd()

    # Walk up the directory tree
    while current != os.path.dirname(current):  # Stop at filesystem root
        # Check for .claude/ directory (our marker)
        if os.path.isdir(os.path.join(current, '.claude')):
            return current
        # Check for .git/ as fallback project root indicator
        if os.path.isdir(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)

    # Fallback to cwd if no project root found
    return os.getcwd()

def dev_mode_enabled() -> bool:
    """Check if dev mode is enabled (marker file exists in project root)."""
    # Find project root first
    project_root = find_project_root()

    # Check for dev-mode file in project root
    paths_to_check = [
        os.path.join(project_root, DEV_MODE_FILE),
        os.path.join(os.getcwd(), DEV_MODE_FILE),  # Also check cwd as fallback
        DEV_MODE_FILE,  # Relative path
    ]

    for path in paths_to_check:
        if os.path.exists(path):
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

        # Only check Edit and Write tools
        if tool_name not in ["Edit", "Write"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path:
            sys.exit(0)

        # Always allow certain files
        if is_always_allowed(file_path):
            sys.exit(0)

        # Check if it's a code file
        if not is_code_file(file_path):
            sys.exit(0)

        # Code file - check if dev mode is enabled
        if dev_mode_enabled():
            sys.exit(0)  # Dev mode active, allow

        # Block - dev mode not enabled
        result = {
            "decision": "block",
            "reason": f"""BLOCKED: Code editing requires dev mode.

File: {file_path}

If you are TECH-LEAD:
  You cannot edit code files directly. Spawn a dev agent instead:

  Task tool:
  - subagent_type: "general-purpose"
  - prompt: "You are a dev agent. First, create file .claude/.dev-mode with content 'dev'. Then implement: [task details]"
  - description: "TASK-XXX: [name]"

If you are DEV agent:
  Create the marker file first:
  Write tool: .claude/.dev-mode with content "dev"

  Then you can edit code files."""
        }
        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Delegation check error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
