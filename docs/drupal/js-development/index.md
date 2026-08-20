---
description: Drupal JavaScript Development - library-based architecture, behaviors, and modern patterns
tracks:
  - project: drupal
    channel: stable
    verified: 2026-08-20
guide-meta:
  concepts:
    - Drupal.behaviors
    - once API
    - drupalSettings
    - library definitions
    - library attachment
    - JS in SDC components
    - ES modules in Drupal
    - JS aggregation
  not:
    - AJAX framework (see drupal/ajax)
    - HTMX (see drupal/htmx)
    - vanilla JS patterns (see js/interaction-craft)
  requires: []
  complements:
    - drupal/ajax
    - drupal/htmx
    - drupal/ajax-htmx-migration
    - drupal/sdc
    - js/interaction-craft
  specializes: ""
  category: drupal
---

# JavaScript Development

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Drupal's JavaScript architecture | [JavaScript Architecture](javascript-architecture.md) | Use this understanding before implementing any JavaScript functionality in Drupal. This is foundational knowledge for all Drupal JS work. |
| Define a JavaScript library | [Library Definitions](library-definitions.md) | Use every time you add JavaScript to a module or theme. All JS must be defined in a library. |
| Choose core dependencies | [Core Dependencies](core-dependencies.md) | Use when defining any JavaScript library. Dependencies ensure required code loads first. |
| Load scripts in header or footer | [Header vs Footer Loading](header-vs-footer-loading.md) | Use when JavaScript affects critical rendering or initial page display. Otherwise, use default footer loading. |
| Attach libraries via PHP | [Library Attachment Methods](library-attachment-methods.md) | Use when deciding how to attach libraries to pages based on context and conditions. |
| Load JavaScript conditionally | [Conditional Loading](conditional-loading.md) | Use when optimizing performance by loading JavaScript only when needed based on content type, route, user role, or other conditions. |
| Initialize JavaScript on page load and AJAX | [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) | **Always** for DOM manipulation in Drupal. Behaviors are the foundation of Drupal JavaScript - they work with AJAX, BigPipe, and dynamic content loading. |
| Prevent duplicate initialization | [Once API](once-api.md) | **Every time** you process elements in a behavior. The once() API prevents duplicate initialization and is required for proper AJAX compatibility. |
| Pass PHP data to JavaScript | [drupalSettings](drupal-settings.md) | Use when passing server-side data (PHP) to client-side JavaScript. Alternative to AJAX requests for static configuration data available at page render. |
| Manipulate the DOM safely | [DOM Manipulation](dom-manipulation.md) | Use when modifying page structure, content, or attributes in response to user interaction or dynamic updates. |
| Choose between HTMX and legacy AJAX | [AJAX Integration](ajax-integration.md) | Use HTMX (Drupal 11.3+) for new declarative dynamic-content work; use the legacy AJAX API for Drupal 10.x or existing systems. Drupal.behaviors work automatically with both via context — no manual re-init needed. |
| Handle user interactions and events | [Event Handling](event-handling.md) | Use when responding to user interactions (clicks, input changes, scrolling) or custom application events. |
| Use ES6+ features | [ES Modules and Modern JavaScript](es-modules-and-modern-javascript.md) | Use when understanding modern JavaScript features available in Drupal 10/11 and how to use ES6+ syntax. |
| Add JavaScript to SDC components | [JavaScript in SDC Components](javascript-in-sdc-components.md) | Use when adding interactive behavior to Single Directory Components. |
| Optimize JavaScript performance | [Performance Optimization](performance-optimization.md) | Use for every JavaScript implementation - performance is not optional. Frontend performance directly impacts user experience and SEO. |
| Enable aggregation and minification | [Aggregation and Minification](aggregation-and-minification.md) | Use in production environments - always enable JavaScript aggregation for performance. |
| Use defer and async attributes | [Defer and Async Attributes](defer-and-async-attributes.md) | Use as default for most JavaScript - improves page load performance by allowing non-blocking script loading. |
| Debounce or throttle events | [Debounce and Throttle](debounce-and-throttle.md) | Use for events that fire rapidly (scroll, resize, input, mousemove) where executing handler every time causes performance issues. |
| Prevent XSS and secure JavaScript | [Security](security.md) | Use any time JavaScript handles user input, manipulates DOM, or processes data from external sources. |
| Test JavaScript functionality | [Testing JavaScript](testing-javascript.md) | Use when verifying JavaScript functionality, especially AJAX interactions, accessibility, and cross-browser compatibility. |
| Avoid common mistakes | [Common Anti-Patterns](common-anti-patterns.md) | Use when reviewing code for mistakes and understanding what NOT to do. |
| Review code quality standards | [Best Practices Summary](best-practices-summary.md) | Use as a code review checklist and development standards reference. |
