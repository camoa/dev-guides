---
description: Intercept HTTP requests with page.route() — fulfill, abort, continue, fallback — and HAR record/replay for deterministic third-party calls.
tldr: Use page.route() with fulfill to return canned responses for third-party dependencies and error states; use abort to silence analytics. Never mock the endpoint that is the subject of the test. Always await route handler setup before the action that triggers the request.
---

# Network Mocking

## When to Use

> Use network mocking for third-party dependencies (Stripe, Algolia, Mapbox), error-state reproduction (500, 429), and slow APIs that aren't the subject of the test. Don't mock the exact thing under test.

## Decision

| Mock when | Don't mock when |
|---|---|
| Third-party dependency — outages cause flake | Auth flows — verify real session behavior |
| Reproducing error states (500, 429, malformed JSON) the backend can't reliably produce | Database writes you intend to assert on later |
| Slow APIs that aren't the subject of the test | The exact endpoint under test |
| Determinism for VR (clock, currency rates) | First-run smoke tests — let real wiring break loudly |

## Pattern

```ts
// 1. fulfill — return a canned response
await page.route('**/api/orders', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, total: 10 }]),
  });
});

// 2. abort — fail the request (e.g. silence analytics)
await page.route('**/analytics.js', route => route.abort());

// 3. continue — pass through with header overrides
await page.route('**/api/**', async route => {
  const headers = { ...route.request().headers(), 'X-Test': 'true' };
  await route.continue({ headers });
});

// 4. fallback — let the next matching handler decide
await page.route('**/*', route => route.fallback());
```

### URL pattern types

| Pattern | Example |
|---|---|
| Glob | `'**/api/users/*'` — `**` matches across slashes; `*` does not |
| RegExp | `/\/api\/users\/\d+/` |
| Function | `url => url.pathname.startsWith('/api/')` |

### HAR record/replay

```bash
# Record once
npx playwright codegen --save-har=tests/.fixtures/orders.har https://example.com
```

```ts
// Replay
await context.routeFromHAR('tests/.fixtures/orders.har', {
  url: '**/api/**',
  update: false,        // true = re-record on this run
  notFound: 'fallback',
});
```

## Common Mistakes

- **Wrong**: Globbing too broadly — `'**/*'` blocks essential CSS/JS. **Right**: Scope handlers to specific URL patterns
- **Wrong**: Mocking the thing under test — defeats the purpose
- **Wrong**: Not `await`ing the route handler setup — race; the test starts before the handler is registered

## See Also

- [API Testing](pw-e2e-api-testing.md) — using the `request` fixture for API-only tests
- [CI Patterns](pw-e2e-ci-patterns.md) — combining mocks with sharding for deterministic CI
- Reference: [Playwright Network](https://playwright.dev/docs/network)
