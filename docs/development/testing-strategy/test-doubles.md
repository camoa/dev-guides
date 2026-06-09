---
description: Test doubles taxonomy — when to use a stub, mock, spy, fake, or dummy, and why mocking your own code is the most expensive mistake.
tldr: Use stubs to return controlled values, mocks to verify side effects occurred, fakes for realistic in-memory alternatives, spies sparingly, dummies to satisfy signatures. Never mock your own internal code — mock only at the boundary (external services, third-party APIs). Mocking what you own produces tests that pass but production breaks.
---

# Test Doubles

## When to Use

> Use test doubles to replace slow, non-deterministic, or unavailable dependencies (databases, HTTP, clocks, third-party APIs) in unit and integration tests. Mock at the boundary — external services — never inside your own application.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Satisfy a required constructor parameter the test doesn't exercise | Dummy | Test doesn't care about that dependency at all |
| Return a canned value so code under test can proceed | Stub | Testing state (return values), not interaction |
| Verify a dependency was called with specific arguments | Mock | Testing that a side effect occurred correctly |
| Record calls but still use the real implementation | Spy | Mostly real behavior plus call verification |
| Replace a complex dependency with a fast, realistic in-memory version | Fake | Need real behavioral correctness, not just pass/fail |

## Pattern

```python
# STUB: controlled data; test does not verify call count
class StubUserRepo:
    def find_by_id(self, user_id):
        return User(id=user_id, name='Alice', active=True)

# MOCK: verify specific interaction occurred
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

# DUMMY: satisfies constructor; test never triggers it
service = PaymentProcessor(logger=DummyLogger())
```

## Common Mistakes

- **Wrong**: Using "mock" as a synonym for all test doubles → **Right**: Choose the right type; stub for state, mock for interaction, fake for behavior
- **Wrong**: Mocking your own internal application code → **Right**: Mock only external boundaries; use real implementations for your own services
- **Wrong**: Stubs that return impossible states → **Right**: Stubs must return values consistent with what the real dependency produces
- **Wrong**: Fake implementations that diverge from real behavior → **Right**: Keep fakes honest; if fake behaves differently, tests pass but production fails

## See Also

- [Accessibility Testing Concepts](accessibility-testing-concepts.md) | Next: [Test Structure and Naming](test-structure-and-naming.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Test Doubles section
- Reference: Martin Fowler, [TestDouble](https://martinfowler.com/bliki/TestDouble.html)
- Reference: Martin Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- Reference: Gerard Meszaros, "xUnit Test Patterns" (2007) — canonical taxonomy source
