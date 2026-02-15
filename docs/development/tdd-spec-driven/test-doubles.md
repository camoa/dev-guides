---
description: When and how to use mocks, stubs, fakes, spies, and dummies in tests
---

# Test Doubles

## When to Use
You need to test code that depends on external systems (databases, APIs, file systems) or collaborating objects that are slow, unavailable, or difficult to set up in tests.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Provide canned responses to calls | Stub | You're testing behavior that depends on a return value, but don't care how it was called |
| Verify interactions (how many times, with what args) | Mock or Spy | You're testing that your code calls a dependency correctly |
| Replace complex external system with simple in-memory version | Fake | You need realistic behavior but can't use real implementation (e.g., in-memory database for tests) |
| Fill parameter lists for code that doesn't use them | Dummy | The method signature requires an object but test doesn't use it |
| Record calls to real implementation | Spy | You want mostly real behavior but need to verify specific interactions |

## Pattern: Types of Test Doubles

```python
# DUMMY: Object passed but never used
class DummyLogger:
    def log(self, message):
        pass  # Does nothing, test doesn't care about logging

def test_processor_with_dummy():
    processor = DataProcessor(logger=DummyLogger())  # Satisfies constructor
    result = processor.process([1, 2, 3])  # Test doesn't verify logging
    assert result == [2, 4, 6]

# STUB: Returns predetermined values
class StubUserRepository:
    def find_by_id(self, user_id):
        return User(id=123, name='Test User', active=True)

def test_user_service_with_stub():
    repo = StubUserRepository()
    service = UserService(repo)
    user = service.get_active_user(123)
    assert user.name == 'Test User'  # Tests service logic, not repository

# FAKE: Working implementation with shortcuts
class FakeDatabase:
    def __init__(self):
        self.data = {}  # In-memory storage instead of real DB

    def save(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

def test_cache_with_fake_db():
    db = FakeDatabase()
    cache = Cache(db)
    cache.set('user:123', {'name': 'Alice'})
    assert cache.get('user:123')['name'] == 'Alice'

# MOCK: Verifies interactions (using framework)
def test_notification_with_mock():
    email_service = Mock()  # Using unittest.mock or similar
    notifier = Notifier(email_service)

    notifier.send_welcome('user@example.com')

    # Verify the call was made with correct arguments
    email_service.send.assert_called_once_with(
        to='user@example.com',
        subject='Welcome',
        body=ANY  # Don't care about exact body
    )

# SPY: Records calls to real implementation
def test_cache_invalidation_with_spy():
    real_db = Database()
    spy_db = Spy(real_db)  # Wraps real object, records calls
    cache = Cache(spy_db)

    cache.invalidate('user:123')

    # Verify real DB was called
    assert spy_db.delete.call_count == 1
    assert spy_db.delete.called_with('user:123')
```

## When to Use Each Type

**Stubs** - Most common; use when testing code that queries dependencies
- Testing logic that depends on return values
- You don't care how many times the dependency was called
- Focus is on state, not interaction

**Mocks** - Use when the side effect IS what you're testing
- Verifying your code calls an API correctly
- Ensuring email notifications are sent
- Testing that audit logs are written

**Fakes** - Use for complex dependencies needing realistic behavior
- In-memory database for integration tests
- Fake payment gateway that simulates success/failure
- File system in memory instead of disk

**Spies** - Use when you mostly want real behavior but need to verify calls
- Testing that cache correctly delegates to real storage
- Verifying retry logic on real HTTP client
- Less common than stubs/mocks

**Dummies** - Rarely needed; use only to satisfy signatures
- Required parameter that test doesn't use
- Often a sign of poor API design

## Common Mistakes

- Over-mocking - Mocking everything makes tests brittle; mock only external boundaries, use real objects for your own code
- Testing mocks instead of real code - Verify mocks return what you expect, but that's testing the test, not the code
- Mocking implementation details - Mock external dependencies, not internal collaborators within your module (leads to brittle tests)
- Complex mock setup that duplicates production logic - If mock setup is complex, use a fake or the real implementation
- Not verifying mocks were called correctly - Mock exists to verify interactions; if you don't assert on calls, use a stub instead
- Mocking language features - Don't mock built-in functions (Math, Date, etc.); use dependency injection to make them testable

## Frameworks by Language

```
Python:      unittest.mock (built-in), pytest with pytest-mock
JavaScript:  Jest (built-in mocking), Sinon.js, Vitest
PHP:         PHPUnit (built-in mocking), Mockery, Prophecy
Java:        Mockito, EasyMock, JMock
C#:          Moq, NSubstitute, FakeItEasy
Ruby:        RSpec mocks (built-in), Mocha
```

## See Also
- Previous: [Unit Testing Fundamentals](unit-testing-fundamentals.md) | Next: [Testing Patterns](testing-patterns.md)
- Reference: [Martin Fowler: Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- Reference: [Martin Fowler: Test Double](https://martinfowler.com/bliki/TestDouble.html)
- Reference: [Understanding Test Doubles: Mock, Spy, Stub and Fake](https://medium.com/@john-o-dev/understanding-test-doubles-mock-spy-stub-and-fake-1ca33c9f2f52)
