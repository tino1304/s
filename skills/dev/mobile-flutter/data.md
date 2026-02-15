# Flutter Data Layer

## Repository Pattern
```dart
abstract class UserRepository {
  Future<User> getUser(String id);
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

## Model (Freezed)
```dart
@freezed
class User with _$User {
  const factory User({required String id, required String name, @JsonKey(name: 'avatar_url') String? avatarUrl}) = _User;
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

## Dio
Use `Dio` with `BaseOptions` for API calls. Add interceptors for auth/logging.
