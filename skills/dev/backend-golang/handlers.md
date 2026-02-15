# Go HTTP Handlers (Echo)

## Handler Groups
```go
type GroupGovernance struct {
    config *Config
}

func (group *GroupGovernance) EvaluateEvent(c echo.Context) error {
    ctx := c.Request().Context()

    var payload content.EventPayload
    if err := c.Bind(&payload); err != nil {
        return httpx.Abort(c, 400, "invalid request body", nil)
    }

    service, err := do.Invoke[*services.ServiceRequest](group.config.Container)
    if err != nil {
        return httpx.Abort(c, 500, "internal server error", nil)
    }

    result, err := service.Process(ctx, &payload)
    return httpx.RestAbort(c, result, err)
}
```

## Route Setup
```go
func New(config *Config) (http.Handler, error) {
    r := echo.New()
    r.Validator = &CustomValidator{validator: validator.New()}

    routesAPI := r.Group("/api/v1")
    routesAPI.Use(corsMiddleware)

    group := &GroupGovernance{config}
    routesAPI.POST("/governance/evaluate", group.EvaluateEvent)
    return r, nil
}
```

## Response Helpers (`pkg/httpx`)
- `httpx.Abort(c, code, msg, data)` — JSON error/success response
- `httpx.RestAbort(c, data, err)` — auto-maps `errorx.Error` to HTTP status
- `httpx.AbortAuthentication(c, msg)` — 401 shorthand

## Auth Middleware
Extract Bearer token → hash with SHA-256 → lookup agent via service → set in context.
