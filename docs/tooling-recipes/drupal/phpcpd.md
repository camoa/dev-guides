---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_phpcpd_tooling
capability: phpcpd
description: Use when a Drupal project needs copy/paste detection over its PHP code. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPCPD (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPCPD (Drupal)

## Goal

PHPCPD reads a codebase's PHP files and reports the blocks that repeat elsewhere
almost unchanged — code that could be one function instead of several copies drifting
apart. With it installed, a duplication claim about a Drupal codebase can be checked
rather than asserted.

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

The package registers no Composer plugin and needs no `allow-plugins` entry —
unlike `drupal/coder` and the PHPStan extensions, nothing here loads through the
plugin API. Composer resolves the version against the PHP running Composer, not
the container's PHP, because the step above runs on the host — the latest
release, 9.1.0, requires PHP 8.4 or later, while earlier releases in the same
fork (8.x) require PHP 8.3 or later. A host on a newer PHP than the DDEV
container's can resolve a version the container cannot run: set
`config.platform.php` to the container's PHP version so Composer resolves
against that instead, or require the package inside the container in the first
place with `ddev composer require --dev systemsdk/phpcpd`.

## Run

```sh
ddev exec vendor/bin/phpcpd --version
```

Prints the installed version and exits 0. If the command is not found, the package
is absent: install, then run it again.

PHPCPD scans directories, not individual files — a file named on its command line
produces `No files found to scan` and exits 1. A real scan names the directories to
check and the suffixes to include, since its default suffix is `.php` alone:

```text
ddev exec vendor/bin/phpcpd --suffix .php --suffix .module web/modules/custom/my_module
```

Findings print to stdout as a list of duplicated blocks with their files and line
ranges. The exit status is non-zero when a clone was found, so a caller can branch on
it without reading the text — the same non-zero status a missing scan target
produces, so an empty scope reads as unmet rather than as clean.
