---
description: "ATK release tracks — 2.1.0-beta5 vs 2.0.0 stable vs 3.0.0-alpha — and what differs if the site runs 2.0.0."
tldr: "This guide targets 2.1.0-beta5 (2026-02-04); latest stable is 2.0.0 (2025-05-15). Use 2.1.0-beta for FedRAMP tests, Feeds, or Tugboat; on a 2.0.0 site the pre-flight filename, setup project and file:create don't exist, so 2.1 instructions break there."
drupal_version: "11.x"
---

# ATK Versions & Compatibility

## When to Use

> Picking the ATK release, or working on a site that runs 2.0.0 stable.

## Decision

| Release | Date | Drupal core | Status |
|---|---|---|---|
| **2.1.0-beta5** | 2026-02-04 | `>=11.0 <12` | Beta. **This guide's target** |
| **2.0.0** | 2025-05-15 | `>=11.0 <12` | Latest stable |
| **3.0.0-alpha9** | 2026-01-19 | `>=11.0 <12` | Alpha; Drupal CMS 2.x |
| **1.3.0** | 2024-11-30 | `^10 \|\| ^11` | Older line |

Dates and core constraints come from the drupal.org release feed. The feed names no recommended release. The demo recipe mirrors the 2.0, 2.1 and 3.0 lines; its 2.1 release is 2.1.0-beta4. Its README says: Drupal 10 uses 1.x, Drupal 11 uses 2.x.

## Compatibility

| Aspect | Constraint | Source |
|---|---|---|
| Drupal core | `>=11.0 <12` | `automated_testing_kit.info.yml` |
| PHP | `>=8.3` | `composer.json` |
| Drush | 13 | Demo recipe requires `drush/drush: ^13`; ATK's `require-dev` is `^13.6` |
| Playwright | `@playwright/test: ^1.48` | `module_support/development/playwright.package.json` |
| Cypress | `cypress: ^13` | `module_support/development/cypress.package.json` |
| Security advisories | **Not covered** | Release feed: "Project has not opted into security advisory coverage" |

## Pattern: install pin

```bash
# This guide's target
composer require 'drupal/automated_testing_kit:2.1.0-beta5'

# Latest stable
composer require 'drupal/automated_testing_kit:^2.0'
```

## If the Site Runs 2.0.0 Stable

Each row was checked by diffing the 2.0.0 and 2.1.0-beta5 tags.

| Area | 2.0.0 | 2.1.0-beta5 |
|---|---|---|
| Pre-flight file | `data/atk_prerequisites.yml`: requires `automated_testing_kit` and `qa_accounts` enabled | `data/preflightTests.yml`: adds a `login_security` warning and `user:unblock qa_administrator` |
| How Playwright runs it | At module load of `atk_commands.js`, once per process (`globalThis.prerequisitesOk`) | `preflightTest()`, called from the setup project |
| Setup project | None; `playwright.config.js` has only `chromium` | `setup` project runs `atk_setup/atk_session.setup.js`; `chromium` depends on it |
| Playwright helpers | 24 exports | 27: adds `preflightTest()`, `getUserPage()`, `skipIfLocal()` |
| Drush | `file:properties` only | Adds `file:create` |
| FedRAMP | No `atk_fedramp/` | `atk_fedramp/` in both runners |
| Feeds | No `atk_feeds/` | `atk_feeds/`, plus `data/rss.xml` served by `TestDataController` |
| Tugboat | No `tugboat` config key | `tugboat: {isTarget, service}`; `execTugboatDrush()` (a Cypress command; internal in Playwright) |

On 2.0.0, Cypress still reads the pre-flight in `before()`, but from `atk_prerequisites.yml`.

## Common Mistakes

- **Following `github.com/PerformantLabs/atk-cypress` or `atk-playwright`** — both 404; the source is `git.drupalcode.org/project/automated_testing_kit`
- **Using 2.1 instructions on a 2.0.0 site** — the pre-flight filename, setup project and `file:create` do not exist there
- **Treating 2.1 as stable** — it has had betas only since 2025-08

## See Also

- [FedRAMP & 2.1 Features](atk-fedramp.md)
- [Installation](atk-installation.md)
- Reference: https://www.drupal.org/project/automated_testing_kit/releases
