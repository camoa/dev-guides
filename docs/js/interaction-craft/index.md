---
description: Interaction Craft — vanilla JS patterns for timing, keyboard accessibility, scroll, drag-and-drop, optimistic UI, touch, clipboard, forms, animations, and performance
guide-meta:
  concepts:
    - debounce throttle
    - keyboard navigation
    - focus trap
    - roving tabindex
    - IntersectionObserver
    - drag and drop
    - optimistic UI
    - touch gestures
    - clipboard API
    - animation orchestration
  not:
    - Drupal.behaviors (see drupal/js-development)
    - CSS animations (see css/css-craft)
    - React event handling
  requires: []
  complements:
    - css/css-craft
    - drupal/js-development
    - media/image-media-craft
  specializes: ""
  category: js
---

# Interaction Craft

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between debounce, throttle, or rAF for an event | [Debounce and Throttle](debounce-and-throttle.md) | Use `throttle` or `requestAnimationFrame` when you want continuous updates (scroll, mousemove, progress). Use `debounce` when you want to react once after the user stops (resize, search input, async validation). |
| Trap focus in a modal, implement roving tabindex | [Keyboard Navigation Craft](keyboard-navigation-craft.md) | Use native HTML for single elements (buttons, links). Use roving tabindex for groups of related controls (tabs, toolbars, menus). |
| Set up IntersectionObserver, scroll-linked state, infinite scroll | [Scroll Interaction Patterns](scroll-interaction-patterns.md) | Use `IntersectionObserver` for threshold-based events (entering viewport, lazy load, infinite scroll). Use `scroll` + rAF for continuous position-linked updates (parallax, progress bars). |
| Build drag-and-drop with touch support and keyboard equivalent | [Drag and Drop Craft](drag-and-drop-craft.md) | Use the HTML Drag API for simple desktop-only drag. Use Pointer Events for touch + cross-device support. |
| Update UI immediately before server confirms | [Optimistic UI](optimistic-ui.md) | Use optimistic UI when the expected server response is success and failure is rare. Skip it for destructive, financial, or irreversible actions. |
| Detect swipes, pinch, long-press on touch devices | [Touch and Gesture Craft](touch-and-gesture-craft.md) | Use Pointer Events API for all gestures — it handles mouse, touch, and pen uniformly. Use `touch-action` CSS to declare which axes you own so the browser can optimize scrolling. |
| Copy to clipboard with visual feedback | [Clipboard and Copy Patterns](clipboard-and-copy-patterns.md) | Use `navigator.clipboard.writeText()` as the primary path on HTTPS. Use `navigator.share()` for mobile share sheets. |
| Decide when to validate, build autosave, inline editing | [Form Interaction Craft](form-interaction-craft.md) | Validate on blur for the first time. After the first error, switch to live validation. |
| Sequence, cancel, or coordinate JS animations | [Animation Orchestration](animation-orchestration.md) | Use CSS transitions for simple state changes. Use WAAPI (`element.animate()`) when you need JS-driven values, sequencing, or mid-animation cancellation. |
| Avoid layout thrashing, prevent memory leaks, break up long tasks | [Performance and Event Handling](performance-and-event-handling.md) | Apply these patterns to every JS interaction. Passive listeners, read/write batching, event delegation, and AbortController cleanup are baselines — not optimizations. |
