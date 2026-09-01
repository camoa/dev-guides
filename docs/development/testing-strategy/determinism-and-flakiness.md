---
description: Flaky test prevention — root causes of non-determinism, the clock injection pattern, async waiting, and how to quarantine and fix flakiness.
tldr: "A test suite with 5% flakiness has a 99.9% chance of at least one failure per run, training teams to ignore failures. Root causes: time/date, randomness, shared state, async timing, real network calls, and filesystem. Fix by injecting clock/random dependencies, isolating test state, and waiting for specific conditions rather than sleeping."
---

# Determinism and Flakiness

## When to Use

> Apply these patterns whenever a test passes sometimes and fails others, or when designing tests to prevent flakiness. A flaky test is worse than no test: it trains developers to ignore failures and erodes trust in the entire suite.

## Why Flakiness Is a First-Class Problem

A test suite with 5% flakiness at 200 tests has a roughly 99.9% chance of at least one failure on any given run, even when all code is correct. That means CI fails every run for reasons unrelated to code. Teams respond by:
- Re-running CI blindly until it passes
- Marking flaky tests as "expected failures" (so they never catch real bugs)
- Disabling the tests entirely

The cost of a flaky test exceeds the cost of deleting it.

## Quarantine vs. Fix

When you find a flaky test:
1. **Quarantine it immediately** — tag it as flaky, skip it in CI, open a ticket. Do not leave it breaking CI.
2. **Investigate the root cause** — look for the sources above; add logging to understand when/why it fails
3. **Fix the root cause** — do not simply increase timeouts or add retries
4. **Remove the quarantine** — once fixed, verify it passes 10+ consecutive runs before unquarantining

Retrying flaky tests in CI (`--retries=2`) is a temporary mitigation, not a fix. Each retry is wasted CI time and a lie that the test is reliable.

## Decision

| Source | Mechanism | Fix |
|---|---|---|
| Time/date | `new Date()`, `DateTime.now()` inside production code | Inject a clock dependency; stub it in tests |
| Random values | `Math.random()`, `uuid()`, random IDs | Inject a random source; seed it in tests |
| Test execution order | Test A modifies global state; Test B depends on it | Each test owns its own setup and teardown |
| Async/timing | `setTimeout`, polling, animation frames, debouncing | Wait for the condition explicitly; never sleep |
| Network | Real HTTP calls in tests | Stub or mock all network calls in unit/integration tests |
| File system | Tests create/modify files; cleanup fails | Use temp directories; clean up in teardown |
| Browser non-determinism | Animation, lazy loading, race conditions | Wait for stability signals; disable animations |

## Pattern

```python
# UNTESTABLE: clock hidden inside the function
def is_subscription_expired(subscription):
    return subscription.expires_at < datetime.now()

# TESTABLE: clock is injected
def is_subscription_expired(subscription, now=None):
    if now is None:
        now = datetime.now()
    return subscription.expires_at < now

def test_subscription_expired_when_past_expiry():
    sub = Subscription(expires_at=datetime(2020, 1, 1))
    assert is_subscription_expired(sub, now=datetime(2025, 6, 1)) is True
```

```javascript
// FLAKY: arbitrary sleep
await page.waitForTimeout(2000);

// CORRECT: wait for the specific condition your assertion depends on
await page.waitForSelector('[data-testid="results"]');
await expect(page.locator('.spinner')).toBeHidden();
await page.waitForLoadState('networkidle');
await expect(page.locator('[data-testid="count"]')).toHaveText('5');
```

**Quarantine workflow:** tag as flaky → skip in CI → open ticket → investigate root cause → fix → verify 10+ consecutive passes → unquarantine. Do not simply increase timeouts or add retries.

## Common Mistakes

- **Wrong**: `sleep` / `waitForTimeout` in E2E tests → **Right**: Wait for the specific condition the assertion depends on
- **Wrong**: Not cleaning up database state between tests → **Right**: Leftover records cause spurious failures depending on run order
- **Wrong**: Global mutable objects (`process.env` modifications, singletons) → **Right**: Always restore after each test
- **Wrong**: Ignoring flaky tests → **Right**: Must quarantine and fix; trains team to ignore all failures
- **Wrong**: Re-running CI until green without investigating → **Right**: Flakiness recurs; erodes confidence further

## See Also

- [Test Structure and Naming](test-structure-and-naming.md) | Next: [Coverage Philosophy](coverage-philosophy.md)
- Related: [testing/playwright](https://camoa.github.io/dev-guides/testing/playwright/) — Playwright-specific stability controls
- Reference: Google Testing Blog, [Flaky Tests](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
