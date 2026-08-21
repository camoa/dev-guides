---
description: "How facet sources connect facets to Search API-backed Views displays"
tldr: "Use this guide when you need to understand how facets connect to your search backend and Views displays, or when a facet source is not appearing. Each saved Views display generates its own source."
drupal_version: "11.x"
---

# Facet Sources

## When to Use

> When you need to understand how facets connect to your search backend and Views displays.

## Decision

A facet source is an adapter plugin that connects facets to a search display. Each Views display that uses a Search API index generates a facet source automatically.

**Auto-generated source ID format:**
```
search_api:views_{display_plugin}__{view_id}__{display_id}
```

**Examples:**
- `search_api:views_page__article_search__page_1` — Page display
- `search_api:views_block__product_search__block_1` — Block display
- `search_api:views_rest_export__api_search__rest_1` — REST display

**Facet source configuration:**

| Setting | Config Key | Default | Purpose |
|---|---|---|---|
| Filter key | `filter_key` | 'f' | URL parameter name for facet filters |
| URL processor | `url_processor` | 'query_string' | How facets appear in URLs |
| Breadcrumb active | `breadcrumb.active` | FALSE | Add active facets to breadcrumb |
| Breadcrumb label before | `breadcrumb.before` | FALSE | Show facet label before values |
| Breadcrumb group | `breadcrumb.group` | FALSE | Group breadcrumb items by facet |

## Pattern

```php
// Get the facet source plugin manager
$source_manager = \Drupal::service('plugin.manager.facets.facet_source');

// Get all facets for a source
$facet_manager = \Drupal::service('facets.manager');
$facets = $facet_manager->getFacetsByFacetSourceId('search_api:views_page__search__page_1');
```

Interface methods:

| Method | Purpose |
|---|---|
| `getFields()` | List fields available for faceting |
| `getQueryTypesForFacet($facet)` | Available query types for a field type |
| `isRenderedInCurrentRequest()` | Is this source active on the current page? |
| `getSearchKeys()` | Current search text entered by user |
| `getCount()` | Total result count from last query |

## Common Mistakes

- **Wrong**: Expecting facets from one View display to appear on another → **Right**: Each display is a separate source. Facets created for one display won't appear on another unless you use the exposed filters approach.
- **Wrong**: Creating facets against an unsaved View → **Right**: Sources are only generated for saved Views displays.

## See Also

- [Facet Configuration](facet-configuration.md) — creating facets for a source
- [URL Processors](url-processors.md) — the filter_key and URL format
- Reference: `src/Plugin/facets/facet_source/`
