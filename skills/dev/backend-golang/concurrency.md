# Go Concurrency

## errgroup (Preferred for parallel tasks)
```go
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    g.Go(func() error { return process(ctx, item) })
}
if err := g.Wait(); err != nil { return err }
```

## Goroutines + WaitGroup
```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(it Item) {
        defer wg.Done()
        process(it)
    }(item)
}
wg.Wait()
```

## Channels
```go
ch := make(chan Result, len(items))
for _, item := range items {
    go func(it Item) { ch <- process(it) }(item)
}
for range items { result := <-ch }
```

## Rules
- Don't start goroutines without a way to stop them
- Use `context.Context` for cancellation/timeouts
- Use `errgroup` when you need error handling
- Use `sync.Mutex` for shared state protection
