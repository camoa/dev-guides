---
description: Reference for all core Drupal breadcrumb builders — which routes they handle and their gotchas
tldr: "Know which builder handles which route so you can decide where to inject custom logic. All core builders register at priority 0 except where noted."
drupal_version: "11.x"
---

# Core Breadcrumb Builders

## When to Use

> Know which builder handles which route so you can decide where to inject custom logic. All core builders register at priority 0 except where noted.

## Items

#### PathBasedBreadcrumbBuilder
**Description:** The default catch-all builder. Always returns `TRUE` from `applies()`. Walks the URL path backwards segment-by-segment, builds a request for each parent path, checks access, resolves the title via `TitleResolverInterface`, and builds links.

**Priority:** 0 (fallback for all routes)

**Key behaviors:**
- Adds `url.path.parent` and `url.path.is_front` cache contexts
- Returns empty breadcrumb on the front page
- Skips `/user` (hardcoded exclusion — acknowledged as a TODO in core)
- Skips front page path from config `system.site:page.front`
- Performs access checks per segment — segments the current user cannot access are silently omitted
- Uses path aliases: the alias hierarchy defines breadcrumb structure (e.g., `/blog/category/post` yields `/blog` + `/blog/category` as crumbs)
- Title resolution: calls `TitleResolver::getTitle()` which requires the route to define `_title` or `_title_callback`; routes without these get no segment

**Gotchas:** Segments without a `_title` or `_title_callback` defined on their route are silently dropped. This is why Easy Breadcrumb is usually preferred — it falls back to the URL slug instead of dropping the crumb.

#### TermBreadcrumbBuilder
**Description:** Handles `entity.taxonomy_term.canonical` routes specifically. Walks the term's parent hierarchy using `loadAllParents()`.

**Priority:** 0 (same as PathBased, but `applies()` checks route name so it wins for taxonomy routes when priority ties are resolved by registration order)

**Key behaviors:**
- Only applies when route is `entity.taxonomy_term.canonical` and the parameter is a `TermInterface`
- Adds `route` cache context in `applies()` (Drupal 12 will formalize this; until then it is also added in `build()`)
- Calls `addCacheableDependency($term)` even for the current term (not shown in crumb) — parent changes must invalidate the crumb
- Resolves translation via `EntityRepositoryInterface::getTranslationFromContext()`

**Gotchas:** Does NOT add the vocabulary or any intermediate category link unless the term hierarchy includes parent terms. Single-level taxonomies produce just Home + current term.

#### CommentBreadcrumbBuilder
**Description:** Handles `comment.reply` routes (the comment reply form). Produces: Home → [Commented Entity] → [Parent Comment if replying to a comment].

**Priority:** 0

**Key behaviors:**
- Adds `route` cache context
- Adds the commented entity as a cacheable dependency
- Adds the parent comment as a cacheable dependency if `pid` parameter is present

#### HelpBreadcrumbBuilder
**Description:** Handles `help.help_topic` routes. Produces: Home → Administration → Help.

**Priority:** 0

**Key behaviors:**
- Adds `url.path.parent` cache context (not `route` — it covers all help topic pages identically)
- Hardcoded three-level structure; no dynamic resolution

## Common Mistakes

- Expecting `PathBasedBreadcrumbBuilder` to show path segments whose routes lack a title — it silently drops them
- Not understanding that Easy Breadcrumb's priority 1003 means it wins for ALL routes including taxonomy canonical (bypasses `TermBreadcrumbBuilder`)

## See Also

- Easy Breadcrumb's taxonomy handling → [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- Writing a custom builder → [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Reference: `core/modules/system/src/PathBasedBreadcrumbBuilder.php`
- Reference: `core/modules/taxonomy/src/TermBreadcrumbBuilder.php`
- Reference: `core/modules/comment/src/CommentBreadcrumbBuilder.php`
