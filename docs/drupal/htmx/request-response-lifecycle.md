---
description: How HTMX requests flow through Drupal's render pipeline — 8-step lifecycle with decision points
drupal_version: "11.x"
---

# Request/Response Lifecycle

## When to Use

> Reference this when debugging HTMX issues or building custom integrations that need to hook into specific lifecycle stages.

## Decision

| At this step | If | Then |
|---|---|---|
| Request Configuration | Element has `data-hx-drupal-only-main-content` | Add `_wrapper_format=drupal_htmx` to trigger HtmxRenderer |
| Server Processing | Route has `_htmx_route: TRUE` | HtmxRenderer automatically invoked by HtmxContentViewSubscriber |
| Response Rendering | Request has `_wrapper_format=drupal_htmx` OR route has `_htmx_route: TRUE` | HtmxRenderer creates minimal response instead of full page |
| Asset Loading | Response includes new CSS/JS | loadjs loads only files not in `ajax_page_state.libraries` |

## Pattern

8-step flow for an HTMX request:

1. **Request Initiated** — User interacts with HTMX-enabled element
2. **Request Configuration** (`htmx:configRequest`) — JS adds `_wrapper_format=drupal_htmx`, `ajax_page_state`, `_triggering_element_name`
3. **Server Processing** — Route to controller/form; Drupal detects HTMX via headers
4. **Response Generation** — Controller returns render array with HTMX attributes/headers via `Htmx` class
5. **Response Rendering** — `HtmxRenderer` creates minimal HTML (noindex meta, no sidebars/header/footer)
6. **Asset Loading** (`htmx:beforeSwap`) — JS extracts and loads new CSS/JS not already on page
7. **Content Swap** — HTMX swaps content per swap strategy (`outerHTML`, `innerHTML`, etc.)
8. **Behaviors Attach** (`htmx:drupal:load`) — Drupal behaviors run on new content

## Common Mistakes

- **Wrong**: Not understanding `onlyMainContent()` vs `_htmx_route` → **Right**: Both trigger HtmxRenderer but through different mechanisms
- **Wrong**: Expecting full page HTML in response → **Right**: HtmxRenderer returns minimal structure with noindex meta tag
- **Wrong**: Not accounting for asset loading delay → **Right**: Behaviors fire AFTER assets load, not immediately after swap
- **Wrong**: Forgetting history cleanup → **Right**: `htmx:beforeHistoryUpdate` removes wrapper_format from URLs automatically

## See Also

- [HTMX vs AJAX Decision](htmx-vs-ajax.md)
- [Basic Setup](basic-setup.md)
- Reference: `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`
- Reference: `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php`
- Reference: `/core/misc/htmx/htmx-assets.js`
- Reference: `/core/misc/htmx/htmx-behaviors.js`
