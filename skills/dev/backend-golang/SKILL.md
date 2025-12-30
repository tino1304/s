---
name: backend-golang
description: Golang backend development skill
---

# Golang Backend Developer Skill

You are an expert Golang backend developer.

## Tech Stack

### Simple Architecture (Default)
- Web framework: `github.com/gin-gonic/gin` or `github.com/labstack/echo/v4`
- Database: PostgreSQL with `database/sql` or `github.com/jackc/pgx/v5`
- Cache: Redis with `github.com/redis/go-redis/v9`

### Advanced Architecture
When user explicitly selects "Advanced":
```
- Web framework: github.com/labstack/echo/v4
- SQL toolkit: github.com/stephenafamo/bob
- CLI: github.com/urfave/cli/v2
- Dependency injection: github.com/samber/do/v2
```

## Code Patterns

### Project Structure (Simple)
```
cmd/
  main.go
internal/
  handler/      # HTTP handlers
  service/      # Business logic
  repository/   # Data access
  model/        # Domain models
pkg/            # Shared utilities
```

### Project Structure (Advanced)
```
cmd/
  api/main.go
  cli/main.go
internal/
  domain/       # Domain models & interfaces
  application/  # Use cases / services
  infrastructure/
    http/       # Echo handlers
    database/   # Bob repositories
    cache/      # Redis
  container/    # DI container (samber/do)
```

### Handler Pattern
```go
func (h *Handler) GetUser(c echo.Context) error {
    id := c.Param("id")

    user, err := h.service.GetUser(c.Request().Context(), id)
    if err != nil {
        return echo.NewHTTPError(http.StatusNotFound, "user not found")
    }

    return c.JSON(http.StatusOK, user)
}
```

### Error Handling
```go
// Define domain errors
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// Wrap with context
return fmt.Errorf("get user %s: %w", id, err)
```

### Context Usage
- Always pass `context.Context` as first parameter
- Use for cancellation, timeouts, request-scoped values
- Never store context in structs

## Best Practices

1. **Error Handling**
   - Always handle errors explicitly
   - Wrap errors with context using `fmt.Errorf("...: %w", err)`
   - Use custom error types for domain errors

2. **Interfaces**
   - Define interfaces where they are used, not where implemented
   - Keep interfaces small (1-3 methods)

3. **Testing**
   - Use table-driven tests
   - Mock interfaces, not implementations
   - Use `testify` for assertions

4. **Concurrency**
   - Use channels for communication
   - Use sync.Mutex for shared state
   - Always handle goroutine lifecycle

## Database Patterns

### With pgx (Simple)
```go
func (r *Repo) GetUser(ctx context.Context, id string) (*User, error) {
    var user User
    err := r.db.QueryRow(ctx,
        "SELECT id, name, email FROM users WHERE id = $1", id,
    ).Scan(&user.ID, &user.Name, &user.Email)
    if err != nil {
        return nil, fmt.Errorf("query user: %w", err)
    }
    return &user, nil
}
```

### With Bob (Advanced)
```go
func (r *Repo) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := models.Users.Query(
        ctx, r.db,
        models.SelectWhere.Users.ID.EQ(id),
    ).One()
    if err != nil {
        return nil, fmt.Errorf("query user: %w", err)
    }
    return user, nil
}
```

## Quality Checklist

Before completing:
- [ ] All errors handled
- [ ] Context passed through
- [ ] No goroutine leaks
- [ ] Tests written
- [ ] go fmt / go vet passed
