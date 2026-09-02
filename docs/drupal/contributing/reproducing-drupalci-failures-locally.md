---
description: Reproducing drupalci CI failures locally — DDEV inner loop, gitlab-ci-local, and per-job debugging commands for phpcs, phpstan, phpunit, eslint, and stylelint
tldr: "Use `ddev phpcs`/`ddev phpunit` (ddev-drupal-contrib) for the day-to-day inner loop, or `drupal-ci-local` to run exact CI jobs locally. There is no Docker-free route."
drupal_version: "11.x"
---

# Reproducing drupalci Failures Locally

## When to Use

> Use this when a CI job fails on your MR and you need to reproduce the failure locally before pushing a fix — faster than pushing a commit and waiting for a full pipeline run.

## Decision

| Reproduction route | Best for | Requirement |
|---|---|---|
| `ddev phpcs` / `ddev phpunit` (via `ddev-drupal-contrib`) | Day-to-day inner loop; contrib module development | Docker + DDEV add-on already installed |
| `gitlab-ci-local` (`drupal-ci-local` wrapper) | Running exact CI jobs locally; debugging job internals | Docker |
| Push a commit and read the pipeline | Browser/Nightwatch tests; full multi-version matrix | None beyond a GitLab account |

**There is no Docker-free route** to run the CI jobs locally. The pipeline jobs run inside Docker containers; both reproduction routes wrap Docker.

## Steps — DDEV Route (inner loop)

When `ddev-drupal-contrib` is set up (see [DDEV + Add-ons](ddev-contribution-environment.md)):

```bash
ddev phpcs                    # runs phpcs at CI standards
ddev phpstan                  # runs phpstan
ddev phpunit web/modules/contrib/my_module/tests   # runs phpunit with core config
ddev eslint                   # JS linting
ddev stylelint                # CSS linting
```

## Steps — gitlab-ci-local Route (full job reproduction)

```bash
# Install drupal-ci-local (wraps the gitlab-ci-local npm package)
npm install -g @laktawan/drupal-ci-local    # or equivalent package

# Run all jobs
drupal-ci-local

# Run a single job by name
drupal-ci-local phpunit
drupal-ci-local phpcs

# Artifacts land in .gitlab-ci-local/
```

## Per-Job Debugging

**phpcs failure:**
```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice \
  --extensions=php,module,inc,install,test,profile,theme,info,txt,md,yml \
  path/to/module
# Auto-fix locally (never runs in CI):
vendor/bin/phpcbf --standard=Drupal,DrupalPractice path/to/module
```

**phpstan failure:**
```bash
vendor/bin/phpstan analyse -c phpstan.neon
# Baseline known issues (do not suppress real errors):
vendor/bin/phpstan analyse -c phpstan.neon --generate-baseline
```

**phpunit failure — distinguish the failure type:**

- *Test failure* — assertion failed; fix the code or test logic.
- *PHP warning* — `failOnWarning="true"` in `core/phpunit.xml.dist` turns warnings into failures; trace the warning source.
- *Deprecation notice* — controlled by `SYMFONY_DEPRECATIONS_HELPER`; fix the deprecated call.

Reproduce a single test:
```bash
vendor/bin/phpunit -c web/core/phpunit.xml.dist \
  --filter testMySpecificTest web/modules/contrib/my_module/tests
```

**eslint / stylelint failure:** jobs emit an `_eslint.patch` / `_stylelint.patch` artifact; run `--fix` locally, then push.

## Verbose Service Logs

Add `CI_DEBUG_SERVICES: "true"` to your local job variables for verbose service output. This generates large artifacts — use sparingly, remove before pushing.

## What Does Not Reproduce Locally

- **Browser / Nightwatch tests** — require a full browser stack.
- **Full multi-version matrix** — `OPT_IN_TEST_PREVIOUS_MAJOR` / `_NEXT_MINOR` variant jobs need the full CI environment. Run them from the pipeline's manual trigger; do not try to replicate locally.

## Common Mistakes

- Running `phpcbf` and pushing without re-running `phpcs` — `phpcbf` does not fix all violations; always verify after auto-fix.
- Interpreting a local DDEV phpunit pass as CI parity when local PHP or PHPUnit version differs from `_TARGET_PHP` / `_TARGET_CORE` — environment must match (see [DDEV + Add-ons](ddev-contribution-environment.md)).
- Using `CI_DEBUG_SERVICES: "true"` in committed configuration — it floods artifact storage.

## See Also

- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Drupal Coding Standards at CI Parity](drupal-coding-standards-ci-parity.md)
- [Drupal Contribution Environment: DDEV + Add-ons](ddev-contribution-environment.md)
- Reference: [project.pages.drupalcode.org/gitlab_templates/info/test-locally/](https://project.pages.drupalcode.org/gitlab_templates/info/test-locally/)
