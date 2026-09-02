---
description: Add JSON-LD BreadcrumbList structured data for Google rich results — Easy Breadcrumb built-in vs manual hook_page_attachments implementation
tldr: "Add JSON-LD breadcrumb structured data to help Google display breadcrumbs in search results instead of the raw URL. This is a meaningful SEO win for content-heavy sites."
drupal_version: "11.x"
---

# Structured Data (SEO)

## When to Use

> Add JSON-LD breadcrumb structured data to help Google and other search engines display breadcrumbs in search results. Google's search results show the breadcrumb trail instead of the full URL when valid `BreadcrumbList` structured data is present. This is a meaningful SEO win for content-heavy sites.

## Decision

| Approach | When to use |
|---|---|
| Easy Breadcrumb `add_structured_data_json_ld` | You have Easy Breadcrumb installed — enable the checkbox and it is done |
| Manual `hook_page_attachments` implementation | Core-only setup with no Easy Breadcrumb |
| Metatag + Schema.org modules | Already using Metatag for other structured data; handles breadcrumbs as part of a broader structured data strategy |

## Pattern

**Easy Breadcrumb approach (recommended):** Enable `add_structured_data_json_ld` at `admin/config/user-interface/easy-breadcrumb`. The `EasyBreadcrumbStructuredDataJsonLd` service runs `EasyBreadcrumbBuilder::build()` independently and injects the result into `<head>` as `<script type="application/ld+json">`.

The generated JSON-LD structure:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "My Article Title"
    }
  ]
}
```

The final segment (current page) intentionally omits the `item` URL when rendered as a non-link — per Google's guidelines, the current page URL is optional in the last `ListItem`.

**Manual approach (without Easy Breadcrumb):**
```php
// my_module.module
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

- Enabling Easy Breadcrumb JSON-LD while also using the Metatag module with breadcrumb schema — two `BreadcrumbList` blocks in `<head>` confuse validators and may confuse Google
- Not using absolute URLs (`setAbsolute(TRUE)`) — relative URLs are invalid in Schema.org `item` properties
- Including a `ListItem` for the domain root (the site itself) — Google recommends starting at the first meaningful content level, not the domain
- Having only one breadcrumb item — a `BreadcrumbList` with one item is invalid per Schema.org spec (needs at least two)

## See Also

- Easy Breadcrumb configuration → [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbStructuredDataJsonLd.php`
- Reference: https://schema.org/BreadcrumbList
- Google guidance: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
