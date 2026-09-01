---
description: Drupal Breadcrumbs — decision guides for core builders, Easy Breadcrumb, custom builders, SEO, theming, and caching
tracks:
  - project: easy_breadcrumb
    channel: stable
    declared: "2.0.10"
    verified: 2026-09-01
guide-meta:
  concepts:
    - breadcrumb builder
    - Easy Breadcrumb
    - custom breadcrumb builder
    - breadcrumb JSON-LD
    - breadcrumb block
  not:
    - navigation menus
    - routing system
  requires: []
  complements:
    - drupal/seo-geo
    - drupal/twig
    - drupal/ui-suite-daisyui
  category: drupal
---

# Drupal Breadcrumbs

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide: core vs Easy Breadcrumb vs custom builder | [Overview & Decision](overview-decision.md) | Use core `PathBasedBreadcrumbBuilder` when basic path-hierarchy breadcrumbs are sufficient. Use Easy Breadcrumb when you need real page titles, current page as final segment, or JSON-LD SEO output. |
| Understand the breadcrumb system architecture | [Core Breadcrumb Architecture](core-breadcrumb-architecture.md) | Read this before writing any custom builder or alter hook. The `BreadcrumbManager` is the chain dispatcher; every breadcrumb request routes through it. |
| Know which core builders handle what | [Core Breadcrumb Builders](core-breadcrumb-builders.md) | Know which builder handles which route so you can decide where to inject custom logic. All core builders register at priority 0 except where noted. |
| Install and configure Easy Breadcrumb | [Easy Breadcrumb Module](easy-breadcrumb-module.md) | Use Easy Breadcrumb when core produces ugly URL-slug titles (e.g., "my-blog-post" instead of "My Blog Post"), when you need the current page title as the last crumb, or when you need built-in JSON-LD SEO output. It is the de facto standard… |
| Tune Easy Breadcrumb settings | [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md) | After installing Easy Breadcrumb, configure at `admin/config/user-interface/easy-breadcrumb`. All settings map to `easy_breadcrumb.settings.yml` which can be exported and version-controlled. |
| Write a custom breadcrumb builder | [Custom Breadcrumb Builder](custom-breadcrumb-builder.md) | Use a custom builder when breadcrumbs must be driven by entity relationships (not URL structure), or when you need different logic for specific routes. Use `hook_system_breadcrumb_alter()` instead for minor adjustments. |
| Alter breadcrumbs with a hook | [Altering Breadcrumbs](altering-breadcrumbs.md) | Use `hook_system_breadcrumb_alter()` for low-overhead adjustments after a builder runs: inserting a segment, removing a specific link, adding cache tags/contexts. For complex logic involving entity loading or routing, write a custom… |
| Add JSON-LD structured data for SEO | [Structured Data (SEO)](structured-data-seo.md) | Add JSON-LD breadcrumb structured data to help Google display breadcrumbs in search results instead of the raw URL. This is a meaningful SEO win for content-heavy sites. |
| Theme the breadcrumb output | [Twig Theming](twig-theming.md) | Override the default breadcrumb template when you need custom markup: different HTML structure, additional CSS classes, aria attributes, or schema microdata. The template override requires no PHP — just create the file in the right place. |
| Use breadcrumbs with UI Suite DaisyUI | [UI Suite DaisyUI Integration](ui-suite-daisyui-integration.md) | When your theme extends `ui_suite_daisyui`, the theme's `breadcrumb.html.twig` delegates to the `ui_suite_daisyui:breadcrumbs` SDC automatically. You get DaisyUI breadcrumb styling with no extra code. |
| Understand breadcrumb caching | [Caching](caching.md) | Breadcrumbs render via BigPipe (the `SystemBreadcrumbBlock` uses `createPlaceholder(): true`). Cache metadata on the `Breadcrumb` object directly controls invalidation. |
| Place the breadcrumb block | [Block Placement](block-placement.md) | The `SystemBreadcrumbBlock` (plugin ID `system_breadcrumb_block`) is the only standard way to render breadcrumbs in a region. Place via the Block UI or via config YAML for themes, recipes, or installation profiles. |
| Avoid common pitfalls | [Best Practices & Anti-Patterns](best-practices-anti-patterns.md) | Read this before writing any breadcrumb-related code. These are the patterns that cause production issues and the ones that solve them. |
| Handle special breadcrumb scenarios | [Common Recipes](common-recipes.md) | Ready-to-apply patterns for the most frequent breadcrumb requirements. Each recipe is self-contained. |
