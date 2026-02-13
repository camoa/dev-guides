---
description: Prevent duplicate JavaScript initialization on elements using the once() API
drupal_version: "10.x/11.x"
---

# Once API

## When to Use

> **Every time** you process elements in a behavior. The once() API prevents duplicate initialization and is required for proper AJAX compatibility.

## Decision

The once() API marks elements as processed using a data attribute, ensuring code runs only once per element even when behaviors re-execute. As of Drupal 10, once() is vanilla JavaScript (removed jQuery.once dependency).

**Critical change in Drupal 10**: `jQuery.once()` removed, replaced with `@drupal/once` npm package. Must use `core/once` dependency and `once()` function.

## Pattern

**Standard once() pattern**:

```javascript
// Returns array of unprocessed elements
once('unique-identifier', '.selector', context).forEach(function (element) {
  // This code runs exactly once per element
  // even if behavior runs multiple times
});
```

**Multiple selectors**:

```javascript
once('tabs-init', '.tab, .accordion, .toggle', context).forEach(function (element) {
  // Handles multiple selector types with one once ID
});
```

**Removing once tracking** (rare, for dynamic updates):

```javascript
// Mark element as unprocessed (removes data attribute)
// Use in detach() when element will be reprocessed
once.remove('unique-id', '.selector', context);
```

**Checking if already processed**:

```javascript
// Use once.find() to get already-processed elements
const processedElements = once.find('unique-id', context);
```

**How it works**: once() adds `data-once-unique-identifier` attribute to processed elements and skips them in subsequent runs.

## Common Mistakes

- **Wrong**: Using jQuery.once() → **Right**: Use once() from core/once
  - **Why**: jQuery.once() removed in Drupal 10, code breaks
- **Wrong**: Same once ID across different purposes → **Right**: Use unique, descriptive IDs
  - **Why**: Elements get skipped incorrectly, mysterious bugs
- **Wrong**: Forgetting context parameter → **Right**: Always pass context as third parameter
  - **Why**: Processes entire document, breaks AJAX, performance penalty
- **Wrong**: Processing without once() → **Right**: Always wrap with once()
  - **Why**: Code runs multiple times, duplicate event bindings, memory leaks, broken functionality
- **Wrong**: Generic once IDs like 'init' → **Right**: Namespace with module name
  - **Why**: Conflicts with other modules using same ID

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Where once() is used
- Reference: [Once API on npm](https://www.npmjs.com/package/@drupal/once) - Full API documentation
- Reference: [Drupal 10 Once Migration](https://www.drupal.org/node/3158256) - jQuery.once removal
- Reference: [Drupal Book: Replace jQuery.once](https://drupalbook.org/blog/replace-jqueryonce-javascript-once-drupal-10)
