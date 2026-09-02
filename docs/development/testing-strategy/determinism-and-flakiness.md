---
description: "Flaky test prevention — root causes of non-determinism, the clock injection pattern, async waiting, and how to quarantine and fix flakiness."
tldr: "A test suite with 5% flakiness has a 99.9% chance of at least one failure per run, training teams to ignore failures. Root causes: time/date, randomness, shared state, async timing, real network calls, and filesystem. Fix by injecting clock/random dependencies, isolating test state, and waiting for specific conditions rather than sleeping."
---

# Determinism and Flakiness

## When to Use

> When a test passes sometimes and fails others — or when you are designing tests to prevent this from happening. A flaky test is worse than no test: it trains developers to ignore failures and erodes trust in the entire suite.

## Why Flakiness Is a First-Class Problem

A test suite with 5% flakiness at 200 tests has a roughly 99.9% chance of at least one failure on any given run, even when all code is correct. That means CI fails every run for reasons unrelated to code. Teams respond by:
- Re-running CI blindly until it passes
- Marking flaky tests as "expected failures" (so they never catch real bugs)
- Disabling the tests entirely

The cost of a flaky test exceeds the cost of deleting it.

## Root Causes of Flakiness

| Source | Mechanism | Fix |
|---|---|---|
| **Time/date** | `new Date()`, `DateTime.now()` inside the code under test | Inject a clock dependency; stub it in tests |
| **Random values** | `Math.random()`, `uuid()`, random IDs | Inject a random source; seed it in tests |
| **Test execution order** | Test A modifies global state; Test B depends on that state | Each test owns its own setup and teardown; no shared mutable state |
| **Async/timing** | `setTimeout`, polling, animation frames, debouncing | Wait for the condition explicitly (await, polling assertion), never sleep |
| **Network** | Real HTTP calls in tests | Stub or mock all network calls in unit/integration tests |
| **File system** | Tests create/modify files; cleanup fails | Use temp directories; clean up in teardown (or use `afterEach`) |
| **Resource exhaustion** | Too many DB connections, file descriptors | Limit concurrency; ensure connections are closed |
| **Browser non-determinism (E2E)** | Animation, lazy loading, race conditions | Wait for stability signals; disable animations; use `networkidle` |

## The Clock Problem (Most Common)

Code that calls the system clock internally is fundamentally untestable for time-sensitive behavior. The fix is dependency injection:

```python
# UNTESTABLE: clock is hidden inside the function
def is_subscription_expired(subscription):
    return subscription.expires_at < datetime.now()

# TESTABLE: clock is injected
def is_subscription_expired(subscription, now=None):
    if now is None:
        now = datetime.now()
    return subscription.expires_at < now

# Test controls time
def test_subscription_expired_when_past_expiry():
    sub = Subscription(expires_at=datetime(2020, 1, 1))
    frozen_now = datetime(2025, 6, 1)
    assert is_subscription_expired(sub, now=frozen_now) is True
```

Libraries like `freezegun` (Python), `sinon.useFakeTimers` (JS), or `\DateTimeImmutable` injection (PHP) can freeze time at the test layer without modifying production code.

## Quarantine vs. Fix

When you find a flaky test:

1. **Quarantine it immediately** — tag it as flaky, skip it in CI, open a ticket. Do not leave it breaking CI.
2. **Investigate the root cause** — look for the sources above; add logging to understand when/why it fails
3. **Fix the root cause** — do not simply increase timeouts or add retries
4. **Remove the quarantine** — once fixed, verify it passes 10+ consecutive runs before unquarantining

Retrying flaky tests in CI (`--retries=2`) is a temporary mitigation, not a fix. Each retry is wasted CI time and a lie that the test is reliable.

## Async Waiting Patterns

The most common E2E flakiness source is improper waiting:

```javascript
// FLAKY: arbitrary sleep
await page.waitForTimeout(2000); // hopes 2s is enough; sometimes isn't

// CORRECT: wait for the condition you actually need
await page.waitForSelector('[data-testid="results"]');          // element appears
await expect(page.locator('.spinner')).toBeHidden();             // loader gone
await page.waitForLoadState('networkidle');                      // no pending XHRs
await expect(page.locator('[data-testid="count"]')).toHaveText('5'); // exact state
```

Always wait for **the specific condition your assertion depends on**, not a fixed duration.

## Common Mistakes

- Using `sleep` / `waitForTimeout` in E2E tests → Introduces arbitrary delays; will be too short sometimes and always too slow
- Not cleaning up database state between tests → Leftover records cause assertions to fail spuriously depending on run order
- Global mutable objects in tests → `process.env` modifications, singleton state; always restore after each test
- Ignoring flaky tests → Trains the team to ignore all failures; must quarantine and fix
- Re-running CI until green without investigating → The flakiness will recur and erode confidence further

## See Also

- ← Previous: [Test Structure and Naming](test-structure-and-naming.md) | Next: [Coverage Philosophy](coverage-philosophy.md) →
- Related: [testing/playwright](https://camoa.github.io/dev-guides/testing/playwright/) — Playwright-specific stability controls
- Reference: Google Testing Blog, [Flaky Tests](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
