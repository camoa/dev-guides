---
description: "Handling duplicate content from faceted URLs — emitting rel=canonical to the base search page, parameter ordering, pagination combinations, and sitemap exclusion"
tldr: "Use this guide when faceted pages create duplicate content issues — the same results at multiple URLs from parameter ordering or pagination. Emit rel=canonical to the unfiltered search page via hook_page_attachments_alter(), and never include faceted URLs in sitemaps."
drupal_version: "11.x"
---

# Canonical URLs & Duplicate Content

## When to Use

> When faceted pages create duplicate content issues — the same results appearing at multiple URLs with different facet parameter ordering.

## Decision

| Source | Example | Problem |
|---|---|---|
| Parameter order | `?f[0]=color:blue&f[1]=size:large` vs `?f[0]=size:large&f[1]=color:blue` | Same results, different URLs |
| Empty facets | `?f[0]=color:blue&f[1]=` | Trailing empty parameter |
| Default values | `?f[0]=category:all` | "All" is the same as no filter |
| Pagination + facets | `?page=2&f[0]=color:blue` | Each page × each facet combo |
| Pretty paths combos | `/search/color/blue/size/large` vs `/search/size/large/color/blue` | Path order variants |

## Pattern

**Emit `rel="canonical"` on faceted pages.** Point every faceted variation at the base search page — strip any canonical another module already set, then emit one for the unfiltered path:

```php
/**
 * Implements hook_page_attachments_alter().
 */
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

`getPathInfo()` drops the query string, so the canonical target is the unfiltered search page. Pair it with the meta `noindex` from [SEO & Bot Protection](seo-bot-protection.md) — canonical consolidates link signals, `noindex` keeps the combinations out of the index.

The `query_string` URL processor generates parameters in a consistent order (by facet weight), which helps — but external links or bookmarks may use different orders.

For multilingual sites, faceted URLs need hreflang tags; the facets module includes a `LanguageSwitcherLinksAlterer` that maintains facet parameters in language switcher links.

Do NOT include faceted URLs in your XML sitemap. Configure your sitemap module (`simple_sitemap`, `xmlsitemap`) to exclude search pages with query parameters and any path matching facet URL patterns.

## Common Mistakes

- **Wrong**: Including faceted URLs in the sitemap → **Right**: This explicitly tells bots to crawl all combinations. Never include faceted URLs in sitemaps.
- **Wrong**: Appending a canonical without removing the existing one → **Right**: Unset any `rel => canonical` already in `html_head_link` first, or the page ships two conflicting canonicals.
- **Wrong**: Ignoring pagination combinations → **Right**: `?page=1&f[0]=color:blue` and `?page=2&f[0]=color:blue` are separate URLs. Canonical should typically point to page 1 or the unfiltered page.
- **Wrong**: Handling canonical without rel=prev/next → **Right**: If faceted pages are paginated, you need both canonical handling and proper pagination signals.

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — the overall strategy
- [URL Processors](url-processors.md) — URL parameter format
