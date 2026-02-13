---
description: Test JavaScript functionality with Nightwatch.js for AJAX, accessibility, and browser compatibility
drupal_version: "10.x/11.x"
---

# Testing JavaScript

## When to Use

> Use when verifying JavaScript functionality, especially AJAX interactions, accessibility, and cross-browser compatibility.

## Decision

Drupal uses Nightwatch.js for JavaScript testing (replaced PHPUnit's FunctionalJavascriptTestBase). Nightwatch runs tests in real browsers using WebDriver, enabling true JavaScript and accessibility testing.

## Pattern

**Test file location**:

```
modules/custom/MODULE/tests/src/Nightwatch/Tests/featureTest.js
```

**Basic Nightwatch test**:

```javascript
module.exports = {
  '@tags': ['module_name'],

  'Test feature behavior': (browser) => {
    browser
      .drupalInstall()
      .drupalLoginAsAdmin()
      .drupalRelativeURL('/admin/config')
      .waitForElementVisible('.element-selector', 1000)
      .click('.button-selector')
      .assert.textContains('.result', 'Expected text')
      .drupalLogAndEnd({onlyOnError: false});
  }
};
```

**Testing AJAX**:

```javascript
'Test AJAX interaction': (browser) => {
  browser
    .click('.ajax-trigger')
    .waitForElementVisible('.ajax-result', 2000)
    .assert.textContains('.ajax-result', 'Updated content');
}
```

**Accessibility testing** (with aXe):

```javascript
'Test accessibility': (browser) => {
  browser
    .drupalRelativeURL('/page')
    .initAccessibility()
    .assert.accessibility();
}
```

**Running tests**:

```bash
# From Drupal root
yarn test:nightwatch tests/Nightwatch/Tests/featureTest.js
```

## Common Mistakes

- **Wrong**: Testing with PHP instead of JavaScript → **Right**: Use Nightwatch for JS
  - **Why**: Can't test actual JavaScript execution, Nightwatch is correct tool
- **Wrong**: No accessibility tests → **Right**: Include accessibility assertions
  - **Why**: Misses WCAG compliance issues that affect users
- **Wrong**: Not testing AJAX scenarios → **Right**: Test AJAX interactions
  - **Why**: Most common source of JavaScript bugs in Drupal
- **Wrong**: Hardcoded waits instead of waitForElement → **Right**: Use smart waits
  - **Why**: Flaky tests, timing issues

## See Also

- [AJAX Integration](ajax-integration.md) - What to test
- Reference: [JavaScript Testing with Nightwatch](https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch)
- Reference: [Nightwatch in Drupal Core](https://www.lullabot.com/articles/nightwatch-in-drupal-core)
- Reference: [Functional JavaScript Testing](https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs)
