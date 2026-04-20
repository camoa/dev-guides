---
description: Breadcrumb JSON-LD structured data for SEO — Easy Breadcrumb built-in toggle vs manual hook_page_attachments vs Metatag Schema, with decision table and implementation notes
tldr: "Add JSON-LD `BreadcrumbList` structured data to help Google display breadcrumb trails in search results instead of bare URLs. This is a quick SEO win — one checkbox if you have Easy Breadcrumb installed."
drupal_version: "11.x"
---

# Breadcrumbs & Structured Data

## When to Use

> Add JSON-LD `BreadcrumbList` structured data to help Google display breadcrumb trails in search results instead of bare URLs. This is a quick SEO win — one checkbox if you have Easy Breadcrumb installed. Choose your approach based on what modules are already active.

## Decision

| Approach | When to use | Why |
|----------|-------------|-----|
| Easy Breadcrumb `add_structured_data_json_ld` | Easy Breadcrumb is installed (comes with `drupal_cms_seo_basic`) | One checkbox at `admin/config/user-interface/easy-breadcrumb` — zero code |
| Manual `hook_page_attachments` | Core-only setup, no Easy Breadcrumb | Full control; use when breadcrumb builder is custom |
| Metatag + Schema Metatag | Already using Schema Metatag for other JSON-LD types | Breadcrumbs become one more schema type in a unified system — avoid running both Easy Breadcrumb JSON-LD and Schema Metatag simultaneously |

**Do not run two approaches at the same time.** Two `BreadcrumbList` blocks in `<head>` confuse validators and may confuse Google.

## Pattern

**Easy Breadcrumb approach (recommended if installed):**

Enable at `admin/config/user-interface/easy-breadcrumb`:

- Check "Add JSON-LD BreadcrumbList structured data"

Generated output injected into `<head>`:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "My Article Title" }
  ]
}
```

The final `ListItem` omits `item` (the URL) when it represents the current page — this is correct per Google's guidelines; the current page URL is optional in the last entry.

**Manual approach (no Easy Breadcrumb):**

See the full implementation in the breadcrumbs guide:

```php
function my_module_page_attachments(array &$attachments): void {
  $breadcrumb = \Drupal::service('breadcrumb')->build(\Drupal::routeMatch());
  $links = $breadcrumb->getLinks();
  if (count($links) < 2) { return; }
  // Build itemListElement array, call setAbsolute(TRUE) on each URL
  // Attach as html_head script[type="application/ld+json"]
}
```

Full implementation: [Structured Data (SEO)](../breadcrumbs/structured-data-seo.md)

## Common Mistakes

- **Wrong**: Enabling Easy Breadcrumb JSON-LD while Schema Metatag also outputs `BreadcrumbList` → **Right**: Use one source only; disable Easy Breadcrumb's JSON-LD if Schema Metatag handles it
- **Wrong**: Relative URLs in `item` properties → **Right**: Always call `setAbsolute(TRUE)` — relative URLs are invalid per Schema.org spec
- **Wrong**: Outputting `BreadcrumbList` with only one `ListItem` → **Right**: Skip output when fewer than 2 links exist; Google's validator rejects single-item breadcrumb lists
- **Wrong**: Breadcrumb structured data that doesn't match the visible breadcrumb trail → **Right**: The JSON-LD must reflect what's actually rendered on the page; mismatches trigger manual actions in Google Search Console

## See Also

- [Easy Breadcrumb Configuration](../breadcrumbs/easy-breadcrumb-configuration.md) — full Easy Breadcrumb setup and segment configuration
- [Structured Data (SEO) — breadcrumbs guide](../breadcrumbs/structured-data-seo.md) — complete manual hook_page_attachments implementation
- [SEO Recipe Baseline](seo-recipe-baseline.md) — Easy Breadcrumb is installed by `drupal_cms_seo_basic`
- [Schema Metatag Setup](schema-metatag-setup.md) — if using Schema Metatag as the unified JSON-LD source
- Reference: [Schema.org BreadcrumbList](https://schema.org/BreadcrumbList)
- Reference: [Google structured data — breadcrumb](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)
