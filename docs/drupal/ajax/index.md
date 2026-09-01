---
description: Drupal AJAX Framework — atomic decision guides for forms, commands, routes, security, performance, and accessibility
tracks:
  - project: drupal
    channel: stable
    verified: 2026-06-07
guide-meta:
  concepts:
    - Drupal AJAX API
    - AJAX commands
    - AJAX form callbacks
    - AJAX modal dialogs
    - custom AJAX commands
    - AJAX routes
    - autocomplete
  not:
    - HTMX (see drupal/htmx)
    - AJAX to HTMX migration
  requires:
    - drupal/forms
  complements:
    - drupal/htmx
    - drupal/ajax-htmx-migration
    - drupal/js-development
  category: drupal
---

# Drupal AJAX

> As of Drupal 11.3, HTMX is available in core and is the recommended approach for new projects. This guide covers the legacy AJAX framework, which remains essential for existing codebases and contributed module patterns.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the AJAX system architecture | [Core Concepts](core-concepts.md) | Drupal AJAX: PHP callbacks return AjaxResponse objects; clients execute commands and re-attach behaviors. Required for ordered sequences, the dialog system, and contrib compatibility. HTMX is the alternative for new work in Drupal 11.3+. |
| Add AJAX to a form element | [Form Element AJAX Configuration](form-element-ajax-configuration.md) | Use the `#ajax` property on any form element when you need server-driven content updates triggered by user interaction without a full page reload. |
| Create dependent fields (category/subcategory) | [Dependent Field Patterns](dependent-field-patterns.md) | Use dependent fields when form options must change based on the value of another field (category/subcategory, country/state, product type/options). |
| Build a multi-step wizard form | [Multi-Step Form Workflows](multi-step-form-workflows.md) | Use multi-step AJAX forms for wizard-style workflows where users navigate sequential steps without page reloads. Use standard forms for simple one-page submissions. |
| Validate fields as user types | [Live Field Validation](live-field-validation.md) | Use live validation when user experience benefits from immediate field-level feedback (email availability checks, username format, real-time constraints). Avoid for simple required-field checks. |
| Update, append, or remove DOM content | [Content Manipulation Commands](content-manipulation-commands.md) | ReplaceCommand swaps the full element (new content must include wrapper ID); HtmlCommand updates inner HTML only. InsertCommand's 3rd param is `$settings` (JS behaviors), not an insertion method — use AppendCommand or PrependCommand for explicit insertion. |
| Add CSS classes or invoke jQuery methods | [CSS Styling Commands](css-styling-commands.md) | Use CssCommand for inline styles, InvokeCommand for jQuery methods, DataCommand for `.data()`. AddCssCommand expects `[['href' => '...']]` (link attribute arrays, not library-registry format) — prefer `#attached` for static assets. |
| Open or close modal dialogs | [Dialog Commands](dialog-commands.md) | Use OpenModalDialogCommand when you need to block page interaction. Use OpenDialogCommand for non-blocking side panels. |
| Show messages or screen reader alerts | [Feedback Commands](feedback-commands.md) | MessageCommand: 4th param is `$clear_previous`; control screen-reader announcements via `$options['announce']`. AnnounceCommand provides screen-reader-only output; 'polite' waits, 'assertive' interrupts. Never use AlertCommand in production. |
| Create a custom AJAX command | [Custom AJAX Commands](custom-ajax-commands.md) | Create custom AJAX commands when core commands don't meet your needs: custom animations, third-party library integration, or complex DOM manipulation requiring JavaScript logic. |
| Build a custom AJAX route (non-Form API) | [Custom Route Implementation](custom-route-implementation.md) | Use custom AJAX routes when you need AJAX endpoints outside Form API: autocomplete, search, content loading, or API-style endpoints. Always implement the `nojs` fallback for JavaScript-disabled environments. |
| Handle file uploads via AJAX | [File Upload Patterns](file-upload-patterns.md) | Use `#type => 'managed_file'` with AJAX for file uploads that need immediate preview or feedback (avatars, attachments, media galleries). Always configure upload validators. |
| Implement autocomplete suggestions | [Autocomplete Implementation](autocomplete-implementation.md) | Use `#autocomplete_route_name` for dynamic suggestions as users type. Use core's `system.entity_autocomplete` for existing entity types. |
| Restrict access to AJAX callbacks | [Access Control Patterns](access-control-patterns.md) | Every AJAX callback and route is an HTTP endpoint and requires access control. AJAX callbacks are not protected by the UI alone — attackers can call them directly. |
| Protect AJAX endpoints from CSRF | [CSRF Protection](csrf-protection.md) | Form API `#ajax` is CSRF-protected automatically. For custom POST AJAX routes use `_csrf_request_header_token: 'TRUE'` (validates X-CSRF-Token header). For GET action links use `_csrf_token: 'TRUE'` (validates `token=` query param). |
| Optimize slow AJAX requests | [Performance Optimization](performance-optimization.md) | Apply these patterns when AJAX requests are slow, causing excessive database queries, large DOM updates, or timeouts on large operations. |
| Cache AJAX responses | [Response Caching](response-caching.md) | Use CacheableAjaxResponse for AJAX responses containing cacheable data: public content, configuration results, or expensive calculations that don't vary per user. Do not cache user-specific data without proper cache contexts. |
| Make AJAX meet WCAG 2.1 AA | [WCAG Compliance Patterns](wcag-compliance-patterns.md) | Apply these patterns to every AJAX implementation. Accessibility is not optional — WCAG 2.1 Level AA is the standard for Drupal sites. |
| Announce updates to screen readers | [Screen Reader Support](screen-reader-support.md) | Every AJAX content update must be announced to screen reader users. Silence after a dynamic update is a WCAG failure. |
| Debug failing AJAX requests | [Debugging Techniques](debugging-techniques.md) | Use these techniques when AJAX requests fail, return unexpected results, or produce errors. Start with the browser DevTools Network tab before adding server-side logging. |
| Write automated AJAX tests | [Testing AJAX](testing-ajax.md) | Use WebDriverTestBase (FunctionalJavascript namespace) for AJAX tests — it drives a real browser. Use BrowserTestBase only for non-JavaScript tests. |
| Integrate React or Vue with Drupal | [Frontend Framework Integration](frontend-framework-integration.md) | Use JSON endpoints with React/Vue for fully decoupled sites. Use Drupal AJAX for simple enhancements. |
| Apply security best practices | [Best Practices: Security](best-practices-security.md) | Apply every item in this guide to every AJAX implementation. AJAX callbacks and routes are HTTP endpoints — they require the same security rigor as any web API. |
| Apply performance best practices | [Best Practices: Performance](best-practices-performance.md) | Apply these standards to every AJAX implementation. Slow AJAX destroys UX. |
| Follow Drupal development standards | [Best Practices: Development Standards](best-practices-development.md) | Apply these standards to all AJAX code. They prevent the most common sources of bugs, broken tests, and maintenance pain. |
| Meet accessibility requirements | [Best Practices: Accessibility](best-practices-accessibility.md) | Every AJAX implementation must meet WCAG 2.1 Level AA. This is not optional — it's a legal and ethical requirement. |
