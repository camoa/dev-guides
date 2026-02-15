---
description: Use Nightwatch.js for JavaScript functional testing, accessibility testing, and cross-browser testing in Drupal.
---

# Nightwatch.js Testing

## When to Use
JavaScript functional testing for complex UI interactions, accessibility testing, cross-browser testing.

## Decision
| Use case | Use Nightwatch? | Alternative |
|---|---|---|
| Accessibility (a11y) testing | YES -- built-in a11y commands | Manual WAVE testing |
| Complex multi-step JS workflows | YES | WebDriverTestBase (if Drupal-specific) |
| Cross-browser compatibility | YES | WebDriverTestBase (Chrome only) |
| Simple AJAX testing | NO | WebDriverTestBase (faster) |

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
yarn test:nightwatch

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
    .assert.axeViolationsCount(0); // No a11y violations
}
```

**File location**: `modules/my_module/tests/src/Nightwatch/Tests/myTest.js`

Reference: `/core/tests/Drupal/Nightwatch/`

## Common Mistakes
- Not installing Node.js/yarn before running -- tests don't execute
- Using absolute URLs instead of `drupalRelativeURL()` -- breaks in different environments
- Not waiting for elements -- intermittent failures
- Running Nightwatch for unit-level JS logic -- overkill (use Jest for unit tests)
- Forgetting `@tags` annotation -- can't filter tests by module

## See Also
- [Spec-Driven Drupal Development](spec-driven-drupal-development.md)
- [Running Tests](running-tests.md)
- Reference: `/core/tests/Drupal/Nightwatch/README.md`
