---
description: Decide between core PathBasedBreadcrumbBuilder, Easy Breadcrumb module, and custom builders for Drupal breadcrumbs
tldr: "Use core `PathBasedBreadcrumbBuilder` when basic path-hierarchy breadcrumbs are sufficient. Use Easy Breadcrumb when you need real page titles, current page as final segment, or JSON-LD SEO output."
drupal_version: "11.x"
---

# Breadcrumb Approach Decision

## When to Use

> Every Drupal site needs breadcrumbs. The decision is which layer to use: core's built-in path-based builder, the Easy Breadcrumb contrib module, or a fully custom implementation. Choose based on how much control you need over segment titles, hierarchy, and SEO output.

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
| Custom per-path breadcrumbs with no code | Easy Breadcrumb custom paths config | Define `path :: Crumb Title \| /crumb-url :: Another Crumb` in settings UI |

## Common Mistakes

- Installing Easy Breadcrumb and expecting it to "take over" without configuring "Use the real page title when available" — it falls back to URL slug guessing without that flag
- Writing a custom builder with priority 0 — it ties with `PathBasedBreadcrumbBuilder`; use priority > 0 (but < 1003 unless intentionally overriding Easy Breadcrumb)
- Using `hook_system_breadcrumb_alter()` for complex logic — if you're loading entities or doing routing work in the hook, write a builder instead
- Forgetting that `BreadcrumbManager` runs `hook_system_breadcrumb_alter` after every builder — alters always fire regardless of which builder won

## See Also

- Core builder details → [Core Breadcrumb Architecture](core-breadcrumb-architecture.md)
- Easy Breadcrumb setup → [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbManager.php`
