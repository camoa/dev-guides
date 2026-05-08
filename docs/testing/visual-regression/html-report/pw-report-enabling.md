---
description: How to enable the Playwright HTML reporter in playwright.config.ts and via CLI.
tldr: Set reporter to 'html' in playwright.config.ts for the simplest case, or use an array of arrays for multiple reporters. CLI --reporter flag overrides config. The most common mistake is the flat string array syntax — multi-reporter requires nested arrays.
---

# Enabling the HTML Reporter

## When to Use

> Use this when configuring the HTML reporter in your Playwright project — either as the only reporter or alongside others.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Only need HTML report | `reporter: 'html'` | Simplest form |
| Need HTML + terminal output | `[['list'], ['html']]` | Multiple reporters run in parallel |
| Temporary override without editing config | `--reporter=html` CLI flag | Takes precedence over config |

## Pattern

Minimal config:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: 'html',
});
```

Combined reporters:

```ts
export default defineConfig({
  reporter: [
    ['list'],
    ['html'],
    ['json', { outputFile: 'results.json' }],
  ],
});
```

CLI override:

```bash
npx playwright test --reporter=html
npx playwright test --reporter=html,list
```

## Common Mistakes

- **Wrong**: `reporter: ['html', 'list']` as flat strings → **Right**: multi-reporter needs `[['list'], ['html']]` — nested arrays
- **Wrong**: including `html` locally but forgetting it in CI config → **Right**: CI artifacts have no triage UI without it; include both places

## See Also

- [Reporter Combos](pw-report-reporter-combos.md)
- [Configuration Reference](pw-report-configuration.md)
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
