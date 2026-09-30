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
  category: drupal
---

# JavaScript Development

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Drupal's JavaScript architecture | [JavaScript Architecture](javascript-architecture.md) | Understand how Drupal loads and manages JavaScript before implementing any JS functionality. Core pattern: libraries define assets, behaviors initialize them, once() prevents duplicate processing. |
| Define a JavaScript library | [Library Definitions](library-definitions.md) | Every JS addition to a module or theme must be defined in a library. Core pattern: MODULE.libraries.yml with js:, dependencies:, and optional css:/version:/attributes:. Gotcha: missing core/drupal or core/once breaks behaviors and once() respectively. |
| Choose core dependencies | [Core Dependencies](core-dependencies.md) | When defining any JavaScript library, declare exactly what your code needs so Drupal loads dependencies automatically. Gotcha: including jQuery when not needed adds ~30KB unnecessarily. |
| Load scripts in header or footer | [Header vs Footer Loading](header-vs-footer-loading.md) | Load JavaScript in the footer by default; only use the header for JS that must execute before page render. Gotcha: header: true is a library-level key, a sibling of js: and version:, not a per-file option. |
| Attach libraries via PHP | [Library Attachment Methods](library-attachment-methods.md) | Choose where to attach a library via #attached based on scope: global (hooks), form-specific (form arrays), template-specific (preprocess), or element-specific (render elements). Gotcha: drupal_add_js() was removed in Drupal 8+. |
| Load JavaScript conditionally | [Conditional Loading](conditional-loading.md) | Evaluate conditions in PHP before attaching libraries, and declare cache contexts so conditional libraries work with page caching. Gotcha: checking conditions in JavaScript instead of PHP defeats the optimization since the JS is already loaded. |
| Initialize JavaScript on page load and AJAX | [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) | Always use Drupal.behaviors for DOM manipulation, since $(document).ready() only runs once and breaks with AJAX and BigPipe. Gotcha: skip the once() wrapper or context parameter and behaviors re-scan the whole DOM or double-bind on every AJAX update. |
| Prevent duplicate initialization | [Once API](once-api.md) | Wrap every element you process in a behavior with once() so it runs exactly once even when the behavior re-executes on AJAX updates. Gotcha: once() writes a single data-once attribute holding a space-separated id list, not a per-id attribute. |
| Pass PHP data to JavaScript | [drupalSettings](drupal-settings.md) | Use drupalSettings to pass server-side data to JavaScript available at page render, as an alternative to an AJAX request. Gotcha: never pass sensitive data — it's visible in page source. |
| Manipulate the DOM safely | [DOM Manipulation](dom-manipulation.md) | Prefer vanilla JavaScript (querySelector, addEventListener, classList) over jQuery for DOM manipulation; jQuery stays acceptable for existing jQuery-heavy code or complex traversal. Gotcha: never use innerHTML with unsanitized user input. |
| Choose between HTMX and legacy AJAX | [AJAX Integration](ajax-integration.md) | Understand the landscape of dynamic content loading in Drupal: HTMX (Drupal 11.3+) is the modern declarative path, the legacy AJAX API is imperative and required for Drupal 10.x or existing systems. Gotcha: both work automatically with Drupal.behaviors via context — no manual re-init needed. |
| Handle user interactions and events | [Event Handling](event-handling.md) | Use vanilla addEventListener for user interactions, event delegation for dynamic content, and debounce/throttle for performance-intensive events, with keyboard handling for accessibility. Gotcha: no debounce on scroll/resize/input executes hundreds of times per second and freezes the UI. |
| Use ES6+ features | [ES Modules and Modern JavaScript](es-modules-and-modern-javascript.md) | Understand modern JavaScript features available in Drupal 10/11: ES6+ syntax works directly in .js files with no build process, since Drupal 10 dropped IE11 support. Gotcha: import/export statements are not fully supported in Drupal's library system yet. |
| Add JavaScript to SDC components | [JavaScript in SDC Components](javascript-in-sdc-components.md) | Place a JavaScript file in the component directory following naming convention, and Drupal creates the library and attaches it automatically when the component renders. Gotcha: the auto-generated library name is core/components.THEME_OR_MODULE--COMPONENT, not sdc/... |
| Optimize JavaScript performance | [Performance Optimization](performance-optimization.md) | Minimize JavaScript weight, load conditionally, use defer, implement debounce/throttle, and avoid layout thrashing on every implementation — performance is not optional. Gotcha: reading layout properties in a loop forces multiple reflows. |
| Enable aggregation and minification | [Aggregation and Minification](aggregation-and-minification.md) | Always enable JavaScript aggregation in production — Drupal aggregates files into a single bundle, minifies, and serves with far-future cache headers. Gotcha: always test with aggregation enabled before deployment, since it works in dev and can break in production. |
| Use defer and async attributes | [Defer and Async Attributes](defer-and-async-attributes.md) | Use defer for most JavaScript — it downloads in parallel and executes in order after DOM ready; use async only for independent scripts where execution order doesn't matter. Gotcha: aggregation may remove defer, so test the configuration. |
| Debounce or throttle events | [Debounce and Throttle](debounce-and-throttle.md) | For events that fire rapidly (scroll, resize, input, mousemove), use Drupal's built-in debounce to execute after events stop, or throttle to cap execution rate. Gotcha: requestAnimationFrame suits visual updates better than throttle since it syncs with refresh rate. |
| Prevent XSS and secure JavaScript | [Security](security.md) | Sanitize all user input before inserting into the DOM, use Drupal.checkPlain() for escaping, and never pass sensitive data through drupalSettings. Gotcha: never use innerHTML with unsanitized data, and avoid eval() or new Function() — both break CSP. |
| Test JavaScript functionality | [Testing JavaScript](testing-javascript.md) | Use Nightwatch.js — which replaced PHPUnit's FunctionalJavascriptTestBase — to verify JavaScript functionality in real browsers via WebDriver, especially AJAX interactions and accessibility. Gotcha: accessibility testing uses .axeInject() and .axeRun(), not .initAccessibility()/.assert.accessibility(). |
| Avoid common mistakes | [Common Anti-Patterns](common-anti-patterns.md) | Review these eight anti-patterns when checking JavaScript code — each includes the WRONG and CORRECT form plus why it matters. Gotcha: an anti-pattern often works initially but fails with AJAX, caching, or scale. |
| Review code quality standards | [Best Practices Summary](best-practices-summary.md) | Senior-developer review questions and a development standards checklist covering architecture, performance, security, and modern-pattern requirements for Drupal JavaScript. |
