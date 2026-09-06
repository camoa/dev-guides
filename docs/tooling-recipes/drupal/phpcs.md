---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_phpcs_tooling
capability: phpcs
description: Use when a Drupal project needs PHP_CodeSniffer with the Drupal and DrupalPractice standards. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHP_CodeSniffer (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHP_CodeSniffer (Drupal)

## Goal

PHP_CodeSniffer reads PHP, CSS and JavaScript against a coding standard and reports
each place the code departs from it. `drupal/coder` supplies the two standards a
Drupal project is held to: `Drupal` for the coding standard itself, and
`DrupalPractice` for the conventions that are not strictly rules. With it installed,
a standards claim about a Drupal codebase can be checked rather than asserted.

`phpcbf` ships in the same package and rewrites the subset of findings that can be
fixed mechanically.

## Install

Allow the plugin that registers the standards, before requiring the package that
carries them. Composer refuses to run an unlisted plugin, so this order matters:
run it the other way round and `coder` installs while its standards do not appear.

```
composer config --no-plugins allow-plugins.dealerdirect/phpcodesniffer-composer-installer true
```

```
composer require --dev drupal/coder
```

`dealerdirect/phpcodesniffer-composer-installer` comes in as a dependency of
`drupal/coder` and writes the standards into PHP_CodeSniffer's own configuration.
There is no separate registration step. A `phpcs --config-set installed_paths …`
command is the manual equivalent for a project that does not allow the plugin, and
running it as well does no harm and no good.

## Run

```
ddev exec vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/custom
```

Findings print to stdout, grouped by file, with a line and column for each. The exit
status is non-zero when anything was reported, so a caller can branch on it without
reading the text.

Point the last argument at whatever the caller means by its own code — a single
module directory, a theme, or several paths in one invocation.

To see which standards are registered rather than which findings exist:

```
ddev exec vendor/bin/phpcs -i
```

`Drupal` and `DrupalPractice` appear in that list once the install above has run. If
the command itself is not found, the package is absent: install, then run it again.
