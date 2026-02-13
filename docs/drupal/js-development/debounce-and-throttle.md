---
description: Optimize high-frequency events with debounce and throttle patterns
drupal_version: "10.x/11.x"
---

# Debounce and Throttle

## When to Use

> Use for events that fire rapidly (scroll, resize, input, mousemove) where executing handler every time causes performance issues.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Search input, form validation | Debounce | Execute only after user stops typing |
| Window resize handlers | Debounce | Execute only after resize completes |
| Scroll progress tracking | Throttle | Execute at controlled intervals |
| Visual updates, animations | requestAnimationFrame | Sync with browser refresh rate |

**Debounce**: Execute handler only after events stop for specified time. **Throttle**: Execute handler at most once per specified interval.

## Pattern

**Debounce pattern** (wait until events stop):

```javascript
// Dependency: core/drupal.debounce
Drupal.behaviors.search = {
  attach(context) {
    once('search', '.search-input', context).forEach(function (input) {
      // Handler executes 300ms after user stops typing
      const debouncedSearch = Drupal.debounce(function (event) {
        performSearch(event.target.value);
      }, 300);

      input.addEventListener('input', debouncedSearch);
    });
  }
};
```

**Throttle pattern** (limit execution rate):

```javascript
// Execute at most once per 100ms
let lastRun = 0;
window.addEventListener('scroll', function () {
  const now = Date.now();
  if (now - lastRun >= 100) {
    lastRun = now;
    handleScroll();
  }
});
```

**requestAnimationFrame** (visual updates):

```javascript
// Better than throttle for visual changes
let ticking = false;
window.addEventListener('scroll', function () {
  if (!ticking) {
    requestAnimationFrame(function () {
      handleScroll();
      ticking = false;
    });
    ticking = true;
  }
});
```

## Common Mistakes

- **Wrong**: No debounce on input events → **Right**: Debounce search/validation
  - **Why**: Handler fires on every keystroke, performance penalty
- **Wrong**: Scroll handler without throttle → **Right**: Throttle or use requestAnimationFrame
  - **Why**: Executes hundreds of times during scroll, freezes UI
- **Wrong**: Using setTimeout instead of debounce → **Right**: Use Drupal.debounce
  - **Why**: setTimeout doesn't cancel previous calls, accumulates
- **Wrong**: requestAnimationFrame for non-visual logic → **Right**: Use throttle instead
  - **Why**: Tied to refresh rate, not appropriate for all throttling

## See Also

- [Event Handling](event-handling.md) - Event patterns
- Reference: [Debounce in Drupal](https://medium.com/@cristinallamas/debounce-functions-in-drupal-js-scripts-3727bdefa11c)
- Reference: [Debounce vs Throttle Visual Guide](https://drupalsun.com/david-corbacho/2012/10/10/debounce-and-throttle-visual-explanation)
