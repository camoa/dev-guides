---
description: "Intercept HTTP requests with page.route() — fulfill, abort, continue, fallback — and HAR record/replay for deterministic third-party calls."
tldr: "Use page.route() with fulfill to return canned responses for third-party dependencies and error states; use abort to silence analytics. Never mock the endpoint that is the subject of the test. Always await route handler setup before the action that triggers the request."
---

# Network Mocking

## When to Use

> Intercepting HTTP requests for determinism, error-state testing, or speed.

## Pattern: URL Patterns

| Pattern | Example | Notes |
|---|---|---|
| Glob | `'**/api/users/*'` | Default. `**` matches across slashes; `*` does not |
| RegExp | `/\/api\/users\/\d+/` | When glob isn't expressive enough |
| Function | `url => url.pathname.startsWith('/api/')` | Most flexible |

Watch the protocol/host: `'**/api/users'` matches both your host and third-parties. Anchor as needed.

## Pattern: The Four Route Handlers

```ts
// 1. fulfill — return a canned response
await page.route('**/api/orders', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, total: 10 }]),
    headers: { 'X-Mocked': 'true' },
  });
});

// 2. abort — fail the request
await page.route('**/analytics.js', route => route.abort());

// 3. continue — pass through, optionally with overrides
await page.route('**/api/**', async route => {
  const headers = { ...route.request().headers(), 'X-Test': 'true' };
  await route.continue({ headers });
});

// 4. fallback — let the next matching handler decide (handler chain)
await page.route('**/*', route => route.fallback());
```

`route.continue()` with no args = "do nothing, real network proceeds." Useful as a logging last-resort handler.

## Decision: When to Mock

| Mock when | Don't mock when |
|---|---|
| Third-party dependency (Stripe, Algolia, Mapbox) — outages cause flake | Auth flows — verify real session behavior |
| Reproducing error states (500, 429, malformed JSON) the backend can't reliably produce | Database writes you intend to assert on later |
| Slow APIs that aren't the subject of the test | The exact thing under test (don't mock `/api/orders` in a "place an order" test) |
| Determinism for VR (clock, currency rates) | First-run smoke tests — let real wiring break loudly |

## Pattern: HAR Record/Replay

```bash
# Record once
npx playwright codegen --save-har=tests/.fixtures/orders.har https://example.com
```

```ts
// Replay
await context.routeFromHAR('tests/.fixtures/orders.har', {
  url: '**/api/**',
  update: false,        // true = re-record on this run
  notFound: 'fallback', // or 'abort'
});
```

HAR matches URL + method + (for POST) body strictly. Useful when:
- the third-party is unstable
- you want byte-exact replay across CI runs
- you need to test against an API you can't yet bring up locally

## Common Mistakes

- **Globbing too broadly** — `'**/*'` blocks essential CSS/JS; scope handlers
- **Mocking the thing under test** — defeats the purpose
- **Forgetting to `await` the route handler setup** — race; the test starts before the handler is registered

## See Also

- [API Testing](pw-e2e-api-testing.md) — using the `request` fixture for API-only tests
- [CI Patterns](pw-e2e-ci-patterns.md) — combining mocks with sharding for deterministic CI
- Reference: [Playwright Network](https://playwright.dev/docs/network)
