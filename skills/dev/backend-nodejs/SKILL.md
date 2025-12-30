---
name: backend-nodejs
description: Node.js/TypeScript backend development skill
---

# Node.js Backend Developer Skill

You are an expert Node.js/TypeScript backend developer.

## Tech Stack

- Runtime: Node.js with TypeScript (strict mode)
- Web framework: Express.js or Fastify
- Database: PostgreSQL with Prisma or Drizzle
- Cache: Redis with ioredis
- Validation: Zod

## Code Patterns

### Project Structure
```
src/
  index.ts           # Entry point
  routes/            # Route definitions
  controllers/       # Request handlers
  services/          # Business logic
  repositories/      # Data access
  models/            # Types and schemas
  middleware/        # Express middleware
  utils/             # Utilities
  config/            # Configuration
```

### Controller Pattern
```typescript
export const getUser = async (
  req: Request<{ id: string }>,
  res: Response,
  next: NextFunction
) => {
  try {
    const { id } = req.params;
    const user = await userService.getById(id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    return res.json(user);
  } catch (error) {
    next(error);
  }
};
```

### Service Pattern
```typescript
export class UserService {
  constructor(private readonly userRepo: UserRepository) {}

  async getById(id: string): Promise<User | null> {
    return this.userRepo.findById(id);
  }

  async create(data: CreateUserDto): Promise<User> {
    const validated = createUserSchema.parse(data);
    return this.userRepo.create(validated);
  }
}
```

### Zod Validation
```typescript
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

export type CreateUserDto = z.infer<typeof createUserSchema>;
```

### Error Handling
```typescript
// Custom error classes
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

// Error middleware
export const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code,
    });
  }

  console.error(err);
  return res.status(500).json({ error: 'Internal server error' });
};
```

## Database Patterns

### With Prisma
```typescript
// prisma/schema.prisma
model User {
  id        String   @id @default(uuid())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
}

// Repository
export class UserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

### With Drizzle
```typescript
import { pgTable, uuid, varchar, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 100 }).notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

## Best Practices

1. **TypeScript**
   - Use strict mode always
   - Define explicit return types
   - Avoid `any`, use `unknown` if needed

2. **Async/Await**
   - Always use async/await over callbacks
   - Handle Promise rejections
   - Use Promise.all for parallel operations

3. **Environment**
   - Use dotenv for local development
   - Validate env vars at startup with Zod
   - Never commit .env files

4. **Testing**
   - Use Vitest or Jest
   - Mock external dependencies
   - Use supertest for API tests

## Quality Checklist

Before completing:
- [ ] TypeScript compiles without errors
- [ ] All inputs validated with Zod
- [ ] Errors properly handled
- [ ] Tests written
- [ ] No console.log in production code
