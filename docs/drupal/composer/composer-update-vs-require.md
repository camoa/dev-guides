---
description: "Choose composer update to move packages inside their current constraint, or composer require to change the constraint itself."
tldr: "Use composer update to move packages inside the constraints composer.json already declares, and composer require to change a constraint. A new constraint, such as a module's major move, is a require."
drupal_version: "10.x, 11.x"
---

# Composer: Update vs Require

## When to Use

Use `composer update` to move packages inside the constraints `composer.json` already declares, and `composer require` to change a constraint. A new constraint, such as a module's major move, is a `require`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| A module's newest release inside its constraint | `composer update drupal/<name> --with-all-dependencies` | Moves the lock only; `composer.json` stays as it is |
| A module's next major version | `composer require drupal/<name>:^2.0 --with-all-dependencies` | Writes the new root constraint, then updates the lock |
| Core, on a `drupal/core-recommended` project | `composer update "drupal/core-*" --with-all-dependencies` | Moves `core-recommended`, `core-composer-scaffold` and `core-project-message` together |
| Core, on a bare `drupal/core` project | `composer update drupal/core --with-dependencies` (drupal.org's form) | No `core-recommended` metapackage exists to move |
| Every package the constraints allow | `composer update` with no names | Routine maintenance; moves everything, edits nothing in `composer.json` |
| Core pinned to one minor | `composer require drupal/core-recommended:~11.2.12 drupal/core-composer-scaffold:~11.2.12` | A tilde constraint on the patch level holds the minor |
| Only Drupal projects | `composer update "drupal/*" --with-all-dependencies` | `update` accepts wildcards in package names |

## Pattern

```bash
# Inside the constraint: composer.json unchanged, composer.lock moves.
composer update drupal/token --with-all-dependencies

# New constraint: composer.json changes, then composer.lock moves.
composer require drupal/token:^2.0 --with-all-dependencies

# Core on a core-recommended project; the quotes stop the shell expanding *.
composer update "drupal/core-*" --with-all-dependencies

# What is behind? Direct Drupal dependencies only.
composer outdated "drupal/*" --direct
```

**Reference:** [Updating Drupal core via Composer](https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer), [Updating Modules and Themes using Composer](https://www.drupal.org/docs/updating-drupal/updating-modules-and-themes-using-composer), Composer `doc/03-cli.md` (update, require, outdated)

## How the Two Commands Differ

- **`update`** resolves dependencies and writes exact versions into `composer.lock`. Named packages, with or without wildcards, limit what may move. It never edits `composer.json`. `--with vendor/pkg:1.2.3` adds a temporary constraint for one run without editing the file.
- **Bare `update`** moves every package, root and transitive, to the newest version the constraints allow. The diff of `composer.lock` is the only record of what moved, so read it.
- **`require`** writes the constraint into `require` (or `require-dev` with `--dev`), then runs an update for the named packages. `--no-update` writes the constraint and stops; a later `composer update` resolves it.
- **`drupal/core-recommended`** pins core's own dependencies to the patch level core tested with. Bare `drupal/core` lets them reach newer minors, which needs more testing.
- **`composer outdated`** marks each package: `=` up to date, `!` a semver-compatible update exists, `~` the new version breaks backwards compatibility. `--strict` exits non-zero when anything is outdated.

## Common Mistakes

- Running `composer require` for a module already inside its constraint → Use `update`. `require` rewrites the constraint, often to one narrower than intended
- Updating `drupal/core` on a `core-recommended` project → Name `"drupal/core-*"`. `drupal/core` is locked by `core-recommended` and cannot move alone
- Leaving `"drupal/core-*"` unquoted → The shell may expand the `*` against local files. Quote it
- Treating bare `composer update` as a named update → It moves every package. Review the lock diff, or name packages
- Editing `composer.lock` by hand → A hand edit bypasses resolution. Let Composer write it

## See Also

- [Composer: Dependency Flags](composer-dependency-flags.md) — `-W` against `-w`, `--dry-run`, `-m`
- [Composer: Resolution Conflicts](composer-conflicts.md) — when an update does not resolve
- Recipe: [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) — the order of an update, from snapshot to commit
- Related: [OWASP Top 10 in Drupal](../security/owasp-top-10-in-drupal.md) — applying security updates promptly
- Related: [Composer module removal order](../best-practices/camoa/composer-module-removal-order.md) — removal is a different change
- Reference: [Composer CLI: update](https://getcomposer.org/doc/03-cli.md#update-u-upgrade)
