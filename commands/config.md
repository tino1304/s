---
description: Configure S plugin settings
---

# S Plugin Configuration

**Arguments:** $ARGUMENTS

## Usage

```
/s:config auto-accept true    # Enable fully autonomous mode
/s:config auto-accept false   # Enable confirmation mode (default)
/s:config show                # Show current config
```

## Instructions

1. Parse the arguments to determine action:
   - `auto-accept true` → Set autonomous mode
   - `auto-accept false` → Set confirmation mode
   - `show` → Display current settings

2. Config is stored in `.claude/s-config.json` in the project root

3. **For `auto-accept true`:**
   ```json
   {
     "autoAccept": true
   }
   ```
   Write this to `.claude/s-config.json`

4. **For `auto-accept false`:**
   ```json
   {
     "autoAccept": false
   }
   ```
   Write this to `.claude/s-config.json`

5. **For `show`:**
   Read `.claude/s-config.json` and display settings.
   If file doesn't exist, show defaults:
   ```
   Current S Plugin Config:
   - autoAccept: false (default)
   ```

6. Confirm the change to user.
