# React Styling

## Tailwind CSS (Preferred)
```tsx
import { cn } from '@/lib/utils';

const variants = {
  primary: 'bg-blue-500 text-white hover:bg-blue-600',
  secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
};
const sizes = { sm: 'px-2 py-1 text-sm', md: 'px-4 py-2', lg: 'px-6 py-3 text-lg' };

export function Button({ variant = 'primary', size = 'md', ...props }: ButtonProps) {
  return <button className={cn('rounded font-medium transition-colors', variants[variant], sizes[size])} {...props} />;
}
```

## Tailwind v4 Warning
v4 has breaking changes. Check version first: `npm list tailwindcss`
- v3: `tailwind.config.js` + `theme.extend`
- v4: CSS `@import "tailwindcss"` + `@theme { --color-*: }`

Do NOT mix v3/v4 patterns.
