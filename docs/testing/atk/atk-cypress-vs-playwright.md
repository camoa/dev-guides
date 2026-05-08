---
description: Choosing Cypress or Playwright as the ATK runner — what differs, what's shared, and why Playwright is the 2026 default.
tldr: Use Playwright for new projects in 2026 — cross-browser, built-in parallelism, web-first assertions, and the emerging community direction. Use Cypress only when an existing suite justifies staying. ATK ships both catalogs; pick one runner per project.
drupal_version: "11.x"
---

# Cypress vs Playwright (ATK Runner Choice)

## When to Use

> Use Playwright when starting fresh in 2026. Use Cypress only when you have an existing suite that justifies staying on it. ATK supports both; pick one per project.

## Decision

| If you... | Pick |
|---|---|
| Have an existing Cypress suite | Cypress (ATK still maintains the Cypress catalog) |
| Are starting fresh in 2026 | Playwright (see [Playwright for Visual Regression](../visual-regression/playwright/index.md) for the runner's full surface — same setup applies to ATK functional tests) |
| Need cross-browser (Firefox, WebKit) | Playwright (Cypress is Chromium-family only) |
| Need parallel sharding without paid services | Playwright (Cypress paid for parallel until recently) |
| Want strong web-first assertions | Playwright (auto-retry semantics) |
| Already use Playwright for visual regression | Playwright (one runner, one set of fixtures) |

## Pattern

### What's the Same Across Runners

| Convention | Cypress | Playwright |
|---|---|---|
| File suffix | `*.cy.js` | `*.spec.js` |
| Test ID prefix | `-CY-` | `-PW-` |
| Helpers | `js-helpers/cypress/*` | `js-helpers/playwright/*` |
| Selector strategy | Same (selector hooks from ATK module) | Same |
| Drush invocation | Same (configurable: local / container / SSH) | Same |
| Pre-flight checks | Same (`atk_prerequisites.yml`) | Same |
| Testor snapshots | Same Drush commands | Same |

### What Differs

| Concern | Cypress | Playwright |
|---|---|---|
| Browsers | Chromium family only | Chromium + Firefox + WebKit |
| Auto-retry semantics | `cy.should()` chains | Web-first `expect()` assertions |
| Test parallelization | Limited free tier; paid for sharding | Built-in workers + sharding |
| Network mocking | `cy.intercept()` | `page.route()` |
| Iframe/cross-origin | Restricted by design | Full support |
| Trace viewer / debugger | Cypress App with time-travel UI | Playwright Trace Viewer with DOM snapshots |

## Common Mistakes

- **Wrong**: Asserting one runner is "better" → **Right**: ATK supports both; pick what your team knows or can adopt
- **Wrong**: Mixing runners on the same component → **Right**: pick one per project; keeping two suites is double the maintenance
- **Wrong**: Assuming tests are 1:1 portable → **Right**: assertion idioms differ; helpers carry over but test bodies need translation

## See Also

- [Cypress → Playwright Migration](atk-cypress-to-playwright-migration.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
