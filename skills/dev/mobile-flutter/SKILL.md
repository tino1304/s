---
name: mobile-flutter
description: Expert Flutter mobile developer skill. Use when building Flutter/Dart apps, implementing widgets, managing state with BLoC/Provider/Riverpod, handling navigation, platform channels, or optimizing mobile app performance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Flutter Mobile Developer Skill

You are an expert Flutter mobile developer with deep knowledge of Dart, Flutter widgets, state management patterns, and cross-platform mobile development.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Flutter 3.x |
| Language | Dart 3.x (null-safe) |
| State Management | BLoC / Provider / Riverpod |
| Navigation | GoRouter / Navigator 2.0 |
| HTTP | Dio / http |
| Local Storage | Hive / SharedPreferences / SQLite |
| Testing | flutter_test / mockito / bloc_test |

## Project Structure

### Feature-First Architecture (Recommended)
```
lib/
├── main.dart
├── app/
│   ├── app.dart              # MaterialApp/CupertinoApp
│   ├── router.dart           # Route configuration
│   └── theme.dart            # App theme
├── core/
│   ├── constants/
│   ├── errors/
│   ├── network/
│   └── utils/
├── features/
│   └── auth/
│       ├── data/
│       │   ├── models/
│       │   ├── repositories/
│       │   └── datasources/
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/
│       │   └── usecases/
│       └── presentation/
│           ├── bloc/         # or providers/
│           ├── pages/
│           └── widgets/
└── shared/
    ├── widgets/
    └── extensions/
```

### Simple Project Structure
```
lib/
├── main.dart
├── models/
├── screens/
├── widgets/
├── services/
├── providers/      # or blocs/
└── utils/
```

## Dart/Flutter Core Principles

1. **Null Safety** - All code must be null-safe
2. **Immutability** - Prefer immutable data classes (use `freezed` or manual)
3. **Composition** - Build small, reusable widgets
4. **Separation of Concerns** - UI, business logic, and data should be separate
5. **Platform Awareness** - Handle iOS/Android differences gracefully

## Widget Patterns

### StatelessWidget Template

```dart
class MyWidget extends StatelessWidget {
  const MyWidget({
    super.key,
    required this.title,
    this.onTap,
  });

  final String title;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Text(title),
    );
  }
}
```

### StatefulWidget Template

```dart
class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({super.key});

  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextField(controller: _controller);
  }
}
```

### Custom Widget with Theme

```dart
class AppButton extends StatelessWidget {
  const AppButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.isLoading = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: theme.colorScheme.primary,
        foregroundColor: theme.colorScheme.onPrimary,
      ),
      child: isLoading
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Text(label),
    );
  }
}
```

## State Management

### BLoC Pattern

```dart
// Events
sealed class AuthEvent {}
class LoginRequested extends AuthEvent {
  LoginRequested(this.email, this.password);
  final String email;
  final String password;
}

// States
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState {
  AuthSuccess(this.user);
  final User user;
}
class AuthFailure extends AuthState {
  AuthFailure(this.message);
  final String message;
}

// Bloc
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc(this._authRepository) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
  }

  final AuthRepository _authRepository;

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      final user = await _authRepository.login(event.email, event.password);
      emit(AuthSuccess(user));
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }
}
```

### Provider Pattern

```dart
class AuthProvider extends ChangeNotifier {
  User? _user;
  bool _isLoading = false;
  String? _error;

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isAuthenticated => _user != null;

  Future<void> login(String email, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _user = await _authRepository.login(email, password);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
```

### Riverpod Pattern

```dart
// Provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.read(authRepositoryProvider));
});

// Notifier
class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._repository) : super(const AuthState.initial());

  final AuthRepository _repository;

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await _repository.login(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }
}

// State with Freezed
@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.error(String message) = _Error;
}
```

## Navigation

### GoRouter Setup

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
  redirect: (context, state) {
    final isLoggedIn = /* check auth */;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!isLoggedIn && !isLoggingIn) return '/login';
    if (isLoggedIn && isLoggingIn) return '/';
    return null;
  },
);
```

### Navigation Usage

```dart
// Navigate to route
context.go('/details/123');

// Push route (can go back)
context.push('/details/123');

// Go back
context.pop();

// With extra data
context.go('/details', extra: myObject);
```

## Data Layer

### Repository Pattern

```dart
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<List<User>> getUsers();
  Future<void> updateUser(User user);
}

class UserRepositoryImpl implements UserRepository {
  UserRepositoryImpl(this._api, this._cache);

  final UserApi _api;
  final UserCache _cache;

  @override
  Future<User> getUser(String id) async {
    final cached = await _cache.getUser(id);
    if (cached != null) return cached;

    final user = await _api.getUser(id);
    await _cache.saveUser(user);
    return user;
  }
}
```

### API Service with Dio

```dart
class ApiService {
  ApiService() : _dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  )) {
    _dio.interceptors.add(LogInterceptor());
    _dio.interceptors.add(AuthInterceptor());
  }

  final Dio _dio;

  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
  }) async {
    final response = await _dio.get<T>(
      path,
      queryParameters: queryParameters,
    );
    return response.data as T;
  }
}
```

### Model with JSON Serialization

```dart
// With json_serializable
@JsonSerializable()
class User {
  const User({
    required this.id,
    required this.name,
    required this.email,
    this.avatarUrl,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  final String id;
  final String name;
  final String email;
  @JsonKey(name: 'avatar_url')
  final String? avatarUrl;

  Map<String, dynamic> toJson() => _$UserToJson(this);
}

// With Freezed (recommended)
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @JsonKey(name: 'avatar_url') String? avatarUrl,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

## Platform Channels

### Calling Native Code

```dart
class NativeService {
  static const _channel = MethodChannel('com.example.app/native');

  Future<String> getNativeValue() async {
    final result = await _channel.invokeMethod<String>('getValue');
    return result ?? '';
  }

  Future<void> setNativeValue(String value) async {
    await _channel.invokeMethod('setValue', {'value': value});
  }
}
```

## Testing

### Widget Test

```dart
void main() {
  testWidgets('Counter increments', (tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('0'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    expect(find.text('1'), findsOneWidget);
  });
}
```

### BLoC Test

```dart
void main() {
  late AuthBloc bloc;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    bloc = AuthBloc(mockRepository);
  });

  blocTest<AuthBloc, AuthState>(
    'emits [loading, success] on successful login',
    build: () {
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => testUser);
      return bloc;
    },
    act: (bloc) => bloc.add(LoginRequested('test@test.com', 'password')),
    expect: () => [
      isA<AuthLoading>(),
      isA<AuthSuccess>(),
    ],
  );
}
```

### Integration Test

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Full app flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Test flow
    await tester.tap(find.byType(ElevatedButton));
    await tester.pumpAndSettle();

    expect(find.text('Success'), findsOneWidget);
  });
}
```

## Common Packages

| Purpose | Package |
|---------|---------|
| State Management | flutter_bloc / provider / riverpod |
| Navigation | go_router |
| HTTP | dio |
| Code Generation | freezed / json_serializable |
| Local DB | hive / sqflite / drift |
| DI | get_it / injectable |
| Forms | flutter_form_builder / reactive_forms |
| Animations | flutter_animate |
| Testing | mockito / bloc_test / mocktail |

## Performance Tips

1. **Use `const` constructors** - Enables widget caching
2. **Avoid rebuilding** - Use `Selector`, `BlocSelector`, or `select` from Riverpod
3. **Lazy loading** - Use `ListView.builder` for long lists
4. **Image caching** - Use `cached_network_image`
5. **Profile builds** - Use Flutter DevTools to find rebuild issues

```dart
// Bad - rebuilds entire list
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// Good - builds items lazily
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
)
```

## When Working on Flutter Code

1. **Check Flutter/Dart version** - Ensure compatibility
2. **Read existing code first** - Understand project patterns
3. **Follow project's state management** - Don't mix BLoC with Provider
4. **Ensure null safety** - No legacy null-unsafe patterns
5. **Handle all states** - Loading, error, empty, success
6. **Test on both platforms** - iOS and Android have differences
7. **Consider accessibility** - Use Semantics widgets
