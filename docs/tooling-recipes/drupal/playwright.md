---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_playwright_tooling
capability: playwright
description: Use when a Drupal project needs Playwright for end-to-end or visual-regression testing. Says how to install it and how to run it.
# Metadata, read only after a match.
label: Playwright (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: drupal
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# Playwright (Drupal)

## Goal

Playwright drives a real browser against a running site and reports what happened — a page that
did not load, a form that did not submit, a screenshot that does not match a baseline. It is the
one tool behind two process recipes: `drupal/e2e-setup-atk.md` runs it against user journeys, and
`drupal/visual-regression-setup.md` runs it against rendered pages. Both name this recipe as their
`playwright` tooling dependency, so it installs and runs the same way for either.

`@playwright/test` is the package: it carries the `playwright` CLI, the test runner, and
`npx playwright install`, which downloads the browser binaries separately from the package.

## Install

Playwright runs on the host, never inside a container — the site is reached by address, not by
being inside the same filesystem as the browser.

```sh
npm install --save-dev @playwright/test
```

```sh
npx playwright install chromium
```

The second step downloads the Chromium binary only; it does not touch system libraries. On a host
missing one, the first run against a real page names it, and `npx playwright install-deps
chromium` installs it — that step needs root or `sudo` on Linux, so it is not run here without a
person's consent.

## Run

```sh
node_modules/.bin/playwright --version
```

Before the Install step, this is not found and exits non-zero: install, then run it again. After
it, it prints the resolved package's version, such as `Version 1.63.0`, and exits 0. The two
process recipes above invoke Playwright as `npx playwright …` for a real run, because `npx`
resolves the same binary and is the form their own commands take; `npx` can also resolve a copy
outside the project, so `node_modules/.bin/playwright` is the more reliable proof this project has
its own.
