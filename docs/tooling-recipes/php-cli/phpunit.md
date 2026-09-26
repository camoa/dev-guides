---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: php_cli_phpunit_tooling
capability: phpunit
description: Use when a PHP CLI project needs PHPUnit installed and configured. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPUnit (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: php-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPUnit (PHP CLI)

## Goal

PHPUnit runs a PHP CLI project's tests and reports each assertion that did not
hold. A PHP CLI project has no framework declaring the constraint on its
behalf, the way `drupal/core-dev` does for Drupal, so `phpunit/phpunit` is
required directly. With it installed, `php-cli/test-execution.md`'s commands
have a runner to execute against.

The current major is 13 (13.3.x), requiring PHP 8.4.1 or later. Composer
resolves the highest version whose own `php` constraint the running PHP
satisfies, so a project on an older PHP receives an earlier compatible major
rather than failing the install. `php-cli/test-execution.md` and
`php-cli/checks.md` observed PHPUnit 11.5.56 on their reference install. On
13.3.4, only that the flags those recipes use still exist was checked; the
exit codes and output shown in those recipes were observed on 11.5 only.

## Install

Composer must run on the machine that will execute PHPUnit, so it resolves
each package's version against that same PHP rather than against a different
one.

```sh
composer require --dev phpunit/phpunit
```

PHPUnit needs a `phpunit.xml` or `phpunit.xml.dist` at the project root,
beside `composer.json` and `vendor/` — the location
`php-cli/test-execution.md`'s precondition assumes. At minimum it needs a
`bootstrap` attribute pointing at `vendor/autoload.php` and one `<testsuites>`
block naming a `<directory>` of tests, so PHPUnit has an autoloader and
something to enumerate.

## Run

```sh
php vendor/bin/phpunit --list-suites
```

Exit 0 with an `Available test suite:` header means the configuration file
parsed, its `bootstrap` path resolved, and PHPUnit reached its `<testsuites>`
block — proof the tool is installed and the configuration is at least
structurally sound. Verified on PHPUnit 11.5.56. The header can print with
nothing listed under it and still exit 0 — PHPUnit lists a suite only where
its `<directory>` glob matches at least one test class, so an empty list on a
project with no tests yet is expected.

If the command itself is not found, the package is absent: install, then run
it again.
