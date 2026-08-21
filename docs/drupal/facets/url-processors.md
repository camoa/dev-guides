---
description: "How facet selections are represented in URLs via the query_string URL processor, filter keys, and URL events"
tldr: "Use this guide when you need to understand how facet selections are represented in URLs, or when customizing URL behavior. Default format is ?f[0]=alias:value with a configurable filter key per source."
drupal_version: "11.x"
---

# URL Processors

## When to Use

> When you need to understand how facet selections are represented in URLs, or when customizing URL behavior.

## Decision

**Default URL format (QueryString), plugin ID `query_string`:**

```
https://example.com/search?search_api_fulltext=drupal&f[0]=category:tutorials&f[1]=tag:php&f[2]=price:[10 TO 50]
```

Breakdown: `f` is the filter key (configurable per facet source), `[0]`/`[1]`/`[2]` are array indices, `category` is the facet URL alias, `:` separates alias and value, `tutorials` is the filter value, `[10 TO 50]` is range syntax.

| Setting | Where | Default | Purpose |
|---|---|---|---|
| Filter key | Facet source config | `f` | The URL parameter name |
| URL processor | Facet source config | `query_string` | The URL processor plugin |
| URL alias | Per-facet config | field name | The facet identifier in URLs |

## Pattern

Events for URL customization:

| Event | When | Use Case |
|---|---|---|
| `QUERY_STRING_CREATED` | After building query string | Modify parameter format |
| `ACTIVE_FILTERS_PARSED` | After parsing URL params | Override active filter detection |
| `URL_CREATED` | After building facet link URL | Modify link destinations |

Multiple facet sources on one page — use different filter keys to prevent conflicts:
- Source A: `filter_key: 'f'`
- Source B: `filter_key: 'g'`

## Common Mistakes

- **Wrong**: Changing the filter key on a live site → **Right**: Existing bookmarked faceted URLs will stop working once the filter key changes.
- **Wrong**: Reusing a URL alias across facets on the same source → **Right**: Two facets on the same source cannot share the same URL alias.
- **Wrong**: Assuming query string is the only option → **Right**: The default `query_string` uses `?f[]=` parameters. For cleaner URLs, see [Pretty Paths](pretty-paths.md).

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — URL implications for crawling
- [Pretty Paths](pretty-paths.md) — cleaner facet URLs
- Reference: `src/Plugin/facets/url_processor/`
