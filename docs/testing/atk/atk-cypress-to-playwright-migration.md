---
description: "What's reusable moving ATK's Cypress suite to Playwright, translation patterns, helper gaps, and side-by-side migration."
tldr: "Preprocess hooks, drushCmd/pantheon/targetSite/tugboat config, preflightTests.yml, qaUsers.json and Testor snapshots carry over unchanged — only test bodies need translation. Playwright's execDrush() returns stdout directly instead of chaining like a Cypress command."
drupal_version: "11.x"
---

# Cypress → Playwright Migration

## When to Use

> Moving an existing Cypress ATK suite to Playwright.

## What's Reusable

| Asset | Reusable? |
|---|---|
| Preprocess hooks (body classes, `data-media-id`) | Yes — module-side |
| `drushCmd`, `pantheon`, `targetSite`, `tugboat` settings | Yes — same keys in `playwright.atk.config.js` |
| `preflightTests.yml`, `qaUsers.json` | Yes — same files |
| Testor snapshots | Yes — Testor is runner-agnostic |
| Test bodies | Translation needed |
| Helpers | Mostly the same names; signatures differ |

## Pattern: Translation Patterns

| Cypress | Playwright |
|---|---|
| `cy.visit('/path')` | `await page.goto(baseUrl + 'path')` |
| `cy.get(sel).click()` | `await page.locator(sel).click()` |
| `cy.get(sel).type('foo')` | `await page.locator(sel).fill('foo')` |
| `cy.get(sel).should('contain', 'X')` | `await expect(page.locator(sel)).toContainText('X')` |
| `cy.execDrush(cmd)` | `atkCommands.execDrush(cmd)` (synchronous; a string locally, a Buffer via Pantheon, SSH or Tugboat) |
| `cy.logInViaForm(account)` | `await atkCommands.getUserPage(browser, account)` or `logInViaForm(page, context, account)` |
| `cy.getNid()` | `await atkCommands.getNid(page)` |
| `cy.inputCKEditor(text)` | `await atkCommands.inputTextIntoCKEditor(page, text)` |
| `{ tags: ['@smoke'] }` | `@smoke` in the test title |
| `describe / it` | `test.describe / test` |

## Helper Gaps

- Playwright only: `expectMessage`, `openSearchForm`, `checkSearchResult`, `deleteCurrentNodeViaUi`, `getUserPage`, `getDrushAlias`, `preflightTest`, `skipIfLocal`
- Cypress only: `getByLabel`, `getIframeBodyWithId`, `save`, `debugLog`, `trace`
- Cypress commands, unexported in Playwright: `execViaSsh`, `execTugboatDrush`
- Different IDs: Cypress user tests are 1020/1021; Playwright's are 1100/1101
- Cypress only: simple sitemap (1080/1081)

## Decision: migrate all at once or incrementally?

| Approach | When |
|---|---|
| All at once | Small suite; one sprint available |
| Incrementally | Larger suite; migrate per area |
| Stay on Cypress | The suite works and the team knows it |

## Pattern: side by side during migration

`atk_setup` puts Playwright tests in `tests/` and Cypress tests in `cypress/e2e/`, so they can coexist. Both write `package.json` at `ATK_HOME`. Merge the two dependency lists by hand, or set a different `ATK_HOME` per runner.

## Common Mistakes

- **Migrating a flaky Cypress suite** — the flakes migrate too
- **Translating literally** — adopt Playwright's web-first assertions
- **Treating `execDrush()` as a Cypress chain** — the Playwright version returns stdout directly: a string locally, a Buffer via Pantheon, SSH or Tugboat

## See Also

- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
