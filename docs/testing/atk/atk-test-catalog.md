---
description: "ATK's test catalog by area for 2.1.0-beta5, how to run a subset by tag, and what the catalog doesn't cover."
tldr: "39 Playwright test declarations (38 active, 18 spec files) and 37 Cypress declarations (36 active, 17 files) cover register/login, contact, error pages, sitemap, caching, entity CRUD, menu, search and feeds — no logout, role-access, admin, forms, navigation, revision or scheduling suite exists. Tags are uneven upstream."
drupal_version: "11.x"
---

# ATK Test Catalog

## When to Use

> Picking which ATK tests to run against your site.

## Pattern: how tests are organised

Each area has a directory, and each test carries a numeric ID in its title:

| Cypress | Playwright |
|---|---|
| `cypress/e2e/atk_register_login/atk_register_login.cy.js` (`ATK-CY-1010`) | `playwright/e2e/atk_register_login/atk_register_login.spec.js` (`ATK-PW-1010`) |
| `cypress/e2e/atk_entity/atk_node.cy.js` (`ATK-CY-1110`) | `playwright/e2e/atk_entity/atk_node.spec.js` (`ATK-PW-1110`) |

## Pattern: catalog by area (2.1.0-beta5)

| IDs | Directory | Covers | Needs |
|---|---|---|---|
| 1000–1030 | `atk_register_login` | Register, login form, login via ULI, reset password | `qa_accounts` |
| 1050–1051 | `atk_contact_us` | Contact webform, site feedback form, email sent | `webform`; `email.provider` for the email check |
| 1060–1061 | `atk_page_error` | 403 and 404 pages | Custom error pages (demo recipe) |
| 1070–1071 | `atk_sitemap` | XML sitemap count and regenerate | `xmlsitemap` |
| 1080–1081 | `atk_simple_sitemap` (Cypress only) | Simple sitemap | `simple_sitemap` |
| 1090 | `atk_caching` | Block caching and cache tags | — |
| 1100–1101 (PW), 1020–1021 (CY) | `atk_entity/atk_user`; CY 1020–1021 also duplicated verbatim in `atk_register_login` | Create and delete a user with Drush | — |
| 1110–1111 | `atk_entity/atk_node` | Page and article CRUD via the UI | — |
| 1120 | `atk_entity/atk_taxonomy` | Term CRUD via the UI | — |
| 1130 | `atk_entity/atk_media` | Image media CRUD via the UI | `media` |
| 1150 | `atk_menu` | Menu item CRUD | — |
| 1160–1163 | `atk_search` | Keyword and advanced search, empty input | Indexed content (cron) |
| 1180 (PW); 1180–1181 (CY, under `ATK-PW-` IDs) | `atk_feeds` | Feed type and import | `feeds` |
| 1200–1251 | `atk_fedramp` | See [FedRAMP & 2.1 Features](atk-fedramp.md) | See [FedRAMP & 2.1 Features](atk-fedramp.md) |

There is no logout test, no role-access suite, no admin, forms or navigation suite, and no revision or scheduling test.

## Pattern: running a subset

Playwright tags sit in the title. Cypress tags sit in `{ tags: [...] }`.

```bash
# Playwright
npx playwright test --grep @smoke
npx playwright test --grep @register-login
npx playwright test --grep-invert @alters-db     # skip tests that change the database
npx playwright test --grep @ATK-PW-1160          # one test
npx playwright test tests/atk_register_login/

# Cypress (@cypress/grep)
npx cypress run --env grepTags=@smoke
npx cypress run --spec "cypress/e2e/atk_register_login/**"
```

Tags are uneven upstream. Several Cypress tests tag `alters-db` without the `@`. `ATK-PW-1012` carries `@ATK-PY-1012`. The Cypress feeds tests use `ATK-PW-` IDs.

## Decision

| If you're starting | Run |
|---|---|
| First-day check | `--grep @smoke` |
| Against a shared test site whose data others rely on | `--grep-invert @alters-db` |
| Per-PR | Smoke, plus tests for the changed area |
| Nightly | Full catalog, plus FedRAMP if on 2.1 |

## Common Mistakes

- **Running the whole catalog without the modules it needs** — contact, sitemap, feeds and FedRAMP tests fail on a bare site
- **Running `@alters-db` tests against shared data** — they create and delete content
- **Editing `tests/atk_*` in place** — re-running `atk_setup` overwrites them; copy and rename instead

## See Also

- [Helper Functions](atk-helper-functions.md)
- [Custom Tests](atk-custom-tests.md)
- [FedRAMP & 2.1 Features](atk-fedramp.md)
