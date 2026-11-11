---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_phpunit_tooling
capability: phpunit
description: Use when a Drupal project needs PHPUnit installed and configured through drupal/core-dev. Says how to install it and how to run it.
# Metadata, read only after a match.
label: PHPUnit (Drupal)
recipe_schema_version: 1.0.0
version: 0.2.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# PHPUnit (Drupal)

## Goal

PHPUnit runs the Unit, Kernel, Functional, FunctionalJavascript and Build tests a
Drupal project writes, and reports each assertion that did not hold. Drupal does not
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

That flag lets Composer move packages the project already has, not only `core-dev`'s own. On
one fresh `drupal/recommended-project` install it moved Symfony, Twig and `nikic/php-parser`,
and took `sebastian/diff` down a major version. The command does not show this, so tell the person
approving the install, and read the lock-file diff afterwards.

Do not add `phpunit/phpunit` to the project's own `composer.json`. `core-dev`
already carries the constraint core itself is tested against, so a direct
requirement is redundant and can drift from core's — it conflicts with the pin
only when its own range excludes what `core-dev` allows.

PHPUnit also needs a `phpunit.xml` at the project root, beside `composer.json` and
`vendor/`, the location that same documentation places it at. Core ships
`<docroot>/core/phpunit.xml.dist`, but a copy of it is not usable as it stands: every relative path
inside it is written for `core/`, and the database and base-URL variables ship empty. The script
under `## Files` writes the file, and this step runs it inside the web container:

```sh
ddev exec php .aida/phpunit/write-phpunit-xml.php
```

The step runs through DDEV, as every other line here does. The container is where PHP and its DOM
extension are certain, because core requires both, and where DDEV sets the site's address. The
script does what [PHPUnit Configuration](../../drupal/tdd/phpunit-configuration.md) describes,
in one pass:

- It reads the docroot from `composer.json`'s `extra.drupal-scaffold.locations.web-root`: `web/`,
  `docroot/`, or none when Drupal sits at the project root.
- It copies `<docroot>/core/phpunit.xml.dist` to `phpunit.xml`, with the docroot and `core/` in
  front of `bootstrap` and of the coverage paths, and the docroot in front of the browser-output
  directory, which it creates.
- It replaces core's testsuites with five, `unit`, `kernel`, `functional`,
  `functional-javascript` and `build`, each scanning `<docroot>/modules/custom/*/tests/src/<Tier>`.
  Core's sixth, `unit-component`, covers core's own components and no project tier. Core's own
  suites also scan every contrib module's tests, and one broken contrib test class then fails the
  whole listing.
- It sets `SIMPLETEST_DB` to `mysql://db:db@db/db` in a DDEV web container whose database is MySQL
  or MariaDB. It sets `SIMPLETEST_BASE_URL` from `DDEV_PRIMARY_URL`, the address DDEV puts in the
  web container's environment. Anywhere else it leaves each value empty, and prints a line saying so.
- It leaves a `phpunit.xml` that already exists as it is, and says so. A second run changes
  nothing.

A person still checks four things:

- A value the script left empty: a project outside DDEV, or a DDEV project on PostgreSQL, fills it
  by hand.
- `DDEV_PRIMARY_URL` is `https://` when DDEV's certificate is trusted. The guide above names
  `https://` as the cause of an "invalid cookie domain" error in FunctionalJavascript tests. A
  project that runs them changes the value to `http://`.
- The suites cover custom modules only. A project whose custom themes or whose own `recipes/`
  folder carry tests adds those directories to the same suites.
- An existing `phpunit.xml` kept its own paths and values, and stays the person's to correct.

The install commits nothing. Commit `.aida/phpunit/` with the `composer.json` and `composer.lock`
changes, so the tree is clean and every checkout has the script. List `phpunit.xml` itself in
`.gitignore`, as the guide advises, because `SIMPLETEST_BASE_URL` names this checkout's site. A
checkout without it, a fresh clone or a task's worktree with its own DDEV project, runs the same
line there and gets its own address. Until the file exists, this recipe's own Run fails, as
`## Run` describes.

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
left unrewritten from core's copy prints `Cannot open bootstrap script` and
exits 2 — each names the specific defect rather than a generic failure.

The header can print with nothing listed under it and still exit 0 — PHPUnit
lists a suite only where its `<directory>` glob matches at least one test class,
so an empty list on a project with no tests yet is expected, verified the same
way. It stops being expected once a module under the configured directories
carries a test file and still does not appear; that combination is a finding.

If the command itself is not found, the package is absent: install, then run it
again.

## Files

One PHP script, written where absent before the first install line runs, the path as the fence's
second word.

```php .aida/phpunit/write-phpunit-xml.php
<?php

/**
 * @file
 * Writes phpunit.xml at the project root from core's phpunit.xml.dist.
 *
 * Run from the project root, beside composer.json. An existing phpunit.xml is
 * left as it is. Exit 1 names what is missing.
 */

if (file_exists('phpunit.xml')) {
  echo "phpunit.xml exists, left as it is; this script writes it only where absent\n";
  exit(0);
}
$composer = json_decode((string) @file_get_contents('composer.json'), TRUE);
if (!is_array($composer)) {
  fwrite(STDERR, "no readable composer.json in " . getcwd() . "; run this from the project root\n");
  exit(1);
}
// The scaffold plugin's own default web-root is '.', the project root.
$docroot = trim($composer['extra']['drupal-scaffold']['locations']['web-root'] ?? '.', '/');
$docroot = ($docroot === '.' || $docroot === '') ? '' : preg_replace('#^\./#', '', $docroot) . '/';
$dist = $docroot . 'core/phpunit.xml.dist';
$doc = new DOMDocument();
$doc->preserveWhiteSpace = TRUE;
if (!is_file($dist) || !$doc->load($dist)) {
  fwrite(STDERR, "cannot read $dist; composer.json names the docroot '$docroot', and drupal/core must be installed there\n");
  exit(1);
}
$root = $doc->documentElement;
$xpath = new DOMXPath($doc);

// The dist's paths are written for core/. bootstrap and the coverage paths,
// <source> from 11.x and <coverage> before it, are read against the file's own
// folder, so core/ goes in front of each.
$in_core = function (string $path) use ($docroot): string {
  $parts = [];
  foreach (explode('/', $docroot . 'core/' . $path) as $part) {
    if ($part === '..' && $parts && end($parts) !== '..') {
      array_pop($parts);
    }
    elseif ($part !== '.' && $part !== '') {
      $parts[] = $part;
    }
  }
  return implode('/', $parts);
};
$root->setAttribute('bootstrap', $in_core($root->getAttribute('bootstrap')));
foreach ($xpath->query('/phpunit/source//directory | /phpunit/coverage//directory') as $node) {
  $node->nodeValue = $in_core($node->nodeValue);
}
// The HTML logger reads this against the folder PHPUnit runs from, the project
// root, so it takes the docroot only.
foreach ($xpath->query('//parameter[@name="outputDirectory"]') as $node) {
  $node->setAttribute('value', $docroot . $node->getAttribute('value'));
  // The logger writes nothing, and says so, while the folder is absent.
  is_dir($node->getAttribute('value')) || mkdir($node->getAttribute('value'), 0775, TRUE);
}
// Core's suites scan core and every contrib module; one broken contrib test
// class then fails the whole listing. These five scan the project's own modules.
$suites = $xpath->query('/phpunit/testsuites')->item(0);
while ($suites->firstChild) {
  $suites->removeChild($suites->firstChild);
}
foreach (['unit' => 'Unit', 'kernel' => 'Kernel', 'functional' => 'Functional', 'functional-javascript' => 'FunctionalJavascript', 'build' => 'Build'] as $name => $tier) {
  $suite = $doc->createElement('testsuite');
  $suite->setAttribute('name', $name);
  $suite->appendChild($doc->createTextNode("\n      "));
  $suite->appendChild($doc->createElement('directory', $docroot . "modules/custom/*/tests/src/$tier"));
  $suite->appendChild($doc->createTextNode("\n    "));
  $suites->appendChild($doc->createTextNode("\n    "));
  $suites->appendChild($suite);
}
$suites->appendChild($doc->createTextNode("\n  "));

$env = function (string $name, string $value) use ($xpath): void {
  $xpath->query("/phpunit/php/env[@name='$name']")->item(0)->setAttribute('value', $value);
};
$said = [];
$url = (string) getenv('DDEV_PRIMARY_URL');
if ($url !== '') {
  $env('SIMPLETEST_BASE_URL', $url);
  $said[] = "SIMPLETEST_BASE_URL: $url, from DDEV_PRIMARY_URL";
}
else {
  $said[] = "SIMPLETEST_BASE_URL: left empty, because DDEV_PRIMARY_URL is not set here; fill it before a Functional test runs";
}
if (getenv('IS_DDEV_PROJECT') === 'true' && getenv('DDEV_DATABASE_FAMILY') === 'mysql') {
  $env('SIMPLETEST_DB', 'mysql://db:db@db/db');
  $said[] = "SIMPLETEST_DB: mysql://db:db@db/db, DDEV's database";
}
else {
  $said[] = "SIMPLETEST_DB: left empty, because this is not a DDEV MySQL or MariaDB web container; fill it before a Kernel test runs";
}
if ($doc->save('phpunit.xml') === FALSE) {
  fwrite(STDERR, "could not write phpunit.xml in " . getcwd() . "\n");
  exit(1);
}
echo "phpunit.xml: written from $dist\n" . implode("\n", $said) . "\n";
```
