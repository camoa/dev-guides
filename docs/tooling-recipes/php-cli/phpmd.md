---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: php_cli_phpmd_tooling
capability: phpmd
description: Use when a PHP CLI project needs PHPMD to flag oversized methods and design smells. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPMD (PHP CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: php-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPMD (PHP CLI)

## Goal

PHPMD reads PHP against a fixed set of rules and reports the shape problems a
standards checker does not look for — a method with too many lines or too many
branches, a class with too many dependencies, a public property that could be
private. `codesize` measures size and complexity; `design` measures coupling and
class shape. With it installed, a claim that a class or method in a PHP CLI
project's library has grown too large to review can be checked rather than
asserted.

## Install

```sh
composer require --dev phpmd/phpmd
```

PHPMD registers no Composer plugin, so there is no `allow-plugins` step and no
separate registration command — the package is ready to run once required.

PHPMD's latest release, 2.15.0 (2023-12-11), runs on PHP 8.3 but its parser
cannot read PHP 8.4 syntax it has never had to handle: `new` without
parentheses, asymmetric visibility (`protected(set)`), and property hooks each
make it error out on the file rather than report on it (phpmd/phpmd issues
#1219, #1237, #1271). A scan over code using any of them fails, not a clean
report. The fix lives only on the unreleased `3.x` branch, whose CLI drops the
positional `phpmd <paths> <format> <ruleset>` form for named flags —
`phpmd analyze <paths> --format <format> --ruleset <ruleset>` — so the `text`
example below changes once 3.0 ships.

## Run

```sh
php vendor/bin/phpmd --version
```

PHPMD's own usage is `phpmd <paths> <report-format> <ruleset(s)>`, all three
positional and required, so a bare `--version` is the only invocation that proves
the tool is present without also naming a scope:

```text
php vendor/bin/phpmd src text codesize,design
```

A library kept to plain `.php` files needs no `--suffixes` flag, since that is
PHPMD's default; a project that commits a `phpmd.xml` names it in place of the two
shipped rulesets. Findings print to stdout in the chosen format. PHPMD 2.15.0
exits 2 when it reports a violation, 1 when it cannot run at all (a path that does
not exist), and 0 when clean — both non-zero exits are findings, not one success
and one failure.

PHPMD skips a file whose extension is not in its list even when the file is named
directly on the command line, so it never reaches an extensionless Composer binary
under `bin/` — that file is linted and analysed by hand or by a glob-capable pass
instead.

If the command itself is not found, the package is absent: install, then run it
again.
