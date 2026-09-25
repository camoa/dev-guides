---
description: "Writing project-specific ATK tests — directory layout, a worked example, and tagging for selective runs."
tldr: "Keep custom tests in directories without the atk_ prefix — atk_setup … back copies all of tests/atk*/, tests/support/* and tests/data/* back into the module, so project helpers and data belong outside those two directories, for example tests/project-support/."
drupal_version: "11.x"
---

# ATK Custom Tests

## When to Use

> Writing project-specific tests beside ATK's catalog.

## Pattern: directory structure

Keep your tests next to ATK's, in directories without the `atk_` prefix:

```
tests/
├── atk_*/            # ATK's catalog, copied by atk_setup
├── data/             # ATK fixtures + your own
├── support/          # atk_commands.js, atk_utilities.js, atk_reporter.js
├── smoke/            # your smoke set
└── content/          # your content tests
```

`atk_setup … back` copies the `tests/atk*` directories back into the module. It also copies **all** of `tests/support/*` and `tests/data/*` back. Keep project helpers and data outside those two directories, for example in `tests/project-support/`.

## Pattern: a custom test using ATK helpers

For fixtures, locators and web-first assertions, see [Playwright for Visual Regression](../visual-regression/playwright/index.md). The same Playwright practice applies here.

```js
import { test, expect } from '@playwright/test'
import * as atkCommands from '../support/atk_commands'
import playwrightConfig from '../../playwright.config'
import qaUserAccounts from '../data/qaUsers.json'

const baseUrl = playwrightConfig.use.baseURL

test('(PROJ-001) admin publishes a landing page @smoke @landing', async ({ browser }) => {
  const page = await atkCommands.getUserPage(browser, qaUserAccounts.admin)
  await page.goto(`${baseUrl}node/add/landing_page`)
  await page.locator('input[name="title[0][value]"]').fill('Spring campaign')
  await page.getByRole('button', { name: 'Save' }).first().click()
  await atkCommands.expectMessage(page, 'has been created')
  atkCommands.deleteNodeWithNid(await atkCommands.getNid(page))
})
```

## Decision: where to put a new test

| Test scope | Location |
|---|---|
| Already covered by ATK | Run ATK's test; don't duplicate |
| Project content type or workflow | `tests/content/`, `tests/workflows/` |
| Project helper | A directory outside `tests/support/`, such as `tests/project-support/` |
| Changed ATK behaviour | Copy the ATK test to your own directory and rename its ID |

## Pattern: tags for selective runs

```js
// Playwright: tags in the title
test('login works @smoke @project', async ({ page }) => { /* ... */ })
```

```js
// Cypress: tags in the options
it('login works', { tags: ['@smoke', '@project'] }, () => { /* ... */ })
```

Run them with `npx playwright test --grep @smoke` or `npx cypress run --env grepTags=@smoke`.

## Common Mistakes

- **Naming your directories `atk_*`, or keeping your files in `tests/support/` or `tests/data/`** — `atk_setup back` copies them into the module
- **Leaving test data behind** — clean up what the test created, as ATK's tests do
- **No tagging strategy** — you cannot run a smoke subset without listing paths

## See Also

- [Test Catalog](atk-test-catalog.md)
- [Helper Functions](atk-helper-functions.md)
- [Selector Hooks](atk-selector-hooks.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
