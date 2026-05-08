---
description: Configuring Playwright and Cypress runners for ATK — baseURL, Drush invocation modes, DDEV TLS, and environment-specific config.
tldr: Set baseURL from DDEV_PRIMARY_URL, use ignoreHTTPSErrors for DDEV self-signed certs, and configure drushCmd to match your environment (local, container exec, or SSH). Wrong drushCmd is the most common ATK CI failure.
drupal_version: "11.x"
---

# ATK Runner Configuration

## When to Use

> Use this guide when configuring Cypress or Playwright to work with ATK's helpers and an environment-aware Drush command.

## Decision

| drushCmd mode | When | Value |
|---|---|---|
| Local CLI | Drush installed on the runner host | `drushCmd: 'drush'` |
| Container exec | Drupal in DDEV/Lando/Docksal | `drushCmd: 'ddev drush'` |
| SSH (Pantheon, remote) | Drupal on a remote host | `drushCmd: 'ssh user@host drush'` or `terminus drush mysite.test --` |

## Pattern

### Playwright config (ATK minimum)

```ts
// tests/playwright/playwright.config.js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [['list'], ['html']],
  use: {
    baseURL: process.env.DDEV_PRIMARY_URL ?? 'https://my-site.ddev.site',
    ignoreHTTPSErrors: true,        // self-signed DDEV TLS
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

For a fully annotated config walkthrough, see [Playwright Config Walkthrough](../visual-regression/playwright/pw-vr-config-walkthrough.md).

### Cypress config

```js
// tests/cypress/cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.DDEV_PRIMARY_URL ?? 'https://my-site.ddev.site',
    specPattern: 'e2e/**/*.cy.js',
    supportFile: 'support/e2e.js',
    chromeWebSecurity: false,       // for DDEV self-signed
    video: false,
    screenshotOnRunFailure: true,
  },
});
```

### Environment-specific ATK config

```js
// atk.config.js
export default {
  baseUrl: process.env.BASE_URL ?? 'https://my-site.ddev.site',
  drushCmd: process.env.DRUSH_CMD ?? 'ddev drush',
  qaAccounts: {
    siteAdmin:    { name: 'site_admin',    pass: 'site_admin' },
    contentAdmin: { name: 'content_admin', pass: 'content_admin' },
    editor:       { name: 'editor',        pass: 'editor' },
    authenticated:{ name: 'auth_user',     pass: 'auth_user' },
  },
};
```

## Common Mistakes

- **Wrong**: Hardcoding `drushCmd: 'drush'` when running against DDEV → **Right**: use `ddev drush`
- **Wrong**: Wrong `baseUrl` → **Right**: tests run against the wrong env (or production by accident)
- **Wrong**: Forgetting `ignoreHTTPSErrors: true` with DDEV → **Right**: every navigation fails on self-signed cert

## See Also

- [Installation](atk-installation.md)
- [CI Integration](atk-ci-integration.md)
- [Playwright for Visual Regression — Config Walkthrough](../visual-regression/playwright/pw-vr-config-walkthrough.md)
