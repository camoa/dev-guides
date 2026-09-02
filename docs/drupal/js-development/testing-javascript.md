---
description: "Test JavaScript functionality with Nightwatch.js for AJAX, accessibility, and browser compatibility"
tldr: "Use Nightwatch.js — which replaced PHPUnit's FunctionalJavascriptTestBase — to verify JavaScript functionality in real browsers via WebDriver, especially AJAX interactions and accessibility. Gotcha: accessibility testing uses .axeInject() and .axeRun(), not .initAccessibility()/.assert.accessibility()."
drupal_version: "11.x"
---

# Testing JavaScript

## When to Use

> Verifying JavaScript functionality, especially AJAX interactions, accessibility, and cross-browser compatibility.

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
    .axeInject()
    .axeRun('body', {});
}
```

**Running tests**:
```bash
# From Drupal root
yarn test:nightwatch tests/Nightwatch/Tests/featureTest.js
```

**Reference**:
- https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch
- https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs

## Common Mistakes

- **Testing with PHP instead of JavaScript** - WHY: Can't test actual JavaScript execution, Nightwatch is correct tool
- **No accessibility tests** - WHY: Misses WCAG compliance issues that affect users
- **Not testing AJAX scenarios** - WHY: Most common source of JavaScript bugs in Drupal
- **Hardcoded waits instead of waitForElement** - WHY: Flaky tests, timing issues

## See Also

- [AJAX Integration](ajax-integration.md) - What to test
- Reference: [Nightwatch in Drupal Core](https://www.lullabot.com/articles/nightwatch-in-drupal-core)
