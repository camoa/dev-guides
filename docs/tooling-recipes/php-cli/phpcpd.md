---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: php_cli_phpcpd_tooling
capability: phpcpd
description: Use when a PHP CLI project needs copy/paste detection over its PHP code. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPCPD (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: php-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPCPD (PHP CLI)

## Goal

PHPCPD reads a codebase's PHP files and reports the blocks that repeat elsewhere
almost unchanged — code that could be one function instead of several copies drifting
apart. With it installed, a duplication claim about a PHP CLI project's library can be
checked rather than asserted.

The original `sebastian/phpcpd` is abandoned; Packagist marks it abandoned and
suggests no replacement, and its own README says the repository is kept only for
archival purposes. `systemsdk/phpcpd` is the actively maintained fork: its
`composer.json` still lists Sebastian Bergmann as lead author alongside the
maintaining developer, and its README describes it as a continuation of the
abandoned project. Install this fork, not the original.

## Install

```sh
composer require --dev systemsdk/phpcpd
```

The package registers no Composer plugin and needs no `allow-plugins` entry.
Composer resolves the required version against whatever PHP runs it, so the release
it picks depends on that PHP's version: the latest release, 9.1.0, requires PHP 8.4
or later; the 8.x line (8.0.0 through 8.3.0) requires PHP 8.3 or later; and 7.0.1
requires PHP 8.1 or later. A project on an older PHP floor pins the release its
floor supports rather than taking the latest.

## Run

```sh
php vendor/bin/phpcpd --version
```

Prints the installed version and exits 0. If the command is not found, the package
is absent: install, then run it again.

PHPCPD scans directories, not individual files — a file named on its command line
produces `No files found to scan` and exits 1. A real scan names the directory to
check, and its default suffix, `.php`, is enough for a library with no other PHP
file extensions to include:

```text
php vendor/bin/phpcpd src
```

Findings print to stdout as a list of duplicated blocks with their files and line
ranges. The exit status is non-zero when a clone was found, so a caller can branch on
it without reading the text — the same non-zero status a missing scan target
produces, so an empty scope reads as unmet rather than as clean.
