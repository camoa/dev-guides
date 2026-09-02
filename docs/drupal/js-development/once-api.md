---
description: "Prevent duplicate JavaScript initialization on elements using the once() API"
tldr: "Wrap every element you process in a behavior with once() so it runs exactly once even when the behavior re-executes on AJAX updates. Gotcha: once() writes a single data-once attribute holding a space-separated id list, not a per-id attribute."
drupal_version: "11.x"
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

**How it works**: once() adds a single `data-once` attribute whose value is a space-separated list of ids, and skips elements already carrying the id in subsequent runs. There is no per-id attribute — a selector written against one never matches.

**Migration reference**: https://drupalbook.org/blog/replace-jqueryonce-javascript-once-drupal-10

## Common Mistakes

- **Using jQuery.once()** - WHY: Removed in Drupal 10, code breaks
- **Same once ID across different purposes** - WHY: Elements get skipped incorrectly, mysterious bugs
- **Forgetting context parameter** - WHY: Processes entire document, breaks AJAX, performance penalty
- **Processing without once()** - WHY: Code runs multiple times, duplicate event bindings, memory leaks, broken functionality
- **Generic once IDs like 'init'** - WHY: Conflicts with other modules using same ID

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Where once() is used
- Reference: [Once API on npm](https://www.npmjs.com/package/@drupal/once) - Full API documentation
- Reference: [Drupal 10 Once Migration](https://www.drupal.org/node/3158256) - jQuery.once removal
