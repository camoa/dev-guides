---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_phpstan_tooling
capability: phpstan
description: Use when a Drupal project needs PHPStan static analysis with the Drupal extension. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPStan (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPStan (Drupal)

## Goal

PHPStan reads PHP without running it and reports what cannot be true — a call to a
method that does not exist, a type that cannot arrive where it is used, a branch
that can never be reached. On its own it does not understand Drupal, so it reports
core's own idioms as errors. `mglaman/phpstan-drupal` teaches it the container, the
entity system and the plugin managers, and the deprecation rules add a reading for
API removals ahead of a major version.

With it installed, a claim that a change breaks nothing can be checked against the
whole codebase rather than against the paths someone remembered to open.

## Install

Allow the plugin that loads the extensions, before requiring the packages that
carry them. Composer refuses to run an unlisted plugin, so this order matters:
run it the other way round and the extensions install without being loaded.

```
composer config --no-plugins allow-plugins.phpstan/extension-installer true
```

```
composer require --dev phpstan/phpstan phpstan/extension-installer mglaman/phpstan-drupal phpstan/phpstan-deprecation-rules
```

`phpstan/extension-installer` registers the Drupal extension and the deprecation
rules itself. Do not also add them under an `includes:` key in the configuration —
they load twice and PHPStan stops with a duplicate-service error.

PHPStan needs a `phpstan.neon` at the project root naming what to analyse, at
minimum a `level` and a `paths` list. Analysis runs against that file; without one
PHPStan has nothing to read.

## Run

```
ddev exec vendor/bin/phpstan analyse
```

Findings print grouped by file, each with a line number and the rule that produced
it. The exit status is non-zero when anything was reported, so a caller can branch
on it without reading the text.

Paths and level come from `phpstan.neon`. To analyse something outside it, name the
path and the level on the command line instead:

```
ddev exec vendor/bin/phpstan analyse --level 8 web/modules/custom/my_module
```

If the command is not found, the package is absent: install, then run it again.
