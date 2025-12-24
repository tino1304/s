#!/usr/bin/env python3
"""
Skill Discovery Script for Coze Toolkit

Role-based skill discovery. Only loads skills for the specified role.

Usage:
  python3 discover-skills.py <role>

Roles: dev, ba, design, pm, tester
"""

import json
import sys
import os
from pathlib import Path

VALID_ROLES = ["dev", "ba", "design", "pm", "tester"]

def get_plugin_root():
    """Get the plugin root directory."""
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if plugin_root:
        return Path(plugin_root)
    return Path(__file__).parent.parent

def load_skill_index(plugin_root: Path) -> dict:
    """Load the skill index file."""
    index_path = plugin_root / "skills" / "skill-index.json"
    if not index_path.exists():
        return {"roles": {}}
    with open(index_path) as f:
        return json.load(f)

def match_skills(prompt: str, skills: list) -> list[dict]:
    """Find skills that match the prompt based on keywords."""
    prompt_lower = prompt.lower()
    matched = []

    for skill in skills:
        keywords = skill.get("keywords", [])
        matches = [kw for kw in keywords if kw.lower() in prompt_lower]
        if matches:
            matched.append({
                "skill": skill,
                "matched_keywords": matches,
                "score": len(matches)
            })

    matched.sort(key=lambda x: x["score"], reverse=True)
    return matched

def read_skill_content(plugin_root: Path, skill_path: str) -> str:
    """Read the skill file content."""
    full_path = plugin_root / "skills" / skill_path
    if not full_path.exists():
        return ""
    with open(full_path) as f:
        return f.read()

def main():
    # Get role from command line argument
    if len(sys.argv) < 2:
        sys.exit(0)

    role = sys.argv[1].lower()
    if role not in VALID_ROLES:
        sys.exit(0)

    try:
        # Read hook input from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        hook_input = json.loads(input_data)
        prompt = hook_input.get("prompt", "")

        if not prompt:
            sys.exit(0)

        plugin_root = get_plugin_root()
        skill_index = load_skill_index(plugin_root)

        # Get skills for the specified role only
        role_data = skill_index.get("roles", {}).get(role, {})
        role_skills = role_data.get("skills", [])

        if not role_skills:
            sys.exit(0)

        # Find matching skills within this role
        matches = match_skills(prompt, role_skills)

        if not matches:
            sys.exit(0)

        # Output matched skill content
        role_name = role_data.get("name", role.upper())
        output_parts = [
            f"[COZE {role_name.upper()} SKILL CONTEXT]",
            f"You are acting as a {role_name}. Follow these guidelines:",
            ""
        ]

        for match in matches[:3]:
            skill = match["skill"]
            skill_name = skill["name"]
            skill_path = skill["path"]

            content = read_skill_content(plugin_root, skill_path)
            if content:
                output_parts.append(f"=== {skill_name.upper()} ===")
                output_parts.append(content)
                output_parts.append("")

        output_parts.append("[END SKILL CONTEXT]")

        print("\n".join(output_parts))
        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"[Skill discovery error: {e}]", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
