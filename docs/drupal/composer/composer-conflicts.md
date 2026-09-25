---
description: "Read a Composer resolution failure by finding the real conflict at the first or last lines of the problem list, then fix one culprit at a time."
tldr: "Use this when composer update or composer require prints 'Your requirements could not be resolved to an installable set of packages.' The real conflict is usually in the first or last few lines of the problem list."
drupal_version: "10.x, 11.x"
---

# Composer: Resolution Conflicts

## When to Use

Use this when `composer update` or `composer require` prints `Your requirements could not be resolved to an installable set of packages.` The real conflict is usually in the first or last few lines of the problem list.

## Decision

| If the output shows... | Then... | Why |
|---|---|---|
| A root requirement locked at its current version | Add `-W`, or name that package too | `-w` and a named update leave root requirements in place |
| A module that does not support the target core | Wait for its release, patch it, or pin core lower | Its `drupal/core` constraint excludes the target |
| A PHP version requirement | Upgrade PHP first | Composer refuses a release whose `php` requirement it does not meet |
| A version blocked by a security advisory | Choose another version or fix the advisory | `block-insecure` removes that version from resolution |
| A long chain of problems | Fix the first or last culprit, run again | One fix often clears the rest |

## Pattern

```bash
# Which packages stop core from reaching 11.3.0?
composer why-not drupal/core 11.3.0

# Same question, other name.
composer prohibits drupal/core 11.3.0

# Undo a failed attempt: files from git, then vendor/ from the restored lock.
git checkout -- composer.json composer.lock
composer install
```

**Reference:** [Updating Drupal core via Composer](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer) (`prohibits`, `why-not`), Composer `doc/03-cli.md`

## Reading the Output

Composer numbers its problems, and each one lists a chain of requirements. Carlos Ospina's talk ["From Fear to Freedom"](https://www.youtube.com/watch?v=UGfrvVQjCQw) gives the reading heuristic: the real conflict sits in the first or last few lines. The lines in between are consequences of it. Name the one package that causes it, fix that, and run again. Fixing several at once hides which fix worked.

Composer changes only code. A failed run leaves only files git can restore: `composer.json`, `composer.lock`, and scaffold files. `composer install` then rebuilds `vendor/` from the restored lock. No database step is needed to undo a Composer run.

## Common Mistakes

- Reading the middle of a long problem list → Start at the first and last lines
- Fixing every listed conflict in one edit → Fix one culprit, run again, then the next
- Loosening a constraint to `*` to make it resolve → That removes the guard that stopped a breaking version. Find the package that blocks
- Deleting `composer.lock` to "start fresh" → That turns a named update into a bare update of everything, with no record of what moved
- Adding an audit ignore to get past a blocked version → A blocked version is a security finding; see [Composer: Audit](composer-audit.md)

## See Also

- [Composer: Dependency Flags](composer-dependency-flags.md) — `-w` is a common cause
- [Composer: Audit](composer-audit.md) — blocked insecure versions
- Recipe: [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) — a resolution failure is a stopping point
- Reference: [Composer CLI: prohibits / why-not](https://getcomposer.org/doc/03-cli.md#prohibits-why-not)
