# Research Rule

**No imagination. Proof required.**

---

## Requirements

### 1. Show Your Sources

Every claim must have proof:
- File path + line number for code
- URL for web sources
- Document name for docs

### 2. Quote Actual Content

```
❌ BAD: "The config has database settings"
✅ GOOD: "config/database.yml:15 → `host: localhost, port: 5432`"
```

### 3. Admit When Unknown

```
❌ BAD: "This probably uses Redis"
✅ GOOD: "No caching config found. Should I search more?"
```

### 4. Verify Before Claiming

```
❌ BAD: Assume file exists
✅ GOOD: Read file first, then report
```

---

## Output Format

### When Evidence Found

```markdown
## Finding: [Discovery]

**Source:** [file:line | URL]

**Evidence:**
> [Actual quote/code]

**Conclusion:** [Interpretation]
```

### When No Evidence

```markdown
## Finding: Unable to confirm [topic]

**Searched:**
- [Where you looked]

**Result:** Not found

**Next:** [Ask user or suggest action]
```

---

## Violations

- Making up file contents
- Claiming without source
- Guessing configurations
- Assuming code behavior without reading

These are **unacceptable**.
