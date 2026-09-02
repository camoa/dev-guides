---
description: Install and use the Easy Breadcrumb contrib module — title resolution, priority 1003, taxonomy hierarchy, and JSON-LD SEO
tldr: "Use Easy Breadcrumb when core produces ugly URL-slug titles (e.g., \"my-blog-post\" instead of \"My Blog Post\"), when you need the current page title as the last crumb, or when you need built-in JSON-LD SEO output. It is the de facto standard…"
drupal_version: "11.x"
---

# Easy Breadcrumb Module

These guides document **Easy Breadcrumb 2.0.10** (2026-08-28), the current stable release on the 2.x branch, which supports Drupal ^9.2 || ^10 || ^11. Verified against the `2.0.10` tag on 2026-09-01: the `easy_breadcrumb.breadcrumb` service, its `Drupal\easy_breadcrumb\EasyBreadcrumbBuilder` class, its `breadcrumb_builder` tag at priority 1003, and every configuration key below are unchanged from the 2.0.9 checkout the guide was originally written against.

## When to Use

> Install Easy Breadcrumb when core's path-based builder produces ugly URL-slug titles (e.g., "my-blog-post" instead of "My Blog Post"), when you want the current page title as the last crumb, or when you need built-in JSON-LD SEO output. It is the de facto standard for Drupal sites that need production-ready breadcrumbs without custom code.

## Decision

| Easy Breadcrumb vs core | Easy Breadcrumb wins | Core wins |
|---|---|---|
| Title source | Resolves real page titles (`_title`/`_title_callback`), menu titles, or entity labels | Raw path slug or route title only |
| Missing titles | Falls back to URL slug with capitalization normalization | Silently drops the segment |
| Current page segment | Configurable — include as link or plain text | Never included |
| Taxonomy hierarchy | Config flag `term_hierarchy` adds all parents | Only on `entity.taxonomy_term.canonical` routes |
| Structured data | Built-in JSON-LD `BreadcrumbList` output | None |
| Admin routes | Configurable — include or exclude | Always included |
| Custom path overrides | Per-path config with regex support | None |
| Code required | Zero | Zero (but limited flexibility) |

## Pattern

Easy Breadcrumb registers its builder at priority 1003:

```yaml
# easy_breadcrumb.services.yml
services:
  easy_breadcrumb.breadcrumb:
    class: Drupal\easy_breadcrumb\EasyBreadcrumbBuilder
    tags:
      - { name: breadcrumb_builder, priority: 1003 }
```

Priority 1003 means it wins for every route where `applies()` returns `TRUE`. The only exception is admin routes when `applies_admin_routes` is set to `FALSE` — in that case `PathBasedBreadcrumbBuilder` or another builder handles admin pages.

**Title resolution chain** (in priority order, stops at first match):
1. `alternative_title_field` value on the entity (e.g., `field_breadcrumb_title`) if configured
2. Page title from `TitleResolverInterface` (requires `_title` or `_title_callback` on route)
3. Entity label via `entity->getTitle()` or `entity->label()` for entity form routes
4. Menu title from `MenuLinkManager::loadLinksByRoute()` if `use_menu_title_as_fallback` enabled
5. Raw URL slug with capitalization transformation (final fallback)

**Alternative title field:** Set `alternative_title_field` to a field machine name (e.g., `field_breadcrumb_title`). Add that field to any entity type. When a node has a value in that field, Easy Breadcrumb uses it as the breadcrumb title instead of the node title. Supports translations.

## Common Mistakes

- Not enabling "Use the real page title when available" — without it, Easy Breadcrumb defaults to URL slug guessing even when routes have proper titles
- Expecting `term_hierarchy` to work without enabling "Use the real page title when available" for the term titles
- Enabling Easy Breadcrumb on admin routes but forgetting to configure excluded paths for paths that should not show breadcrumbs
- Using Easy Breadcrumb's JSON-LD while also having another SEO module output breadcrumb structured data — duplicate `BreadcrumbList` in `<head>` confuses Google

## See Also

- All configuration options → [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- JSON-LD output → [Structured Data (SEO)](structured-data-seo.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbBuilder.php`
- Reference: `modules/contrib/easy_breadcrumb/src/TitleResolver.php`
- Documentation: https://www.drupal.org/docs/contributed-modules/easy-breadcrumb
