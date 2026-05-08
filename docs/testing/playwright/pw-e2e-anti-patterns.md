---
description: Ranked list of Playwright E2E anti-patterns that cause flake or wasted CI minutes — with the correct pattern for each.
tldr: The top three flake causes are waitForTimeout as the default wait, tests that depend on each other's state, and brittle CSS selectors instead of role/label/test-id. Replace each with web-first assertions, fixture-based state isolation, and getByRole/getByLabel.
---

# Anti-Patterns

## When to Use

> Reference this list when a test is flaky, slow, or unexpectedly failing — most root causes trace to one of these patterns.

## Decision

Ranked by how often they cause flake or wasted CI minutes:

| Rank | Anti-Pattern | Fix |
|---|---|---|
| 1 | `page.waitForTimeout(2000)` as the default wait | Replace with web-first assertion or `waitForResponse` |
| 2 | Tests that depend on each other's state | Each test creates its own state; `test.describe.serial` is a smell |
| 3 | Brittle CSS selectors (`.btn.btn-primary.mt-3 > span:nth-child(2)`) | Use `getByRole`, `getByLabel`, or `getByTestId` |
| 4 | Missing `await` on async calls | Turn on `eslint-plugin-playwright` |
| 5 | Asserting implementation details (`.has-loaded` CSS class) | Prefer user-visible: `getByText('5 results')` |
| 6 | Test files >500 lines / mega-test asserting 20 things | Split per journey; use `test.step()` |
| 7 | `expect(true).toBe(false)` for sad-path | Use `throw new Error('Unexpected branch')` or `test.fail()` |
| 8 | Overusing `page.evaluate()` | Most calls have a Playwright API that preserves auto-wait and trace |
| 9 | `isVisible()` / `textContent()` for assertions | Always `expect(locator)` — these return immediately, no auto-retry |
| 10 | Disabling `fullyParallel` to "stabilize" | Hides flake; fix locator/auth/state isolation instead |
| 11 | Committing `playwright/.auth/*.json` | Leaks session cookies; gitignore |
| 12 | Trace Viewer only for failures | Open them on slow CI runs to find race conditions in green tests |
| 13 | `.first()` instead of `.filter()` | Hides "two elements match" bugs; pair with `.toHaveCount(1)` |
| 14 | Mixing VR (`toHaveScreenshot`) and functional E2E in the same test | Different stability requirements; keep separate |

## Common Mistakes

- **Wrong**: Bumping `expect.timeout` to silence flake — masks real bugs. **Right**: Investigate the underlying race condition
- **Wrong**: `PWDEBUG=1` left on in CI — slows suite dramatically. **Right**: Only set in local dev
- **Wrong**: `test.only` committed — CI doesn't catch it without `forbidOnly: true` in config

## See Also

- [Assertions](pw-e2e-assertions.md) — correct auto-retry usage
- [Locators](pw-e2e-locators.md) — resilient locator priority order
- [CI Patterns](pw-e2e-ci-patterns.md) — `forbidOnly`, retries, artifact strategy
- [Debugging](pw-e2e-debugging.md) — finding the root cause of flake
