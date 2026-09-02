---
description: "Investigate Playwright test failures and flake with UI Mode, Trace Viewer, Inspector, page.pause(), and Codegen."
tldr: "Start with UI Mode (npx playwright test --ui) — it caches setup, has a locator picker, and shows DOM snapshots per action. Set trace:'on-first-retry' in CI config so the first lean run is fast and the retry captures the smoking gun cheaply."
---

# Debugging

## When to Use

> Investigating test failures or flake.

## Pattern: UI Mode (Start Here)

```bash
npx playwright test --ui
```

Interactive runner with:
- Sidebar listing every test
- Timeline of every action with DOM snapshots
- **Locator picker** — hover to highlight, click to copy the recommended Playwright locator
- Watch mode (re-runs on file change)
- Network log, console log, test source, call log in one pane

Use it for everything except CI. Faster than headed runner because it caches setup.

## Pattern: Trace Viewer

```ts
// playwright.config.ts
use: {
  trace: 'on-first-retry',          // best CI default
  video: 'retain-on-failure',
  screenshot: 'only-on-failure',
}
```

Modes:
- `'on'` — every test (heavy, dev only)
- `'on-first-retry'` — first attempt lean; retry records (recommended CI default)
- `'retain-on-failure'` — always record; keep only on failure
- `'off'` — no trace

Open with `npx playwright show-trace trace.zip`.

The trace contains DOM snapshots before/after every action, network waterfall, console messages, source line of every action. **Killer feature for debugging CI flakes.**

## Pattern: Inspector

```bash
PWDEBUG=1 npx playwright test login.spec.ts
# or
npx playwright test login.spec.ts --debug
```

Opens Chromium + Playwright Inspector pane with play/step/pause/resume controls and live locator suggestions. `PWDEBUG=console` is a quieter variant exposing a `playwright` global in DevTools.

## Pattern: `page.pause()`

Inline breakpoint:

```ts
test('debug me', async ({ page }) => {
  await page.goto('/');
  await page.pause(); // inspector opens here when run with --debug
  /* ... */
});
```

## Pattern: Codegen

```bash
npx playwright codegen
npx playwright codegen https://playwright.dev
npx playwright codegen --browser=firefox
npx playwright codegen --save-har=tests/.fixtures/orders.har https://example.com
```

Records interactions and emits Playwright code with recommended locators. Useful for:
- Bootstrapping a new test
- Discovering the right `getByRole` for an unfamiliar element
- Recording HAR files

Codegen output is starting-point quality — refactor into Page Objects or fixtures.

## Pattern: VS Code Extension

The official `Playwright Test for VSCode` extension adds:
- Run/debug gutters on each test
- Watch mode
- Locator picker integrated with editor
- One-click trace viewing
- Record-new-test action

## Common Mistakes

- **Skipping UI Mode** — friction-free debugging; learn it first
- **`trace: 'on'` in CI** — gigabytes of trace data; use `'on-first-retry'`
- **Unzipping `trace.zip` before opening** — viewer expects archive intact
- **`PWDEBUG=1` reaching CI** — it forces headed browsers and sets every action, navigation and test timeout to 0, so a hung test never fails; the job runs until the CI runner kills it. `--debug` is the same thing plus `--timeout=0 --max-failures=1 --headed --workers=1`. Keep both out of CI env

## See Also

- [Test Organization](pw-e2e-test-organization.md) — `test.step` entries in Trace Viewer
- [Anti-Patterns](pw-e2e-anti-patterns.md) — ranked list of flake causes
- Reference: [Playwright Debugging](https://playwright.dev/docs/debug)
