---
description: ATK pre-flight checks — YAML-defined site-readiness assertions that run before any test, catching misconfigured environments early.
tldr: Pre-flight runs before any test via atk_prerequisites.yml and aborts with a structured error if any check fails. Run it in CI always — that is exactly where misconfigured environments produce confusing test failures. Extend it only when your tests assume state that isn't enforced by Composer or config-import.
drupal_version: "11.x"
---

# ATK Pre-flight Checks

## When to Use

> Use ATK pre-flight when running against a freshly-stood-up environment that may not be fully configured. It is highest-value in CI where misconfigured environments cause confusing cascading failures.

## Decision

| Add a custom check when... | Skip when... |
|---|---|
| Your tests assume a specific module is enabled | Module is enforced by Composer dep |
| Your tests assume a specific config value | Config is enforced via config-import in the bootstrap |
| Your tests need a specific user not in `qa_accounts` | Test creates the user as part of setup |

## Pattern

Pre-flight runs before any test executes. Configured via YAML:

```yaml
# atk_prerequisites.yml — example shape; see the canonical 2.0.x version in the repo
required_modules:
  - automated_testing_kit
  - qa_accounts
  - reroute_email

mail:
  reroute_address: qa@example.com
  reroute_enabled: true

users:
  - name: site_admin
    role: administrator

settings:
  - { key: system.site:mail, value: 'noreply@example.com' }
```

If any check fails, the test run aborts with a structured error pointing at the failing item.

Documented built-in checks:
- Required modules enabled (`automated_testing_kit`, `qa_accounts`, `reroute_email`)
- Outbound email rerouted to a safe address
- Required QA users exist with expected roles
- Configuration values match

```bash
drush atk:preflight
```

## Common Mistakes

- **Wrong**: Skipping pre-flight in CI → **Right**: its value is highest exactly there, where misconfigured environments cause confusing test failures
- **Wrong**: Pre-flight failing on prod-like env mistakes (real mail address, real users) → **Right**: that's correct behavior; pre-flight is protecting you
- **Wrong**: Hardcoding email checks for prod → **Right**: pre-flight is for test environments only

## See Also

- [Installation](atk-installation.md)
- [CI Integration](atk-ci-integration.md)
- Reference: `atk_prerequisites.yml` in the 2.0.x branch at `git.drupalcode.org/project/automated_testing_kit`
