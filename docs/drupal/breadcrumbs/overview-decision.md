---
description: Decide between core PathBasedBreadcrumbBuilder, Easy Breadcrumb module, and custom builders for Drupal breadcrumbs
drupal_version: "11.x"
---

# Breadcrumb Approach Decision

## When to Use

> Use core `PathBasedBreadcrumbBuilder` when basic path-hierarchy breadcrumbs are sufficient. Use Easy Breadcrumb when you need real page titles, current page as final segment, or JSON-LD SEO output. Use a custom builder when breadcrumb logic must be driven by entity relationships, not URL structure.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Basic breadcrumbs that just work | Core `PathBasedBreadcrumbBuilder` | Zero config, handles access checks, follows path alias hierarchy |
| Real page titles instead of URL slugs | Easy Breadcrumb module | Priority 1003 wins over core's 0; resolves actual page titles per segment |
| Current page title as final segment | Easy Breadcrumb (`include_title_segment`) | Built-in config option, no code required |
| JSON-LD structured data for SEO | Easy Breadcrumb (`add_structured_data_json_ld`) | Built-in; generates `BreadcrumbList` and injects into `<head>` |
| Taxonomy term hierarchy in breadcrumb | Easy Breadcrumb (`term_hierarchy`) or core `TermBreadcrumbBuilder` | Core handles term canonical routes; Easy Breadcrumb extends to all paths |
| Breadcrumb driven by entity type logic | Custom builder with `BreadcrumbBuilderInterface` | Full control, proper service priority, clean cache metadata |
| Minor tweak to an existing breadcrumb | `hook_system_breadcrumb_alter()` | Low-overhead hook runs after any builder wins; add/remove/modify links |
| Breadcrumb from menu hierarchy, not path | `menu_breadcrumb` contrib module | Builds from menu trail instead of URL segments |
| Custom per-path breadcrumbs with no code | Easy Breadcrumb custom paths config | Define `path :: Crumb Title\|/crumb-url :: Another Crumb` in settings UI |

## Common Mistakes

- **Wrong**: Installing Easy Breadcrumb without enabling "Use the real page title when available" → **Right**: Enable `title_from_page_when_available` in Easy Breadcrumb settings; without it, Easy Breadcrumb guesses from URL slugs
- **Wrong**: Custom builder with priority 0 → **Right**: Use priority > 0 (but < 1003 unless intentionally overriding Easy Breadcrumb); priority 0 ties with `PathBasedBreadcrumbBuilder`
- **Wrong**: Using `hook_system_breadcrumb_alter()` for complex entity-loading logic → **Right**: Write a custom builder; the alter hook runs on every page load and should stay lightweight
- **Wrong**: Assuming `hook_system_breadcrumb_alter` only fires when your builder wins → **Right**: Alters always fire after whichever builder won

## See Also

- [Core Breadcrumb Architecture](core-breadcrumb-architecture.md)
- [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbManager.php`
