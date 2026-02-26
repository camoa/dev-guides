---
description: Install and use the Easy Breadcrumb contrib module — title resolution, priority 1003, taxonomy hierarchy, and JSON-LD SEO
drupal_version: "11.x"
---

# Easy Breadcrumb Module

## When to Use

> Use Easy Breadcrumb when core produces ugly URL-slug titles (e.g., "my-blog-post" instead of "My Blog Post"), when you need the current page title as the last crumb, or when you need built-in JSON-LD SEO output. It is the de facto standard for production Drupal breadcrumbs without custom code.

## Decision

| Feature | Easy Breadcrumb | Core |
|---|---|---|
| Title source | Resolves real page titles, menu titles, or entity labels | Raw path slug or route `_title` only |
| Missing titles | Falls back to URL slug with capitalization normalization | Silently drops the segment |
| Current page segment | Configurable — include as link or plain text | Never included |
| Taxonomy hierarchy | Config flag `term_hierarchy` adds all parents | Only on `entity.taxonomy_term.canonical` routes |
| Structured data | Built-in JSON-LD `BreadcrumbList` output | None |
| Custom path overrides | Per-path config with regex support | None |
| Code required | Zero | Zero (but limited flexibility) |

## Pattern

Easy Breadcrumb registers at priority 1003 — wins for every route where `applies()` returns `TRUE`:

```yaml
# easy_breadcrumb.services.yml
services:
  easy_breadcrumb.breadcrumb:
    class: Drupal\easy_breadcrumb\EasyBreadcrumbBuilder
    tags:
      - { name: breadcrumb_builder, priority: 1003 }
```

**Title resolution chain** (stops at first match):
1. `alternative_title_field` value on the entity (e.g., `field_breadcrumb_title`) if configured
2. Page title from `TitleResolverInterface` (requires `_title` or `_title_callback` on route)
3. Entity label via `entity->label()` for entity form routes
4. Menu title from `MenuLinkManager::loadLinksByRoute()` if `use_menu_title_as_fallback` enabled
5. Raw URL slug with capitalization transformation (final fallback)

**Alternative title field:** Set `alternative_title_field` to a field machine name (e.g., `field_breadcrumb_title`). Add that field to any entity type. When a node has a value in that field, Easy Breadcrumb uses it as the breadcrumb title instead of the node title. Supports translations.

## Common Mistakes

- **Wrong**: Not enabling "Use the real page title when available" → **Right**: Enable `title_from_page_when_available`; without it Easy Breadcrumb defaults to URL slug guessing even when routes have proper titles
- **Wrong**: Expecting `term_hierarchy` to work without enabling the real page title option → **Right**: Enable `title_from_page_when_available` first for term titles to resolve correctly
- **Wrong**: Enabling Easy Breadcrumb JSON-LD while another SEO module also outputs breadcrumb structured data → **Right**: Use one source of `BreadcrumbList`; duplicate entries in `<head>` confuse Google

## See Also

- [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- [Structured Data (SEO)](structured-data-seo.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbBuilder.php`
- Documentation: https://www.drupal.org/docs/contributed-modules/easy-breadcrumb
