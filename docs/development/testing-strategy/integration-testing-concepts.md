---
description: Integration testing — verifying component seams with a real test database while stubbing external third-party services.
tldr: Integration tests verify seams between components using a real test database and real internal implementations, stubbing only external third-party services (email, payment APIs). They deliver the highest ROI per test in most modern applications and catch what unit tests miss.
---

# Integration Testing Concepts

## When to Use

> Use integration tests to verify that two or more components work correctly together — a service with its database, a controller with its service layer, a React component with its data-fetching hook. Mock outward (external); use real implementations inward (your code, your DB).

## Boundary Strategy

```
┌─────────────────────────────────────────────────────┐
│              Your Application                       │
│                                                     │
│  Controller → Service → Repository → [Database]    │
│                                ↕                   │
│              [Your test uses a real test DB here]  │
│                                                     │
│  Service → [EmailService] ← STUB THIS              │
│  Service → [StripeAPI]    ← STUB THIS              │
│  Service → [AnotherService you own] ← KEEP REAL    │
└─────────────────────────────────────────────────────┘
```

Mock outward (third-party, slow, non-deterministic). Use real implementations inward (your code, your database).

## Decision

| What integration tests cover | What unit tests miss |
|---|---|
| ORM/query behavior — does your query return what you expect? | Any behavior requiring real database state |
| Request/response serialization — HTTP layer input/output | Wire-up between layers |
| Transaction semantics — multi-step write rollbacks | Database constraint enforcement |
| Service wiring — dependency injection produces correct object graph | Cross-component flows |
| Database constraint enforcement (FK, unique) | Real collaboration between components |

## Pattern

```javascript
// Integration test: real in-memory DB, real service layer, stubbed email API
test('POST /register creates user and triggers welcome email', async () => {
  const db = new InMemoryDatabase();
  const emailSpy = jest.fn();
  const app = buildApp({ db, emailService: { sendWelcome: emailSpy } });

  const res = await request(app)
    .post('/register')
    .send({ email: 'alice@example.com', password: 'S3cret!' });

  expect(res.status).toBe(201);
  const saved = await db.users.findByEmail('alice@example.com');
  expect(saved).toBeDefined();
  expect(saved.passwordHash).not.toBe('S3cret!');
  expect(emailSpy).toHaveBeenCalledWith('alice@example.com');
});
```

**Boundary rule:** real implementations inside the seam (your code, your DB); stub everything outside (email API, payment gateway, external HTTP).

## Common Mistakes

- **Wrong**: Mocking your own code in an integration test → **Right**: Defeats the purpose; you are testing mocks, not integrations
- **Wrong**: Sharing database state between tests → **Right**: Use transactions that rollback, or truncate tables in teardown
- **Wrong**: Integration test that spins up a full browser → **Right**: That is an E2E test; put it in that suite
- **Wrong**: Using production database in tests → **Right**: Always use an isolated test database
- **Wrong**: Integration tests for everything → **Right**: Reserve for seams; pure logic belongs in unit tests

## See Also

- [Unit Testing Concepts](unit-testing-concepts.md) | Next: [Functional Testing Concepts](functional-testing-concepts.md)
- Related: [Test Doubles](test-doubles.md) — what to stub and what not to
- Related: [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) — Kernel tests as Drupal's integration layer
- Reference: Martin Fowler, [IntegrationTest](https://martinfowler.com/bliki/IntegrationTest.html)
