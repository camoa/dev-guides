---
description: "ATK vs Lullabot/playwright-drupal vs core PHPUnit FunctionalJavascript vs Nightwatch, and core's accepted move to Playwright."
tldr: "Choose ATK for a Drupal-aware Cypress/Playwright test catalog, Lullabot/playwright-drupal for isolated parallel test sites, or core PHPUnit to stay in PHP. Nightwatch is not deprecated — core accepted a policy to replace it with Playwright, but nothing has landed yet."
drupal_version: "11.x"
---

# ATK Ecosystem & Alternatives

## When to Use

> Choosing between ATK, Lullabot's playwright-drupal and core's PHPUnit FunctionalJavascript, given core's move from Nightwatch to Playwright.

## Decision

| Tool | Strength | Weakness |
|---|---|---|
| **ATK** | Drupal-aware test catalog for Cypress and Playwright; FedRAMP tests on 2.1 | Small adoption (107 sites on drupal.org, 2026-09-24); not covered by security advisories; 2.1 is beta |
| **Lullabot/playwright-drupal** | Parallel tests on SQLite site copies; Drush from tests; browser console errors; PHP error log attached to results; `VisualDiffTestCases` | Playwright only; no test catalog |
| **PHPUnit FunctionalJavascript (core)** | Stays in PHP; runs under `phpunit` via `WebDriverTestBase` | No Drupal site-level test catalog; you write every test |
| **Core's Nightwatch** | Still ships in core 11.x | Core accepted a policy (#3467492, November 2025) to replace it with Playwright |

## Decision: which to combine?

| Goal | Combination |
|---|---|
| Drupal-aware tests + isolated parallel sites | ATK tests on Lullabot/playwright-drupal infrastructure |
| Drupal-aware tests + visual regression | ATK + Playwright `toHaveScreenshot()` (or Lullabot's `VisualDiffTestCases`) |
| Just want to start | ATK alone: apply the demo recipe, run the catalog, extend |
| FedRAMP-oriented checks | ATK 2.1.0-beta |

## Drupal Core's Direction

Nightwatch is **not** deprecated. Core accepted a policy in November 2025 (#3467492) to replace it with Playwright. The migration issue (#3553673) is still open and targets Drupal 12. Nothing has landed in core yet.

## Common Mistakes

- **Treating ATK and Lullabot's playwright-drupal as either/or** — they solve different problems
- **Starting new Nightwatch coverage** — core has decided to move away from it; the work will need migrating
- **Assuming ATK has security advisory coverage** — the project has not opted in

## See Also

- [ATK Overview](atk-overview.md)
- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- Reference: https://www.drupal.org/project/drupal/issues/3467492
