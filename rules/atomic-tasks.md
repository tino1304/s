# Atomic Tasks Rule

**MANDATORY** for Tech Lead when creating tasks.

## Principle

Tasks must be atomic - the smallest unit of work that delivers value.

## Rules

1. **One task = One focus**
   - Single responsibility
   - One file or tightly coupled files only
   - Clear start and end

2. **Size limits**
   - Max 1-3 files per task
   - If touching 4+ files → break it down
   - If task description > 10 lines → too big

3. **Time box**
   - Should be completable in one session
   - If it feels like "a lot" → split it

4. **Signs task is too big**
   - Multiple unrelated changes
   - "And also..." in description
   - Nested subtasks
   - Unclear acceptance criteria

## Examples

### BAD - Too big
```
Task: Implement user authentication
- Create login form
- Add JWT handling
- Set up middleware
- Create user model
- Add password hashing
```

### GOOD - Atomic
```
Task-001: Create User model with password hashing
Task-002: Create login form component
Task-003: Add JWT token generation endpoint
Task-004: Add auth middleware
Task-005: Integrate login form with JWT endpoint
```

## Enforcement

Before creating any task file, ask:
> "Can this be split further while still delivering value?"

If yes → split it.
