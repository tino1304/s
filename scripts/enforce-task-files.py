#!/usr/bin/env python3
"""
Task File Enforcer Hook

Runs on PreToolUse for Write/Edit.
- Enforces task files go to .claude/tasks/
- Auto-creates .claude/tasks/ directory
- Validates task file format has required sections
"""

import json
import sys
import os
import re

# Task file patterns
TASK_FILE_PATTERN = re.compile(r'task-\d{3}.*\.md$', re.IGNORECASE)
TRACKER_FILE = 'TRACKER.md'

# Required sections in task files
REQUIRED_SECTIONS = ['Assignment', 'Report', 'Review']

def get_project_root():
    """Get the project root by walking up to find .claude/ or .git/."""
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

def ensure_tasks_dir():
    """Ensure .claude/tasks/ directory exists."""
    project_root = get_project_root()
    tasks_dir = os.path.join(project_root, '.claude', 'tasks')

    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir, exist_ok=True)
        return f"Created directory: {tasks_dir}"
    return None

def is_task_file(file_path):
    """Check if this is a task-related file."""
    basename = os.path.basename(file_path)
    return bool(TASK_FILE_PATTERN.match(basename)) or basename == TRACKER_FILE

def get_correct_path(file_path):
    """Get the correct path under .claude/tasks/."""
    project_root = get_project_root()
    basename = os.path.basename(file_path)
    return os.path.join(project_root, '.claude', 'tasks', basename)

def is_in_correct_location(file_path):
    """Check if file is already in .claude/tasks/."""
    project_root = get_project_root()
    correct_dir = os.path.join(project_root, '.claude', 'tasks')
    file_dir = os.path.dirname(os.path.abspath(file_path))
    return file_dir == os.path.abspath(correct_dir)

def validate_task_content(content, file_path):
    """Validate task file has required section headers."""
    basename = os.path.basename(file_path)

    # Skip validation for TRACKER.md
    if basename == TRACKER_FILE:
        return None

    # Check for required sections (as markdown headers)
    missing = []
    for section in REQUIRED_SECTIONS:
        # Look for ## Assignment, ## Report, ## Review (or # or ###)
        pattern = rf'^#+\s*{section}'
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            missing.append(section)

    if missing:
        return f"Task file missing required sections: {', '.join(missing)}"

    return None

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only handle Write and Edit
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")

    if not file_path:
        sys.exit(0)

    # Check if this is a task file
    if not is_task_file(file_path):
        sys.exit(0)

    # Ensure .claude/tasks/ exists
    created_msg = ensure_tasks_dir()

    # Check if file is in correct location
    if not is_in_correct_location(file_path):
        correct_path = get_correct_path(file_path)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"📁 Task files must be in .claude/tasks/\n\nRedirect to: {correct_path}\n\nPlease use the correct path."
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # For Write tool, validate content
    if tool_name == "Write":
        content = tool_input.get("content", "")
        validation_error = validate_task_content(content, file_path)

        if validation_error:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"📋 {validation_error}\n\nTask files must include:\n## Assignment\n## Report\n## Review"
                }
            }
            print(json.dumps(output))
            sys.exit(0)

    # Passed all checks
    if created_msg:
        # Inform about directory creation (non-blocking)
        print(json.dumps({"message": created_msg}))

    sys.exit(0)

if __name__ == "__main__":
    main()
