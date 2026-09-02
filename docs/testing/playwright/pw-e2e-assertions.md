---
description: "Use web-first assertions correctly — auto-retry semantics, locator vs page assertions, soft assertions, polling, and negation."
tldr: "Always use expect(locator) — not isVisible() or textContent() — because only expect() auto-retries until the condition holds or expect.timeout elapses. Never use waitForTimeout(); replace with a web-first assertion or expect.poll() for conditions outside the DOM."
---

# Web-First Assertions

## When to Use

> Asserting state in E2E tests. `expect()` against a Locator/Page **auto-retries** until either the condition holds or `expect.timeout` (default 5000ms) elapses.

## Decision: Locator Assertions — State

| Assertion | Passes when |
|---|---|
| `toBeVisible()` | Element attached **and** non-empty bounding box, not `display:none`/`visibility:hidden` |
| `toBeHidden()` | Element detached or invisible |
| `toBeAttached()` | Element in the DOM (may be invisible) — for elements that exist before they animate in |
| `toBeEnabled()` / `toBeDisabled()` | Element's enabled state |
| `toBeEditable()` | Element enabled and not `readonly` |
| `toBeChecked({ checked: false })` | Checkbox/radio state |
| `toBeFocused()` | Element is `document.activeElement` |
| `toBeEmpty()` | No text and no element children |
| `toBeInViewport({ ratio: 0.5 })` | Intersection ratio ≥ given value |

## Decision: Locator Assertions — Content / Attributes

| Assertion | Notes |
|---|---|
| `toHaveText('exact')` / `toHaveText(/regex/)` / `toHaveText(['a','b'])` | Array form asserts against multiple matched elements in order |
| `toContainText('substr')` | Substring match — most common in real tests |
| `toHaveValue('foo')` / `toHaveValues(['a','b'])` | For inputs / `<select multiple>` |
| `toHaveAttribute('name', 'value' \| /regex/)` | |
| `toHaveClass('foo')` / `toHaveClass(/active/)` | |
| `toHaveCount(n)` | Number of matched elements |
| `toHaveCSS('background-color', 'rgb(0, 0, 0)')` | Computed style |
| `toHaveId('myid')` | |
| `toHaveJSProperty('checked', true)` | JS property the DOM doesn't expose as attribute |
| `toHaveRole('button')` | Accessibility role (since 1.44) |
| `toHaveScreenshot(...)` | **VR — covered in the VR guide. Don't use in functional E2E** |

## Decision: Page Assertions

| Assertion | Notes |
|---|---|
| `expect(page).toHaveURL('https://example.com/foo')` / `(/foo$/)` | Auto-retries until URL matches |
| `expect(page).toHaveTitle('Welcome')` / `(/regex/)` | Auto-retries until `<title>` matches |

## Decision: APIResponse Assertions

| Assertion | Notes |
|---|---|
| `expect(response).toBeOK()` | Status in 200–299 range |

## Auto-Retry Semantics

- Each assertion polls the DOM/network/page state
- **Default global timeout is 5000ms**, configurable via `expect.timeout` or per-call `{ timeout: 10_000 }`
- Polling interval increases backoff-style; you don't control it directly
- **Only `expect()` (not `isVisible()`/`textContent()`) auto-retries** — calling `await locator.isVisible()` returns immediately and is a common flake source

## Pattern: Generic Polling

For conditions outside the DOM (network state, external service):

```ts
// Poll a function until it returns the expected value
await expect.poll(async () => {
  const res = await request.get('/api/health');
  return res.status();
}, {
  message: 'Health endpoint should become 200',
  intervals: [1_000, 2_000, 5_000],
  timeout: 30_000,
}).toBe(200);

// Run a block until it passes (assertions inside re-evaluate)
await expect(async () => {
  const response = await page.request.get('/api/orders');
  expect(response.status()).toBe(200);
  expect((await response.json()).count).toBeGreaterThan(0);
}).toPass({ timeout: 30_000 });
```

`toPass` is the right tool when an action triggers an asynchronous chain (queue worker, search reindex, Drupal cron) and you must wait for eventually-consistent state.

## Pattern: Soft Assertions

`expect.soft()` records a failure but doesn't stop the test — useful for triage:

```ts
await expect.soft(page.getByRole('heading')).toHaveText('Welcome');
await expect.soft(page.getByRole('navigation')).toBeVisible();
await expect.soft(page.getByRole('contentinfo')).toBeVisible();
// Test continues even if heading is wrong; final result still fails
```

Don't soft-assert the action itself: `.soft(button).toBeEnabled()` followed by `.click()` will throw on a disabled button anyway.

## Pattern: Negation

Every matcher is negatable:

```ts
await expect(page.getByText('Loading...')).not.toBeVisible();
await expect(page.getByRole('alert')).not.toContainText('Error');
```

Note: `.not.toBeVisible()` differs from `.toBeHidden()` — the former passes for both detached and hidden; `toBeHidden` is "still attached but invisible."

## Pattern: Per-Test Timeout Override

```ts
const slowExpect = expect.configure({ timeout: 30_000 });
await slowExpect(page.getByText('Long-running job complete')).toBeVisible();
```

## Common Mistakes

- **Using `isVisible()`/`textContent()` for assertions** — no auto-retry; the test passes when it shouldn't, or fails because the element hasn't rendered yet. Always use `expect(locator)`
- **Hardcoded `waitForTimeout(2000)`** — bypasses auto-retry; replace with `expect()` or `waitForResponse`
- **Bumping `expect.timeout` to silence flake** — masks real bugs; investigate the underlying race

## See Also

- [Locators](pw-e2e-locators.md) — how to target elements
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drupal-specific waits (Big Pipe, AJAX, search reindex)
- Reference: [Playwright Assertions](https://playwright.dev/docs/test-assertions)
