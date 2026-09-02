---
description: "Optimize high-frequency events with debounce and throttle patterns"
tldr: "For events that fire rapidly (scroll, resize, input, mousemove), use Drupal's built-in debounce to execute after events stop, or throttle to cap execution rate. Gotcha: requestAnimationFrame suits visual updates better than throttle since it syncs with refresh rate."
drupal_version: "11.x"
---

# Debounce and Throttle

## When to Use

> Events that fire rapidly (scroll, resize, input, mousemove) where executing handler every time causes performance issues.

## Decision

**Debounce**: Execute handler only after events stop for specified time. **Throttle**: Execute handler at most once per specified interval. Use Drupal's built-in debounce (core/drupal.debounce dependency).

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

**When to use which**:
- **Debounce**: Search input, form validation, window resize
- **Throttle**: Scroll handlers, progress tracking
- **requestAnimationFrame**: Animations, visual updates, position tracking

**Reference**: https://medium.com/@cristinallamas/debounce-functions-in-drupal-js-scripts-3727bdefa11c

## Common Mistakes

- **No debounce on input events** - WHY: Handler fires on every keystroke, performance penalty
- **Scroll handler without throttle** - WHY: Executes hundreds of times during scroll, freezes UI
- **Using setTimeout instead of debounce** - WHY: Doesn't cancel previous timeouts, accumulates calls
- **requestAnimationFrame for non-visual logic** - WHY: Tied to refresh rate, not appropriate for all throttling

## See Also

- [Event Handling](event-handling.md) - Event patterns
- Reference: [Debounce vs Throttle Visual Guide](https://drupalsun.com/david-corbacho/2012/10/10/debounce-and-throttle-visual-explanation)
