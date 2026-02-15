# Node.js Structure

TypeScript strict mode. Async/await everywhere.

```
src/
  index.ts           # Entry
  routes/            # Route definitions
  controllers/       # Request handlers
  services/          # Business logic
  repositories/      # Data access
  models/            # Types and Zod schemas
  middleware/        # Express middleware
  utils/
  config/
```

## Controller → Service → Repository
```typescript
// Controller
export const getUser = async (req: Request<{ id: string }>, res: Response, next: NextFunction) => {
  try {
    const user = await userService.getById(req.params.id);
    if (!user) return res.status(404).json({ error: 'Not found' });
    return res.json(user);
  } catch (error) { next(error); }
};

// Service
class UserService {
  constructor(private readonly repo: UserRepository) {}
  async getById(id: string): Promise<User | null> { return this.repo.findById(id); }
}
```
