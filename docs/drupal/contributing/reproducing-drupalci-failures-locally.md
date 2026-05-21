---
description: Reproducing drupalci CI failures locally — DDEV inner loop, gitlab-ci-local, and per-job debugging commands for phpcs, phpstan, phpunit, eslint, and stylelint
tldr: "Use `ddev phpcs`/`ddev phpunit` (ddev-drupal-contrib) for the day-to-day inner loop, or `drupal-ci-local` to run exact CI jobs locally. There is no Docker-free route."
drupal_version: "11.x"
---

# Reproducing drupalci Failures Locally

## When to Use

> Use this when a CI job fails on your MR and you need to reproduce the failure locally before pushing a fix — faster than waiting for a full pipeline run.

## Decision

| Reproduction route | Best for | Requirement |
|---|---|---|
| `ddev phpcs` / `ddev phpunit` (via `ddev-drupal-contrib`) | Day-to-day inner loop; contrib module development | Docker + DDEV add-on already installed |
| `gitlab-ci-local` (`drupal-ci-local` wrapper) | Running exact CI jobs locally; debugging job internals | Docker |
| Push a commit and read the pipeline | Browser/Nightwatch tests; full multi-version matrix | None beyond a GitLab account |

There is no Docker-free route to run the CI jobs locally.

## Pattern

**DDEV route (inner loop):**

```bash
ddev phpcs
ddev phpstan
ddev phpunit web/modules/contrib/my_module/tests
ddev eslint
ddev stylelint
```

**gitlab-ci-local route (full job reproduction):**

```bash
npm install -g @laktawan/drupal-ci-local

drupal-ci-local          # run all jobs
drupal-ci-local phpunit  # run a single job by name
drupal-ci-local phpcs
# Artifacts land in .gitlab-ci-local/
```

**phpcs — debug and fix:**

```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice \
  --extensions=php,module,inc,install,test,profile,theme,info,txt,md,yml \
  path/to/module

# Auto-fix locally (never runs in CI):
vendor/bin/phpcbf --standard=Drupal,DrupalPractice path/to/module
```

**phpunit — isolate a single test:**

```bash
vendor/bin/phpunit -c web/core/phpunit.xml.dist \
  --filter testMySpecificTest web/modules/contrib/my_module/tests
```

**phpunit failure types:**
- *Test failure* — assertion failed; fix the code or test logic
- *PHP warning* — `failOnWarning="true"` in `core/phpunit.xml.dist` turns warnings into failures
- *Deprecation notice* — controlled by `SYMFONY_DEPRECATIONS_HELPER`; fix the deprecated call

**eslint / stylelint:** jobs emit a `_eslint.patch` / `_stylelint.patch` artifact; run `--fix` locally, then push.

## Common Mistakes

- **Wrong**: Running `phpcbf` and pushing without re-running `phpcs` → **Right**: Always verify after auto-fix; `phpcbf` does not fix all violations
- **Wrong**: Interpreting a local DDEV phpunit pass as CI parity when PHP/PHPUnit versions differ → **Right**: Environment must match `_TARGET_PHP` / `_TARGET_CORE`
- **Wrong**: Using `CI_DEBUG_SERVICES: "true"` in committed configuration → **Right**: Use it sparingly; it floods artifact storage

## What Does Not Reproduce Locally

- Browser / Nightwatch tests — require a full browser stack
- Full multi-version matrix (`OPT_IN_TEST_PREVIOUS_MAJOR` / `_NEXT_MINOR`) — run from the pipeline's manual trigger

## See Also

- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Drupal Coding Standards at CI Parity](drupal-coding-standards-ci-parity.md)
- [Drupal Contribution Environment: DDEV + Add-ons](ddev-contribution-environment.md)
- Reference: [project.pages.drupalcode.org/gitlab_templates/info/test-locally/](https://project.pages.drupalcode.org/gitlab_templates/info/test-locally/)
