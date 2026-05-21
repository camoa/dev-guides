---
description: Scaffold a new contrib module or theme — info.yml required keys, composer.json structure, .gitignore, .gitlab-ci.yml include, and PHPUnit test taxonomy
tldr: "A contrib module repo is the project root; `web/` and `vendor/` are gitignored. Required keys in `info.yml`: `name`, `type`, `core_version_requirement`. Include `composer.json` even without non-Drupal dependencies. Never hardcode PHPUnit version — copy `phpunit.xml.dist` from the target core."
drupal_version: "11.x"
---

# Contrib Project Scaffolding: info.yml, composer.json, CI Config

## When to Use

> Use this when creating a new contrib module or theme, or when setting up CI for an existing one.

## Directory Layout

```
my_module/
├── my_module.info.yml          # REQUIRED
├── composer.json               # Required with non-Drupal deps; best practice always
├── src/                        # PSR-4 classes (Form/, Plugin/, Service/, …)
├── my_module.module            # Optional procedural hooks
├── config/
│   ├── install/                # Default config shipped with the module
│   └── schema/                 # Config schema definitions
├── templates/                  # Twig templates
├── tests/src/
│   ├── Unit/
│   ├── Kernel/
│   ├── Functional/
│   └── FunctionalJavascript/
├── .gitlab-ci.yml              # Recommended
├── phpcs.xml.dist
├── phpstan.neon
├── phpunit.xml.dist
├── .gitignore                  # Excludes /web/ /vendor/ /.ddev/
└── web/                        # Generated — NOT committed
```

## Pattern

**`*.info.yml` — required keys:**

```yaml
name: My Module
type: module
description: 'What this module does.'
core_version_requirement: '^10.3 || ^11'
package: Custom

dependencies:
  - drupal:field
  - drupal:views
lifecycle: stable   # stable | experimental | deprecated | obsolete
```

**`composer.json`:**

```json
{
  "name": "drupal/my_module",
  "type": "drupal-module",
  "license": "GPL-2.0-or-later",
  "require": { "drupal/core": "^10.3 || ^11" },
  "require-dev": {
    "drupal/core-dev": "^10.3 || ^11",
    "drupal/coder": "^8.3",
    "phpstan/phpstan": "^1.12 || ^2.1",
    "mglaman/phpstan-drupal": "^1.3 || ^2.0"
  },
  "autoload": {
    "psr-4": { "Drupal\\my_module\\": "src/" }
  },
  "autoload-dev": {
    "psr-4": { "Drupal\\Tests\\my_module\\": "tests/src/" }
  }
}
```

**`.gitlab-ci.yml`:**

```yaml
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
  _TARGET_CORE: "^10 || ^11"
  _TARGET_PHP: "8.3"
  OPT_IN_TEST_PREVIOUS_MAJOR: "1"
```

## PHPUnit Test Taxonomy

| Type | Base class | Needs | Dir |
|---|---|---|---|
| **Unit** | `Drupal\Tests\UnitTestCase` | Nothing — pure PHP | `tests/src/Unit/` |
| **Kernel** | `Drupal\KernelTests\KernelTestBase` | Drupal services; no full DB install | `tests/src/Kernel/` |
| **Functional** | `Drupal\Tests\BrowserTestBase` | Full site install, DB, `SIMPLETEST_BASE_URL` | `tests/src/Functional/` |
| **FunctionalJavascript** | `Drupal\FunctionalJavascriptTests\WebDriverTestBase` | Above + ChromeDriver | `tests/src/FunctionalJavascript/` |

Namespace convention: `Drupal\Tests\<module>\<TestType>\…`

For `phpunit.xml.dist`: never hardcode a version — copy from the target core's `core/phpunit.xml.dist`. The schema differs between D10 (PHPUnit 9.x, `<coverage>` block, `DrupalListener`) and D11 (PHPUnit 11, `<source>` block, `failOnWarning`).

## Common Mistakes

- **Wrong**: Including `web/` or `vendor/` in the repo → **Right**: Gitignore them; they are generated
- **Wrong**: Hardcoding PHPUnit version in `phpunit.xml.dist` → **Right**: Copy from the target core
- **Wrong**: Omitting `composer.json` → **Right**: Include it even without non-Drupal dependencies
- **Wrong**: Using `type: module` for themes → **Right**: Use `type: theme`
- **Wrong**: Setting `core_version_requirement` too narrowly → **Right**: Use `'^10.3 || ^11'` for broad compatibility

## See Also

- [Drupal Contribution Environment: DDEV + Add-ons](ddev-contribution-environment.md)
- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Serving as a Drupal Module/Theme Maintainer](module-theme-maintainer.md)
- Reference: [drupal.org/docs/develop/creating-modules/let-drupal-know-about-your-module-with-an-infoyml-file](https://www.drupal.org/docs/develop/creating-modules/let-drupal-know-about-your-module-with-an-infoyml-file)
- Reference: [drupal.org/docs/develop/using-composer/managing-dependencies-for-a-contributed-project](https://www.drupal.org/docs/develop/using-composer/managing-dependencies-for-a-contributed-project)
