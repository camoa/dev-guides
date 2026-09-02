---
description: "E2E testing — when and how to test critical user journeys through a real browser, and why to keep the suite small."
tldr: "E2E tests verify complete user journeys through a real browser — use them sparingly for critical paths only. E2E tests are 10–100x slower than integration tests; a 500-test suite can take 30+ minutes. Use data-testid selectors and never test logic variants in E2E."
---

# E2E Testing Concepts

## When to Use

> When you need to verify that a complete user journey works correctly through a real browser, real JavaScript execution, and real application stack. E2E tests are the most expensive tests to write, run, and maintain — use them sparingly, only for critical journeys where no cheaper test gives adequate confidence.

## What E2E Tests Are For

E2E tests verify the **integrated system from the user's perspective**:
- Real browser (Chromium, Firefox, WebKit) executes JavaScript
- Real network requests hit a real (or realistic) server
- Real CSS, rendering, layout, and interaction events occur
- Client-side behavior (form validation, modals, AJAX updates) is exercised

This is the only layer that catches:
- CSS/JS conflicts that break interactive behavior
- Network request failures that only appear in a real browser context
- Client-side routing errors in SPAs
- Cross-browser rendering or event handling differences
- Third-party script interference

## The Cost of E2E Tests

E2E tests are 10–100× slower than integration tests. Each test typically:
- Launches a browser process
- Navigates to a URL (network + render)
- Interacts with DOM elements (potentially with timing dependencies)
- Can be flaky due to animation, network jitter, timing, or state pollution

An E2E suite with 500 tests can take 30+ minutes to run, which pushes developers to skip it. **Keep E2E tests few. Cover critical paths only.**

## What to Cover with E2E Tests

Cover in E2E:
- The most critical user journeys (sign-up, log-in, purchase, content creation)
- Flows that require JavaScript interaction (AJAX forms, rich text editors, drag-and-drop)
- Critical integration with third-party scripts (analytics, payment widgets)
- Smoke tests that verify the app is alive after deployment

Do NOT cover in E2E:
- Logic variants and edge cases (test those with unit tests)
- Every page in the site (smoke a representative sample)
- Things already covered by integration tests
- Error states that require mocking (flaky to induce in E2E)

## Pattern

```javascript
// Playwright E2E: critical user journey
// One test per journey; no logic variants here

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

Keep E2E tests declarative and high-level. If you find yourself testing logic details in E2E, move those cases down the stack.

## Common Mistakes

- Using E2E as the primary test type → Enormously expensive suite, slow CI, high flakiness, low maintainability
- Testing every edge case in E2E → These belong in unit/integration; E2E verifies the happy path works end-to-end
- No test isolation → Tests share user accounts, browser cookies, or database state; one failure cascades
- Brittle selectors (CSS class names, positional selectors) → Use `data-testid` attributes or semantic role + label queries for stability
- Not running E2E in CI with the same environment as production → Catches a different set of bugs than local runs

## See Also

- ← Previous: [Functional Testing Concepts](functional-testing-concepts.md) | Next: [Visual Regression Concepts](visual-regression-concepts.md) →
- Related: [testing/playwright](https://camoa.github.io/dev-guides/testing/playwright/) — how to write Playwright E2E tests
- Related: [testing/atk](https://camoa.github.io/dev-guides/testing/atk/) — Drupal E2E catalog (ATK)
- Reference: Playwright documentation, [Testing Best Practices](https://playwright.dev/docs/best-practices)
