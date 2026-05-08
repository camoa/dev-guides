---
description: Use web-first assertions correctly — auto-retry semantics, locator vs page assertions, soft assertions, polling, and negation.
tldr: Always use expect(locator) — not isVisible() or textContent() — because only expect() auto-retries until the condition holds or expect.timeout elapses. Never use waitForTimeout(); replace with a web-first assertion or expect.poll() for conditions outside the DOM.
---

# Web-First Assertions

## When to Use

> Use `expect(locator)` for all E2E assertions — it auto-retries until either the condition holds or `expect.timeout` (default 5000ms) elapses. Use `expect.poll()` for conditions outside the DOM (network state, external service).

## Decision

| Assertion | Passes when |
|---|---|
| `toBeVisible()` | Element attached and non-empty bounding box, not `display:none`/`visibility:hidden` |
| `toBeHidden()` | Element detached or invisible |
| `toBeAttached()` | Element in the DOM (may be invisible) — for elements that exist before they animate in |
| `toBeEnabled()` / `toBeDisabled()` | Element's enabled state |
| `toBeChecked({ checked: false })` | Checkbox/radio state |
| `toBeFocused()` | Element is `document.activeElement` |
| `toHaveText('exact')` / `toHaveText(/regex/)` | Text content — array form asserts multiple elements in order |
| `toContainText('substr')` | Substring match — most common in real tests |
| `toHaveValue('foo')` | Input / select value |
| `toHaveAttribute('name', 'value')` | DOM attribute |
| `toHaveCount(n)` | Number of matched elements |
| `toHaveCSS('background-color', 'rgb(0,0,0)')` | Computed style |
| `toHaveRole('button')` | Accessibility role (since 1.44) |
| `expect(page).toHaveURL(/foo$/)` | Auto-retries until URL matches |
| `expect(page).toHaveTitle('Welcome')` | Auto-retries until `<title>` matches |
| `expect(response).toBeOK()` | HTTP status 200–299 |

## Pattern

```ts
// Standard web-first assertion
await expect(page.getByRole('heading')).toHaveText('Welcome');

// Negation — every matcher is negatable
await expect(page.getByText('Loading...')).not.toBeVisible();

// Soft assertion — records failure but continues test
await expect.soft(page.getByRole('heading')).toHaveText('Welcome');
await expect.soft(page.getByRole('navigation')).toBeVisible();

// Per-test timeout override
const slowExpect = expect.configure({ timeout: 30_000 });
await slowExpect(page.getByText('Long-running job complete')).toBeVisible();
```

### Generic polling

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

// Block polling — for async chains (queue worker, search reindex, cron)
await expect(async () => {
  const response = await page.request.get('/api/orders');
  expect(response.status()).toBe(200);
  expect((await response.json()).count).toBeGreaterThan(0);
}).toPass({ timeout: 30_000 });
```

## Common Mistakes

- **Wrong**: `await locator.isVisible()` for assertions — returns immediately, no auto-retry; flake source. **Right**: `await expect(locator).toBeVisible()`
- **Wrong**: `waitForTimeout(2000)` — bypasses auto-retry; replace with `expect()` or `waitForResponse`
- **Wrong**: Bumping `expect.timeout` to silence flake — masks real bugs. **Right**: Investigate the underlying race
- **Wrong**: `toHaveScreenshot()` in functional E2E tests — that's VR, covered in the VR guide. Keep them separate

## See Also

- [Locators](pw-e2e-locators.md) — how to target elements
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drupal-specific waits (Big Pipe, AJAX, search reindex)
- Reference: [Playwright Assertions](https://playwright.dev/docs/test-assertions)
