---
description: Facets canonical URLs and duplicate content — parameter order variants, sitemap exclusion, hreflang with facets, and canonical hook pattern
drupal_version: "11.x"
---

# Canonical URLs & Duplicate Content

## When to Use

> Use this guide when faceted pages create duplicate content issues — the same results appearing at multiple URLs due to different facet parameter ordering or pagination combinations.

## Decision

**Sources of duplicate content with facets:**

| Source | Example | Problem |
|---|---|---|
| Parameter order | `?f[0]=color:blue&f[1]=size:large` vs `?f[0]=size:large&f[1]=color:blue` | Same results, different URLs |
| Empty facets | `?f[0]=color:blue&f[1]=` | Trailing empty parameter |
| Default values | `?f[0]=category:all` | "All" is the same as no filter |
| Pagination + facets | `?page=2&f[0]=color:blue` | Each page × each facet combo |
| Pretty paths combos | `/search/color/blue/size/large` vs `/search/size/large/color/blue` | Path order variants |

## Pattern

**Canonical URL hook:**

```php
function my_module_page_attachments_alter(array &$attachments) {
  $request = \Drupal::request();
  $facet_params = $request->query->all('f');

  if (!empty($facet_params)) {
    $base_url = $request->getSchemeAndHttpHost() . $request->getPathInfo();

    // Remove existing canonical.
    if (isset($attachments['#attached']['html_head_link'])) {
      foreach ($attachments['#attached']['html_head_link'] as $key => $link) {
        if (isset($link[0]['rel']) && $link[0]['rel'] === 'canonical') {
          unset($attachments['#attached']['html_head_link'][$key]);
        }
      }
    }

    $attachments['#attached']['html_head_link'][] = [
      ['rel' => 'canonical', 'href' => $base_url],
      TRUE,
    ];
  }
}
```

**Sitemap exclusion** — Do NOT include faceted URLs in your XML sitemap. Configure `simple_sitemap` or `xmlsitemap` to exclude:
- Search pages with query parameters
- Any path matching facet URL patterns

**Hreflang with multilingual** — The facets module includes a `LanguageSwitcherLinksAlterer` that maintains facet parameters in language switcher links. Faceted URLs need hreflang tags on multilingual sites.

## Common Mistakes

- **Wrong**: Including faceted URLs in sitemap → **Right**: This explicitly tells bots to crawl all those combinations. Never include faceted URLs in sitemaps.
- **Wrong**: Not accounting for pagination combinations → **Right**: `?page=1&f[0]=color:blue` and `?page=2&f[0]=color:blue` are separate URLs. Canonical should point to page 1 or the unfiltered page.

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — the overall strategy
- [URL Processors](url-processors.md) — URL parameter format
