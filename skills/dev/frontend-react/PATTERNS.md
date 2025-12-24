# React Patterns Reference

## Forms with React Hook Form + Zod

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof schema>;

export function SignUpForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await signUp(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input {...register('email')} placeholder="Email" />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <input {...register('password')} type="password" placeholder="Password" />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <input {...register('confirmPassword')} type="password" placeholder="Confirm Password" />
        {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing up...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

## Data Fetching with TanStack Query

### Basic Query

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch single item
function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => api.getUser(userId),
    enabled: !!userId,
  });
}

// Fetch list with filters
function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => api.getUsers(filters),
    placeholderData: keepPreviousData,
  });
}

// Infinite scroll
function useInfiniteUsers() {
  return useInfiniteQuery({
    queryKey: ['users', 'infinite'],
    queryFn: ({ pageParam }) => api.getUsers({ cursor: pageParam }),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}
```

### Mutations

```tsx
function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newUser: CreateUserInput) => api.createUser(newUser),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });
}

// Optimistic updates
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserInput }) =>
      api.updateUser(id, data),
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: ['users', id] });
      const previous = queryClient.getQueryData(['users', id]);
      queryClient.setQueryData(['users', id], (old: User) => ({ ...old, ...data }));
      return { previous };
    },
    onError: (err, { id }, context) => {
      queryClient.setQueryData(['users', id], context?.previous);
    },
    onSettled: (data, error, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['users', id] });
    },
  });
}
```

## Authentication Pattern

```tsx
// auth-context.tsx
interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (credentials: Credentials) => {
    const user = await api.login(credentials);
    setUser(user);
  };

  const logout = async () => {
    await api.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}

// Protected route
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <LoadingSpinner />;

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
```

## Modal/Dialog Pattern

```tsx
// use-dialog.ts
function useDialog() {
  const [isOpen, setIsOpen] = useState(false);
  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);

  return { isOpen, open, close, toggle };
}

// Controlled dialog component
interface DialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: React.ReactNode;
}

function Dialog({ open, onOpenChange, children }: DialogProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onOpenChange(false);
    };

    if (open) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [open, onOpenChange]);

  if (!open) return null;

  return createPortal(
    <div className="dialog-overlay" onClick={() => onOpenChange(false)}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body
  );
}

// Usage
function Example() {
  const deleteDialog = useDialog();

  return (
    <>
      <button onClick={deleteDialog.open}>Delete</button>
      <Dialog open={deleteDialog.isOpen} onOpenChange={deleteDialog.close}>
        <h2>Confirm Delete</h2>
        <p>Are you sure?</p>
        <button onClick={deleteDialog.close}>Cancel</button>
        <button onClick={handleDelete}>Delete</button>
      </Dialog>
    </>
  );
}
```

## Debounced Search

```tsx
function useDebouncedValue<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebouncedValue(query, 300);

  const { data, isLoading } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => api.search(debouncedQuery),
    enabled: debouncedQuery.length > 2,
  });

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      {isLoading && <Spinner />}
      {data?.map((result) => <SearchResult key={result.id} {...result} />)}
    </div>
  );
}
```

## Intersection Observer (Lazy Loading)

```tsx
function useIntersectionObserver(
  ref: RefObject<Element>,
  options?: IntersectionObserverInit
) {
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsIntersecting(entry.isIntersecting);
    }, options);

    observer.observe(element);

    return () => observer.disconnect();
  }, [ref, options?.threshold, options?.root, options?.rootMargin]);

  return isIntersecting;
}

// Lazy image
function LazyImage({ src, alt, ...props }: ImgHTMLAttributes<HTMLImageElement>) {
  const ref = useRef<HTMLDivElement>(null);
  const isVisible = useIntersectionObserver(ref, { rootMargin: '100px' });
  const [loaded, setLoaded] = useState(false);

  return (
    <div ref={ref} className="lazy-image-container">
      {isVisible && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setLoaded(true)}
          className={cn('lazy-image', { loaded })}
          {...props}
        />
      )}
    </div>
  );
}
```

## Render Props Pattern

```tsx
interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  children: (position: MousePosition) => React.ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return <>{children(position)}</>;
}

// Usage
<MouseTracker>
  {({ x, y }) => (
    <div style={{ position: 'fixed', left: x, top: y }}>
      Cursor here
    </div>
  )}
</MouseTracker>
```

## URL State Sync

```tsx
function useQueryParams<T extends Record<string, string>>() {
  const [searchParams, setSearchParams] = useSearchParams();

  const params = useMemo(() => {
    const result: Record<string, string> = {};
    searchParams.forEach((value, key) => {
      result[key] = value;
    });
    return result as T;
  }, [searchParams]);

  const setParams = useCallback(
    (newParams: Partial<T>) => {
      setSearchParams((prev) => {
        const updated = new URLSearchParams(prev);
        Object.entries(newParams).forEach(([key, value]) => {
          if (value === undefined || value === '') {
            updated.delete(key);
          } else {
            updated.set(key, value);
          }
        });
        return updated;
      });
    },
    [setSearchParams]
  );

  return [params, setParams] as const;
}

// Usage
function ProductList() {
  const [{ category, sort }, setParams] = useQueryParams<{
    category?: string;
    sort?: string;
  }>();

  return (
    <div>
      <select
        value={category ?? ''}
        onChange={(e) => setParams({ category: e.target.value })}
      >
        <option value="">All</option>
        <option value="electronics">Electronics</option>
      </select>
    </div>
  );
}
```
