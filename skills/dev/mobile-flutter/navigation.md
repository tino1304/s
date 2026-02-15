# Flutter Navigation (GoRouter)

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen(),
      routes: [
        GoRoute(path: 'details/:id', builder: (_, state) => DetailsScreen(id: state.pathParameters['id']!)),
      ],
    ),
    GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
  ],
  redirect: (context, state) {
    final loggedIn = /* check auth */;
    if (!loggedIn && state.matchedLocation != '/login') return '/login';
    if (loggedIn && state.matchedLocation == '/login') return '/';
    return null;
  },
);
```

## Usage
- `context.go('/path')` — navigate (replaces)
- `context.push('/path')` — push (can go back)
- `context.pop()` — go back
