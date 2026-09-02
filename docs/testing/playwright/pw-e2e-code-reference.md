---
description: "Quick reference for Playwright E2E APIs, config keys, and CLI commands."
tldr: "Quick lookup for getByRole/getByLabel/getByTestId locators, expect() assertions, test.extend fixtures, page.route mocking, request fixture, and the sharding/debugging CLI commands."
---

# Code Reference

## Key APIs

| API | Use |
|---|---|
| `page.getByRole(role, opts)` | Primary locator strategy |
| `page.getByLabel(text)` | Form fields |
| `page.getByTestId(id)` | Test contract via `data-testid` (or configured attribute) |
| `page.locator(selector)` | CSS / XPath fallback |
| `locator.filter({ hasText, has, hasNot, hasNotText })` | Narrowing |
| `expect(locator).toBeVisible()` etc. | Web-first assertions |
| `expect.poll(fn).toBe(value)` | Generic polling |
| `expect(async () => ...).toPass()` | Block polling |
| `test.extend({...})` | Custom fixtures |
| `test.use({ storageState })` | Auth replay |
| `page.route(url, handler)` | Network mocking |
| `request.get/post/...` | API testing |
| `page.pause()` | Inline debugger |
| `test.step('label', async () => ...)` | Action grouping |

## Config Keys (E2E-Specific)

| Key | Default | Purpose |
|---|---|---|
| `expect.timeout` | 5000ms | Web-first assertion polling budget |
| `actionTimeout` | 0 | Per-action timeout; falls back to test timeout |
| `navigationTimeout` | 0 | Per-navigation timeout |
| `testIdAttribute` | `data-testid` | What `getByTestId` reads |
| `retries` | 0 | Retries per test (use 2 in CI) |
| `fullyParallel` | false | Parallelize across all tests, not just files |
| `forbidOnly` | false | Error out if any `test.only` / `describe.only` reached the run — set `!!process.env.CI` |

## CLI

```bash
# Sharding
npx playwright test --shard=1/4

# Reports
npx playwright merge-reports --reporter=html ./all-blob-reports

# Debugging
npx playwright test --ui
npx playwright test --debug
PWDEBUG=1 npx playwright test
npx playwright codegen URL
npx playwright show-trace trace.zip
```

## See Also

- [Playwright for Visual Regression](../visual-regression/playwright/index.md) — setup, browser projects, viewport matrix, screenshot APIs, baseline files, stability controls, determinism, config walkthrough, CLI cheatsheet, programmatic API, Drupal/DDEV plumbing
- [Visual Regression Workflow](../visual-regression/workflow/index.md) — VR procedure
- [Pixelmatch Image Diff](../visual-regression/pixelmatch/index.md) — diff engine internals
- [Playwright HTML Report](../visual-regression/html-report/index.md) — triage UI for both VR and E2E failures
- [Automated Testing Kit (ATK)](../atk/index.md) — Drupal-specific test catalog using Playwright
- Reference: [Playwright Locators](https://playwright.dev/docs/locators)
- Reference: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- Reference: [Playwright Authentication](https://playwright.dev/docs/auth)
- Reference: [Playwright Network](https://playwright.dev/docs/network)
- Reference: [Playwright API Testing](https://playwright.dev/docs/api-testing)
