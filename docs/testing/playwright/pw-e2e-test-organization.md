---
description: "Structure Playwright tests with describe blocks, hooks, tags, annotations, parameterization, and test.step for readable traces."
tldr: "Use fullyParallel:true globally and reserve test.describe.serial only for genuine multi-step wizards where each step depends on the previous. Use test.step() aggressively in long tests — steps appear collapsibly in the HTML report and Trace Viewer, making triage dramatically faster."
---

# Test Organization

## When to Use

> Structuring describe blocks, hooks, tags, and parallelism.

## Pattern: Grouping and Concurrency

```ts
test.describe('checkout flow', () => {
  // tests share a describe scope; default = sequential within file
});

test.describe.serial('multi-step wizard', () => {
  // First failure skips the rest; retries the whole group as a unit
  // Use only when steps genuinely depend on each other
});

test.describe.parallel('independent CRUD', () => {
  // Tests run in parallel even within the same file
});

test.describe.skip('flaky vendor area, ticket #1234', () => { /* ... */ });
test.describe.fixme('todo, after launch', () => { /* ... */ });
test.describe.only('focus', () => { /* ... */ }); // dev-only; CI fails if .only leaks
```

Prefer `fullyParallel: true` in `playwright.config.ts` and `test.describe.serial` only for the genuine wizard case. Most "serial" usage is hidden test coupling — refactor to fixtures.

## Pattern: Hooks

```ts
test.beforeAll(async ({ browser }) => { /* once per worker */ });
test.afterAll(async () => { /* once per worker */ });
test.beforeEach(async ({ page }) => { /* before every test */ });
test.afterEach(async ({ page }, testInfo) => { /* after every test */ });
```

Prefer **fixtures over hooks** for anything that produces state a test consumes. Hooks are good for cross-cutting setup that doesn't return a value (seed time, register a global error listener).

## Pattern: Skipping and Conditional Execution

```ts
test('only on chromium', async ({ browserName }) => {
  test.skip(browserName !== 'chromium', 'WebKit lacks feature X');
});

test.fixme('broken, see #4567', async () => { /* not executed, marked failing-known */ });
test.fail('expected failure', async () => { /* fails if it passes */ });
test.slow(); // multiplies timeouts by 3 for this test
```

## Pattern: Tags

```ts
test('homepage smoke', { tag: ['@smoke', '@critical'] }, async ({ page }) => {
  /* ... */
});
```

```bash
npx playwright test --grep @smoke
npx playwright test --grep-invert @slow
```

## Pattern: Annotations (Richer Than Tags — Surface in HTML Report)

```ts
test('checkout', {
  annotation: [
    { type: 'issue', description: 'https://jira/PROJ-123' },
    { type: 'severity', description: 'critical' },
  ],
}, async ({ page }) => { /* ... */ });
```

## Pattern: Parameterization

```ts
const roles = ['admin', 'editor', 'anonymous'];
for (const role of roles) {
  test.describe(`as ${role}`, () => {
    test.use({ storageState: `playwright/.auth/${role}.json` });
    test('can view homepage', async ({ page }) => { /* ... */ });
  });
}
```

## Pattern: `test.step` — Nesting Actions in the Trace

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

Steps appear collapsibly in the HTML report and Trace Viewer. Use them aggressively in long tests; makes triage 10× faster.

## Common Mistakes

- **`test.describe.serial` for "convenience"** — hides test coupling; refactor to fixtures
- **`test.only` committed** — CI doesn't catch it without `forbidOnly: true`
- **Test files >500 lines** — split per user journey

## See Also

- [Fixtures](pw-e2e-fixtures.md) — typed, composable alternative to `beforeEach` for state
- [Debugging](pw-e2e-debugging.md) — `test.step` entries in Trace Viewer
- [CI Patterns](pw-e2e-ci-patterns.md) — `forbidOnly`, `fullyParallel`, retries config
