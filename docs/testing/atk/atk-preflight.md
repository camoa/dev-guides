---
description: "How ATK's YAML pre-flight (data/preflightTests.yml) runs inside the test run, its file shape, and when to extend it."
tldr: "The pre-flight runs inside the test run, not via a Drush command — Playwright's setup project calls preflightTest() before chromium; Cypress checks in a global before(). Only eq conditions are implemented; there is no drush atk:preflight command in any release."
drupal_version: "11.x"
---

# ATK Pre-flight Checks

## When to Use

> Stopping a run early when the target site is not ready for ATK.

## Pattern

There is **no Drush command** for the pre-flight. It runs inside the test run.

| Runner | Where it runs | File read |
|---|---|---|
| Playwright | `test.beforeAll()` in `atk_setup/atk_session.setup.js` calls `atkCommands.preflightTest()`. The `setup` project runs before `chromium` | `tests/data/preflightTests.yml` |
| Cypress | A global `before()` in `cypress/support/e2e.js` | `cypress/data/preflightTests.yml` |

To run only the Playwright pre-flight and session setup: `npx playwright test --project=setup`.

## Pattern: the file shape

Each entry is a Drush command, a message, and optional conditions on its JSON output. This is the shipped `data/preflightTests.yml`:

```yaml
- command: 'pm:list --format=json'
  message: 'Automated Testing Kit, QA Accounts must be enabled. (See data/preflightTests.yml for details)'
  json:
    automated_testing_kit.status:
      eq: 'Enabled'
    qa_accounts.status:
      eq: 'Enabled'
    login_security.status:
      eq: 'Enabled'
      warning: |
        Login Security is not installed or enabled.
        It may affect FedRAMP tests.
- command: 'user:unblock qa_administrator'
  message: 'QA Administrator account must be unblocked before running tests.'
```

- A `json` key is a dotted path into the command's output, read by `getProperty()`.
- `eq` is the only condition implemented.
- A condition with `warning` logs and continues. Any other failure stops the run with `message`.
- An entry without `json` just runs its command. The `user:unblock` entry works as a setup step, not a check.

## Decision: when to extend

| Add an entry when... | Skip when... |
|---|---|
| Your tests assume a module is enabled | Composer and config import already enforce it |
| Your tests assume a config value (`config:get … --format=json`) | Your bootstrap imports that config |
| A step must run before every run | The test itself does the setup |

## Common Mistakes

- **Running `drush atk:preflight`** — no such command exists in any release
- **Running only the `chromium` project with `--no-deps`** — this skips the pre-flight and session setup
- **Writing conditions other than `eq`** — ATK ignores them silently
- **Editing the module's copy** — `atk_setup` copied the file; edit `tests/data/preflightTests.yml` (or `cypress/data/`)

## See Also

- [Installation](atk-installation.md)
- [Runner Configuration](atk-runner-config.md)
- [Code Reference](atk-code-reference.md)
