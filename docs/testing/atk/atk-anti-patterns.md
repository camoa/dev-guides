---
description: ATK anti-patterns — the most common wrong choices across URLs, versions, configuration, test management, and compliance.
tldr: The most damaging ATK mistakes are following dead GitHub URLs, skipping the demo recipe, editing shipped tests in-place, hardcoding drushCmd or credentials, and treating FedRAMP test passes as compliance certification.
drupal_version: "11.x"
---

# ATK Anti-Patterns

## When to Use

> Use this guide as a pre-flight sanity check before deploying ATK, or when debugging unexpected failures.

## Pattern

| Wrong | Right |
|---|---|
| Linking to `github.com/PerformantLabs/atk-cypress` or `atk-playwright` | Those URLs 404; canonical is `git.drupalcode.org/project/automated_testing_kit` |
| Pinning to ATK 1.x for D11 | 2.0+ for D11; 1.x is D10 maintenance |
| Assuming a `ddev-atk` addon exists | Use `ddev/github-action-setup-ddev` + ATK module install |
| Editing ATK's shipped tests in-place | Copy + rename; modifications lost on upgrade |
| Running ATK's tests without the demo recipe | Apply `automated_testing_kit_demo_recipe` first; tests assume content/users |
| Hardcoding `drushCmd: 'drush'` against DDEV | Use `ddev drush` or the configurable invocation |
| Pushing un-sanitised Testor snapshots | Always `--sanitize` |
| Storing AWS keys in `.testor.yml` | Env vars / CI secrets only |
| Skipping pre-flight in CI | Pre-flight catches misconfigured environments before tests pile up errors |
| Treating FedRAMP test pass as compliance certification | Tests are one verification; full FedRAMP requires audit |
| Pinning to 2.1-beta in production | Stay on 2.0 stable until 2.1 ships stable |
| Mixing both runners on the same component | One runner per project |
| Expecting ATK to ship visual regression | Layer Playwright's native VR on top |
| Relying on volatile Drupal class names in selectors | Use ATK's selector hook attribute (`data-qa-id` historically) |
| Making tests depend on each other's state | Each test owns its setup + cleanup; use Testor for baseline reset |

## See Also

- [ATK Overview](atk-overview.md)
- [Selector Hooks](atk-selector-hooks.md)
- [Testor Snapshots](atk-testor.md)
- [FedRAMP & 2.1 Features](atk-fedramp.md)
