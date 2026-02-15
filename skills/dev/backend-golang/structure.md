# Go Project Structure

```
cmd/
  core/main.go              # Entry point (server, workers)
  scheduler/main.go         # Standalone worker
internal/
  api/                      # Echo HTTP handlers + routing
  bob/models/               # Generated DB models (Bob ORM)
  container/                # DI setup (samber/do)
  content/                  # Domain types, interfaces, contracts
  datastore/                # Database access (pgx + Bob)
  services/                 # Business logic
pkg/
  caching/                  # Redis cache utilities
  db/                       # DB/Redis connection helpers
  env/                      # Environment variable helpers
  errorx/                   # Error types with Kind + HTTP status
  httpx/                    # Echo response helpers
```

## Key Patterns
- **content/** defines interfaces (`DatastoreX`) + domain types — no implementation
- **datastore/** implements those interfaces with pgx + Bob
- **services/** holds business logic, receives datastores via DI
- **container/** wires everything with `samber/do`
- **api/** groups handlers by domain (`GroupGovernance`, `GroupAgent`)

## Interface-Driven Design
Define interfaces in `content/`, implement in `datastore/`:
```go
// content/0_contract.go
type DatastoreAgent interface {
    FindByID(ctx context.Context, id uuid.UUID) (*Agent, error)
    FindByToken(ctx context.Context, token string) (*Agent, error)
}
```
Verify implementation at compile time:
```go
var _ content.DatastoreAgent = (*DatastoreAgentPgx)(nil)
```
