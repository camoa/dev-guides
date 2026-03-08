---
description: XML sitemap configuration for Drupal 11 — Simple Sitemap vs XML Sitemap, multilingual hreflang, IndexNow, and image sitemaps
drupal_version: "11.x"
---

# XML Sitemap

## When to Use

> Configure an XML sitemap whenever you launch a Drupal site. Search engines use sitemaps to discover and prioritize content. Simple Sitemap 4.2.3 is the recommended choice — it handles multilingual hreflang, IndexNow instant indexing, and image sitemaps out of the box. Use XML Sitemap only if you have a legacy site that already depends on it.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| New Drupal 11 site | Simple Sitemap 4.2.3 | Active development, IndexNow, hreflang, image support |
| Multilingual site | Simple Sitemap + metatag_hreflang | Automatic hreflang per translation |
| Already using XML Sitemap | XML Sitemap 2.0.0 | Avoid migration cost if working |
| Need instant indexing | Simple Sitemap + simple_sitemap_engines | IndexNow support for Bing/Yandex |
| Image-heavy site (ecommerce, media) | Simple Sitemap with image extension | Google Image sitemap protocol |
| High-volume site (100k+ nodes) | Simple Sitemap with cron chunking | Configurable chunk size prevents timeout |

## Pattern

### Install and Enable

```bash
composer require drupal/simple_sitemap:^4.2
drush en simple_sitemap simple_sitemap_engines
```

Admin path: `/admin/config/search/simplesitemap`

### Entity Type Configuration

Enable sitemap generation per entity type and bundle at:
`/admin/config/search/simplesitemap/entities`

```yaml
# simple_sitemap.bundle_settings.node.article.yml
changefreq: daily
priority: 0.8
include_images: true
```

Key config fields:
- **Variant** — default (XML) or custom variants (news, image)
- **Priority** — 0.0 to 1.0; set higher for cornerstone content
- **Change frequency** — hint to crawlers, not a guarantee
- **Include images** — adds image:image tags for inline images

### IndexNow Configuration

```yaml
# Enable via UI at /admin/config/search/simplesitemap/engines
# Or in settings.php:
$config['simple_sitemap_engines.settings']['enabled'] = TRUE;
$config['simple_sitemap_engines.settings']['engines'] = ['bing', 'yandex'];
```

IndexNow submits a URL immediately on node save. No API key needed for Bing.

### Multilingual / Hreflang

Simple Sitemap automatically generates `<xhtml:link rel="alternate" hreflang="...">` entries when:
1. Drupal's Language module is enabled
2. Content has translations
3. Simple Sitemap regenerates (cron or manual)

Verify at: `/sitemap.xml` — each URL entry should contain alternate hreflang links.

### Submit to Search Engines

Reference the sitemap in `robots.txt`:
```
Sitemap: https://example.com/sitemap.xml
```

Submit manually via Google Search Console at `https://search.google.com/search-console/sitemaps`.

## Common Mistakes

- **Wrong**: Leaving all content types at default priority 0.5 → **Right**: Assign 0.8+ to cornerstone pages, 0.4 to archives
- **Wrong**: Not regenerating after bulk content imports → **Right**: Trigger regeneration via drush: `drush simple-sitemap:generate`
- **Wrong**: Enabling sitemap on every entity type including users/taxonomy terms → **Right**: Only include publicly accessible, indexable content
- **Wrong**: Not referencing sitemap in robots.txt → **Right**: Add `Sitemap:` line so crawlers auto-discover it
- **Wrong**: Image sitemap with alt text missing → **Right**: Ensure all media has alt text — it populates image:title in the sitemap

## See Also

- [Robots.txt](robots-txt.md) — where to add the Sitemap: reference line
- [Metatag for Multilingual](metatag-multilingual.md) — hreflang coordination
- Reference: [Simple Sitemap project page](https://www.drupal.org/project/simple_sitemap)
- Reference: [Google XML Sitemap protocol](https://www.sitemaps.org/protocol.html)
- Reference: [IndexNow specification](https://www.indexnow.org/)
