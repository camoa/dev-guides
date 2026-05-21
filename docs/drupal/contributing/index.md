---
description: Drupal contribution mechanics — three contribution workflows, drupalci pipeline, CI failure reproduction, coding standards, DDEV environment setup, project scaffolding, issue lifecycle, merge requests, RTBC etiquette, and module maintainership
guide-meta:
  concepts:
    - Drupal contribution
    - drupalci pipeline
    - gitlab_templates
    - merge request
    - issue fork
    - RTBC
    - phpcs
    - DrupalPractice
    - phpstan
    - mglaman/phpstan-drupal
    - drupal/coder
    - ddev-drupal-contrib
    - ddev-drupal-suite
    - ddev-drupal-core-dev
    - info.yml
    - core_version_requirement
    - issue lifecycle
    - Needs review
    - Needs work
    - GitLab scoped labels
    - state::rtbc
    - state::needsReview
    - Contribution Records
    - credit system
    - drupalorg-cli
    - allow_failure
    - OPT_IN_TEST_PREVIOUS_MAJOR
    - phpunit.xml.dist
    - core gates
    - issue fork branch
  not:
    - AI contribution policy
    - AI disclosure
    - Vibe Coded
    - context poisoning
    - Drupal AI module
    - composer patches
    - Composer workflows unrelated to contrib
  requires: []
  complements:
    - drupal/contributing-with-ai
    - drupal/testing
  specializes: ""
  category: drupal
---

# Drupal Contribution

> General contribution mechanics for Drupal core, your own contrib projects, and someone else's contrib. The AI-specific overlay (disclosure thresholds, AI policy, AI code review discipline) lives in [Contributing with AI](../contributing-with-ai/index.md).

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the three contribution workflows (core / own contrib / others') | [Three Contribution Workflows](three-contribution-workflows-compared.md) | Read this first: the three workflows differ in authority, CI ownership, and who merges. Target `main` for all new core work; contrib follows each project's branch conventions. |
| Understand how the drupalci pipeline works | [drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md) | Contrib projects opt into the DA-managed pipeline via a one-line include (gitlab_templates v1.15.4). Only `composer` and `phpcs` are blocking by default; all other validation jobs are `allow_failure: true` unless the maintainer enforces them. |
| Reproduce a CI failure locally | [Reproducing drupalci Failures Locally](reproducing-drupalci-failures-locally.md) | Use `ddev phpcs`/`ddev phpunit` (ddev-drupal-contrib) for the day-to-day inner loop, or `drupal-ci-local` to run exact CI jobs locally. There is no Docker-free route. |
| Set up phpcs / phpstan to match CI | [Drupal Coding Standards at CI Parity](drupal-coding-standards-ci-parity.md) | Install `drupal/coder` per-project, register the Drupal standards, run `phpcbf` then re-run `phpcs` — CI never auto-fixes. PHPStan is non-blocking by default; resolve tool versions from `drupal/core-dev`, never hardcode. |
| Set up my DDEV environment for contribution | [DDEV Contribution Environment](ddev-contribution-environment.md) | DDEV is the community standard. Use `ddev-drupal-contrib` for single contrib modules (module repo is the project root; `web/` and `vendor/` are generated and gitignored), `ddev-drupal-suite` for multi-module, and `ddev-drupal-core-dev` for core. |
| Scaffold a new contrib module or theme | [Contrib Project Scaffolding](contrib-project-scaffolding.md) | A contrib module repo is the project root; `web/` and `vendor/` are gitignored. Required keys in `info.yml`: `name`, `type`, `core_version_requirement`. Include `composer.json` even without non-Drupal dependencies. Never hardcode PHPUnit version — copy `phpunit.xml.dist` from the target core. |
| Understand the issue lifecycle | [Drupal Issue Lifecycle](drupal-issue-lifecycle.md) | Detect whether a project uses the classic queue or GitLab by following the Issues link. RTBC has no single standardized GitLab equivalent — ask the maintainer. Triage access on GitLab requires Planner role or higher. |
| Create an issue fork and open a merge request | [Issue Forks & Merge Requests](issue-forks-merge-requests.md) | Create an issue fork via the drupal.org UI or `drupalorg issue:branch`. Branch name must include the issue number. Always target the most recent development branch (`main` for core). Mark MR ready when you set the issue to Needs review. |
| Know RTBC discipline, comment etiquette, and credit | [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md) | RTBC asserts the full checklist (tests pass, phpcs clean, all threads resolved, gates passed for core) — never just a code read. Credit is maintainer-granted via Contribution Records; never demand it. |
| Manage my own module or theme as a maintainer | [Module/Theme Maintainer](module-theme-maintainer.md) | As maintainer you own the `.gitlab-ci.yml` (make phpcs blocking at minimum), the triage queue (respond promptly), and all credit decisions. Add a co-maintainer before stepping down. |
