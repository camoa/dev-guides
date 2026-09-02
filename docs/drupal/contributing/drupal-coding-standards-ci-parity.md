---
description: Drupal coding standards at CI parity — phpcs Drupal/DrupalPractice rulesets, phpstan setup, phpcs.xml.dist config, and the fix loop for local-to-CI consistency
tldr: "Install `drupal/coder` per-project, register the Drupal standards, run `phpcbf` then re-run `phpcs` — CI never auto-fixes. PHPStan is non-blocking by default; resolve tool versions from `drupal/core-dev`, never hardcode."
drupal_version: "11.x"
---

# Drupal Coding Standards at CI Parity: phpcs & phpstan

## When to Use

> Use this when setting up local code-quality enforcement to match what the CI pipeline checks. The goal is zero surprises when phpcs or phpstan runs on your MR.

## The Two phpcs Rulesets

Both rulesets ship in `drupal/coder` (current: **v9.0.0**, released Mar 2026) and run through PHP_CodeSniffer.

| Ruleset | Role | CI behavior |
|---|---|---|
| `Drupal` | **Mandatory** — formatting, naming, control structures | Blocking (`allow_failure: false` by default) |
| `DrupalPractice` | **Recommended** — best practices, common mistakes; may false-positive | Same job, non-blocking by default on `phpstan` but phpcs is blocking |

## What the `Drupal` Standard Encodes

- **Naming** — functions: `module_function_name()`; constants: `UPPER_CASE`; classes: `UpperCamelCase`; methods: `lowerCamelCase`; interfaces suffix `Interface`, traits suffix `Trait`, test classes suffix `Test`.
- **Formatting** — **2-space indent, never tabs**; ~80-character line target; `['key' => 'value']` short array syntax; spaces around binary operators and after control keywords; single quotes by default.
- **Type hints** — mandatory in Drupal 9+ code; return types required.
- **Docblocks** — every function/class/method/property/constant needs a `/** */` docblock (including private); summary line under 80 chars; `@param`, `@return`, `@throws` with lowercase PHPDoc types; hook implementations documented as `Implements hook_name().`

> **JS/CSS:** `drupal/coder` dropped JS/CSS sniffs. Use **ESLint** and **Stylelint** for those — route JS/CSS standards questions there, not to `coder`.

## Installing and Running Locally

```bash
# Install as dev dependency (per-project — preferred for team consistency)
composer require --dev drupal/coder squizlabs/php_codesniffer

# Register the Drupal standards
./vendor/bin/phpcs --config-set installed_paths vendor/drupal/coder/coder_sniffer
./vendor/bin/phpcs -i    # confirms "Drupal" and "DrupalPractice" are listed

# Check your module
./vendor/bin/phpcs --standard=Drupal,DrupalPractice \
  --extensions=php,module,inc,install,test,profile,theme,info,txt,md,yml \
  path/to/module

# Auto-fix locally (LOCAL ONLY — CI never auto-fixes)
./vendor/bin/phpcbf --standard=Drupal,DrupalPractice path/to/module
```

**The fix loop:** run `phpcbf` → re-run `phpcs` → commit clean code. CI only reports violations; it never auto-fixes.

## The phpcs.xml.dist Config File

A `phpcs.xml.dist` at the project root scopes standards enforcement to your code:

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

CI reads this file automatically when present. Without it, the CI job uses defaults.

## PHPStan Setup

PHPStan runs with `mglaman/phpstan-drupal` as a Drupal API extension. The `phpstan.neon` at your project root:

```neon
includes:
  - vendor/mglaman/phpstan-drupal/extension.neon

parameters:
  level: 2
  paths:
    - src
    - tests
```

PHPStan defaults to `allow_failure: true` in the templates — it is non-blocking unless the maintainer enforces it. Still run it locally; phpstan catches real bugs that phpcs misses.

**Version matrix:** PHPStan `^1.12.27 || ^2.1.54` on D11; `^1.x` only on D10. `mglaman/phpstan-drupal` `^1.3.9 || ^2.0.15` on D11. Resolve from `drupal/core-dev` — do not hardcode.

## DrupalPractice False Positives

`DrupalPractice` catches common mistakes but sometimes flags code that is intentionally written differently. Suppress a false positive with a targeted inline annotation:

```php
// phpcs:ignore DrupalPractice.General.OptionsT9n.MissingT9n
$options = ['value' => 'Value'];
```

Prefer narrowing the suppression scope to the specific rule rather than `// phpcs:ignore` (which suppresses all rules for that line).

## Common Mistakes

- Running `phpcbf` and assuming it fixed everything — re-run `phpcs` after auto-fix; some violations require manual resolution.
- Routing JS/CSS questions to `drupal/coder` — it no longer handles those; use ESLint/Stylelint.
- Hardcoding PHPUnit/PHPStan version constraints in `composer.json` instead of resolving from the target core — CI uses the core-resolved version.
- Setting `level: 9` PHPStan on a new module that has no baseline — start at 2–4 and raise it; false positives at high levels are common in Drupal code.
- Using a global `phpcs` install instead of a per-project `--dev` dependency — version skew causes different results locally vs. CI.

## See Also

- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Reproducing drupalci Failures Locally](reproducing-drupalci-failures-locally.md)
- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- AI overlay: [Contributing with AI — Coding Standards](../contributing-with-ai/coding-standards.md)
- Reference: [project.pages.drupalcode.org/coding_standards/php/](https://project.pages.drupalcode.org/coding_standards/php/)
- Reference: [drupal.org/project/coder](https://www.drupal.org/project/coder)
