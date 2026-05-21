---
description: Drupal coding standards at CI parity — phpcs Drupal/DrupalPractice rulesets, phpstan setup, phpcs.xml.dist config, and the fix loop for local-to-CI consistency
tldr: "Install `drupal/coder` per-project, register the Drupal standards, run `phpcbf` then re-run `phpcs` — CI never auto-fixes. PHPStan is non-blocking by default; resolve tool versions from `drupal/core-dev`, never hardcode."
drupal_version: "11.x"
---

# Drupal Coding Standards at CI Parity: phpcs & phpstan

## When to Use

> Use this when setting up local code-quality enforcement to match what the CI pipeline checks. The goal is zero surprises when phpcs or phpstan runs on your MR.

## Decision

| Ruleset | Role | CI behavior |
|---|---|---|
| `Drupal` | **Mandatory** — formatting, naming, control structures | Blocking (`allow_failure: false` by default) |
| `DrupalPractice` | **Recommended** — best practices, common mistakes; may false-positive | Same job; phpcs is blocking |

> **JS/CSS:** `drupal/coder` dropped JS/CSS sniffs. Use ESLint and Stylelint for those.

## Pattern

**Install and run locally:**

```bash
# Install as dev dependency (preferred for team consistency)
composer require --dev drupal/coder squizlabs/php_codesniffer

# Register the Drupal standards
./vendor/bin/phpcs --config-set installed_paths vendor/drupal/coder/coder_sniffer
./vendor/bin/phpcs -i    # confirms "Drupal" and "DrupalPractice" are listed

# Check your module
./vendor/bin/phpcs --standard=Drupal,DrupalPractice \
  --extensions=php,module,inc,install,test,profile,theme,info,txt,md,yml \
  path/to/module

# Fix loop: auto-fix → re-run → commit clean code
./vendor/bin/phpcbf --standard=Drupal,DrupalPractice path/to/module
```

**`phpcs.xml.dist` at the project root:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ruleset name="my_module">
  <description>Drupal coding standards for my_module.</description>
  <file>src</file>
  <file>tests</file>
  <rule ref="Drupal"/>
  <rule ref="DrupalPractice"/>
  <arg name="extensions" value="php,module,inc,install,test,profile,theme,yml"/>
</ruleset>
```

**PHPStan setup (`phpstan.neon`):**

```neon
includes:
  - vendor/mglaman/phpstan-drupal/extension.neon

parameters:
  level: 2
  paths:
    - src
    - tests
```

**Suppress a `DrupalPractice` false positive (narrow scope):**

```php
// phpcs:ignore DrupalPractice.General.OptionsT9n.MissingT9n
$options = ['value' => 'Value'];
```

## Key Standards Rules

- **Naming:** functions `module_function_name()`; constants `UPPER_CASE`; classes `UpperCamelCase`; methods `lowerCamelCase`; interfaces suffix `Interface`; traits suffix `Trait`; test classes suffix `Test`
- **Formatting:** 2-space indent (never tabs); ~80-char line target; `['key' => 'value']` short array syntax; single quotes by default
- **Type hints:** mandatory in Drupal 9+ code; return types required
- **Docblocks:** every function/class/method/property/constant needs one; hook implementations documented as `Implements hook_name().`

## Common Mistakes

- **Wrong**: Running `phpcbf` and assuming it fixed everything → **Right**: Re-run `phpcs` after auto-fix; some violations require manual resolution
- **Wrong**: Routing JS/CSS questions to `drupal/coder` → **Right**: It no longer handles those; use ESLint/Stylelint
- **Wrong**: Hardcoding PHPUnit/PHPStan version constraints in `composer.json` → **Right**: Resolve from the target core's `drupal/core-dev`
- **Wrong**: Setting `level: 9` PHPStan on a new module with no baseline → **Right**: Start at 2–4 and raise it
- **Wrong**: Using a global `phpcs` install → **Right**: Per-project `--dev` dependency avoids version skew

## See Also

- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Reproducing drupalci Failures Locally](reproducing-drupalci-failures-locally.md)
- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- AI overlay: [Contributing with AI — Coding Standards](../contributing-with-ai/coding-standards.md)
- Reference: [project.pages.drupalcode.org/coding_standards/php/](https://project.pages.drupalcode.org/coding_standards/php/)
- Reference: [drupal.org/project/coder](https://www.drupal.org/project/coder)
