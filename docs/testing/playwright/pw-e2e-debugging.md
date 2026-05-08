---
description: Investigate Playwright test failures and flake with UI Mode, Trace Viewer, Inspector, page.pause(), and Codegen.
tldr: Start with UI Mode (npx playwright test --ui) — it caches setup, has a locator picker, and shows DOM snapshots per action. Set trace:'on-first-retry' in CI config so the first lean run is fast and the retry captures the smoking gun cheaply.
---

# Debugging

## When to Use

> Use UI Mode for local debugging — it's the fastest feedback loop. Use Trace Viewer (`trace: 'on-first-retry'`) for CI failure investigation. Use Inspector or `page.pause()` for inline step-through.

## Decision

| Tool | When |
|---|---|
| **UI Mode** (`--ui`) | Local debugging — start here always |
| **Trace Viewer** (`show-trace trace.zip`) | CI failure investigation |
| **Inspector** (`--debug` / `PWDEBUG=1`) | Step-through debugging of a single test |
| **`page.pause()`** | Inline breakpoint inside a test |
| **Codegen** | Bootstrapping a new test, discovering the right locator |

## Pattern

```bash
# UI Mode — interactive runner with DOM snapshots and locator picker
npx playwright test --ui

# Trace Viewer — open a trace archive from CI
npx playwright show-trace trace.zip

# Inspector — step/play/pause controls
npx playwright test login.spec.ts --debug
PWDEBUG=1 npx playwright test login.spec.ts
```

### Trace config (playwright.config.ts)

```ts
use: {
  trace: 'on-first-retry',       // recommended CI default
  video: 'retain-on-failure',
  screenshot: 'only-on-failure',
}
```

Trace modes: `'on'` (dev only — heavy), `'on-first-retry'` (CI default), `'retain-on-failure'`, `'off'`.

### Inline breakpoint

```ts
test('debug me', async ({ page }) => {
  await page.goto('/');
  await page.pause(); // Inspector opens here when run with --debug
});
```

### Codegen

```bash
npx playwright codegen https://example.com
npx playwright codegen --browser=firefox
npx playwright codegen --save-har=tests/.fixtures/orders.har https://example.com
```

Codegen records interactions and emits Playwright code with recommended locators. Use as starting-point quality — refactor into Page Objects or fixtures.

### VS Code extension

The official `Playwright Test for VSCode` extension adds run/debug gutters, watch mode, locator picker integrated with editor, one-click trace viewing, and record-new-test action.

## Common Mistakes

- **Wrong**: Skipping UI Mode — learn it first; it's friction-free
- **Wrong**: `trace: 'on'` in CI — gigabytes of trace data. **Right**: `'on-first-retry'`
- **Wrong**: Unzipping `trace.zip` before opening — viewer expects the archive intact

## See Also

- [Test Organization](pw-e2e-test-organization.md) — `test.step()` for collapsible trace sections
- [Anti-Patterns](pw-e2e-anti-patterns.md) — ranked list of flake causes
- Reference: [Playwright Debugging](https://playwright.dev/docs/debug)
