---
description: "How to enable the Playwright HTML reporter in playwright.config.ts and via CLI."
tldr: "Set reporter to 'html' in playwright.config.ts for the simplest case, or use an array of arrays for multiple reporters. CLI --reporter flag overrides config. The most common mistake is the flat string array syntax — multi-reporter requires nested arrays."
---

# Enabling the HTML Reporter

## When to Use

> Configuring the HTML reporter in your Playwright project.

## Pattern: Config

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: 'html',
});
```

## Pattern: Combined Reporters

Each entry runs in parallel; first one wins terminal output:

```ts
export default defineConfig({
  reporter: [
    ['list'],
    ['html'],
    ['json', { outputFile: 'results.json' }],
  ],
});
```

## Pattern: CLI Override

CLI takes precedence over config:

```bash
npx playwright test --reporter=html
npx playwright test --reporter=html,list
```

## Decision

| Situation | Choose | Why |
|---|---|---|
| Only need HTML report | `reporter: 'html'` | Simplest form |
| Need HTML + terminal output | `[['list'], ['html']]` | Multiple reporters run in parallel |
| Temporary override without editing config | `--reporter=html` CLI flag | Takes precedence over config |

## Common Mistakes

- **`reporter: ['html', 'list']`** as flat strings without arrays — invalid syntax; needs `[['list'], ['html']]`
- **Forgetting `html` in CI** while including it locally — CI artifacts have no triage UI; you need it both places

## See Also

- [Reporter Combos](pw-report-reporter-combos.md)
- [Configuration Reference](pw-report-configuration.md)
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
