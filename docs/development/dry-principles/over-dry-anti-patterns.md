---
description: Recognizing when abstractions hurt more than help and when to choose duplication over the wrong abstraction
---

# Over-DRY Anti-Patterns

## When to Use

When evaluating whether an abstraction is helping or hurting, and when to choose duplication over the wrong abstraction.

## Common Over-DRY Anti-Patterns

| Anti-Pattern | What It Looks Like | Why It's Harmful | Solution |
|--------------|-------------------|------------------|----------|
| **Premature Abstraction** | Creating abstractions before understanding variance | Wrong abstractions hard to change, couple unrelated code | Wait for Rule of Three, use WET/AHA |
| **God Objects** | Single class/module handles everything "to avoid duplication" | Violates Single Responsibility, hard to test, high coupling | Split by responsibility, accept some duplication |
| **Forced Unification** | Merging similar but not identical concepts | Complexity grows as special cases accumulate | Keep separate if they serve different purposes |
| **Leaky Abstractions** | Abstraction exposes implementation details | Defeats purpose, creates coupling | Redesign abstraction or accept duplication |
| **Coupling Through DRY** | Shared state/schema couples independent modules | Changes ripple across unrelated code | Use separate models, accept some duplication |
| **Abstraction Layers** | Too many layers of indirection | Cognitive overhead, hard to debug | Inline unnecessary layers |

## Anti-Pattern: Premature Abstraction

```python
# ANTI-PATTERN: Abstract after seeing TWO similar functions
def send_email(to, subject, body):
    # ...
    pass

def send_sms(to, message):
    # ...
    pass

# Premature abstraction (only 2 instances!)
class Notifier:
    def __init__(self, channel_type, recipient_field):
        self.channel_type = channel_type
        self.recipient_field = recipient_field

    def send(self, recipient, **kwargs):
        if self.channel_type == 'email':
            self._send_email(recipient, kwargs['subject'], kwargs['body'])
        elif self.channel_type == 'sms':
            self._send_sms(recipient, kwargs['message'])
        # What about push? Slack? Discord? This abstraction is already awkward.

# BETTER: Wait for third instance, then abstract with full understanding
# Keep send_email and send_sms separate until pattern is clear
```

## Anti-Pattern: God Object

```typescript
// ANTI-PATTERN: Everything in one class to "avoid duplication"
class UserManager {
  // User CRUD
  createUser(data) { /* ... */ }
  updateUser(id, data) { /* ... */ }
  deleteUser(id) { /* ... */ }

  // Authentication (should be separate)
  login(email, password) { /* ... */ }
  logout(userId) { /* ... */ }

  // Authorization (should be separate)
  hasPermission(userId, permission) { /* ... */ }

  // Profile (should be separate)
  updateAvatar(userId, image) { /* ... */ }

  // Email (definitely should be separate)
  sendWelcomeEmail(userId) { /* ... */ }
  sendPasswordReset(userId) { /* ... */ }
}

// BETTER: Split by responsibility
class UserRepository { /* CRUD */ }
class AuthService { /* Authentication */ }
class AuthorizationService { /* Permissions */ }
class UserProfileService { /* Profile operations */ }
class UserNotificationService { /* Emails */ }

// Yes, more classes. But each is focused, testable, and maintainable.
```

## Anti-Pattern: Coupling Through Shared Schema

```typescript
// ANTI-PATTERN: Frontend, backend, database share exact same schema
// Seems DRY, but creates hidden coupling

// shared-schema.ts
interface User {
  id: number;
  email: string;
  passwordHash: string;  // Sensitive! Should NOT be in frontend
  internalNotes: string; // Admin-only, not for API
  createdAt: Date;
  lastLoginIp: string;   // Privacy concern
}

// Now frontend, backend, database all use same User type
// Problem: Any change affects ALL layers
// Security problem: Frontend sees passwordHash field
// Privacy problem: API returns lastLoginIp

// BETTER: Separate models per boundary
// database/models.ts
interface UserEntity {
  id: number;
  email: string;
  passwordHash: string;
  internalNotes: string;
  createdAt: Date;
  lastLoginIp: string;
}

// api/dto.ts
interface UserDto {
  id: number;
  email: string;
  createdAt: string;  // Serialized differently
  // No passwordHash, no internalNotes, no lastLoginIp
}

// frontend/types.ts
interface User {
  id: number;
  email: string;
  createdAt: Date;
}

// Mappers between layers (small duplication, huge benefit)
function toDto(entity: UserEntity): UserDto {
  return {
    id: entity.id,
    email: entity.email,
    createdAt: entity.createdAt.toISOString(),
  };
}
```

## Anti-Pattern: Over-Generalization

```java
// ANTI-PATTERN: Generic abstraction that handles too many cases
public class DataProcessor<T, R, C extends ProcessingContext> {
    private Validator<T> validator;
    private Transformer<T, R> transformer;
    private Persister<R, C> persister;

    public R process(T input, C context) throws ProcessingException {
        if (!validator.validate(input, context.getValidationRules())) {
            throw new ValidationException();
        }
        R transformed = transformer.transform(input, context.getTransformOptions());
        persister.persist(transformed, context);
        return transformed;
    }
}

// Usage is incredibly complex
DataProcessor<UserInput, UserEntity, UserProcessingContext> processor =
    new DataProcessor<>(
        new UserValidator(),
        new UserTransformer(),
        new UserPersister()
    );

// BETTER: Specific classes that are obvious
public class UserService {
    public User createUser(CreateUserRequest request) {
        validateUserInput(request);
        User user = buildUserFromRequest(request);
        repository.save(user);
        return user;
    }
}
```

## The Wrong Abstraction Cost

From Sandi Metz:

1. Developer sees duplication
2. Developer creates abstraction to eliminate duplication
3. New requirement emerges that doesn't quite fit abstraction
4. Developer adds conditional to abstraction to handle new case
5. Repeat step 3-4 multiple times
6. Abstraction becomes complex, brittle, hard to understand
7. **Cost of wrong abstraction > cost of duplication**

**Solution**: Prefer duplication over wrong abstraction. When abstraction is wrong:

1. Re-introduce duplication by inlining abstraction into callers
2. Delete the abstraction
3. Let new pattern emerge naturally
4. Abstract again when pattern is clear

## Common Mistakes

- **Worshipping DRY as absolute rule** — Context and judgment matter; sometimes duplication is better
- **Confusing DRY with code minimization** — DRY is about knowledge, not lines of code
- **Creating abstractions too early** — Without understanding variance, abstractions will be wrong
- **Never revisiting abstractions** — Wrong abstractions accumulate; refactor when painful
- **Sharing code across boundaries that should be independent** — Microservices, frontend/backend need separate models

## See Also

- [DRY vs WET vs AHA](dry-vs-wet-vs-aha.md)
- [Rule of Three](rule-of-three.md)
- [Sandi Metz - The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- [Dan Abramov - Goodbye, Clean Code](https://overreacted.io/goodbye-clean-code/)
