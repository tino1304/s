# Flutter Widgets

## StatelessWidget
```dart
class MyWidget extends StatelessWidget {
  const MyWidget({super.key, required this.title, this.onTap});
  final String title;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap: onTap, child: Text(title));
  }
}
```

## StatefulWidget
```dart
class _MyWidgetState extends State<MyWidget> {
  late final TextEditingController _controller;

  @override
  void initState() { super.initState(); _controller = TextEditingController(); }

  @override
  void dispose() { _controller.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => TextField(controller: _controller);
}
```

## Rules
- Use `const` constructors where possible
- Use `super.key` in constructors
- Always dispose controllers/listeners
- Use `Theme.of(context)` for theming
