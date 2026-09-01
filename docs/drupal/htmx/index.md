---
description: Drupal HTMX — decision guides for native HTMX integration in Drupal 11.3+
tracks:
  - project: drupal
    channel: stable
    verified: 2026-06-07
guide-meta:
  concepts:
    - HTMX in Drupal
    - hx-get
    - hx-post
    - hx-swap
    - hx-trigger
    - HTMX controllers
    - HTMX response headers
    - Drupal behaviors HTMX
    - HTMX asset loading
  not:
    - legacy AJAX API (see drupal/ajax)
    - AJAX to HTMX migration (see drupal/ajax-htmx-migration)
  requires: []
  complements:
    - drupal/ajax
    - drupal/ajax-htmx-migration
    - drupal/forms
    - drupal/routing
  category: drupal
---

# Drupal HTMX

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what HTMX is and why Drupal adopted it | [HTMX Overview](htmx-overview.md) | Use HTMX when you're building interactive Drupal features that update page regions without full page reloads and want a simpler approach than traditional AJAX. Use traditional AJAX when you need complex command sequences or contrib module compatibility. |
| Decide between HTMX and traditional AJAX | [HTMX vs AJAX](htmx-vs-ajax.md) | Use HTMX when replacing content with simple swaps, dependent form fields, load more, or modals. Use traditional AJAX when you need complex command sequences, heavy client-side processing, or contrib module integration. |
| Understand the request/response lifecycle | [Request/Response Lifecycle](request-response-lifecycle.md) | Reference this when debugging HTMX issues or building custom integrations that need to hook into specific lifecycle stages. |
| Enable HTMX in my module with routes and controllers | [Basic Setup](basic-setup.md) | Use this when creating a custom module and adding HTMX functionality for the first time. |
| Understand what core/drupal.htmx loads | [Library Dependencies](library-dependencies.md) | Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`. The library loads three integration JS files and depends on the HTMX 2.0.4 vendor library, Drupal core JS, drupalSettings, and loadjs. |
| Detect HTMX requests and access request metadata | [Request Detection](request-detection.md) | Use this when you need to detect if a request is from HTMX and access metadata (triggering element, target, prompt) in controllers or forms. |
| Build forms with cascading selects or dependent fields | [Dynamic Forms](dynamic-forms.md) | Use this when building forms with cascading selects, conditional fields, or form elements that update based on user input without full page reload. |
| Build HTMX-enabled controllers | [HTMX Controllers](htmx-controllers.md) | Use this when building controller routes that return dynamic content for HTMX requests. |
| Configure HTMX attributes on elements | [HTMX Attributes Reference](htmx-attributes.md) | Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods. |
| Set HTMX response headers (redirect, trigger, retarget) | [Response Headers](response-headers.md) | Use this when you need to control client-side behavior after a response — redirect, trigger events, change swap strategy, or update browser history. |
| Run Drupal behaviors on HTMX-loaded content | [Drupal Behaviors Integration](drupal-behaviors.md) | Use this when you need to run JavaScript behaviors on content loaded via HTMX, or clean up when content is removed. |
| Understand differential CSS/JS loading | [Asset Loading](asset-loading.md) | Reference this when debugging missing assets in HTMX responses or understanding how differential loading works. |
| Implement load more, infinite scroll, polling, live search | [Production Patterns](production-patterns.md) | Reference this for proven HTMX implementations of common UI patterns: load more, infinite scroll, modals, real-time updates, and live search. |
| See a complete production HTMX implementation | [Production Example: ConfigSingleExportForm](production-example-config-export.md) | Reference this when you want a complete, production-ready HTMX implementation demonstrating cascading selects, OOB updates, and history management — all from Drupal core. |
| Follow security, performance, and accessibility standards | [Best Practices](best-practices.md) | Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards. |
| Debug HTMX issues | [Troubleshooting](troubleshooting.md) | Use this when HTMX isn't working as expected — attributes not applying, content not swapping, behaviors not running, or history not updating. |
| Migrate from AJAX to HTMX | [AJAX Migration](ajax-migration.md) | Use this when converting existing AJAX implementations to HTMX, or running both systems in parallel during gradual migration. |
| Find Drupal core HTMX implementation files | [Core File Reference](core-file-reference.md) | Use this to locate Drupal core HTMX implementation files for deeper understanding or debugging. |
