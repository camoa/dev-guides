---
description: Configure title tags, meta descriptions, canonical URLs, and robots meta in Drupal 11 using the Metatag module with token-based defaults
tldr: "You need to configure the foundational meta tags — title, description, canonical, and robots — that affect search engine indexing and click-through rates. These are configured in the Metatag module's core submodule (always enabled) at…"
drupal_version: "11.x"
---

# Core Meta Tags

## When to Use

> You need to configure the foundational meta tags — title, description, canonical, and robots — that affect search engine indexing and click-through rates. These are configured in the Metatag module's core submodule (always enabled) at `/admin/config/search/metatag`. Configure Global defaults first, then override per content type.

## Decision

| If you need... | Approach | Why |
|----------------|----------|-----|
| Consistent title format across all content | Token pattern in Global group | Single change applies everywhere |
| Different title format for front page | Front page group override | Home page often uses brand name only |
| Meta description from a summary field | Token in Content type group | Pulls from `field_summary` or `body:summary` |
| Block indexing for utility pages | Robots tag in Content type group | Keeps index clean without .htaccess |
| Canonical URL for nodes | Leave at default — Metatag auto-sets | Drupal provides `[current-page:url]` automatically |
| Canonical for custom/non-node paths | Explicit canonical in Global or route-specific config | Auto-detection fails on Views pages |

## Pattern

### Title Tag

Configure at `/admin/config/search/metatag`. Recommended token patterns:

```
Global:        [site:name] | [current-page:title]
Front page:    [site:name] — [site:slogan]
Content type:  [node:title] | [site:name]
Taxonomy:      [term:name] | [site:name]
```

The `|` separator is conventional — search engines display ~50-60 characters before truncating. The site name after `|` reinforces brand on every SERP result.

### Meta Description

```
Global:        [site:slogan]
Content type:  [node:field_summary]
               (fallback: leave empty — blank is better than a repeated slogan)
```

Key rule: if a node has no summary field value, the token resolves to empty, and search engines generate a snippet from page content. This is preferable to a generic fallback that repeats on every page.

### Canonical URL

Metatag sets `[current-page:url]` as the canonical by default. Override only when:

- A Views page aggregates content from multiple sources (set explicit path)
- A node is accessible at multiple aliases (set the primary alias)

```
Default canonical: [current-page:url]   ← do not change for standard nodes
Views page:        https://example.com/news  ← hardcode or use route-specific config
```

### Robots Meta

| Content type | Robots value | Rationale |
|-------------|-------------|-----------|
| Article, Page | `index, follow` (default) | Standard — index these |
| Thank You / Confirmation pages | `noindex, follow` | No search value; follow links |
| Internal search results | `noindex, nofollow` | Google does not want to index search result pages |
| Staging/preview nodes | `noindex, nofollow` | Prevent accidental staging indexing |

Configure per content type at `/admin/config/search/metatag` → select content type → Robots field.

## Default Configuration Reference

| Group | Title pattern | Description | Robots |
|-------|--------------|-------------|--------|
| Global | `[site:name] \| [current-page:title]` | `[site:slogan]` | `index, follow` |
| Front page | `[site:name] — [site:slogan]` | (site description) | `index, follow` |
| Content (node) | `[node:title] \| [site:name]` | `[node:field_summary]` | `index, follow` |
| Taxonomy term | `[term:name] \| [site:name]` | `[term:description]` | `index, follow` |
| User profile | `[user:display-name] \| [site:name]` | (leave empty) | `noindex, follow` |
| 404 page | (not configurable via Metatag) | — | — |

## Common Mistakes

- **Wrong**: Using the same description token at Global level that all content types inherit → **Right**: Set description at the content type level to pull from `[node:field_summary]`; Global description should be the site's unique value proposition for pages without specific content
- **Wrong**: Setting `noindex` on content type defaults and forgetting to override on individual nodes → **Right**: Check robots value before publishing; Metatag field on the entity overrides the content type default
- **Wrong**: Titles over 60 characters → **Right**: Keep the pattern under 60 characters for most titles; long node titles will still truncate in SERPs but that is unavoidable
- **Wrong**: Duplicate titles across pages (e.g., missing `[node:title]` token) → **Right**: Always include a unique per-page token component in title patterns
- **Wrong**: Canonical pointing to a non-canonical alias after Pathauto regenerates → **Right**: Use `[current-page:url]` which always resolves to the current canonical alias, not a hardcoded path

## See Also

- [Metatag Architecture](metatag-architecture.md) — cascading inheritance model and submodule overview
- [Canonical URLs](canonical-urls.md) — duplicate content and domain-level canonicalization
- [Open Graph](open-graph.md) — social sharing tags that build on these core tags
- [Pathauto Patterns](pathauto-patterns.md) — URL aliases that feed into canonical tokens
- Reference: [Metatag module documentation](https://www.drupal.org/project/metatag)
- Reference: [Google title tag guidelines](https://developers.google.com/search/docs/appearance/title-link)
