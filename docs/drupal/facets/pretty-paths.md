---
description: "The facets_pretty_paths contrib module for path-based facet URLs instead of query string parameters"
tldr: "Use this guide when you want cleaner facet URLs — /search/color/blue/size/large instead of ?f[0]=color:blue&f[1]=size:large. Contrib, not included in Facets core; don't mix with query string on the same source."
drupal_version: "11.x"
---

# Pretty Paths

## When to Use

> When you want cleaner facet URLs — `/search/color/blue/size/large` instead of `?f[0]=color:blue&f[1]=size:large`.

## Decision

**Module:** `drupal/facets_pretty_paths` (contrib, not included in Facets core)

```bash
composer require drupal/facets_pretty_paths
drush en facets_pretty_paths
```

| Approach | URL Format |
|---|---|
| Default (query string) | `/search?f[0]=color:blue&f[1]=size:large` |
| Pretty Paths | `/search/color/blue/size/large` |

Pretty paths are easier to block in robots.txt and easier to set up canonical URLs for, since the path structure is predictable:

```
# Block all faceted variations under /search/
Disallow: /search/*/
```

## Pattern

Enable the module, then configure the facet source's URL processor to use Pretty Paths instead of the default query string processor.

## Common Mistakes

- **Wrong**: Mixing pretty paths and query string on the same facet source → **Right**: Choose one URL processor per facet source.
- **Wrong**: Using a facet URL alias that collides with a real Drupal path (e.g., `node`) → **Right**: Check for path conflicts before assigning aliases.
- **Wrong**: Ignoring cache growth after switching → **Right**: Pretty paths create more unique cache entries — monitor cache size.

## See Also

- [URL Processors](url-processors.md) — the default query string approach
- [SEO & Bot Protection](seo-bot-protection.md) — how pretty paths help with SEO
- Reference: https://www.drupal.org/project/facets_pretty_paths
