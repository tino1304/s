# Node.js Validation (Zod)

```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

export type CreateUserDto = z.infer<typeof createUserSchema>;
```

## Env Validation
Validate environment variables at startup with Zod. Never commit .env files.

## Rules
- Validate all inputs at system boundaries
- Use `z.infer` to derive types from schemas
- Avoid `any`, use `unknown` if needed
