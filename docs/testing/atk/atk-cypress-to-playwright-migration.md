---
description: Migrating an existing Cypress ATK suite to Playwright — what's reusable, translation patterns, and when to migrate incrementally vs all at once.
tldr: Selector hooks, Drush config, Testor snapshots, qa_accounts, and pre-flight checks are all reusable. Test logic needs translation — adopt Playwright's web-first assertions rather than translating literally. Never build a compatibility shim.
drupal_version: "11.x"
---

# Cypress → Playwright Migration (ATK)

## When to Use

> Use this guide when moving an existing Cypress ATK suite to Playwright.

## Decision

### Migrate all at once or incrementally?

| Approach | When |
|---|---|
| All at once | Suite < 30 tests; small team; can dedicate a sprint |
| Incrementally | Larger suite; mix CI to run both; migrate per-area |
| Stay on Cypress | Existing investment; team velocity > migration value |

## Pattern

### What's reusable

| Asset | Reusable? |
|---|---|
| Selector hooks | Yes — same `data-qa-id` attribute |
| Drush invocation strategy | Yes — same `drushCmd` pattern |
| Testor snapshots | Yes — runner-agnostic |
| Pre-flight checks | Yes |
| qa_accounts users + roles | Yes |
| Test logic / assertions | Translation needed (idiom differences) |
| Helper functions | Mostly yes — APIs are parallel; runner-specific glue differs |

### Translation patterns

| Cypress | Playwright |
|---|---|
| `cy.visit('/path')` | `await page.goto('/path')` |
| `cy.get(sel).click()` | `await page.locator(sel).click()` |
| `cy.get(sel).type('foo')` | `await page.locator(sel).fill('foo')` |
| `cy.get(sel).should('be.visible')` | `await expect(page.locator(sel)).toBeVisible()` |
| `cy.get(sel).should('contain', 'X')` | `await expect(page.locator(sel)).toContainText('X')` |
| `cy.intercept('POST', '/api', ...)` | `await page.route('/api', ...)` |
| `cy.exec('drush ...')` | `runDrush(...)` (use ATK helper) |
| `cy.session('user', () => {...})` | `storageState` + `auth.setup.ts` pattern |
| `describe / it` | `test.describe / test` |

### Side-by-side during migration

```
tests/
├── cypress/                    # existing suite
│   ├── e2e/
│   └── cypress.config.js
└── playwright/                 # new suite
    ├── e2e/
    └── playwright.config.js
```

CI runs both; remove Cypress when migration completes.

## Common Mistakes

- **Wrong**: Migrating without first stabilizing the Cypress suite → **Right**: flake migrates with you
- **Wrong**: Translating tests literally without adopting Playwright's web-first assertions → **Right**: verbose; doesn't gain stability benefits
- **Wrong**: Attempting a "compatibility shim" library → **Right**: every team that tries this regrets it; idiom differences are real

## See Also

- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
