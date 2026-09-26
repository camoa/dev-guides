---
description: "ATK's two config files per runner, the *.atk.config.js keys, how execDrush() picks a Drush target, and qaUsers.json."
tldr: "*.atk.config.js sets drushCmd, *Url routes, email and the pantheon/targetSite/tugboat blocks; execDrush() tries Pantheon, then SSH targetSite, then Tugboat, then drushCmd, in that order. baseURL lives in the runner's own config, not *.atk.config.js."
drupal_version: "11.x"
---

# ATK Runner Configuration

## When to Use

> Pointing ATK at a site and telling it how to reach Drush.

## Pattern: the two config files per runner

| File | Holds |
|---|---|
| `playwright.config.js` / `cypress.config.js` | Runner settings and the target URL (`use.baseURL` / `e2e.baseUrl`) |
| `playwright.atk.config.js` / `cypress.atk.config.js` | ATK settings, as CommonJS `module.exports` |

ATK's `playwright.config.js` sets `testDir: './tests'`, `fullyParallel: true` and `trace: 'on'`. On CI it sets `retries: 2` and `workers: 1`. The timeout is 180000 ms. Reporters are `html` and `./tests/support/atk_reporter.js` at level `debug`. Firefox and WebKit projects ship commented out. For every Playwright key, see [Playwright for Visual Regression — Config Walkthrough](../visual-regression/playwright/pw-vr-config-walkthrough.md).

ATK's `cypress.config.js` sets `baseUrl`, registers `cypress-log-to-term` and `@cypress/grep`, and sets `env.atkLogLevel: 0`.

## Pattern: `*.atk.config.js` keys

| Key | Purpose |
|---|---|
| `drushCmd` | Local Drush command, default `'drush'` |
| `*Url` keys (`logInUrl`, `nodeEditUrl`, `termAddUrl`, …) | Drupal routes the tests visit; `{nid}`, `{tid}`, `{mid}` are placeholders |
| `authDir`, `dataDir`, `supportDir`, `testDir` | Where ATK reads and writes files |
| `email` | `provider: 'mailpit'` with `url`, or `provider: 'testmail'` with `namespace` and `apiKey`; optional `reroute` |
| `pantheon` | `{isTarget, site, environment}` |
| `targetSite` | `{isTarget, root, remoteHost, remoteUser, sshOptions}` |
| `tugboat` | `{isTarget, service}` |

## Pattern: how ATK reaches Drush

`execDrush()` checks the targets in this order and uses the first with `isTarget: true`:

| Target | Config | Runs |
|---|---|---|
| Pantheon | `pantheon: {isTarget: true, site: 'mysite', environment: 'test'}` | `terminus remote:drush mysite.test -- <cmd>` |
| SSH host | `targetSite: {isTarget: true, remoteHost, remoteUser, sshOptions}` | `ssh -T <sshOptions> … <user>:<host> '<drushCmd> <cmd>'` |
| Tugboat | `tugboat: {isTarget: true, service: '<id>'}` | `tugboat shell <id> command="vendor/drush/drush/drush <cmd>"` |
| None | `drushCmd: 'drush'` or `'ddev drush'` | `<drushCmd> <cmd>` on the runner host |

For DDEV, Lando or Docksal, set `drushCmd` to the wrapper, for example `'ddev drush'`.

## Pattern: test accounts

`data/qaUsers.json` defines the accounts that tests log in with (trimmed; each entry also has `accountType`):

```json
{
  "admin":         { "userName": "qa_administrator", "userPassword": "qa_administrator", "userRoles": ["administrator"] },
  "authenticated": { "userName": "qa_authenticated", "userPassword": "qa_authenticated", "userRoles": ["authenticated"] }
}
```

The `qa_accounts` module creates these users when it is enabled. Its accounts use the username as the password.

## Common Mistakes

- **Using `drushCmd: 'drush'` against DDEV from the host** — Drush calls fail; use `'ddev drush'`
- **Putting Pantheon or SSH details in `drushCmd`** — use the `pantheon` or `targetSite` block
- **Leaving `tugboat.isTarget: true` in Cypress** — ATK's shipped `cypress.atk.config.js` sets it `true`, so every Drush call goes to Tugboat
- **Looking for `baseUrl` in `*.atk.config.js`** — the URL lives in the runner's own config

## See Also

- [Installation](atk-installation.md)
- [Pre-flight Checks](atk-preflight.md)
- [Playwright for Visual Regression — Config Walkthrough](../visual-regression/playwright/pw-vr-config-walkthrough.md)
