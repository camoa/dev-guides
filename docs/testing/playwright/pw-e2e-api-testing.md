---
description: Test HTTP APIs with the request fixture, share cookies between API and browser contexts, and use the API+UI hybrid pattern for fast deterministic E2E.
tldr: "The request fixture shares the browser context's cookie jar — use it to log in via API then drive UI as an authenticated user. The killer pattern: create state via JSON:API (fast), drive UI for the feature under test, verify via API (authoritative)."
---

# API Testing

## When to Use

> Use the `request` fixture for HTTP contract tests and for setting up state via API before driving UI. Use the API+UI hybrid when you need both deterministic state and user-journey coverage.

## Pattern: the `request` fixture

```ts
test('order API', async ({ request }) => {
  const get = await request.get('/api/orders/42');
  expect(get.ok()).toBeTruthy();          // 200–299
  expect(get.status()).toBe(200);
  expect(get.headers()['content-type']).toContain('application/json');
  const body = await get.json();
  expect(body.total).toBe(123.45);

  const post = await request.post('/api/orders', {
    data: { items: [{ sku: 'X', qty: 2 }] }, // auto-serializes to JSON
    headers: { Authorization: 'Bearer …' },
  });
  await expect(post).toBeOK(); // web-first variant

  await request.put('/api/orders/42', { data: { status: 'paid' } });
  await request.delete('/api/orders/42');

  // Multipart
  await request.post('/api/upload', {
    multipart: {
      file: { name: 'a.png', mimeType: 'image/png', buffer: Buffer.from('...') },
      caption: 'Hello',
    },
  });
});
```

`request` reads `baseURL`, `extraHTTPHeaders`, `httpCredentials`, `ignoreHTTPSErrors`, and `proxy` from `use:` — same knobs as the browser context.

## Decision

| Test value | Approach |
|---|---|
| HTTP contract (status, JSON shape, headers) | Pure API — no browser; 10–100× faster |
| User journey (forms, JS-rendered components, navigation) | UI-only E2E |
| Both: verify a feature end-to-end with deterministic state | **API + UI hybrid** |

## Pattern

```ts
// Basic request fixture usage
test('order API', async ({ request }) => {
  const get = await request.get('/api/orders/42');
  await expect(get).toBeOK(); // 200–299
  expect(get.status()).toBe(200);
  const body = await get.json();
  expect(body.total).toBe(123.45);

  await request.post('/api/orders', {
    data: { items: [{ sku: 'X', qty: 2 }] }, // auto-serializes to JSON
    headers: { Authorization: 'Bearer …' },
  });
});
```

### Cookie sharing between API and UI

```ts
test('login via API, drive UI as authed user', async ({ request, page }) => {
  // Login via API — Set-Cookie ends up in the shared jar
  const res = await request.post('/user/login?_format=json', {
    data: { name: 'admin', pass: 'admin' },
  });
  await expect(res).toBeOK();

  // page is now authenticated
  await page.goto('/admin');
  await expect(page.getByRole('heading', { name: 'Administration' })).toBeVisible();
});
```

### API + UI hybrid (the killer pattern)

```ts
test('publishing a node updates JSON:API', async ({ request, page }) => {
  // 1. Set up state via API (fast)
  const created = await request.post('/jsonapi/node/article', { /* ... */ });
  const nuid = (await created.json()).data.id;

  // 2. Drive UI for the actual feature under test
  await page.goto(`/node/${nuid}/edit`);
  await page.getByLabel('Published').check();
  await page.getByRole('button', { name: 'Save' }).click();

  // 3. Verify via API (cheap, deterministic)
  const verify = await request.get(`/jsonapi/node/article/${nuid}`);
  const body = await verify.json();
  expect(body.data.attributes.status).toBe(true);
});
```

## Common Mistakes

- **Wrong**: Using UI for state setup that could be done via API — slow tests
- **Wrong**: Asserting only via UI when API verification would be more authoritative
- **Wrong**: Spinning up `request` for every assertion instead of using the shared fixture

## See Also

- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — JSON:API + UI hybrid applied to Drupal entity CRUD
- [Network Mocking](pw-e2e-network-mocking.md) — intercepting API calls for determinism
- Reference: [Playwright API Testing](https://playwright.dev/docs/api-testing)
