---
description: Facets URL processors — default query_string format, filter key, URL alias, events for customization, multiple sources on one page
drupal_version: "11.x"
---

# URL Processors

## When to Use

> Use this guide when you need to understand how facet selections are represented in URLs, or when customizing URL behavior.

## Decision

**Default URL format (query_string plugin):**

```
https://example.com/search?search_api_fulltext=drupal&f[0]=category:tutorials&f[1]=tag:php&f[2]=price:[10 TO 50]
```

| Part | Meaning |
|---|---|
| `f` | Filter key (configurable per facet source) |
| `[0]`, `[1]`, `[2]` | Array indices |
| `category` | Facet URL alias |
| `:` | Separator between alias and value |
| `tutorials` | The filter value |
| `[10 TO 50]` | Range syntax |

**URL configuration:**

| Setting | Where | Default | Purpose |
|---|---|---|---|
| Filter key | Facet source config | `f` | The URL parameter name |
| URL processor | Facet source config | `query_string` | The URL processor plugin |
| URL alias | Per-facet config | field name | The facet identifier in URLs |

## Pattern

**Events for URL customization:**

| Event | When | Use Case |
|---|---|---|
| `QUERY_STRING_CREATED` | After building query string | Modify parameter format |
| `ACTIVE_FILTERS_PARSED` | After parsing URL params | Override active filter detection |
| `URL_CREATED` | After building facet link URL | Modify link destinations |

**Multiple facet sources on one page** — Each facet source can have its own filter key. If two Views with facets appear on the same page, use different filter keys to prevent conflicts:
- Source A: `filter_key: 'f'`
- Source B: `filter_key: 'g'`

## Common Mistakes

- **Wrong**: Changing the filter key on a live site → **Right**: Changing the filter key breaks all bookmarked faceted URLs. Plan before going live.
- **Wrong**: Two facets on the same source sharing the same URL alias → **Right**: URL alias conflicts break URL parameter handling.
- **Wrong**: Only blocking `f[0]` in robots.txt without the URL-encoded form → **Right**: `f[0]` becomes `f%5B0%5D` in URLs. Both patterns must be blocked. See [SEO & Bot Protection](seo-bot-protection.md).

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — URL implications for crawling
- [Pretty Paths](pretty-paths.md) — cleaner facet URLs
- Reference: `web/modules/contrib/facets/src/Plugin/facets/url_processor/`
