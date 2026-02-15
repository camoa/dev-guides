---
description: Coverage targets by context, what to test vs skip, branch vs line coverage, and coverage tools
---

# Test Coverage Strategy

## When to Use
You're deciding what to test, how much to test, and evaluating whether your test suite is adequate. Coverage metrics are tools for finding gaps, not goals to hit.

## The Coverage Paradox

**100% coverage doesn't mean your code is correct.** You can execute every line and still miss:
- Wrong business logic
- Edge cases not covered
- Race conditions
- Integration bugs
- Security vulnerabilities

**0% coverage doesn't mean your code is wrong.** Some code is so simple that tests add no value:
- Plain getters/setters with no logic
- Data transfer objects (POJOs/DTOs)
- Configuration classes

**The goal: meaningful coverage that catches real bugs, not percentage targets.**

## Industry Guidelines

| Coverage % | Interpretation |
|-----------|----------------|
| < 60% | Insufficient for most projects; high risk of undetected bugs |
| 60-75% | Acceptable for many projects (Google considers 60% acceptable) |
| 75-80% | Commendable (Google considers 75% commendable); good target for most teams |
| 80-90% | Excellent (Google considers 90% exemplary); covers critical paths and most edge cases |
| > 90% | Diminishing returns; likely testing trivial code or writing tests to hit metric |

**Context matters:**
- **Safety-critical systems** (medical, aviation): 90%+ with extensive integration testing
- **Financial systems**: 80-90% with focus on calculations and transactions
- **Internal tools**: 60-75% may be sufficient
- **Prototypes/MVPs**: Test critical path only; coverage is secondary

## What to Test

**Always test:**
- Business logic with decisions/calculations
- Code that handles money, permissions, or sensitive data
- Complex algorithms
- Edge cases that have caused bugs before
- Public APIs and library interfaces
- Code that changes frequently

**Consider testing:**
- Moderate complexity code
- Integration points between systems
- Code that's hard to verify manually
- Frameworks/infrastructure (one test to verify setup)

**Don't test:**
- Trivial getters/setters with no logic
- Framework code (trust the framework)
- Generated code (code generator should be tested)
- Constants and configuration
- Private methods (test through public interface)

## Pattern: Coverage-Driven Test Gaps

```python
# Code with 100% line coverage but poor test quality
def calculate_discount(price, customer_type):
    if customer_type == 'VIP':
        return price * 0.8  # 20% off
    else:
        return price * 0.9  # 10% off

# BAD: 100% line coverage but doesn't test edge cases
def test_calculate_discount():
    assert calculate_discount(100, 'VIP') == 80
    assert calculate_discount(100, 'regular') == 90
    # Missing: negative prices, zero, None, invalid customer_type

# GOOD: Tests edge cases and business rules
@pytest.mark.parametrize("price,customer_type,expected", [
    (100, 'VIP', 80),           # Happy path VIP
    (100, 'regular', 90),       # Happy path regular
    (0, 'VIP', 0),             # Zero price
    (1.99, 'VIP', 1.59),       # Fractional price
    (100, 'UNKNOWN', 90),      # Unknown type defaults to regular
])
def test_calculate_discount_comprehensive(price, customer_type, expected):
    assert calculate_discount(price, customer_type) == pytest.approx(expected)

def test_calculate_discount_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_discount(-10, 'VIP')
```

## Coverage Tools by Language

```
Python:               coverage.py, pytest-cov
JavaScript/TypeScript: Istanbul (nyc), Jest (built-in), Vitest (built-in)
PHP:                  PHPUnit (built-in), Xdebug
Java:                 JaCoCo, Cobertura
C#:                   Coverlet, dotCover
Ruby:                 SimpleCov
Go:                   go test -cover (built-in)
```

## Using Coverage to Find Gaps

**Step 1: Run coverage report**
```bash
# Example: pytest with coverage
pytest --cov=myapp --cov-report=html
# Opens htmlcov/index.html showing line-by-line coverage
```

**Step 2: Identify untested critical code**
- Sort by coverage % to find poorly tested files
- Look for red/yellow lines in critical business logic
- Ignore low coverage in trivial code (DTOs, configs)

**Step 3: Prioritize gaps**
- High risk + low coverage = urgent (business logic, security, money)
- High risk + high coverage = maintain
- Low risk + low coverage = acceptable (simple getters)
- Low risk + high coverage = probably over-tested

**Step 4: Write tests for gaps**
- Focus on missing edge cases first
- Add tests for uncovered branches
- Don't write tests just to hit percentage

## Branch Coverage vs Line Coverage

```python
# 100% line coverage, 50% branch coverage
def is_valid_password(password):
    if password and len(password) >= 8:  # Two conditions!
        return True
    return False

# This test achieves 100% line coverage
def test_password():
    assert is_valid_password("LongPassword") == True
    assert is_valid_password("short") == False

# But misses these branches:
# - password is None (first condition false)
# - password is empty string (first condition false)
# - password exists but len < 8 (first true, second false)

# GOOD: 100% branch coverage
@pytest.mark.parametrize("password,expected", [
    ("ValidPass123", True),    # Both conditions true
    ("short", False),          # Exists but too short
    ("", False),              # Empty (first condition false)
    (None, False),            # None (first condition false)
])
def test_password_validation(password, expected):
    assert is_valid_password(password) == expected
```

**Prefer branch coverage over line coverage.** Most tools support both.

## Common Mistakes

- Treating coverage as a goal - Coverage is a diagnostic tool, not a target; focus on meaningful tests
- Gaming the metric - Writing tests that execute code without asserting behavior just to hit percentage
- 100% coverage obsession - Wastes time on trivial code; diminishing returns above 80-90%
- Ignoring branch coverage - Line coverage can be 100% while missing half the logic branches
- Testing implementation details - High coverage of internals that change frequently makes tests brittle
- No coverage measurement - Flying blind; coverage tools reveal what you're not testing

## See Also
- Previous: [Integration Testing Strategy](integration-testing.md) | Next: [Refactoring with Confidence](refactoring-confidence.md)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) (what makes tests meaningful)
- Reference: [Is 70%, 80%, 90%, or 100% Coverage Good Enough?](https://www.qt.io/quality-assurance/blog/is-70-80-90-or-100-code-coverage-good-enough)
- Reference: [Test Coverage Guide 2025](https://www.devzery.com/post/test-coverage-guide-expert-strategies-improve-software-quality)
