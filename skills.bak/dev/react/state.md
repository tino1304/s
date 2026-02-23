# React State Management

## Local: useState/useReducer
Component-specific state that doesn't need sharing.

## Shared: Context + useReducer
```tsx
type Action = { type: 'INCREMENT' } | { type: 'SET'; payload: number };
function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT': return state + 1;
    case 'SET': return action.payload;
    default: return state;
  }
}
```

## Server State: TanStack Query
```tsx
const { data, isLoading } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUser(userId),
  staleTime: 5 * 60 * 1000,
});
```

## Global: Zustand
```tsx
const useStore = create<StoreState>((set) => ({
  count: 0,
  increment: () => set((s) => ({ count: s.count + 1 })),
}));
```
