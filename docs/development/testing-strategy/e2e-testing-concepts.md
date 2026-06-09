---
description: E2E testing — when and how to test critical user journeys through a real browser, and why to keep the suite small.
tldr: E2E tests verify complete user journeys through a real browser — use them sparingly for critical paths only. E2E tests are 10–100x slower than integration tests; a 500-test suite can take 30+ minutes. Use data-testid selectors and never test logic variants in E2E.
---

# E2E Testing Concepts

## When to Use

> Use E2E tests for the most critical user journeys where no cheaper test gives adequate confidence. Do NOT use E2E as the primary test type — it is the most expensive layer and the last resort, not the first.

## Decision

| Cover in E2E | Do NOT cover in E2E |
|---|---|
| Critical user journeys (sign-up, log-in, purchase, content creation) | Logic variants and edge cases (unit tests) |
| Flows requiring JavaScript interaction (AJAX forms, rich editors, drag-and-drop) | Every page in the site (smoke a representative sample) |
| Critical third-party script integration (analytics, payment widgets) | Things already covered by integration tests |
| Smoke tests verifying the app is alive after deployment | Error states requiring mocking (flaky to induce in E2E) |

## Pattern

```javascript
// Playwright E2E: one test per critical journey — no logic variants
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products/widget');
  await page.click('[data-testid="add-to-cart"]');
  await page.goto('/cart');
  await page.click('[data-testid="checkout"]');
  await page.fill('[name="email"]', 'alice@example.com');
  await page.fill('[name="card"]', '4242424242424242');
  await page.click('[data-testid="pay"]');
  await expect(page.locator('[data-testid="confirmation"]')).toBeVisible();
});
```

Keep E2E tests declarative and high-level. If you find yourself testing logic details, move those cases down the stack.

## Common Mistakes

- **Wrong**: Using E2E as the primary test type → **Right**: Enormous suite, slow CI, high flakiness, low maintainability
- **Wrong**: Testing every edge case in E2E → **Right**: Edge cases belong in unit/integration; E2E verifies the happy path end-to-end
- **Wrong**: Tests share user accounts, cookies, or DB state → **Right**: Full test isolation; one failure must not cascade
- **Wrong**: CSS class names or positional selectors → **Right**: Use `data-testid` attributes or semantic role + label queries for stability
- **Wrong**: Not running E2E in CI with the same environment as production → **Right**: Must match local baseline capture conditions

## See Also

- [Functional Testing Concepts](functional-testing-concepts.md) | Next: [Visual Regression Concepts](visual-regression-concepts.md)
- Related: [testing/playwright](https://camoa.github.io/dev-guides/testing/playwright/) — how to write Playwright E2E tests
- Related: [testing/atk](https://camoa.github.io/dev-guides/testing/atk/) — Drupal E2E catalog (ATK)
- Reference: Playwright, [Testing Best Practices](https://playwright.dev/docs/best-practices)
