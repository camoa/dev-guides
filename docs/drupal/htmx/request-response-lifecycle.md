---
description: "How HTMX requests flow through Drupal's render pipeline — 8-step lifecycle with decision points"
tldr: "Reference this when debugging HTMX issues or building custom integrations that need to hook into a specific lifecycle stage: request configuration, HtmxRenderer, differential asset loading, content swap, then behavior attach."
drupal_version: "11.x"
---

# Request/Response Lifecycle

## When to Use

> You need to understand how HTMX requests flow through Drupal's render pipeline to debug issues or build custom integrations.

## Steps

1. **Request Initiated** — User interacts with HTMX-enabled element (button click, form change, etc.)

2. **Request Configuration** (`htmx:configRequest` event) — JavaScript adds parameters:
   - `_wrapper_format=drupal_htmx` (if `data-hx-drupal-only-main-content` present)
   - `ajax_page_state` parameters for differential asset loading
   - `_triggering_element_name` from `HX-Trigger-Name` header

   Reference: `/core/misc/htmx/htmx-assets.js` lines 39-62

3. **Server Processing** — Request routes to controller/form, Drupal detects HTMX via headers

4. **Response Generation** — Controller returns render array with HTMX attributes/headers applied via `Htmx` class

5. **Response Rendering** — `HtmxRenderer` creates minimal HTML response:
   ```html
   <!doctype html>
   <html>
   <head>
   <meta name="robots" content="noindex">
   <title>Page Title</title>
   <css-placeholder token="...">
   <js-placeholder token="...">
   </head>
   <body>
   <!-- Status messages -->
   <!-- Main content -->
   </body>
   </html>
   ```

   Reference: `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php` lines 53-73

6. **Asset Loading** (`htmx:beforeSwap` event) — JavaScript extracts and loads new CSS/JS files not already on page

   Reference: `/core/misc/htmx/htmx-assets.js` lines 84-146

7. **Content Swap** — HTMX swaps content according to swap strategy (`outerHTML`, `innerHTML`, etc.)

8. **Behaviors Attach** (`htmx:drupal:load` event) — Drupal behaviors run on new content

   Reference: `/core/misc/htmx/htmx-behaviors.js` lines 14-16

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Request Configuration | Element has `data-hx-drupal-only-main-content` | Add `_wrapper_format=drupal_htmx` to trigger HtmxRenderer |
| Server Processing | Route has `_htmx_route: TRUE` | HtmxRenderer automatically invoked by HtmxContentViewSubscriber |
| Response Rendering | Request has `_wrapper_format=drupal_htmx` OR route has `_htmx_route: TRUE` | HtmxRenderer creates minimal response instead of full page |
| Asset Loading | Response includes new CSS/JS | loadjs loads only files not in `ajax_page_state.libraries` |

## Common Mistakes

- Not understanding `onlyMainContent()` vs `_htmx_route` — Both trigger HtmxRenderer but through different mechanisms
- Expecting full page HTML — HtmxRenderer returns minimal structure with noindex meta tag
- Not accounting for asset loading delay — Behaviors fire AFTER assets load, not immediately after swap
- Forgetting history cleanup — `htmx:beforeHistoryUpdate` removes wrapper_format from URLs

## See Also

- Previous: [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- Next: [Basic Setup](basic-setup.md)
- Reference: `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php` — Handles `_htmx_route` option
