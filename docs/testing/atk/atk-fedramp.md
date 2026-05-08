---
description: ATK 2.1-beta FedRAMP compliance test pack — login attempt limits, CORS, session timeout, unauthorized access, Feeds, and Tugboat support.
tldr: ATK 2.1-beta adds FedRAMP-aligned tests (login lockout, CORS headers, session timeout, 403 checks) plus Feeds, Tugboat Drush, and persistent sessions. These tests pass does not mean the site is FedRAMP-compliant — they are one verification mechanism. Stay on 2.0 stable if you don't need these features.
drupal_version: "11.x"
---

# ATK FedRAMP & 2.1 Features

## When to Use

> Use ATK 2.1-beta when you need FedRAMP-aligned compliance tests, Feeds module testing, Tugboat support, or persistent sessions across tests. Stay on 2.0.0 stable for all other production D11 sites.

## Decision

| Need | Track |
|---|---|
| FedRAMP-aligned testing | 2.1-beta — accept beta status |
| Feeds workflow testing | 2.1-beta |
| Tugboat preview env support | 2.1-beta or roll your own |
| Production-stable D11 without those needs | 2.0.0 stable |

## Pattern

### What 2.1-beta adds

| Feature | Purpose |
|---|---|
| Login attempt limits test | Verify failed-login lockout behavior |
| CORS protection test | Verify cross-origin headers behave correctly |
| Session timeout test | Verify automatic session termination by inactivity |
| Unauthorized resource access test | Verify files / routes that should be 403 are 403 |
| Feeds test | Verify Feeds module import workflows |
| Tugboat Drush support | Configurable Drush invocation for Tugboat preview env |
| Persistent user sessions | Sessions persist across tests instead of relogin per test |

### Enabling the FedRAMP pack

```bash
# Install 2.1-beta
composer require 'drupal/automated_testing_kit:^2.1@beta'
drush en automated_testing_kit qa_accounts

# Pre-flight will now check FedRAMP-related config
drush atk:preflight

# Run the FedRAMP test suite
npx playwright test --grep "@fedramp"
```

### Compliance posture

FedRAMP-aligned tests are one verification mechanism alongside:
- Manual configuration review
- `drush security:check` baseline
- Module security advisory tracking
- Penetration testing
- Architecture review

### Beta caveats

- 2.1 is not stable as of 2026-05; production use means accepting beta status
- Tests may evolve before stable release; CI may show different results between beta point releases
- Watch `drupal.org/project/automated_testing_kit/issues` for breaking changes

## Common Mistakes

- **Wrong**: Treating "FedRAMP pack passes" as "the site is FedRAMP-compliant" → **Right**: these are tests, not a certification
- **Wrong**: Pinning to `^2.1` in production before stable release → **Right**: breaking changes possible between betas
- **Wrong**: Skipping the four FedRAMP tests because "they sound enterprisey" → **Right**: they catch real auth/session bugs valuable for any site

## See Also

- [Versions & Compatibility](atk-versions.md)
- [CI Integration](atk-ci-integration.md)
- Reference: https://www.drupal.org/project/automated_testing_kit/releases
