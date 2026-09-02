---
description: "Handle user interactions with addEventListener, event delegation, and debouncing"
tldr: "Use vanilla addEventListener for user interactions, event delegation for dynamic content, and debounce/throttle for performance-intensive events, with keyboard handling for accessibility. Gotcha: no debounce on scroll/resize/input executes hundreds of times per second and freezes the UI."
drupal_version: "11.x"
---

# Event Handling

## When to Use

> Responding to user interactions (clicks, input changes, scrolling) or custom application events.

## Decision

Use vanilla JavaScript addEventListener for modern code. Implement event delegation for dynamic content. Use debounce/throttle for performance-intensive events. Ensure accessibility with keyboard events.

## Pattern

**Standard event handling**:
```javascript
Drupal.behaviors.eventHandling = {
  attach(context) {
    once('events', '.button', context).forEach(function (element) {
      element.addEventListener('click', function (event) {
        event.preventDefault();
        // Handle click
      });
    });
  }
};
```

**Event delegation** (for dynamic content):
```javascript
// Instead of binding to individual elements
// Bind to parent, filter by selector
document.addEventListener('click', function (event) {
  if (event.target.matches('.dynamic-element')) {
    // Handle click on dynamically-added elements
    handleClick(event.target);
  }
});
```

**Debounced events** (performance):
```javascript
// Dependency: core/drupal.debounce
const handleInput = Drupal.debounce(function (event) {
  // Expensive operation (search, validation)
  // Runs max once per 300ms
}, 300);

element.addEventListener('input', handleInput);
```

**Keyboard accessibility**:
```javascript
element.addEventListener('keydown', function (event) {
  // Enter or Space activates like click
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    element.click();
  }
});
```

**Custom events**:
```javascript
// Dispatch custom event
const customEvent = new CustomEvent('drupal:moduleEvent', {
  detail: {data: 'value'},
  bubbles: true
});
element.dispatchEvent(customEvent);

// Listen for custom event
document.addEventListener('drupal:moduleEvent', function (event) {
  console.log(event.detail.data);
});
```

**Reference**: Debounce in core - https://medium.com/@cristinallamas/debounce-functions-in-drupal-js-scripts-3727bdefa11c

## Common Mistakes

- **No debounce on scroll/resize/input** - WHY: Executes hundreds of times per second, freezes UI
- **Binding events without once()** - WHY: Duplicate bindings on AJAX updates, memory leaks
- **Missing keyboard handling** - WHY: Breaks accessibility, fails WCAG compliance
- **Using jQuery .on() unnecessarily** - WHY: addEventListener is native, faster, no jQuery dependency
- **Not removing listeners in detach()** - WHY: Memory leaks, ghost event handlers

## See Also

- [Debounce and Throttle](debounce-and-throttle.md) - Performance patterns
- Reference: [Accessibility Event Patterns](https://www.drupal.org/docs/drupal-apis/javascript-api/accessibility-tools-for-javascript-in-drupal)
