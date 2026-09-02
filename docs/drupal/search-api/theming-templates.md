---
description: Search API theming — available templates, Views templates for search results, and highlighted excerpt access
tldr: "Use this when customizing the display of search results or search-related elements."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> When customizing the display of search results or search-related elements.

## Decision: Templates

| Template | Purpose |
|---|---|
| `search-api-server.html.twig` | Server admin page |
| `search-api-index.html.twig` | Index admin page |

Most search result theming is done through Views templates, not Search API templates directly.

## Pattern: Views Templates for Search

| Template | Purpose |
|---|---|
| `views-view--VIEWNAME.html.twig` | The search page wrapper |
| `views-view-unformatted--VIEWNAME.html.twig` | Result list |
| `views-view-fields--VIEWNAME.html.twig` | Individual result |
| `views-exposed-form--VIEWNAME.html.twig` | Search form |

## Pattern: Highlighted Excerpts

When the Highlight processor is enabled, access the excerpt in Views:
- Add "Search: Excerpt" field to the View
- Or access via `{{ row.search_api_excerpt }}` in row template

## See Also

- [Views Integration](views-integration.md) — Views setup for search
- [Relevance & Boosting](relevance-boosting.md) — HTML element processing
