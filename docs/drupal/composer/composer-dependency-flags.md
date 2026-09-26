---
description: "Choose -W over -w so a shared root dependency can move, and use --dry-run to preview an update before anything is written."
tldr: "Use these flags to decide which of a named package's dependencies may move, and --dry-run to see the result before anything is written. The usual choice is --with-all-dependencies, because --with-dependencies leaves root requirements locked."
drupal_version: "10.x, 11.x"
---

# Composer: Dependency Flags and Dry Run

## When to Use

Use these flags to decide which of a named package's dependencies may move, and `--dry-run` to see the result before anything is written. The usual choice is `--with-all-dependencies`, because `--with-dependencies` leaves root requirements locked.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| The named packages and every dependency, root requirements included | `--with-all-dependencies` / `-W` | A shared dependency that is also in `composer.json` can move |
| The named packages and only non-root dependencies | `--with-dependencies` / `-w` | Root requirements stay at their locked version |
| The same, on `require` | `--update-with-all-dependencies` / `-W`, or `--update-with-dependencies` / `-w` | `require` accepts `--with-all-dependencies` and `--with-dependencies` as aliases |
| The fewest transitive moves | Add `--minimal-changes` / `-m` | Changes a transitive dependency only when the new constraint demands it |
| A preview | Add `--dry-run` | Resolves and prints the operations; writes nothing |

## Pattern

```bash
# Preview: prints the lock operations; composer.json and composer.lock stay untouched.
composer update drupal/webform --with-all-dependencies --dry-run

# Nothing to move prints this line on standard error:
#   Nothing to modify in lock file

# Move the module and its dependencies, changing as little else as possible.
composer update drupal/webform -W -m
```

**Reference:** Composer `doc/03-cli.md` (update and require options), `src/Composer/Installer.php`, `src/Composer/Command/RequireCommand.php` at tag 2.10.3

## What Each Flag Does

- **`-W` / `--with-all-dependencies`** — updates the named packages' dependencies, including those that are also root requirements. drupal.org writes the long form in its module and `core-recommended` instructions.
- **`-w` / `--with-dependencies`** — updates the named packages' dependencies, except those that are root requirements. When a new release needs a newer version of a package `composer.json` also requires, `-w` keeps that package locked, and the update fails to resolve.
- **`require`'s names** — the primary names are `--update-with-dependencies` and `--update-with-all-dependencies`. `--with-dependencies` and `--with-all-dependencies` are aliases, and `-w` and `-W` are the short forms.
- **`-m` / `--minimal-changes`** — since Composer 2.7. With `-w` or `-W`, it changes transitive dependencies only where the new constraints demand it.
- **`--dry-run`** — turns on verbose output and turns off scripts, operations, the lock write and the autoloader dump. It prints `Lock file operations: N installs, N updates, N removals` and each operation. On `require`, `--dry-run` never writes `composer.json`. A package already current prints `Nothing to modify in lock file` on standard error, so a check that reads only standard output sees nothing.
- **`--no-update`** on `require` — writes the constraint only. Several `require --no-update` calls followed by one `composer update` resolve all the new constraints together.

## Common Mistakes

- Defaulting to `-w` because it sounds safer → It fails whenever a shared dependency is a root requirement. Use `-W`, and add `-m` if you want fewer moves
- Treating a clean `--dry-run` as proof the update works → It proves resolution only. Patches, scripts and `updatedb` do not run in a dry run
- Grepping standard output for `Nothing to modify in lock file` → Composer prints it on standard error. Redirect `2>&1` first
- Running several `require` calls, each with its own update → Use `--no-update` on each, then one `composer update`, so the constraints resolve together

## See Also

- [Composer: Update vs Require](composer-update-vs-require.md) — which command to run
- [Composer: Resolution Conflicts](composer-conflicts.md) — reading the failure `-w` often produces
- Recipe: [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) — where the dry run sits in the order
- Reference: [Composer CLI: require](https://getcomposer.org/doc/03-cli.md#require-r)
