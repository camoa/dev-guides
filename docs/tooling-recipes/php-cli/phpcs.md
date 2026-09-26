---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: php_cli_phpcs_tooling
capability: phpcs
description: Use when a PHP CLI project needs PHP_CodeSniffer with the PSR12 standard installed. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHP_CodeSniffer (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: php-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHP_CodeSniffer (PHP CLI)

## Goal

PHP_CodeSniffer reads PHP against a coding standard and reports each place
the code departs from it. `PSR12` ships in the base package, so a PHP CLI
project needs no extra standards package the way a Drupal project needs
`drupal/coder` for `Drupal` and `DrupalPractice`. With it installed,
`php-cli/checks.md`'s `coding-standards` row has a binary to run.

The project moved its source to the PHPCSStandards organisation on GitHub
and now ships a 4.x major there, but the Composer package name is unchanged:
`squizlabs/php_codesniffer` is still the name Packagist and the 4.x releases
publish under.

## Install

Composer must run on the machine that will execute PHP_CodeSniffer, so it
resolves the package's version against that same PHP rather than against a
different one.

```sh
composer require --dev squizlabs/php_codesniffer
```

No Composer plugin is involved. `dealerdirect/phpcodesniffer-composer-installer`,
which the Drupal sibling recipe needs, only registers a standard shipped by a
separate package such as `drupal/coder`; `PSR12` ships inside
`squizlabs/php_codesniffer` itself and needs no registration step.

## Run

```sh
php vendor/bin/phpcs -i
```

Exit 0 with a line reading `The installed coding standards are …` naming
`PSR12` among them proves the standard is registered, not just that the
binary exists. On PHP_CodeSniffer 4.x, with only `squizlabs/php_codesniffer`
installed, the bundled set is `PEAR, PSR1, PSR2, PSR12, Squiz, Zend` — 4.x
dropped `MySource`. Installing `drupal/coder` on top adds four names, not
two: `Drupal` and `DrupalPractice` from coder itself, plus `VariableAnalysis`
and `SlevomatCodingStandard` from the sniff packages coder requires —
verified against `phpcs -i` run with `drupal/coder` 8.3.31 installed, on
PHP_CodeSniffer 3.13.5. The coder major decides the phpcs major: coder 8.3.31
requires `squizlabs/php_codesniffer` `^3.13`, while coder 9.0.0 (2026-03-13)
and 9.0.1 require `^4.0.1`. `drupal/core-dev` 11.4.5 pins `drupal/coder`
`^8.3.30`, so a Drupal 11 project runs phpcs 3.x; `drupal/core-dev`
12.0.0-alpha1 pins `^9.0`. The four added names do not come from squizlabs's
own standards and do not change with the major.

If the command itself is not found, the package is absent: install, then run
it again.
