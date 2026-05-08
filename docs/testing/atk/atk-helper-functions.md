---
description: ATK's ~24 utility helpers — loginAsRole, runDrush, testorPull, expectEmailSent, and more — and how to import them in Playwright and Cypress.
tldr: ATK ships ~24 helpers covering auth (loginAsRole), Drush invocation (runDrush), snapshot management (testorPull), form interactions, email verification, and cleanup. Use loginAsRole instead of hardcoded credentials; use runDrush instead of cy.exec — both handle environment-specific invocation automatically.
drupal_version: "11.x"
---

# ATK Helper Functions

## When to Use

> Use ATK's helpers in your custom tests instead of reimplementing them. Use `loginAsRole()` over hardcoded credentials; use `runDrush()` over `cy.exec('drush ...')`.

## Decision

| Need | Helper |
|---|---|
| Log in for a test | `loginAsRole(page, 'editor')` — uses qa_accounts users |
| Run any Drush command | `runDrush(args)` — handles environment-specific invocation |
| Reset DB to known state | `testorPull()` — pulls fresh snapshot |
| Verify an email was sent | `expectEmailSent(predicate)` — works with Mailtrap or Testmail |
| Clean up after a test | `deleteAllOfType('article')` — removes test fixtures |

## Pattern

### Canonical helpers by category

| Category | Helpers |
|---|---|
| Auth | `loginViaForm()`, `loginAsRole()`, `logout()`, `getCurrentUser()` |
| Drush | `runDrush()`, `drushConfigGet()`, `drushConfigSet()` |
| Snapshots | `testorPull()`, `testorPush()`, `testorReset()` |
| Forms | `fillFormField()`, `submitForm()`, `assertFormError()` |
| Email | `expectEmailSent()`, `latestEmail()`, `clearMailbox()` |
| Cleanup | `deleteAllOfType()`, `resetUsers()`, `truncateTable()` |
| Navigation | `gotoNode()`, `gotoAdminPage()`, `expectAccessDenied()` |

### Import in Playwright

```ts
import { test, expect } from '@playwright/test';
import { loginAsRole, gotoAdminPage } from '../helpers/atk';

test('admin can access content list', async ({ page }) => {
  await loginAsRole(page, 'site_admin');
  await gotoAdminPage(page, '/admin/content');
  await expect(page.locator('h1')).toHaveText('Content');
});
```

### Import in Cypress

```js
import { loginAsRole, gotoAdminPage } from '../helpers/atk';

describe('admin access', () => {
  it('can reach content list', () => {
    loginAsRole('site_admin');
    gotoAdminPage('/admin/content');
    cy.get('h1').should('have.text', 'Content');
  });
});
```

## Common Mistakes

- **Wrong**: Reimplementing helpers in your project → **Right**: adds maintenance; leverage what's there
- **Wrong**: Calling Drush directly with `cy.exec()` instead of `runDrush()` → **Right**: bypasses the configurable invocation, fails in CI/Pantheon
- **Wrong**: Hardcoded user credentials in test files → **Right**: use `loginAsRole()` against the qa_accounts seed

## See Also

- [Custom Tests](atk-custom-tests.md)
- [Testor Snapshots](atk-testor.md)
- Reference: `js-helpers/playwright/` and `js-helpers/cypress/` in the module
