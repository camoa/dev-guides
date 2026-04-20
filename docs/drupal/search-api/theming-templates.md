---
description: Search API theming — available templates, Views templates for search results, and highlighted excerpt access
tldr: "Use this when customizing the display of search results or search-related elements."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> Use this when customizing the display of search results or search-related elements.

## Decision

Most search result theming is done through Views templates, not Search API templates directly.

| Template | Purpose |
|---|---|
| `search-api-server.html.twig` | Server admin page |
| `search-api-index.html.twig` | Index admin page |

## Pattern

**Views templates for search results:**

| Template | Purpose |
|---|---|
| `views-view--VIEWNAME.html.twig` | The search page wrapper |
| `views-view-unformatted--VIEWNAME.html.twig` | Result list |
| `views-view-fields--VIEWNAME.html.twig` | Individual result |
| `views-exposed-form--VIEWNAME.html.twig` | Search form |

**Highlighted excerpts** — when the Highlight processor is enabled:
- Add "Search: Excerpt" field to the View in Views UI
- Or access via `{{ row.search_api_excerpt }}` in row template

## Common Mistakes

- **Wrong**: Looking for Search API-specific result templates → **Right**: Search results render through Views. Override the Views templates for your search view.

## See Also

- [Views Integration](views-integration.md)
- [Relevance & Boosting](relevance-boosting.md) — HTML element processing
- Reference: `web/modules/contrib/search_api/templates/`
