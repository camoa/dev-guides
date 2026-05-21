---
description: The drupalci pipeline and gitlab_templates — which CI jobs run on your MR, what each does, job blocking behavior, key variables, and how to override templates
tldr: "Contrib projects opt into the DA-managed pipeline via a one-line include in `.gitlab-ci.yml` (currently gitlab_templates v1.15.4). Only `composer` and `phpcs` are blocking by default; all other validation jobs are `allow_failure: true` unless the maintainer enforces them."
drupal_version: "11.x"
---

# The drupalci Pipeline & gitlab_templates

## When to Use

> Read this when you need to understand which CI jobs run on your merge request, what each job does, and how the shared template system works. This is the reference for interpreting a pipeline result.

## How the Pipeline is Wired

```yaml
# .gitlab-ci.yml (contrib module)
include:
  - project: 'project/gitlab_templates'
    file: '/includes/include.drupalci.main.yml'
    ref: '$_GITLAB_TEMPLATES_REF'
  - project: 'project/gitlab_templates'
    file: '/includes/include.drupalci.variables.yml'
    ref: '$_GITLAB_TEMPLATES_REF'
  - project: 'project/gitlab_templates'
    file: '/includes/include.drupalci.workflows.yml'
    ref: '$_GITLAB_TEMPLATES_REF'

variables:
  _TARGET_CORE: "^11"
  _TARGET_PHP: "8.3"
```

`$_GITLAB_TEMPLATES_REF` is a DA-managed variable that auto-updates to the latest stable tag (currently **v1.15.4**). Pinning to a fixed tag requires setting both `_GITLAB_TEMPLATES_REF` and `_CURL_TEMPLATES_REF` to match.

## Decision

| Stage | Job | Default blocking? |
|---|---|---|
| Build | `composer` | **Yes** |
| Validation | `composer-lint` | `allow_failure: true` |
| Validation | `phpcs` | **Yes** |
| Validation | `phpstan` | `allow_failure: true` |
| Validation | `cspell` | `allow_failure: true` |
| Validation | `eslint` | `allow_failure: true` |
| Validation | `stylelint` | `allow_failure: true` |
| Validation | `secret-detection` | `allow_failure: true` |
| Test | `phpunit` | **Yes** |
| Test | `nightwatch` | `allow_failure: true` |
| Test | `test-only changes` | Conditional |
| Contrib | `upgrade-status` | Opt-in (manual trigger) |
| Contrib | `drupal-cms` | Opt-in |

## Pattern

```yaml
# Make phpstan blocking on your project
phpstan:
  allow_failure: false

# Override a specific job in your .gitlab-ci.yml
phpcs:
  allow_failure: false

phpstan:
  variables:
    _PHPSTAN_LEVEL: "8"

some-job:
  when: never    # skip entirely
```

**v1.15.0 change:** `OPT_IN_TEST_*` variant jobs moved to **manual trigger** — they no longer auto-run. A green pipeline can mean they were never triggered.

## Key Variables

| Variable | Purpose |
|---|---|
| `_TARGET_CORE` | Drupal core version to test against (e.g. `"^11"`) |
| `_TARGET_PHP` | PHP version (default `8.2` on D11) |
| `_GITLAB_TEMPLATES_REF` | Template version pin (DA-managed) |
| `SKIP_PHPCS`, `SKIP_PHPSTAN`, … | Opt-out a job entirely |
| `OPT_IN_TEST_PREVIOUS_MAJOR` | Enable previous-major variant (manual trigger) |
| `_PHPUNIT_CONCURRENT` | `1` → switches phpunit to `run-tests.sh` concurrency mode |
| `SYMFONY_DEPRECATIONS_HELPER` | Controls deprecation handling in tests |

## Pinned Tool Versions

| Tool | Drupal 11.x | Drupal 10.x |
|---|---|---|
| PHPUnit | `^11.5.50` | `^9.5` / `^9.6` |
| PHPStan | `^1.12.27 \|\| ^2.1.54` | `^1.x` only |
| `mglaman/phpstan-drupal` | `^1.3.9 \|\| ^2.0.15` | `^1.x` |
| `drupal/coder` | `^8.3.30` | `^8.3.x` |

Do not hardcode these — resolve from the target core's `drupal/core-dev` at setup time.

## Common Mistakes

- **Wrong**: Reading a "passed" pipeline as full CI coverage when opt-in variant jobs were never triggered → **Right**: Manually trigger `OPT_IN_TEST_*` jobs to validate coverage
- **Wrong**: Assuming linting failures block the MR → **Right**: Check each job's `allow_failure` setting per project
- **Wrong**: Pinning `_GITLAB_TEMPLATES_REF` without also setting `_CURL_TEMPLATES_REF` → **Right**: They must match
- **Wrong**: Running phpunit without the core config → **Right**: `failOnWarning` behavior lives in `core/phpunit.xml.dist`, not the wrapper

## See Also

- [Reproducing drupalci Failures Locally](reproducing-drupalci-failures-locally.md)
- [Drupal Coding Standards at CI Parity](drupal-coding-standards-ci-parity.md)
- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- Reference: [project.pages.drupalcode.org/gitlab_templates/](https://project.pages.drupalcode.org/gitlab_templates/)
- Reference: [drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/gitlab-ci](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/gitlab-ci)
