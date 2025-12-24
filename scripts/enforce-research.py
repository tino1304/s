#!/usr/bin/env python3
"""
Research Proof Enforcer

Runs on PostToolUse for Read, Glob, Grep, WebSearch, WebFetch.
Checks if the model is showing proof for research findings.
Injects reminder if research tools are used without proper citation.
"""

import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_output = input_data.get("tool_output", "")

    # Research tools that require proof
    research_tools = ["Read", "Glob", "Grep", "WebSearch", "WebFetch"]

    if tool_name in research_tools:
        # Inject reminder after research tool use
        reminder = f"""
[RESEARCH RULE REMINDER]
You just used {tool_name}. When reporting findings, you MUST:

1. Show SOURCE: file:line or URL
2. Show EVIDENCE: actual quote/code
3. Show CONCLUSION: your interpretation

Format:
## Finding: [What you discovered]
**Source:** [exact location]
**Evidence:**
> [actual content you found]
**Conclusion:** [your interpretation]

❌ NEVER say "probably", "likely", "I assume" without evidence
✅ ALWAYS cite what you actually found

[END REMINDER]
"""
        print(reminder)

    sys.exit(0)

if __name__ == "__main__":
    main()
