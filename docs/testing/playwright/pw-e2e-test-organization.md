---
description: Structure Playwright tests with describe blocks, hooks, tags, annotations, parameterization, and test.step for readable traces.
tldr: Use fullyParallel:true globally and reserve test.describe.serial only for genuine multi-step wizards where each step depends on the previous. Use test.step() aggressively in long tests — steps appear collapsibly in the HTML report and Trace Viewer, making triage dramatically faster.
---

# Test Organization

## When to Use

> Use `describe` to group related tests, `tags` for selective runs, `test.step()` to annotate long flows in the trace, and fixtures over hooks whenever the setup produces state.

## Decision

| Concurrency mode | When |
|---|---|
| `fullyParallel: true` (global default) | Independent tests — the normal case |
| `test.describe.serial` | Multi-step wizard where step N depends on step N-1 state |
| `test.describe.parallel` | Override parallel on a file that would otherwise be serial |

## Pattern

```ts
// Grouping
test.describe('checkout flow', () => { /* sequential within file by default */ });
test.describe.serial('multi-step wizard', () => { /* first failure skips rest; retries whole group */ });
test.describe.parallel('independent CRUD', () => { /* force parallel within file */ });
test.describe.skip('flaky vendor area, ticket #1234', () => { /* ... */ });
```

### Hooks

```ts
test.beforeAll(async ({ browser }) => { /* once per worker */ });
test.afterAll(async () => { /* once per worker */ });
test.beforeEach(async ({ page }) => { /* before every test */ });
test.afterEach(async ({ page }, testInfo) => { /* after every test */ });
```

### Skipping and conditional execution

```ts
test('only on chromium', async ({ browserName }) => {
  test.skip(browserName !== 'chromium', 'WebKit lacks feature X');
});
test.fixme('broken, see #4567', async () => { /* not executed, marked failing-known */ });
test.slow(); // multiplies timeouts by 3 for this test
```

### Tags and annotations

```ts
// Tags — for grep-based filtering
test('homepage smoke', { tag: ['@smoke', '@critical'] }, async ({ page }) => { /* ... */ });
// npx playwright test --grep @smoke

// Annotations — surface in HTML report
test('checkout', {
  annotation: [{ type: 'issue', description: 'https://jira/PROJ-123' }],
}, async ({ page }) => { /* ... */ });
```

### Parameterization

```ts
const roles = ['admin', 'editor', 'anonymous'];
for (const role of roles) {
  test.describe(`as ${role}`, () => {
    test.use({ storageState: `playwright/.auth/${role}.json` });
    test('can view homepage', async ({ page }) => { /* ... */ });
  });
}
```

### `test.step` — nesting actions in the trace

```ts
test('purchase', async ({ page }) => {
  await test.step('login', async () => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('a@b');
  });
  await test.step('add to cart', async () => { /* ... */ });
  await test.step('checkout', async () => { /* ... */ });
});
```

## Common Mistakes

- **Wrong**: `test.describe.serial` for "convenience" — hides test coupling. **Right**: Refactor to fixtures
- **Wrong**: `test.only` committed — CI doesn't catch it without `forbidOnly: true`
- **Wrong**: Test files >500 lines. **Right**: Split per user journey

## See Also

- [Fixtures](pw-e2e-fixtures.md) — typed, composable alternative to `beforeEach` for state
- [Debugging](pw-e2e-debugging.md) — `test.step` entries in Trace Viewer
- [CI Patterns](pw-e2e-ci-patterns.md) — `forbidOnly`, `fullyParallel`, retries config
