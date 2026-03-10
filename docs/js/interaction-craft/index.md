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

| I need to... | Guide |
|---|---|
| Choose between debounce, throttle, or rAF for an event | [Debounce and Throttle](debounce-and-throttle.md) |
| Trap focus in a modal, implement roving tabindex | [Keyboard Navigation Craft](keyboard-navigation-craft.md) |
| Set up IntersectionObserver, scroll-linked state, infinite scroll | [Scroll Interaction Patterns](scroll-interaction-patterns.md) |
| Build drag-and-drop with touch support and keyboard equivalent | [Drag and Drop Craft](drag-and-drop-craft.md) |
| Update UI immediately before server confirms | [Optimistic UI](optimistic-ui.md) |
| Detect swipes, pinch, long-press on touch devices | [Touch and Gesture Craft](touch-and-gesture-craft.md) |
| Copy to clipboard with visual feedback | [Clipboard and Copy Patterns](clipboard-and-copy-patterns.md) |
| Decide when to validate, build autosave, inline editing | [Form Interaction Craft](form-interaction-craft.md) |
| Sequence, cancel, or coordinate JS animations | [Animation Orchestration](animation-orchestration.md) |
| Avoid layout thrashing, prevent memory leaks, break up long tasks | [Performance and Event Handling](performance-and-event-handling.md) |
