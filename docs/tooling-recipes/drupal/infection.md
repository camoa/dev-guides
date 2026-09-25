---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_infection_tooling
capability: infection
description: Use when a Drupal project needs Infection mutation testing with a coverage driver in place. Says how to install it and how to run it.
# Metadata, read only after a match.
label: Infection (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# Infection (Drupal)

## Goal

Infection runs a test suite once, then mutates the source a statement at a time and
reruns the tests that cover each mutant. A mutant a test kills is caught; a mutant
that survives ran against the suite and produced no failure, which is the gap a
passing suite alone cannot show. The result is a Mutation Score Indicator alongside
the list of survivors, so a claim that tests cover the changed code can be checked
past whether they merely execute it.

## Install

Allow the plugin that registers extensions, before requiring the package that
carries it. Composer refuses to run an unlisted plugin, so this order matters: run
it the other way round and `infection/infection` installs while the plugin does not
run.

```sh
composer config --no-plugins allow-plugins.infection/extension-installer true
```

```sh
composer require --dev infection/infection
```

`infection/extension-installer` is a direct dependency of `infection/infection`
itself, not a separate package to add. It runs on every `composer install` and
`composer update` and registers any installed package typed `infection-extension`,
such as an alternate test-framework adapter. There is no separate registration step.

Infection also needs an `infection.json5` at the project root naming the source
directories to mutate, and a coverage driver — pcov or Xdebug — enabled in the web
container it runs in. Neither is something this Install section adds: `infection.json5`
is project configuration, and DDEV ships Xdebug already installed but disabled by
default, toggled with `ddev xdebug on` rather than through Composer. DDEV documents
adding a PHP extension package through `webimage_extra_packages` in `.ddev/config.yaml`
for anything its base image does not ship already; `php${DDEV_PHP_VERSION}-pcov` is
available from the same upstream package repository DDEV uses for PHP extensions, as
an alternative to enabling Xdebug. Without a coverage driver enabled, Infection does
not run mutation testing at all: verified against Infection 0.35.4's own
`CoverageChecker`, it aborts with "Coverage needs to be generated but no code coverage
generator (pcov, phpdbg or xdebug) has been detected" rather than skipping only the
lines coverage did not reach.

## Run

```sh
ddev exec vendor/bin/infection --version
```

Prints the application name and version and exits 0, confirming the binary resolves
inside the container. Verified against Infection 0.35.4's own `Application` class:
it extends Symfony Console's `Application`, and `--version` carries no positional
argument, so Infection's own routing — which otherwise rewrites a bare invocation to
its `run` command — leaves it untouched and Symfony's own `--version` handling
answers instead. Neither `infection.json5` nor a coverage driver is needed to answer
this.

```text
ddev exec vendor/bin/infection run --no-interaction web/modules/custom/my_module/src
```

This is the form mutation runs take once `infection.json5` and a coverage driver are
in place; `--version` above only proves the binary is on the container's `PATH`. If
the command is not found at all, the package is absent: install, then run it again.
