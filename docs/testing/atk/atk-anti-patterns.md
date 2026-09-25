---
description: "19 wrong-vs-right ATK mistakes across URLs, commands, config, testing and compliance."
tldr: "The most repeated ATK mistakes: following dead PerformantLabs GitHub URLs, running drush atk:preflight or drush testor:*, selecting [data-qa-id], enabling ATK or qa_accounts on production, and treating a green FedRAMP run as compliance certification."
drupal_version: "11.x"
---

# ATK Anti-Patterns

## When to Use

> Before adopting ATK, or when debugging unexpected failures.

## Common Mistakes

- **Wrong**: linking to `github.com/PerformantLabs/atk-cypress` or `atk-playwright` → **Right**: those 404; use `git.drupalcode.org/project/automated_testing_kit`
- **Wrong**: running `drush atk:preflight` → **Right**: the pre-flight runs inside the test run (`setup` project or Cypress `before()`)
- **Wrong**: running `drush testor:*` → **Right**: Testor is its own CLI: `testor snapshot:restore --name=qa`
- **Wrong**: selecting `[data-qa-id=…]` → **Right**: ATK adds only body classes and `data-media-id`; use Drupal's markup or your own attribute
- **Wrong**: importing from `../helpers/atk` → **Right**: `import * as atkCommands from '../support/atk_commands'`
- **Wrong**: `drush recipe modules/contrib/automated_testing_kit_demo_recipe` → **Right**: `drush recipe ../recipes/automated_testing_kit_demo_recipe`
- **Wrong**: copying from `tests/playwright/` or `js-helpers/` → **Right**: run `module_support/atk_setup playwright`
- **Wrong**: `drushCmd: 'drush'` against DDEV from the host → **Right**: `drushCmd: 'ddev drush'`
- **Wrong**: putting Terminus or SSH in `drushCmd` → **Right**: use the `pantheon` or `targetSite` block
- **Wrong**: editing `tests/atk_*` in place → **Right**: copy to your own directory; `atk_setup` overwrites them
- **Wrong**: running the catalog on a bare site → **Right**: apply the demo recipe, or enable each suite's modules
- **Wrong**: removing `sanitize.command` from `.testor.yml` → **Right**: keep it; `snapshot:create` sanitises by default
- **Wrong**: committing `.testor_secret.yml` → **Right**: keep secrets in it or in environment variables
- **Wrong**: enabling ATK or `qa_accounts` in production → **Right**: test sites only; ATK serves `data/` to anonymous users and `qa_accounts` sets password = username
- **Wrong**: installing both `drupal/qa_accounts` and `performant-labs/qa_accounts` → **Right**: pick one; they share a machine name
- **Wrong**: treating a FedRAMP pass as certification → **Right**: it is one check among several
- **Wrong**: using 2.1 steps on a 2.0.0 site → **Right**: check [Versions & Compatibility](atk-versions.md) first
- **Wrong**: expecting ATK to ship visual regression → **Right**: layer Playwright's VR on top
- **Wrong**: tests that depend on each other's state → **Right**: each test cleans up; restore a Testor snapshot for a baseline

## See Also

- [ATK Overview](atk-overview.md)
- [Selector Hooks](atk-selector-hooks.md)
- [Testor Snapshots](atk-testor.md)
- [FedRAMP & 2.1 Features](atk-fedramp.md)
