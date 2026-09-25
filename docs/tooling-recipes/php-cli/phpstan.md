---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: php_cli_phpstan_tooling
capability: phpstan
description: Use when a PHP CLI project needs PHPStan static analysis installed. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPStan (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: php-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPStan (PHP CLI)

## Goal

PHPStan reads PHP without running it and reports what cannot be true — a call
to a method that does not exist, a type that cannot arrive where it is used,
a branch that can never be reached. A PHP CLI project needs no framework
extension for it, unlike a Drupal project reading the container and the
entity system, so the base package is enough. With it installed,
`php-cli/checks.md`'s `static-analysis` row has a binary to run.

## Install

Composer must run on the machine that will execute PHPStan, so it resolves
the package's version against that same PHP rather than against a different
one.

```sh
composer require --dev phpstan/phpstan
```

No extension-installer plugin is needed: `php-cli/checks.md`'s
`static-analysis` row runs plain `analyse`, with no Drupal or other extension
loaded through `phpstan/extension-installer`.

PHPStan needs a `phpstan.neon` at the project root naming what to analyse, at
minimum a `level` and a `paths` list. Without one, PHPStan runs at level 0
against whatever paths are given on the command line — analysis is not
skipped, but it stops short of the project's intended level.

## Run

```sh
php vendor/bin/phpstan --version
```

Exit 0 with a line reading `PHPStan - PHP Static Analysis Tool <version>`
means the binary is installed and runnable. Verified on PHPStan 2.2.8.

If the command is not found, the package is absent: install, then run it
again.
