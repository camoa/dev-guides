---
description: The drupalci pipeline and gitlab_templates — which CI jobs run on your MR, what each does, job blocking behavior, key variables, and how to override templates
tldr: "Contrib projects opt into the DA-managed pipeline via a one-line include in `.gitlab-ci.yml` (currently gitlab_templates v1.15.4). Only `composer` and `phpcs` are blocking by default; all other validation jobs are `allow_failure: true` unless the maintainer enforces them."
drupal_version: "11.x"
---

# The drupalci Pipeline & gitlab_templates

## When to Use

> Read this when you need to understand which CI jobs run on your merge request, what each job does, and how the shared template system works. This is the reference for interpreting a pipeline result.

## How the Pipeline is Wired

Contrib projects opt into the Drupal Association's centrally-managed pipeline by adding a one-line include to their `.gitlab-ci.yml`. This keeps ~2,000 contrib projects on a shared, maintained pipeline without each project managing its own CI configuration from scratch.

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

## Job Set (v1.15.4)

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

**Critical fact:** all linting and validation jobs except `composer` and `phpcs` default to `allow_failure: true` — they are **non-blocking**. A maintainer opts into enforcement per job:

```yaml
# Make phpstan blocking on your project
phpstan:
  allow_failure: false
```

**v1.15.0 change:** `OPT_IN_TEST_*` variant jobs (previous major, next minor, max PHP) moved to **manual trigger**. They no longer auto-run. A green pipeline can simply mean they were never triggered — do not imply coverage from opt-in variants unless you explicitly triggered them.

## Key Variables

| Variable | Purpose |
|---|---|
| `_TARGET_CORE` | Drupal core version to test against (e.g. `"^11"`) |
| `_TARGET_PHP` | PHP version (default `8.2` on D11) |
| `_TARGET_DB_TYPE` | Database type |
| `_GITLAB_TEMPLATES_REF` | Template version pin (DA-managed) |
| `SKIP_PHPCS`, `SKIP_PHPSTAN`, … | Opt-out a job entirely |
| `OPT_IN_TEST_PREVIOUS_MAJOR` | Enable previous-major variant (manual trigger) |
| `OPT_IN_TEST_NEXT_MINOR` | Enable next-minor variant (manual trigger) |
| `_PHPUNIT_CONCURRENT` | `1` → switches phpunit to `run-tests.sh` concurrency mode |
| `_PHPUNIT_EXTRA` | Extra args passed to the phpunit job |
| `SYMFONY_DEPRECATIONS_HELPER` | Controls deprecation handling in tests |

## How the phpunit Job Runs

The `phpunit` job runs:
```
vendor/bin/phpunit -c web/core/phpunit.xml.dist --webroot=web
```

When `_PHPUNIT_CONCURRENT: 1` it switches to `core/scripts/run-tests.sh`. The **binding constraint** is not the wrapper — it is the core `phpunit.xml.dist`, which carries `failOnWarning="true"` (and `failOnPhpunitWarning` in Drupal 11.3.x). Tests fail on warnings regardless of wrapper.

## Pinned Tool Versions (resolved from core, never hardcoded)

| Tool | Drupal 11.x | Drupal 10.x |
|---|---|---|
| PHPUnit | `^11.5.50` | `^9.5` / `^9.6` |
| PHPStan | `^1.12.27 \|\| ^2.1.54` | `^1.x` only |
| `mglaman/phpstan-drupal` | `^1.3.9 \|\| ^2.0.15` | `^1.x` |
| `drupal/coder` | `^8.3.30` | `^8.3.x` |

Do not hardcode these — resolve them from the target core's `drupal/core-dev` at setup time.

## Reading a Pipeline Result

Pipeline stages run in order: **Build → Validation → Test**. Per-job status:

- **Green** — passed
- **Red** — failed; if `allow_failure: true`, the pipeline continues
- **Yellow (manual)** — opt-in variant, not yet triggered; not covered
- **Gray (skipped)** — skipped by rule or `SKIP_*` variable

A pipeline shows "passed" while `allow_failure` jobs are red and manual jobs un-run. **The MR is mergeable only when all non-`allow_failure`, non-manual jobs pass.** The Test Report tab (from `junit` artifacts) surfaces per-test failures inline.

## How Projects Override the Templates

Jobs are defined via hidden templates (`.job-base`, `.job-rule`) using YAML `extends:` and `!reference`. Override without copying the template:

```yaml
# Override a specific job in your .gitlab-ci.yml
phpcs:
  allow_failure: false           # make non-blocking

phpstan:
  variables:
    _PHPSTAN_LEVEL: "8"          # increase strictness

some-job:
  when: never                    # skip entirely
```

## Common Mistakes

- Reading a "passed" pipeline as full CI coverage when opt-in variant jobs were never triggered — those tests are unrun, not passing.
- Assuming linting failures block the MR — check each job's `allow_failure` setting per project.
- Pinning `_GITLAB_TEMPLATES_REF` without also setting `_CURL_TEMPLATES_REF` — they must match.
- Running phpunit without the core config — the `failOnWarning` behavior lives in `core/phpunit.xml.dist`, not the wrapper.

## See Also

- [Reproducing drupalci Failures Locally](reproducing-drupalci-failures-locally.md)
- [Drupal Coding Standards at CI Parity](drupal-coding-standards-ci-parity.md)
- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- Reference: [project.pages.drupalcode.org/gitlab_templates/](https://project.pages.drupalcode.org/gitlab_templates/)
- Reference: [drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/gitlab-ci](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/gitlab-ci)
