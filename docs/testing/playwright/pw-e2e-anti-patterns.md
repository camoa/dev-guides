---
description: "Ranked list of Playwright E2E anti-patterns that cause flake or wasted CI minutes — with the correct pattern for each."
tldr: "The top three flake causes are waitForTimeout as the default wait, tests that depend on each other's state, and brittle CSS selectors instead of role/label/test-id. Replace each with web-first assertions, fixture-based state isolation, and getByRole/getByLabel."
---

# Anti-Patterns

## Decision

Ranked by how often they cause flake or wasted CI minutes:

1. **`page.waitForTimeout(2000)` as the default wait** — always wrong outside debugging. Replace with web-first assertion or `waitForResponse`
2. **Tests that depend on each other's state** — a test that only passes when the previous one ran is a bug. Each test creates its own state and cleans up. `test.describe.serial` is a smell
3. **Brittle CSS selectors instead of role/label/test-id** — `.btn.btn-primary.mt-3 > span:nth-child(2)` breaks on the next theme refactor
4. **Missing `await` on async calls** — `page.click(...)` returns a Promise; without `await`, the next line races. Turn on `eslint-plugin-playwright`
5. **Asserting implementation details** — `await expect(page.locator('.has-loaded')).toBeVisible()` ties to CSS-class side effect. Prefer user-visible: `await expect(page.getByText('5 results')).toBeVisible()`
6. **Test files >500 lines / mega-test asserting 20 things** — split per journey; use `test.step()` to keep readable
7. **`expect(true).toBe(false)` for sad-path** — use `throw new Error('Unexpected branch')` or `test.fail()`
8. **Overusing `page.evaluate()`** — bypasses auto-wait, breaks trace viewer's locator picker, Selenium-porting tell. Most calls have a Playwright API
9. **Using `isVisible()` / `textContent()` for assertions** — return immediately, no auto-retry. Always `expect(locator)`
10. **Disabling `fullyParallel` to "stabilize"** — hides flake; right answer is locator/auth/state isolation
11. **Committing `playwright/.auth/*.json`** — leaks session cookies; gitignore
12. **Trace viewer only for failures** — open them on slow CI runs to find race conditions in green tests
13. **`.first()` instead of `.filter()`** — hides "two elements match" bugs. Pair `.toHaveCount(1)` if uniqueness matters
14. **Mixing VR (`toHaveScreenshot`) and functional E2E in the same test** — different stability requirements; keep separate

## See Also

- [Assertions](pw-e2e-assertions.md) — correct auto-retry usage
- [Locators](pw-e2e-locators.md) — resilient locator priority order
- [CI Patterns](pw-e2e-ci-patterns.md) — `forbidOnly`, retries, artifact strategy
- [Debugging](pw-e2e-debugging.md) — finding the root cause of flake
