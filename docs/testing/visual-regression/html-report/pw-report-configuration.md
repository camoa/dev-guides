---
description: Complete reference for all Playwright HTML reporter configuration options.
tldr: The HTML reporter accepts outputFolder, open, host, port, attachmentsBaseURL, and noSnippets options. All have environment variable overrides. The most common mistake is omitting the trailing slash on attachmentsBaseURL.
---

# Configuration Reference

## When to Use

> Use this as a reference for every HTML reporter option when setting up or tuning your Playwright config.

## All Options

```ts
reporter: [['html', { /* options */ }]]
```

| Option | Type | Default | Purpose |
|---|---|---|---|
| `outputFolder` | `string` | `'playwright-report'` | Where to write the report bundle. Overridden by `PLAYWRIGHT_HTML_REPORT` |
| `open` | `'always' \| 'never' \| 'on-failure'` | `'on-failure'` local / `'never'` CI | Auto-launch browser after run. Overridden by `PLAYWRIGHT_HTML_OPEN` |
| `host` | `string` | `'localhost'` | Bind interface for `show-report`. Overridden by `PLAYWRIGHT_HTML_HOST`. Use `'0.0.0.0'` for LAN/DDEV |
| `port` | `number` | `9323` | Bind port for `show-report`. Overridden by `PLAYWRIGHT_HTML_PORT` |
| `attachmentsBaseURL` | `string` | same dir as `index.html` | Override fetch root for screenshots/videos/traces |
| `noSnippets` | `boolean` | `false` | Strip source-code snippets from report (smaller bundle, less context) |

## Pattern

Full example:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [['html', {
    outputFolder: 'reports/html',
    open: 'never',
    host: '0.0.0.0',
    port: 9323,
    attachmentsBaseURL: 'https://my-cdn.example.com/reports/abc123/',
  }]],
});
```

## Common Mistakes

- **Wrong**: hardcoding `host: 'localhost'` then trying to share on LAN → **Right**: bind to `'0.0.0.0'`
- **Wrong**: `attachmentsBaseURL` without trailing slash → **Right**: URL concatenation breaks
- **Wrong**: `noSnippets: true` when you want context → **Right**: saves bundle size but loses test source in the report

## See Also

- [Enabling](pw-report-enabling.md)
- [Sharing](pw-report-sharing.md)
- [Running Modes](pw-report-running-modes.md)
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
