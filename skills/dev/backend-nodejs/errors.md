# Node.js Error Handling

```typescript
export class AppError extends Error {
  constructor(message: string, public statusCode = 500, public code?: string) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) { super(`${resource} not found`, 404, 'NOT_FOUND'); }
}

// Middleware
export const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message, code: err.code });
  }
  console.error(err);
  return res.status(500).json({ error: 'Internal server error' });
};
```

Handle Promise rejections. Use Promise.all for parallel operations.
