---
description: Test pyramid vs trophy vs diamond strategies, what to test at each level, and integration test structure
---

# Integration Testing Strategy

## When to Use
Your unit tests verify individual components work correctly, and now you need to verify they work together correctly. Essential for multi-component systems, APIs, databases, and microservices.

## Test Pyramid vs Test Trophy vs Test Diamond

**Test Pyramid** (Mike Cohn, 2000s)
```
      /\      E2E (UI) Tests - Few, slow, brittle
     /  \
    /____\    Integration/API Tests - Some, medium speed
   /      \
  /________\  Unit Tests - Many, fast, isolated
```
Most tests should be fast unit tests; fewer integration tests; minimal E2E tests.

**Test Trophy** (Kent C. Dodds, 2018)
```
     ___      E2E Tests - Some (more than pyramid)
    /   \
   |     |    Integration Tests - MOST (focus here)
   |_____|
  /       \   Unit Tests - Many but not majority
 /_________\  Static Analysis - Foundation
```
Integration tests give best ROI: test real interactions without full system overhead.

**Test Diamond** (Emerging, 2024+)
```
     /\       E2E Tests - Some
    /  \
   /____\     Integration Tests - Many (balanced with unit)
   \    /
    \  /      Unit Tests - Many (balanced with integration)
     \/
```
Balance unit and integration tests equally; E2E tests for critical user journeys only.

**2025 Update**: Kent C. Dodds questioned whether E2E tests should be larger proportion of trophy now that tools like Playwright and Vitest Browser Mode make E2E tests as cheap and fast as integration tests.

## Decision: What to Test at Each Level

| Test for... | At this level | Why |
|---|---|---|
| Pure logic, algorithms, calculations | Unit tests | Fast, isolated, no dependencies |
| Single class/module behavior | Unit tests | Focus on one thing, easy to debug |
| Database queries, ORM mappings | Integration tests | Must verify actual database behavior |
| API endpoints (request to response) | Integration tests | Verify routing, serialization, validation |
| Service-to-service communication | Integration tests | Mock external services, test your integration code |
| Authentication, authorization flows | Integration tests | Complex interactions, must test real behavior |
| Critical user journeys (signup, purchase) | E2E tests | Verify entire system works together from user perspective |
| Cross-browser compatibility | E2E tests | Can't unit test browser differences |
| Performance under load | Load tests (separate) | Requires realistic data volume and concurrency |

## Pattern: Integration Test Structure

```python
# Integration test: User registration with database and email service
class TestUserRegistration:
    """
    Integration tests for user registration feature.
    Tests real database but mocks external email service.
    """

    def setup_method(self):
        # Use real database (in-memory SQLite or dockerized Postgres)
        self.db = TestDatabase()
        self.db.migrate()

        # Mock external email service (don't send real emails in tests)
        self.email_service = Mock(spec=EmailService)

        # Real application components
        self.user_repo = UserRepository(self.db)
        self.registration_service = RegistrationService(
            user_repo=self.user_repo,
            email_service=self.email_service
        )

    def teardown_method(self):
        self.db.drop_all()
        self.db.close()

    def test_successful_registration_saves_user_and_sends_email(self):
        # ARRANGE
        email = "alice@example.com"
        password = "SecurePass123!"

        # ACT
        user = self.registration_service.register(email, password)

        # ASSERT: User saved to real database
        saved_user = self.user_repo.find_by_email(email)
        assert saved_user.id == user.id
        assert saved_user.email == email
        assert bcrypt.verify(password, saved_user.password_hash)

        # ASSERT: Welcome email sent
        self.email_service.send_welcome.assert_called_once_with(email)

    def test_duplicate_email_raises_error_without_sending_email(self):
        # ARRANGE: Existing user
        self.registration_service.register("alice@example.com", "pass123")

        # ACT & ASSERT: Second registration fails
        with pytest.raises(DuplicateEmailError):
            self.registration_service.register("alice@example.com", "different")

        # ASSERT: Email service not called for failed registration
        assert self.email_service.send_welcome.call_count == 1  # Only first registration
```

## What to Mock in Integration Tests

**Mock external boundaries:**
- Third-party APIs (payment gateways, email services, external data sources)
- Slow external services (even if owned by you)
- Non-deterministic systems (real-time data feeds)

**Use real implementations for:**
- Your own database (use test database, not production)
- Your own services within the same system
- File system (use temp directories)
- In-memory caches

## Integration Test Performance

**Fast integration tests** (goal: < 100ms per test):
- Use in-memory databases (SQLite, H2)
- Use test containers that spin up/down quickly
- Parallelize tests
- Share database schema setup across tests (but not data)

**Acceptable integration tests** (100ms - 1s):
- Real database (Postgres/MySQL in Docker)
- Multiple service interactions
- File I/O operations

**Slow integration tests** (> 1s):
- Full database migrations
- Complex data setup
- Many external service calls

If tests are slow, revisit what you're testing - might be E2E test disguised as integration test.

## Common Mistakes

- Testing everything at integration level - Expensive; test logic at unit level, interactions at integration level
- Using production database for tests - Dangerous and slow; use dedicated test database
- Not isolating test data - Tests interfere with each other; use transactions that rollback or clean database between tests
- Mocking your own code in integration tests - Defeats the purpose; mock external boundaries, use real code for your system
- Integration tests that are actually E2E tests - If test starts HTTP server and makes real HTTP calls through full stack, that's E2E
- Sharing state between integration tests - Tests should be independent; use setup/teardown to ensure clean state

## See Also
- Previous: [From Spec to Implementation](spec-to-implementation.md) | Next: [Test Coverage Strategy](test-coverage.md)
- Related: [Test Doubles](test-doubles.md) (what to mock)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) (FIRST principles apply to integration tests too)
- Reference: [Test Pyramid Guide 2025](https://fullscale.io/blog/modern-test-pyramid-guide/)
- Reference: [Kent C. Dodds: Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
