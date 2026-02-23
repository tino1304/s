# Flutter State Management

## BLoC
```dart
sealed class AuthEvent {}
class LoginRequested extends AuthEvent { LoginRequested(this.email, this.password); final String email, password; }

sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthSuccess extends AuthState { AuthSuccess(this.user); final User user; }
class AuthFailure extends AuthState { AuthFailure(this.message); final String message; }

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc(this._repo) : super(AuthInitial()) { on<LoginRequested>(_onLogin); }
  final AuthRepository _repo;
  Future<void> _onLogin(LoginRequested e, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try { emit(AuthSuccess(await _repo.login(e.email, e.password))); }
    catch (e) { emit(AuthFailure(e.toString())); }
  }
}
```

## Provider
Use `ChangeNotifier` + `notifyListeners()` for simple state.

## Riverpod
Use `StateNotifierProvider` + `@freezed` states for scalable apps.
