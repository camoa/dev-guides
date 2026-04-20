---
description: Facets Pretty Paths contrib module — cleaner facet URLs as path segments instead of query parameters, SEO benefits, and gotchas
tldr: "Use this guide when you want cleaner facet URLs — `/search/color/blue/size/large` instead of `?f[0]=color:blue&f[1]=size:large`."
drupal_version: "11.x"
---

# Pretty Paths

## When to Use

> Use this guide when you want cleaner facet URLs — `/search/color/blue/size/large` instead of `?f[0]=color:blue&f[1]=size:large`.

## Decision

**Module:** `drupal/facets_pretty_paths` (contrib — not included in Facets core)

**URL format comparison:**

| Approach | URL Format |
|---|---|
| Default (query string) | `/search?f[0]=color:blue&f[1]=size:large` |
| Pretty Paths | `/search/color/blue/size/large` |

**SEO advantage** — Pretty paths are easier to block in robots.txt with a single rule:
```
Disallow: /search/*/
```

And easier to set up canonical URLs since the path structure is predictable.

## Pattern

```bash
composer require drupal/facets_pretty_paths
drush en facets_pretty_paths
```

Then configure the facet source to use the pretty paths URL processor instead of `query_string`.

## Common Mistakes

- **Wrong**: Using both pretty paths and query string URL processors on the same source → **Right**: Choose one URL processor per facet source. Don't mix them.
- **Wrong**: Using Drupal path segments as facet URL aliases → **Right**: Ensure facet URL aliases don't conflict with actual Drupal paths (e.g., don't use 'node' as a facet alias).
- **Wrong**: Not accounting for increased cache entries → **Right**: Pretty paths create more unique cache entries than query strings. Monitor cache size on high-traffic sites.

## See Also

- [URL Processors](url-processors.md) — the default query string approach
- [SEO & Bot Protection](seo-bot-protection.md) — how pretty paths help with SEO
- Reference: https://www.drupal.org/project/facets_pretty_paths
