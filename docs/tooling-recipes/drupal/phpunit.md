---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_phpunit_tooling
capability: phpunit
description: Use when a Drupal project needs PHPUnit installed and configured through drupal/core-dev. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPUnit (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.1
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPUnit (Drupal)

## Goal

PHPUnit runs the Unit, Kernel, Functional and FunctionalJavascript tests a Drupal
project writes, and reports each assertion that did not hold. Drupal does not
declare `phpunit/phpunit` on its own; `drupal/core-dev` pulls in the version core
itself is tested against, along with the other packages Drupal's own test base
classes need. With it installed, a test-first claim about a Drupal codebase can
be run rather than asserted.

The PHPUnit constraint `drupal/core-dev` carries, by core branch (Packagist):

| Core branch | `drupal/core-dev` requires |
|---|---|
| 11.3–11.4 | `^11.5.50` |
| 11.2 | `^10.5.19 \|\| ^11.5.3` |
| 11.0–11.1 | `^10.5.19` |
| 10.6 | `^9.6.34` |
| 10.2–10.5 | `^9.6.13` |
| 10.0–10.1 | `^9.5` |

## Install

`drupal/core-dev` pulls in `open-telemetry/sdk`, and that package requires
`tbachert/spi` — a Composer plugin. Core's own root `composer.json` sets
`tbachert/spi` to `false`, and an unattended `composer require` cannot answer
the interactive prompt Composer would otherwise show for an unlisted plugin, so
it throws `PluginBlockedException` instead. Record the same answer first.
`core-dev`'s dependency tree carries three more Composer plugins —
`phpstan/extension-installer` directly, `dealerdirect/phpcodesniffer-composer-installer`
through `drupal/coder`, and `php-http/discovery` through
`open-telemetry/exporter-otlp` — which a project built from
`drupal/recommended-project` already allows; only `tbachert/spi` is missing
there. Allowing all four here keeps the step correct for a project that was not
built from that template.

```sh
ddev composer config --no-plugins allow-plugins.tbachert/spi false
ddev composer config --no-plugins allow-plugins.phpstan/extension-installer true
ddev composer config --no-plugins allow-plugins.dealerdirect/phpcodesniffer-composer-installer true
ddev composer config --no-plugins allow-plugins.php-http/discovery true
```

Require `drupal/core-dev` as a dev dependency, with the flag drupal.org's own
"Running PHPUnit tests" documentation gives so Composer resolves the whole
dependency set against what the project already requires, rather than only
against `core-dev` itself.

```sh
ddev composer require drupal/core-dev --dev --update-with-all-dependencies
```

Do not add `phpunit/phpunit` to the project's own `composer.json`. `core-dev`
already carries the constraint core itself is tested against, so a direct
requirement is redundant and can drift from core's — it conflicts with the pin
only when its own range excludes what `core-dev` allows.

PHPUnit also needs a `phpunit.xml` at the project root, beside `composer.json` and
`vendor/` — the location that same documentation places it at. Copy the file
core ships, `<docroot>/core/phpunit.xml.dist`, to `phpunit.xml` at the project
root once. The path assumes a `web/` docroot; read the project's own docroot
from `composer.json`'s `extra.drupal-scaffold.locations.web-root` first if it
differs, and adjust the source path to match.

The copy is not usable as it stands. Every relative path inside it —
`bootstrap`, each testsuite's `<directory>`, the browser-output directory — is
written for `core/` and resolves to nothing once the file sits at the project
root, and the database and base-URL environment variables ship empty. Making it
usable is several edits inside one XML file: which lines change, to what, and
why the docroot has to be repeated in front of each one is not a command an
argv-safe step can express without a shell to carry it, so it is done by hand.
Follow [PHPUnit Configuration](../../drupal/tdd/phpunit-configuration.md) for
the rewrite, line by line.

## Run

```sh
ddev exec vendor/bin/phpunit -c phpunit.xml --list-suites
```

Exit 0 with an `Available test suite:` header (PHPUnit prints the plural
`Available test suites:` once more than one is listed) means the file at the project root
parsed, its `bootstrap` path resolved, and PHPUnit reached its `<testsuites>`
block — proof the tool is installed and the configuration is at least
structurally sound. Verified on PHPUnit 11.5.56: a `-c` target that does not
exist prints `Could not read XML from file` and exits 2, and a `bootstrap` path
left unrewritten after the copy above prints `Cannot open bootstrap script` and
exits 2 — each names the specific defect rather than a generic failure.

The header can print with nothing listed under it and still exit 0 — PHPUnit
lists a suite only where its `<directory>` glob matches at least one test class,
so an empty list on a project with no tests yet is expected, verified the same
way. It stops being expected once a module under the configured directories
carries a test file and still does not appear; that combination is a finding.

If the command itself is not found, the package is absent: install, then run it
again.
