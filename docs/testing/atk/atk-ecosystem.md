---
description: ATK vs Lullabot/playwright-drupal vs PHPUnit FunctionalJavascript vs Nightwatch — when to use each and when to combine them.
tldr: Use ATK for a curated Drupal-aware test catalog; use Lullabot/playwright-drupal for parallel SQLite infrastructure — they solve different problems and combining both is valid. Avoid starting new projects on Nightwatch, which is being replaced in Drupal core by Playwright.
drupal_version: "11.x"
---

# ATK Ecosystem & Alternatives

## When to Use

> Use this guide when choosing between ATK, Lullabot's playwright-drupal, core's PHPUnit FunctionalJavascript, and the broader migration from Nightwatch to Playwright.

## Decision

| Tool | Strength | Weakness |
|---|---|---|
| **ATK** | Curated Drupal-aware catalog; supports both Cypress + Playwright; selector hooks; FedRAMP pack | Smaller adoption (~89 sites on drupal.org); no SA coverage; you still install the runner separately |
| **Lullabot/playwright-drupal** | Parallel SQLite per worker; console error capture; `VisualDiffTestCases` for VR | Playwright-only; no test catalog; you write all the tests |
| **PHPUnit FunctionalJavascript (core)** | Stays in PHP; runs in `phpunit`; CI-friendly with no JS runtime | Slow; harder to debug than browser-driven tools; tied to Mink WebDriver |
| **Drupal core's Nightwatch (legacy)** | Was core's recommended JS E2E framework | Being replaced by Playwright per drupal.org #3467492 — don't start new projects on it |

### Which to Combine?

| Goal | Combination |
|---|---|
| Drupal-aware tests + parallel infrastructure | ATK + Lullabot/playwright-drupal (use both) |
| Drupal-aware tests + visual regression | ATK + Playwright VR APIs (or `VisualDiffTestCases` from Lullabot's package) |
| Just want to start | ATK alone — install runner of choice, run the demo recipe, extend |
| FedRAMP compliance | ATK 2.1-beta — currently the only option |

## Pattern

Drupal core's policy issue **#3467492** ("Replace Nightwatch with Playwright") signals the broader ecosystem direction. Even if you stay on Cypress for now, expect new tooling, examples, and integration help in the wider community to land first on Playwright.

## Common Mistakes

- **Wrong**: Picking Cypress for a new project in 2026 → **Right**: ATK still ships Cypress tests, but the centre of gravity is Playwright; you'll have less community help long-term
- **Wrong**: Using ATK and Lullabot's playwright-drupal as either/or → **Right**: they solve different problems; using both is fine and common
- **Wrong**: Expecting Nightwatch to be the answer for new work → **Right**: it's being replaced in core

## See Also

- [ATK Overview](atk-overview.md)
- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- Reference: https://github.com/Lullabot/playwright-drupal
- Reference: https://www.drupal.org/project/drupal/issues/3467492
