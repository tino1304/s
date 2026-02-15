# React Testing

## Component Test
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('calls onClick when clicked', async () => {
  const user = userEvent.setup();
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);
  await user.click(screen.getByRole('button', { name: /click me/i }));
  expect(onClick).toHaveBeenCalledOnce();
});
```

## Hook Test
```tsx
import { renderHook, act } from '@testing-library/react';

it('increments', () => {
  const { result } = renderHook(() => useCounter());
  act(() => { result.current.increment(); });
  expect(result.current.count).toBe(1);
});
```

## Rules
- Query by role/label, not test IDs
- Use `userEvent` over `fireEvent`
- Test behavior, not implementation
