---
description: "The facets_pretty_paths contrib module for path-based facet URLs instead of query string parameters"
tldr: "Use this guide when you want cleaner facet URLs — /search/color/blue/size/large instead of ?f[0]=color:blue&f[1]=size:large. Contrib, not included in Facets core; don't mix with query string on the same source."
drupal_version: "11.x"
---

# Pretty Paths

## When to Use

> When you want cleaner facet URLs — `/search/color/blue/size/large` instead of `?f[0]=color:blue&f[1]=size:large`.

## Decision: facets_pretty_paths Module

**Module:** `drupal/facets_pretty_paths` (contrib, not included in Facets core)

```bash
composer require drupal/facets_pretty_paths
drush en facets_pretty_paths
```

Enable the module, then configure the facet source's URL processor to use Pretty Paths instead of the default query string processor.

## Pattern: URL Format Comparison

| Approach | URL Format |
|---|---|
| Default (query string) | `/search?f[0]=color:blue&f[1]=size:large` |
| Pretty Paths | `/search/color/blue/size/large` |

## Decision: SEO Advantage

Pretty paths are easier to block in robots.txt:

```
# Block all faceted variations under /search/
Disallow: /search/*/
```

And easier to set up canonical URLs since the path structure is predictable.

## Common Mistakes

- **Pretty paths + query string conflict** — Don't mix both URL processors. Choose one per facet source.
- **Path conflicts** — Ensure facet URL aliases don't conflict with actual Drupal paths (e.g., don't use 'node' as a facet alias).
- **Cache invalidation** — Pretty paths create more unique cache entries. Monitor cache size.

## See Also

- [URL Processors](url-processors.md) — the default query string approach
- [SEO & Bot Protection](seo-bot-protection.md) — how pretty paths help with SEO
- Reference: https://www.drupal.org/project/facets_pretty_paths
