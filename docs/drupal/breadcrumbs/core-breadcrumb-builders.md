---
description: Reference for all core Drupal breadcrumb builders — which routes they handle and their gotchas
tldr: "Know which builder handles which route so you can decide where to inject custom logic. All core builders register at priority 0 except where noted."
drupal_version: "11.x"
---

# Core Breadcrumb Builders

## When to Use

> Know which builder handles which route so you can decide where to inject custom logic. All core builders register at priority 0 except where noted.

## Decision

| Builder | Route(s) | Priority | Gotcha |
|---|---|---|---|
| `PathBasedBreadcrumbBuilder` | All routes (catch-all) | 0 | Silently drops segments whose routes lack `_title` or `_title_callback` |
| `TermBreadcrumbBuilder` | `entity.taxonomy_term.canonical` | 0 | Only adds parents present in the term hierarchy; single-level = just Home + term |
| `CommentBreadcrumbBuilder` | `comment.reply` | 0 | None notable |
| `HelpBreadcrumbBuilder` | `help.help_topic` | 0 | Hardcoded Home → Administration → Help; no dynamic resolution |

## Pattern

**PathBasedBreadcrumbBuilder** — the default catch-all:
- Walks the URL path backwards segment-by-segment; builds a request for each parent path
- Adds `url.path.parent` and `url.path.is_front` cache contexts
- Performs access checks per segment — inaccessible segments are silently omitted
- Title resolution: calls `TitleResolver::getTitle()` which requires `_title` or `_title_callback` on the route
- Skips `/user` (hardcoded exclusion) and the front page path from `system.site:page.front`

**TermBreadcrumbBuilder:**
- Applies only when route is `entity.taxonomy_term.canonical` and parameter is a `TermInterface`
- Walks `loadAllParents()` — only adds terms present in the hierarchy
- Resolves translation via `EntityRepositoryInterface::getTranslationFromContext()`
- Adds `addCacheableDependency($term)` even for the current term

**Easy Breadcrumb at priority 1003 bypasses all core builders for all routes** — if Easy Breadcrumb is installed and `applies()` returns `TRUE`, none of the above builders run.

## Common Mistakes

- **Wrong**: Expecting `PathBasedBreadcrumbBuilder` to show path segments whose routes lack a title → **Right**: Those segments are silently dropped; Easy Breadcrumb falls back to URL slug instead
- **Wrong**: Expecting `TermBreadcrumbBuilder` to run when Easy Breadcrumb is installed → **Right**: Easy Breadcrumb's priority 1003 wins for taxonomy canonical routes too

## See Also

- [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Reference: `core/modules/system/src/PathBasedBreadcrumbBuilder.php`
- Reference: `core/modules/taxonomy/src/TermBreadcrumbBuilder.php`
- Reference: `core/modules/comment/src/CommentBreadcrumbBuilder.php`
