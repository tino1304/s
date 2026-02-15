# React Hooks

## Custom Hook Pattern
```tsx
function useAsync<T>(asyncFn: () => Promise<T>, deps: DependencyList = []) {
  const [state, setState] = useState<{ data: T | null; error: Error | null; loading: boolean }>({
    data: null, error: null, loading: true,
  });

  useEffect(() => {
    let cancelled = false;
    setState(prev => ({ ...prev, loading: true }));
    asyncFn()
      .then(data => { if (!cancelled) setState({ data, error: null, loading: false }); })
      .catch(error => { if (!cancelled) setState({ data: null, error, loading: false }); });
    return () => { cancelled = true; };
  }, deps);

  return state;
}
```

## Rules
- Always handle cleanup in useEffect
- useCallback for functions passed to children
- useMemo for expensive computations only — profile first
- Never call hooks conditionally
