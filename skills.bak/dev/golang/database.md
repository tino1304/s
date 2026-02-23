# Go Database (Bob + pgx)

## Bob Query Builder
```go
// Insert
result, err := models.GovernanceEvents.Insert(params).One(ctx, ds.bobExecutor)

// Select with conditions
mods := []bob.Mod[*dialect.SelectQuery]{
    models.SelectWhere.GovernanceEvents.ID.EQ(id),
}
result, err := models.GovernanceEvents.Query(mods...).One(ctx, ds.bobExecutor)

// Update
models.GovernanceEvents.Update(
    um.Where(models.UpdateWhere.GovernanceEvents.ID.EQ(id)),
    models.GovernanceEventSetter{Status: omit.From("completed")}.UpdateMod(),
).Exec(ctx, ds.bobExecutor)
```

## Datastore Pattern
```go
type DatastoreAgentPgx struct {
    pool        PGXPool
    bobExecutor BobExecutor
}

var _ content.DatastoreAgent = (*DatastoreAgentPgx)(nil)

func (ds *DatastoreAgentPgx) FindByID(ctx context.Context, id uuid.UUID) (*Agent, error) {
    result, err := models.Agents.Query(
        models.SelectWhere.Agents.ID.EQ(id),
    ).One(ctx, ds.bobExecutor)
    if err != nil { return nil, err }
    return AgentBobToRaw(result), nil
}
```

## Conventions
- Use `omit.From()` / `omitnull.From()` for nullable Bob setters
- Convert Bob models to domain types via `XxxBobToRaw()` mappers
- Always pass `context.Context` to all DB calls
- Regenerate models with `bobgen-psql` after schema changes
