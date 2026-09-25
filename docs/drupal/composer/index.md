---
description: Drupal Composer — update vs require, dependency flags, patches, composer audit, and reading a resolution conflict
tracks: []
guide-meta:
  concepts:
    - composer update
    - composer require
    - --with-all-dependencies
    - --with-dependencies
    - --dry-run
    - --minimal-changes
    - cweagans/composer-patches
    - composer.lock
    - composer.json
    - composer audit
    - composer audit --locked
    - patches.lock.json
    - composer why-not
    - composer prohibits
    - dependency resolution conflicts
  not:
    - module removal order (see drupal/best-practices/camoa)
    - database updates and config export (see drupal/config-management)
  requires: []
  complements:
    - agentic-recipes/drupal/dependency-update
    - drupal/security
    - drupal/github-actions
    - drupal/config-management
  category: drupal
---

# Drupal Composer

Composer mechanics for updating a Drupal site's dependencies: `update` against `require`, the dependency flags, `--dry-run`, patches, `composer audit`, and reading a resolution failure. The agentic recipe [`drupal_dependency_update`](../../agentic-recipes/drupal/dependency-update.md) prescribes the order of the steps; these guides do not repeat it.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Update a module within its constraint, move it to a new major version, update Drupal core, or update every package the constraints allow | [Composer: Update vs Require](composer-update-vs-require.md) | Use composer update to move packages inside the constraints composer.json already declares, and composer require to change a constraint. A new constraint, such as a module's major move, is a require. |
| Choose between `-W` and `-w`, preview an update without writing anything, or keep an update's side effects small | [Composer: Dependency Flags and Dry Run](composer-dependency-flags.md) | Use these flags to decide which of a named package's dependencies may move, and --dry-run to see the result before anything is written. The usual choice is --with-all-dependencies, because --with-dependencies leaves root requirements locked. |
| Apply, inventory or troubleshoot a patch, or know whether a failed patch stopped Composer | [Composer: Patches](composer-patches.md) | Use cweagans/composer-patches to apply a fix to core or a contrib package before its maintainer releases it. Read its output on every run, because the 1.x line skips a failed patch and Composer still succeeds. |
| Check the lock file for advisories and abandoned packages, or accept one | [Composer: Audit](composer-audit.md) | Use composer audit --locked to check the lock file for packages with security advisories and for abandoned packages. On Composer 2.10 and later it exits 0 when clean and 1 when it finds anything. |
| Read a failed resolution and fix it | [Composer: Resolution Conflicts](composer-conflicts.md) | Use this when composer update or composer require prints 'Your requirements could not be resolved to an installable set of packages.' The real conflict is usually in the first or last few lines of the problem list. |
