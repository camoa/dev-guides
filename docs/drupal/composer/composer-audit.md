---
description: "Run composer audit --locked to check the lock file for advisories and abandoned packages, and accept a finding with a reviewable reason."
tldr: "Use composer audit --locked to check the lock file for packages with security advisories and for abandoned packages. On Composer 2.10 and later it exits 0 when clean and 1 when it finds anything."
drupal_version: "10.x, 11.x"
---

# Composer: Audit

## When to Use

Use `composer audit --locked` to check the lock file for packages with security advisories and for abandoned packages. On Composer 2.10 and later it exits 0 when clean and 1 when it finds anything.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| To audit what the project will deploy | `composer audit --locked` | Reads `composer.lock`, whatever `vendor/` holds |
| A machine-readable result | `--format=json` | Also `table`, `plain`, `summary` |
| To accept one advisory (2.10+) | `config.policy.advisories.ignore-id` with a reason | The `policy` block replaces most of `config.audit` |
| To accept one advisory (before 2.10) | `config.audit.ignore` with a reason | Deprecated in 2.10, still read when `policy` is absent |
| To accept an abandoned package (2.10+) | `config.policy.abandoned.ignore` with a reason | Accepts names and patterns |
| To accept an abandoned package (2.9.x) | `config.audit.ignore-abandoned` with a reason | Added in 2.9.0; deprecated in 2.10; not available on 2.7–2.8 |

## Pattern

```json
{
  "config": {
    "policy": {
      "advisories": {
        "ignore-id": {
          "GHSA-xxxx-xxxx-xxxx": "Affected path not reachable; the module's REST resource is disabled."
        }
      },
      "abandoned": {
        "ignore": {
          "vendor/legacy-lib": "Transitive via drupal/foo; removal tracked for next release."
        }
      }
    }
  }
}
```

**Reference:** Composer `doc/06-config.md` (policy, audit) and `CHANGELOG.md` at tag 2.10.3

## What Audit Checks and Blocks

- **Exit code** — from 2.10.0, always 0 or 1. From 2.8.4 to 2.9.x it was 1 for advisories, 2 for abandoned, 3 for both. A CI step that tests `-eq 1` on an older Composer misses abandoned packages.
- **Abandoned packages fail by default** — `audit.abandoned` defaults to `fail` since 2.7; it was `report` in 2.6. In the 2.10 `policy` block, `policy.abandoned.audit` also defaults to `fail`.
- **Insecure versions are blocked during resolution** — `audit.block-insecure`, added in 2.9 and defaulting to `true`, stops `update`, `require` and `remove` from choosing a version with an active advisory. In 2.10 this is `policy.advisories.block`. A blocked version shows up as a resolution failure, not as an audit finding.
- **`policy` replaces `audit`** — the legacy `config.audit` keys are read only when the matching `policy` section is absent, all or nothing per policy. Do not split one policy across both blocks.
- **Implicit audits** — `update` and `require` audit after they finish. `--no-audit` skips it. Since 2.6.2 a finding in that implicit audit does not change their exit code, so run `composer audit` on its own.

## Security Best Practices

- Every accepted entry carries a reason a reviewer can check: why the advisory does not apply, or when the abandoned package leaves. An ignore with no reason is a hidden vulnerability
- Ignore by advisory ID, never by package name. A package-name ignore silences future advisories too
- Do not use `--ignore-severity` in CI to make a build pass. It hides every advisory at that level, including new ones
- Review accepted entries on every update. Remove each one the update resolves
- `composer audit` is a gate on every build; the [code quality checks guide](../github-actions/code-quality-checks.md) covers wiring it into CI

## Common Mistakes

- Auditing `vendor/` instead of the lock → Use `--locked`, so a stale install does not hide a finding
- Using `config.audit.ignore` on a 2.10 project that also has a `policy.advisories` block → The legacy key is ignored. Move it to `policy.advisories.ignore-id`
- Accepting an advisory to unblock an update → Fix the resolution first; an ignore is for a finding that does not apply

## See Also

- [Composer: Update vs Require](composer-update-vs-require.md) — the update that resolves most findings
- Related: [Code quality checks](../github-actions/code-quality-checks.md) — `composer audit` in CI
- Related: [OWASP Top 10 in Drupal](../security/owasp-top-10-in-drupal.md) — vulnerable components
- Recipe: [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) — an unaccepted finding stops the run
- Reference: [Composer config: policy](https://getcomposer.org/doc/06-config.md#policy)
