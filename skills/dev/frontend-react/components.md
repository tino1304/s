# React Components

Functional components only. No class components.

```tsx
interface Props {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  onClick?: () => void;
}

export function Component({ children, variant = 'primary', onClick }: Props) {
  return <div className={cn('base', variant)} onClick={onClick}>{children}</div>;
}
```

## Compound Components
Use Context for shared state between related components (Tabs, Accordion, etc.).

## Discriminated Unions
```tsx
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };
```

## Rules
- Props: use `React.ReactNode` for children, explicit interfaces
- Composition over inheritance
- Keep components small and focused
- Use semantic HTML (`<button>` not `<div onClick>`)
