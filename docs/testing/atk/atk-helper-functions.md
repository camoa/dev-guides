---
description: "ATK's Playwright and Cypress helper functions (atk_commands.js), by category, with runnable examples for both runners."
tldr: "Playwright ships 27 helpers in atk_commands.js (login, execDrush, config, users, nodes/media, assertions, preflightTest, skipIfLocal) plus 4 in atk_utilities.js. Never call Drush with execSync or cy.exec — it bypasses the Pantheon, SSH and Tugboat routing; read credentials from data/qaUsers.json, never hardcode them."
drupal_version: "11.x"
---

# ATK Helper Functions

## When to Use

> Reusing ATK's helpers in your own tests.

## Pattern: the helpers (Playwright `atk_commands.js`, 2.1.0-beta5)

| Category | Helpers |
|---|---|
| Login | `logInViaForm(page, context, account)`, `logInViaUli(page, context, uid)`, `logOutViaUi(page)`, `getUserPage(browser, account)` |
| Drush | `execDrush(cmd, args = [], options = [])`, `execPantheonDrush(cmd)`, `getDrushAlias()` |
| Config | `getDrupalConfiguration(objectName, key)`, `setDrupalConfiguration(objectName, key, value)` |
| Users | `createUserWithUserObject(user, roles, args, options)`, `deleteUserWithEmail`, `deleteUserWithUid`, `deleteUserWithUserName`, `getUidWithEmail`, `getUsernameWithEmail` |
| Nodes and media | `getNid(page)`, `getMid(imageLocator)`, `deleteNodeWithNid(nid)`, `deleteNodeViaUiWithNid(page, context, nid)`, `deleteCurrentNodeViaUi(page)` |
| Assertions | `expectMessage(page, text)`, `expectEmail(mailto, subject)` |
| Page helpers | `inputTextIntoCKEditor(page, text)`, `openSearchForm(page)`, `checkSearchResult(page, item)` |
| Run control | `preflightTest()`, `skipIfLocal()` |

`atk_utilities.js` adds `createRandomString()`, `createRandomUser()`, `readYAML()` and `getProperty()`.

`getUserPage()` reuses a stored login for 15 minutes. It keeps `loginAuth-<userName>.json` in `supportDir`.

## Pattern: Playwright

```js
import { test, expect } from '@playwright/test'
import * as atkCommands from '../support/atk_commands'
import playwrightConfig from '../../playwright.config'
import qaUserAccounts from '../data/qaUsers.json'

const baseUrl = playwrightConfig.use.baseURL

test('admin reaches the content list', async ({ browser }) => {
  const page = await atkCommands.getUserPage(browser, qaUserAccounts.admin)
  await page.goto(`${baseUrl}admin/content`)
  await expect(page.locator('h1')).toHaveText('Content')
  atkCommands.execDrush('cr')
})
```

## Pattern: Cypress

Cypress helpers are custom commands. `cypress/support/e2e.js` loads them.

```js
import qaUserAccounts from '../../data/qaUsers.json'

describe('admin access', () => {
  it('reaches the content list', () => {
    cy.logInViaForm(qaUserAccounts.admin)
    cy.visit('admin/content')
    cy.execDrush('cr')
  })
})
```

## Decision

| Need | Helper |
|---|---|
| Log in for a test | `getUserPage(browser, qaUserAccounts.admin)` (PW) / `cy.logInViaForm(account)` (CY) |
| Run any Drush command | `execDrush()` — it follows the config's target |
| Read or write config | `getDrupalConfiguration()` / `setDrupalConfiguration()` |
| Check an email arrived | `expectEmail(mailto, subject)` — Mailpit or testmail.app |
| Clean up | `deleteNodeWithNid()`, `deleteUserWithUserName()` |

## Common Mistakes

- **Calling Drush with `execSync` or `cy.exec`** — it bypasses the Pantheon, SSH and Tugboat routing
- **Hardcoding credentials** — read them from `data/qaUsers.json`
- **Relying on `expectEmail()` without an `email.provider`** — it logs a warning and checks nothing

## See Also

- [Selector Hooks](atk-selector-hooks.md)
- [Custom Tests](atk-custom-tests.md)
- [Runner Configuration](atk-runner-config.md)
