---
description: "Integration testing — verifying component seams with a real test database while stubbing external third-party services."
tldr: "Integration tests verify seams between components using a real test database and real internal implementations, stubbing only external third-party services (email, payment APIs). They deliver the highest ROI per test in most modern applications and catch what unit tests miss."
---

# Integration Testing Concepts

## When to Use

> When you need to verify that two or more components work correctly together — a service with its database, a controller with its service layer, a React component with its data-fetching hook. Integration tests occupy the middle layer of the pyramid/trophy and deliver the highest ROI per test in most modern applications.

## What Is an Integration Test?

An integration test verifies the **seams** — the points where one unit hands off to another. The canonical integration test:

- Uses a real database (test database, in-memory, or containerized)
- Stubs or mocks **external** third-party services (email, payment gateway, external APIs)
- Does **not** mock internal application components — those are tested together for real

A seam is the boundary between what you own and what you depend on. Keep real implementations inside the seam; replace everything outside it.

## What Integration Tests Cover (and Unit Tests Miss)

- ORM/query behavior: does your query return what you expect when the database has that data?
- Request/response serialization: does the HTTP layer parse input and format output correctly?
- Transaction semantics: does a multi-step write rollback correctly on failure?
- Service wiring: does dependency injection produce the correct object graph?
- Database constraint enforcement: do foreign key or unique constraints fire at the right moments?

None of these are verifiable by a unit test — they require real collaboration between components.

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

## Pattern

```javascript
// Integration test: a user registration endpoint
// - Real in-memory DB (fast, real SQL)
// - Real service layer and repository
// - Stub only the external email API

test('POST /register creates user and triggers welcome email', async () => {
  // Arrange: real app with test DB, stubbed email
  const db = new InMemoryDatabase();
  const emailSpy = jest.fn();
  const app = buildApp({ db, emailService: { sendWelcome: emailSpy } });

  // Act: real HTTP request through the full stack
  const res = await request(app)
    .post('/register')
    .send({ email: 'alice@example.com', password: 'S3cret!' });

  // Assert: behavior observable from outside
  expect(res.status).toBe(201);
  const saved = await db.users.findByEmail('alice@example.com');
  expect(saved).toBeDefined();
  expect(saved.passwordHash).not.toBe('S3cret!'); // hashed
  expect(emailSpy).toHaveBeenCalledWith('alice@example.com');
});
```

## Common Mistakes

- Mocking your own code in an integration test → Defeats the purpose; you are testing mocks, not integrations
- Sharing database state between tests → Tests fail in unpredictable order; use transactions that rollback, or truncate tables in teardown
- Building integration tests that are actually E2E tests → If the test spins up a full browser, it is an E2E test — put it in that suite
- Using production database in tests → Dangerous, slow, and non-repeatable
- Integration tests for everything → Reserve for seams and cross-component flows; pure logic belongs in unit tests

## See Also

- ← Previous: [Unit Testing Concepts](unit-testing-concepts.md) | Next: [Functional Testing Concepts](functional-testing-concepts.md) →
- Related: [Test Doubles](test-doubles.md) — what to stub and what not to
- Related: [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) — Kernel tests as Drupal's integration layer
- Reference: Martin Fowler, [IntegrationTest](https://martinfowler.com/bliki/IntegrationTest.html)
