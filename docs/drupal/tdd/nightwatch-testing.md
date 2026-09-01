---
description: "Nightwatch.js is not deprecated but core has accepted a policy to replace it with Playwright; use it only for cross-browser runs and axe accessibility sweeps, WebDriverTestBase for everything else."
tldr: "Reach for Nightwatch only for cross-browser runs and axe-based accessibility sweeps WebDriverTestBase can't do; it is not deprecated, but core accepted a policy in Nov 2025 to replace it with Playwright (not yet landed)."
---

# Nightwatch.js Testing

## When to Use
JavaScript-in-JavaScript functional testing that PHPUnit's browser tiers cannot express: cross-browser runs, and the accessibility sweeps core still drives through axe. Read the status note first — Nightwatch works today and is on a decided path out.

## Status: not deprecated, but replacement is decided
Nightwatch is **not** deprecated. It entered core in 8.6 ([change record](https://www.drupal.org/node/2968570)), still ships in 11.4.x as `nightwatch ^3.12.3` with `core/tests/Drupal/Nightwatch/` and a `yarn test:nightwatch` script, and no change record announces a deprecation.

What is decided is the direction. Core accepted a policy in November 2025 ([#3467492](https://www.drupal.org/project/drupal/issues/3467492)) to add Playwright, convert the Nightwatch tests to it, and move some coverage to PHPUnit FunctionalJavascript with Axe — the stated reason being that Nightwatch is "extremely unreliable and the cause of many random pipeline test failures."

What has **not** happened is any of it. Playwright appears in no core branch, including `main`; the migration issue ([#3553673](https://www.drupal.org/project/drupal/issues/3553673)) is open and targets Drupal 12; and the companion effort to move the axe tests into PHPUnit ([#3338664](https://www.drupal.org/project/drupal/issues/3338664)) has not landed either. The official documentation carries no transition notice.

**What that means for a module.** FunctionalJavascript (`WebDriverTestBase`) is the recommendation for JavaScript and Ajax behaviour and is unaffected by any of this. Reach for Nightwatch only for what that tier genuinely cannot do, and treat new Nightwatch coverage as work with a migration attached.

## Decision
| Use case | Use Nightwatch? | Alternative |
|---|---|---|
| JavaScript or Ajax behaviour in a Drupal page | NO | `WebDriverTestBase` — the recommended tier, and the one unaffected by the Playwright policy |
| Accessibility (a11y) sweeps | Works today, via axe | PHPUnit FunctionalJavascript + Axe is where core intends this to land ([#3338664](https://www.drupal.org/project/drupal/issues/3338664)) |
| Cross-browser compatibility | Yes — the one thing the PHPUnit tiers cannot do | None in core today |
| Complex multi-step JS workflows | Only if `WebDriverTestBase` cannot express it | `WebDriverTestBase` |
| Unit-level JavaScript logic | NO | Core ships no JS unit-test runner — a module adds its own (Jest, Vitest) outside core's tooling |

## Pattern
**Nightwatch test structure** (`tests/src/Nightwatch/Tests/myTest.js`):
```javascript
module.exports = {
  '@tags': ['my_module'],

  before(browser) {
    browser
      .drupalInstall({
        installProfile: 'standard'
      });
  },

  'Test page loads': (browser) => {
    browser
      .drupalRelativeURL('/my-module/page')
      .waitForElementVisible('body', 1000)
      .assert.textContains('h1', 'Expected Title')
      .end();
  },

  after(browser) {
    browser.drupalUninstall();
  }
};
```

**Running Nightwatch tests**:
```bash
# Inside core/ directory
yarn install
cp .env.example .env
# Edit .env: set DRUPAL_TEST_BASE_URL, etc.

# Run all tests
yarn test:nightwatch --env local

# Run specific tag
yarn test:nightwatch --tag my_module

# Run specific file
yarn test:nightwatch tests/Drupal/Nightwatch/Tests/myTest.js
```

**Accessibility testing**:
```javascript
'Test accessibility': (browser) => {
  browser
    .drupalRelativeURL('/admin/content')
    .waitForElementVisible('body', 1000)
    .axeInject()
    .axeRun('body', {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'],
      },
    });
}
```

**File location**: `modules/my_module/tests/src/Nightwatch/Tests/myTest.js`

**How discovery actually works.** `nightwatch.conf.js` globs `**/tests/**/Nightwatch/**/*.js` upward from `core/`, and only collects a directory whose next segment is `Tests`, `Commands`, `Assertions`, or `Pages` — a file one level off that path is silently never run. The search root is the parent of `core/`, overridable with `DRUPAL_NIGHTWATCH_SEARCH_DIRECTORY`, and directories can be excluded with `DRUPAL_NIGHTWATCH_IGNORE_DIRECTORIES` (`vendor/**` is always ignored).

Reference: `/core/tests/Drupal/Nightwatch/` — the directory holds `Commands/`, `Assertions/`, `Tests/`, `globals.js` and `nightwatch.conf.js`. There is **no README.md** inside it; the Nightwatch instructions live in `/core/tests/README.md`.

## Common Mistakes
- Not installing Node.js/yarn before running → tests don't execute
- Using absolute URLs instead of `drupalRelativeURL()` → breaks in different environments
- Not waiting for elements → intermittent failures
- Running Nightwatch for unit-level JS logic → overkill, and core ships no JS unit-test runner to fall back on — a module supplies its own (Jest, Vitest) outside core's tooling
- Reaching for Nightwatch because a test needs a browser → `WebDriverTestBase` drives a real browser too, is the recommended tier, and is not the one core has decided to replace
- Forgetting `@tags` annotation → can't filter tests by module

## See Also
- ← Previous: Spec-Driven Drupal Development | Next: Running Tests →
- Reference: `/core/tests/README.md`, "Running Nightwatch tests" (line 91 onward in 11.4.x)
- Official documentation: [JavaScript testing using Nightwatch](https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch) — carries no transition notice as of 2026-09-01
- Policy: [#3467492 Replace Nightwatch with Playwright](https://www.drupal.org/project/drupal/issues/3467492) (accepted November 2025) and [#3553673](https://www.drupal.org/project/drupal/issues/3553673) (migration, open, Drupal 12)
