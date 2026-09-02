---
description: "Test doubles taxonomy — when to use a stub, mock, spy, fake, or dummy, and why mocking your own code is the most expensive mistake."
tldr: "Use stubs to return controlled values, mocks to verify side effects occurred, fakes for realistic in-memory alternatives, spies sparingly, dummies to satisfy signatures. Never mock your own internal code — mock only at the boundary (external services, third-party APIs). Mocking what you own produces tests that pass but production breaks."
---

# Test Doubles

## When to Use

> When the code under test depends on something slow (database, HTTP, filesystem), non-deterministic (clock, random), or unavailable in tests (third-party API). Test doubles replace those dependencies with controlled stand-ins so unit and integration tests remain fast, isolated, and repeatable.

## The Taxonomy (Meszaros)

Gerard Meszaros coined the term "test double" (from "stunt double") and defined five distinct types. These names are often confused — using the wrong one produces brittle tests or missed coverage.

| Type | Definition | Verifies? | Realistic? |
|---|---|---|---|
| **Dummy** | Passed to satisfy a parameter; never actually used | No | No |
| **Stub** | Returns predetermined values to queries from the code under test | No | No |
| **Spy** | Records calls; still delegates to a real or partial implementation | After the fact | Partially |
| **Mock** | Pre-programmed with expectations; fails if not called correctly | Yes — interactions | No |
| **Fake** | A working simplified implementation (in-memory DB, fake payment gateway) | Via behavior | Yes, simplified |

## Decision: Which Double to Reach For

| If you need... | Use... | Why |
|---|---|---|
| Satisfy a required constructor parameter the test doesn't exercise | Dummy | Test doesn't care about that dependency at all |
| Return a canned value so code under test can proceed | Stub | You are testing state (return values), not interaction |
| Verify a dependency was called — with what arguments, how many times | Mock | You are testing that a side effect occurred correctly |
| Record calls but still use the real implementation | Spy | You want mostly real behavior plus call verification |
| Replace a complex dependency with a fast, realistic in-memory version | Fake | You need real behavioral correctness, not just pass/fail |

## Pattern

```python
# STUB: return controlled data; test does not verify how many times called
class StubUserRepo:
    def find_by_id(self, user_id):
        return User(id=user_id, name='Alice', active=True)

# MOCK: verify specific interaction occurred (using a mocking framework)
def test_sends_welcome_email_on_registration():
    email_service = Mock()
    service = RegistrationService(email=email_service)
    service.register('alice@example.com', 'password')
    email_service.send_welcome.assert_called_once_with('alice@example.com')

# FAKE: in-memory implementation with real behavior
class FakeEmailService:
    def __init__(self):
        self.sent = []
    def send_welcome(self, address):
        self.sent.append(('welcome', address))
    def send_reset(self, address, token):
        self.sent.append(('reset', address, token))

# DUMMY: satisfies the constructor; test doesn't exercise it
service = PaymentProcessor(logger=DummyLogger())  # test never triggers logging
```

## Over-Mocking Anti-Pattern

The most expensive test double mistake is mocking your own internal code. When you mock every collaborator:

- You are testing that mocks were called (interaction testing), not that behavior is correct
- Refactoring breaks tests even when behavior is unchanged
- The test suite gives false confidence: everything passes, production breaks

**Mock at the boundary, not inside it.** If your application is a single process, mock the external services it calls (email API, payment gateway, third-party HTTP), but use real implementations for your own services and repositories (with a test database).

## When to Use Each

**Stubs** (most common): use whenever testing code that queries a dependency and you care about the return value, not how often it was called.

**Mocks**: use when the side effect IS the behavior being tested — email was sent, event was published, audit log was written.

**Fakes**: use when a stub is too simple (doesn't model state correctly) and the real dependency is too slow. The canonical fake is an in-memory database.

**Spies**: use sparingly; mostly useful when you want to verify call count on a real object without replacing it entirely.

**Dummies**: use only to satisfy API signatures; their presence usually signals a design smell (god object constructor).

## Common Mistakes

- Using "mock" as a synonym for all test doubles → Creates confusion; choose the right type for the right use case
- Mocking what you own → Leads to interaction-coupled tests that break on every refactor
- Stubs that return impossible states → `stub.find_user.returns(null)` when your DB never returns null for a found user; tests verify impossible scenarios
- Fake implementations that diverge from real behavior → If the fake behaves differently than the real dependency, tests pass but production fails; keep fakes honest

## See Also

- ← Previous: [Accessibility Testing Concepts](accessibility-testing-concepts.md) | Next: [Test Structure and Naming](test-structure-and-naming.md) →
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Test Doubles section with code examples
- Reference: Martin Fowler, [TestDouble](https://martinfowler.com/bliki/TestDouble.html)
- Reference: Martin Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- Reference: Gerard Meszaros, "xUnit Test Patterns" (2007) — canonical taxonomy source
