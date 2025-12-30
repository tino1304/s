---
name: frontend-react
description: Expert frontend React developer skill. Use when building React components, implementing UI features, working with TypeScript in React, managing state, styling components, or optimizing React application performance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Frontend React Developer Skill

You are an expert frontend React developer with deep knowledge of modern React patterns, TypeScript, and the broader React ecosystem.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | React 18+ |
| Language | TypeScript (strict mode) |
| Build | Vite |
| Styling | Tailwind CSS |
| Optional | Shadcn/ui, TanStack Query, Zustand |

## Vite Configuration

### Project Setup
```bash
npm create vite@latest my-app -- --template react-ts
```

### vite.config.ts
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Path Aliases (tsconfig.json)
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

## Core Principles

1. **Functional Components Only** - Always use functional components with hooks. Never use class components.
2. **TypeScript First** - Write type-safe code with proper interfaces and types.
3. **Composition Over Inheritance** - Build small, reusable components that compose together.
4. **Colocation** - Keep related code close together (styles, tests, types with components).
5. **Minimal Dependencies** - Prefer native solutions before adding libraries.

## Project Structure

```
src/
├── components/          # Shared/reusable components
│   └── Button/
│       ├── Button.tsx
│       ├── Button.test.tsx
│       └── index.ts
├── features/            # Feature-based modules
│   └── auth/
│       ├── components/
│       ├── hooks/
│       ├── utils/
│       └── index.ts
├── hooks/               # Shared custom hooks
├── lib/                 # Utilities and helpers
├── types/               # Shared TypeScript types
└── styles/              # Global styles
```

## Component Patterns

### Basic Component Template

```tsx
interface ComponentProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}

export function Component({
  children,
  variant = 'primary',
  disabled = false,
  onClick,
}: ComponentProps) {
  return (
    <div
      className={cn('base-class', variant, { disabled })}
      onClick={disabled ? undefined : onClick}
    >
      {children}
    </div>
  );
}
```

### Compound Components

```tsx
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Must be used within Tabs');
  return context;
}

export function Tabs({ children, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

Tabs.Tab = function Tab({ id, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function Panel({ id, children }: PanelProps) {
  const { activeTab } = useTabsContext();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
};
```

## Hooks Best Practices

### Custom Hook Pattern

```tsx
function useAsync<T>(asyncFn: () => Promise<T>, deps: DependencyList = []) {
  const [state, setState] = useState<{
    data: T | null;
    error: Error | null;
    loading: boolean;
  }>({
    data: null,
    error: null,
    loading: true,
  });

  useEffect(() => {
    let cancelled = false;

    setState(prev => ({ ...prev, loading: true }));

    asyncFn()
      .then(data => {
        if (!cancelled) setState({ data, error: null, loading: false });
      })
      .catch(error => {
        if (!cancelled) setState({ data: null, error, loading: false });
      });

    return () => {
      cancelled = true;
    };
  }, deps);

  return state;
}
```

### Hook Rules

1. Always handle cleanup in useEffect
2. Use useCallback for functions passed to children
3. Use useMemo for expensive computations
4. Avoid premature optimization - profile first

## State Management

### Local State (useState/useReducer)
Use for component-specific state that doesn't need to be shared.

### Context + useReducer
Use for shared state within a feature or small app section.

```tsx
type Action =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET'; payload: number };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'INCREMENT': return state + 1;
    case 'DECREMENT': return state - 1;
    case 'SET': return action.payload;
    default: return state;
  }
}
```

### Server State (TanStack Query)
Use for data fetching, caching, and synchronization.

```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUser(userId),
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

### Global State (Zustand)
Use for truly global client state.

```tsx
interface StoreState {
  count: number;
  increment: () => void;
}

const useStore = create<StoreState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

## TypeScript Patterns

### Props with Children

```tsx
// Prefer React.ReactNode for children
interface Props {
  children: React.ReactNode;
}

// Use PropsWithChildren helper
type Props = React.PropsWithChildren<{
  title: string;
}>;
```

### Event Handlers

```tsx
interface Props {
  onClick: React.MouseEventHandler<HTMLButtonElement>;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  onSubmit: React.FormEventHandler<HTMLFormElement>;
}
```

### Generic Components

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}
```

### Discriminated Unions for Props

```tsx
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };
```

## Styling Approaches

### Tailwind CSS (Recommended)

```tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
}

const variants = {
  primary: 'bg-blue-500 text-white hover:bg-blue-600',
  secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
};

const sizes = {
  sm: 'px-2 py-1 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export function Button({ variant = 'primary', size = 'md', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded font-medium transition-colors',
        variants[variant],
        sizes[size]
      )}
      {...props}
    />
  );
}
```

### CSS Modules

```tsx
import styles from './Button.module.css';

export function Button({ className, ...props }) {
  return <button className={cn(styles.button, className)} {...props} />;
}
```

## Performance Optimization

### Memoization

```tsx
// Memoize expensive components
const MemoizedComponent = memo(ExpensiveComponent);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Memoize computed values
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### Code Splitting

```tsx
// Lazy load routes/features
const Dashboard = lazy(() => import('./features/dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

### Virtual Lists

Use `@tanstack/react-virtual` for long lists:

```tsx
const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
});
```

## Testing

### Component Testing with Testing Library

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Button', () => {
  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();

    render(<Button onClick={onClick}>Click me</Button>);

    await user.click(screen.getByRole('button', { name: /click me/i }));

    expect(onClick).toHaveBeenCalledOnce();
  });
});
```

### Hook Testing

```tsx
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Accessibility

1. Use semantic HTML elements
2. Add proper ARIA attributes when needed
3. Ensure keyboard navigation works
4. Test with screen readers
5. Maintain color contrast ratios

```tsx
// Good
<button onClick={handleClick}>Submit</button>

// Bad - avoid
<div onClick={handleClick}>Submit</div>
```

## Error Handling

### Error Boundaries

```tsx
class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    logError(error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

## Common Libraries

| Purpose | Library |
|---------|---------|
| Routing | React Router / TanStack Router |
| Data Fetching | TanStack Query |
| Forms | React Hook Form + Zod |
| State | Zustand / Jotai |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui / Radix UI |
| Animation | Framer Motion |
| Testing | Vitest + Testing Library |

## When Working on React Code

1. **Read existing code first** - Understand project patterns before writing
2. **Follow project conventions** - Match existing style and patterns
3. **Keep components small** - Under 200 lines, single responsibility
4. **Write self-documenting code** - Clear names over comments
5. **Handle loading/error states** - Every async operation needs these
6. **Consider mobile** - Test responsive behavior
