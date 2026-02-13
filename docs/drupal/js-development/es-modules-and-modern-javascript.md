---
description: Modern ES6+ JavaScript features available in Drupal 10/11 without build process
drupal_version: "10.x/11.x"
---

# ES Modules and Modern JavaScript

## When to Use

> Use when understanding modern JavaScript features available in Drupal 10/11 and how to use ES6+ syntax.

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

## Common Mistakes

- **Wrong**: Using import/export statements → **Right**: Use IIFE pattern for now
  - **Why**: Not fully supported in Drupal library system yet, breaks loading
- **Wrong**: Arrow functions in IIFE parameters → **Right**: Use standard function syntax
  - **Why**: Unnecessary, standard function works fine
- **Wrong**: Assuming all ES2020+ features work → **Right**: Check browser support
  - **Why**: Browser support varies, test compatibility
- **Wrong**: Using *.es6.js extension → **Right**: Use .js extension directly
  - **Why**: Transpilation system removed in Drupal 10

## See Also

- Reference: [ES6 directly in .js files](https://www.drupal.org/node/3305487)
- Reference: [ES6 for Drupal Developers](https://preston.so/writing/es6-for-drupal-developers-es6-modules-classes-and-promises/)
- Reference: [JavaScript Dependency Plan](https://www.drupal.org/project/drupal/issues/3238507)
