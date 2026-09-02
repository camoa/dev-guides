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
| Understand what HTMX is and why Drupal adopted it | [HTMX Overview](htmx-overview.md) | Use HTMX to build interactive Drupal features that update page regions without full page reloads. Drupal 11.3 adopted it as a simpler, declarative alternative to AJAX with up to 71% less JavaScript; skipping `_htmx_route: TRUE` or `onlyMainContent()` produces full page renders instead of minimal responses. |
| Decide between HTMX and traditional AJAX | [HTMX vs AJAX](htmx-vs-ajax.md) | Use HTMX when replacing content with simple swaps, dependent form fields, load more, or modals; use traditional AJAX for complex command sequences, heavy client-side processing, or contrib module integration. HTMX returns HTML render arrays, not JSON commands. |
| Understand the request/response lifecycle | [Request/Response Lifecycle](request-response-lifecycle.md) | Reference this when debugging HTMX issues or building custom integrations that need to hook into a specific lifecycle stage: request configuration, HtmxRenderer, differential asset loading, content swap, then behavior attach. |
| Enable HTMX in my module with routes and controllers | [Basic Setup](basic-setup.md) | Use this when creating a custom module and adding HTMX functionality: define a route with `_htmx_route: TRUE`, build a controller that applies `Htmx` attributes, and rely on `applyTo()` for automatic library attachment. |
| Understand what core/drupal.htmx loads | [Library Dependencies](library-dependencies.md) | Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`. The library loads three integration JS files and depends on the HTMX 2.0.4 vendor library, Drupal core JS, drupalSettings, and loadjs. |
| Detect HTMX requests and access request metadata | [Request Detection](request-detection.md) | Use this when you need to detect if a request is from HTMX and access metadata (triggering element, target, prompt) in controllers or forms via HtmxRequestInfoTrait's 8 methods. |
| Build forms with cascading selects or dependent fields | [Dynamic Forms](dynamic-forms.md) | Use this when building forms with cascading selects, conditional fields, or any form that updates based on user input without full page reload. FormBuilder handles form_build_id automatically via OOB swap. |
| Build HTMX-enabled controllers | [HTMX Controllers](htmx-controllers.md) | Use this when building controller routes that return dynamic content for HTMX requests. Return standard render arrays and either set `_htmx_route: TRUE` or check `isHtmxRequest()` to serve minimal responses. |
| Configure HTMX attributes on elements | [HTMX Attributes Reference](htmx-attributes.md) | Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods; chaining without calling `applyTo()` never applies the configuration. |
| Set HTMX response headers (redirect, trigger, retarget) | [Response Headers](response-headers.md) | Use this when you need to control client-side behavior after response — redirect, trigger events, change swap strategy, or update browser history — via the Htmx class's 11 response header methods. |
| Run Drupal behaviors on HTMX-loaded content | [Drupal Behaviors Integration](drupal-behaviors.md) | Use this when you need to run JavaScript behaviors on content loaded via HTMX, or clean up when content is removed. Behaviors run after `htmx:drupal:load`, which fires only after settle AND asset loading complete. |
| Understand differential CSS/JS loading | [Asset Loading](asset-loading.md) | Reference this when debugging missing assets in HTMX responses. Drupal only loads assets not already on the page, comparing requested libraries against ajax_page_state via loadjs; behaviors attach only after assets finish loading. |
| Implement load more, infinite scroll, polling, live search | [Production Patterns](production-patterns.md) | Reference this for proven HTMX implementations of common UI patterns: load more (swap beforeend + select), infinite scroll (trigger revealed), modals, polling (trigger every Ns), and debounced live search. |
| See a complete production HTMX implementation | [Production Example: ConfigSingleExportForm](production-example-config-export.md) | Reference this when you want a complete, production-ready HTMX implementation demonstrating cascading selects, OOB updates, and history management — all from Drupal core's ConfigSingleExportForm. |
| Follow security, performance, and accessibility standards | [Best Practices](best-practices.md) | Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards. Validate server-side, cache aggressively, use aria-live for dynamic regions, and never build HTML strings by hand. |
| Debug HTMX issues | [Troubleshooting](troubleshooting.md) | Use this when HTMX isn't working as expected — attributes not applying, content not swapping, behaviors not running, or history not updating. Confirm `applyTo()` was called and use `htmx.logAll()` for lifecycle visibility. |
| Migrate from AJAX to HTMX | [AJAX Migration](ajax-migration.md) | Use this when converting existing AJAX implementations to HTMX, or running both systems in parallel during gradual migration. Simple content replacement and dependent fields migrate well; complex command sequences and heavy JS processing should stay AJAX. |
| Find Drupal core HTMX implementation files | [Core File Reference](core-file-reference.md) | Use this to locate Drupal core HTMX implementation files for deeper understanding or debugging. Documentation may lag behind code, so check the actual core implementation rather than relying on the test module as a best-practices reference. |
