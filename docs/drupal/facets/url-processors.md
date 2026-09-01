---
description: "How facet selections are represented in URLs via the query_string URL processor, filter keys, and URL events"
tldr: "Use this guide when you need to understand how facet selections are represented in URLs, or when customizing URL behavior. Default format is ?f[0]=alias:value with a configurable filter key per source."
drupal_version: "11.x"
---

# URL Processors

## When to Use

> When you need to understand how facet selections are represented in URLs, or when customizing URL behavior.

## Decision: Default URL Format (QueryString)

**Plugin ID:** `query_string`

**URL format:**

```
https://example.com/search?search_api_fulltext=drupal&f[0]=category:tutorials&f[1]=tag:php&f[2]=price:[10 TO 50]
```

**Breakdown:**

- `f` — Filter key (configurable per facet source)
- `[0]`, `[1]`, `[2]` — Array indices
- `category` — Facet URL alias
- `:` — Separator between alias and value
- `tutorials` — The filter value
- `[10 TO 50]` — Range syntax

## Decision: URL Configuration

| Setting | Where | Default | Purpose |
|---|---|---|---|
| Filter key | Facet source config | `f` | The URL parameter name |
| URL processor | Facet source config | `query_string` | The URL processor plugin |
| URL alias | Per-facet config | field name | The facet identifier in URLs |

## Pattern: Events for URL Customization

| Event | When | Use Case |
|---|---|---|
| `QUERY_STRING_CREATED` | After building query string | Modify parameter format |
| `ACTIVE_FILTERS_PARSED` | After parsing URL params | Override active filter detection |
| `URL_CREATED` | After building facet link URL | Modify link destinations |

## Pattern: Multiple Facet Sources on One Page

Each facet source can have its own filter key. If two Views with facets appear on the same page, use different filter keys to prevent conflicts:

- Source A: `filter_key: 'f'`
- Source B: `filter_key: 'g'`

## Common Mistakes

- **Changing filter key breaks existing links** — If you change the filter key after the site is live, all bookmarked faceted URLs will stop working.
- **URL alias conflicts** — Two facets on the same source cannot share the same URL alias.
- **Pretty paths vs query string** — The default `query_string` uses `?f[]=` parameters. For cleaner URLs, see [Pretty Paths](pretty-paths.md).

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — URL implications for crawling
- [Pretty Paths](pretty-paths.md) — cleaner facet URLs
- Reference: `src/Plugin/facets/url_processor/`
