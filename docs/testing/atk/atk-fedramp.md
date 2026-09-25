---
description: "What ATK 2.1.0-beta's FedRAMP-oriented tests need, how to run them, and the compliance-posture caveat."
tldr: "2.1.0-beta adds FedRAMP-oriented tests (rapid login, CORS/CSRF, session termination, unauthorized access, HTTPS redirect, security headers), Feeds tests and Tugboat routing — Playwright ships 6 FedRAMP spec files, Cypress 4. A green run covers some control areas; it is not an audit, and 2.1 has had betas only since 2025-08-05."
drupal_version: "11.x"
---

# ATK FedRAMP & 2.1 Features

## When to Use

> Running ATK 2.1-beta for its FedRAMP-oriented tests, the Feeds test, Tugboat support or session reuse.

## What 2.1-Beta Adds

| Feature | Where |
|---|---|
| Rapid logins and failed-login limits (1200, 1201) | `atk_fedramp/atk_rapid_login` |
| CORS and CSRF (1210, 1211; PW also 1213) | `atk_fedramp/atk_cors` |
| Session termination by inactivity (1220; PW also 1221, 1222) | `atk_session.spec.js` / `atk_session_termination.cy.js` |
| Unauthorised file and route access (PW 1230, 1231, 1234, 1235; CY 1230–1232) | `atk_access.spec.js` / `atk_unathorized_access.cy.js` |
| HTTP to HTTPS redirect (PW 1240) | `atk_encryption.spec.js` |
| Security headers and session cookie flags (PW 1250, 1251) | `atk_security_headers.spec.js` |
| Feeds import (PW 1180; CY 1180, 1181 under `ATK-PW-` IDs) | `atk_feeds/` |
| Tugboat Drush routing | `tugboat` config block; `execTugboatDrush()` (Cypress command; unexported in Playwright) |
| Session reuse | `atk_setup/atk_session.setup.js`, `getUserPage()` |

Playwright ships 6 FedRAMP spec files; Cypress ships 4.

## Pattern: what the tests need

| Test | Needs (from the test's own comments) |
|---|---|
| 1200 | `session_management`, with session limiting on |
| 1201 | `login_security`, "User failed attempts" set to 3 |
| 1220 | `autologout`, and an `autologout_testing` role |
| 1230 | `file:create`; skipped on `ddev.site` by `skipIfLocal()` |
| 1235 | A private file system |
| 1240 | HTTPS; skipped on `ddev.site` |

The 2.1 demo recipe installs these modules and the `autologout_testing` role. The demo submodule sets up private files.

## Compliance Posture

These tests cover **some FedRAMP control areas**. They are not a FedRAMP audit. Use them alongside configuration review, advisory tracking, penetration testing and architecture review.

## Pattern: running the pack

```bash
composer require 'drupal/automated_testing_kit:2.1.0-beta5' 'drupal/qa_accounts:^1.1' 'drupal/login_security:^2.0'
drush en automated_testing_kit qa_accounts login_security

npx playwright test --grep @fedramp
npx playwright test --grep ATK-PW-1240      # 1240 has no tags; match its title
```

The pre-flight only **warns** when `login_security` is missing.

Cypress FedRAMP tests use `@ATK-1200`-style ID tags, not `@ATK-CY-1200`. `--env grepTags=@fedramp` misses 1231 and 1232, which have no tags.

## Beta Caveats

- 2.1 has had no stable release since its first pre-release, 2.1.0-beta0 (2025-08-05)
- Tests may change between betas
- Watch `drupal.org/project/issues/automated_testing_kit` for breaking changes

## Decision

| Need | Release |
|---|---|
| FedRAMP-oriented tests | 2.1.0-beta |
| Feeds workflow test | 2.1.0-beta |
| Tugboat Drush routing | 2.1.0-beta |
| Stable D11 without those | 2.0.0 |

## Common Mistakes

- **Treating a green FedRAMP run as compliance** — these are tests, not a certification
- **Expecting 1230 and 1240 to run under DDEV** — `skipIfLocal()` skips them there
- **Running FedRAMP tests without their modules** — they fail for setup reasons, not security reasons

## See Also

- [Versions & Compatibility](atk-versions.md)
- [Test Catalog](atk-test-catalog.md)
- [CI Integration](atk-ci-integration.md)
