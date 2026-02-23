# Node.js Database

## Prisma
```typescript
// schema.prisma
model User {
  id        String   @id @default(uuid())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
}

// Repository
class UserRepository {
  constructor(private readonly prisma: PrismaClient) {}
  async findById(id: string) { return this.prisma.user.findUnique({ where: { id } }); }
}
```

## Drizzle
```typescript
import { pgTable, uuid, varchar, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 100 }).notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```
