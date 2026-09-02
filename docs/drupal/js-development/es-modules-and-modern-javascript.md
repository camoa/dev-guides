---
description: "Modern ES6+ JavaScript features available in Drupal 10/11 without build process"
tldr: "Understand modern JavaScript features available in Drupal 10/11: ES6+ syntax works directly in .js files with no build process, since Drupal 10 dropped IE11 support. Gotcha: import/export statements are not fully supported in Drupal's library system yet."
drupal_version: "11.x"
---

# ES Modules and Modern JavaScript

## When to Use

> Understanding modern JavaScript features available in Drupal 10/11 and how to use ES6+ syntax.

## Decision

**Drupal 10+**: ES6+ syntax directly in .js files (no build process required). The *.es6.js transpilation system was removed because all supported browsers now support ES6. Use modern JavaScript features but be aware of browser support requirements.

**Critical change**: Drupal 10 dropped IE11 support, enabling native ES6+. No babel/webpack required for standard development.

## Pattern

**Modern JavaScript features available**:
```javascript
// Arrow functions
once('modern', '.element', context).forEach((element) => {
  element.addEventListener('click', (e) => handleClick(e));
});

// Destructuring
const {apiEndpoint, itemsPerPage} = settings.moduleName.config;

// Template literals
const message = `Loading ${itemsPerPage} items from ${apiEndpoint}`;

// const/let (block scope)
const config = settings.moduleName;
let counter = 0;

// Spread operator
const mergedSettings = {...defaults, ...customSettings};

// Async/await
async function fetchData() {
  const response = await fetch(endpoint);
  const data = await response.json();
  return data;
}
```

**ES Modules** (limited support currently):
```javascript
// Import/export not fully supported in Drupal library system yet
// Use traditional IIFE pattern for now
(function (Drupal, once) {
  'use strict';
  // Module code
})(Drupal, once);
```

**Reference**:
- https://www.drupal.org/node/3305487 - ES6 directly in .js files
- https://preston.so/writing/es6-for-drupal-developers-es6-modules-classes-and-promises/ - ES6 patterns

## Common Mistakes

- **Using import/export statements** - WHY: Not fully supported in Drupal library system yet, breaks loading
- **Arrow functions in IIFE parameters** - WHY: Unnecessary, standard function works fine
- **Assuming all ES2020+ features work** - WHY: Browser support varies, check compatibility
- **Using *.es6.js extension** - WHY: Removed in Drupal 10, use .js directly

## See Also

- Reference: [Drupal 10 JavaScript Dependency Plan](https://www.drupal.org/project/drupal/issues/3238507)
- Reference: [ES6 for Drupal Developers](https://preston.so/writing/es6-for-drupal-developers-es6-modules-classes-and-promises/)
