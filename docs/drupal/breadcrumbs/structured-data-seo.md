---
description: Add JSON-LD BreadcrumbList structured data for Google rich results — Easy Breadcrumb built-in vs manual hook_page_attachments implementation
drupal_version: "11.x"
---

# Structured Data (SEO)

## When to Use

> Add JSON-LD breadcrumb structured data to help Google display breadcrumbs in search results instead of the raw URL. This is a meaningful SEO win for content-heavy sites.

## Decision

| Approach | When to use |
|---|---|
| Easy Breadcrumb `add_structured_data_json_ld` | You have Easy Breadcrumb installed — enable the checkbox, done |
| Manual `hook_page_attachments` implementation | Core-only setup with no Easy Breadcrumb |
| Metatag + Schema.org modules | Already using Metatag for other structured data; handles breadcrumbs as part of a broader strategy |

## Pattern

**Easy Breadcrumb approach (recommended):** Enable `add_structured_data_json_ld` at `admin/config/user-interface/easy-breadcrumb`. The `EasyBreadcrumbStructuredDataJsonLd` service injects the result into `<head>` as `<script type="application/ld+json">`.

Generated JSON-LD:
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

The final segment intentionally omits the `item` URL when it is a non-link — per Google's guidelines, the current page URL is optional in the last `ListItem`.

**Manual approach (without Easy Breadcrumb):**
```php
function my_module_page_attachments(array &$attachments): void {
  $breadcrumb = \Drupal::service('breadcrumb')->build(\Drupal::routeMatch());
  $links = $breadcrumb->getLinks();
  if (count($links) < 2) { return; }
  $items = [];
  foreach ($links as $pos => $link) {
    $item = ['@type' => 'ListItem', 'position' => $pos + 1, 'name' => (string) $link->getText()];
    $url = $link->getUrl()->setAbsolute(TRUE)->toString();
    if ($url) { $item['item'] = $url; }
    $items[] = $item;
  }
  $data = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $items];
  $attachments['#attached']['html_head'][] = [
    ['#type' => 'html_tag', '#tag' => 'script', '#value' => json_encode($data), '#attributes' => ['type' => 'application/ld+json']],
    'breadcrumb_json_ld',
  ];
}
```

## Common Mistakes

- **Wrong**: Enabling Easy Breadcrumb JSON-LD while also using Metatag with breadcrumb schema → **Right**: Use one source only; two `BreadcrumbList` blocks in `<head>` confuse validators and may confuse Google
- **Wrong**: Using relative URLs in `item` properties → **Right**: Call `setAbsolute(TRUE)` — relative URLs are invalid in Schema.org `item`
- **Wrong**: A `BreadcrumbList` with only one item → **Right**: Schema.org spec requires at least two `ListItem` entries; skip output when fewer than 2 links exist

## See Also

- [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbStructuredDataJsonLd.php`
- Reference: https://schema.org/BreadcrumbList
- Google guidance: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
