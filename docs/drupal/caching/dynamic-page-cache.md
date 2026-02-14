---
description: Cache pages for authenticated users with Dynamic Page Cache and placeholders
---

# Dynamic Page Cache

## When to Use

When you need to cache pages for authenticated users or pages with personalized content. Dynamic Page Cache caches page structure while excluding personalized parts (converted to placeholders).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Cache pages for authenticated users | Dynamic Page Cache | Only cache system that works for authenticated; caches page minus placeholders |
| Cache pages with personalized elements | Dynamic Page Cache + lazy builders | Caches common structure, defers personalized parts to placeholders |
| Cache pages with high-cardinality contexts | Dynamic Page Cache with auto-placeholdering | Drupal auto-creates placeholders for expensive contexts (e.g., per-user content) |
| Bypass dynamic page cache | max-age 0 or uncacheable context | Set `max-age = 0` or add `session` context |

**Dynamic Page Cache works for all users** (anonymous and authenticated) but is less effective than Page Cache for anonymous (Page Cache is preferred when applicable).

## Pattern

**Dynamic Page Cache is automatic**:
```php
// Render array automatically uses Dynamic Page Cache if:
// 1. max-age > 0
// 2. Response is cacheable
// 3. Page Cache not applicable (authenticated or session exists)
```

**Auto-placeholdering creates placeholders automatically**:
```php
// High-cardinality context triggers placeholder
$build = [
  '#markup' => $user_specific_content,
  '#cache' => [
    'contexts' => ['user'],  // Per-user content; auto-placeholdered
    'max-age' => 3600,
  ],
];
// Dynamic Page Cache creates placeholder automatically
```

**Manual lazy builder** (explicit control):
```php
$build = [
  '#lazy_builder' => ['MyController::buildContent', []],
  '#create_placeholder' => TRUE,
];
// Explicitly creates placeholder in cached page
```

**Cache metadata from placeholders bubbles**:
```php
// Placeholder's cache metadata still affects page-level caching
// If placeholder has max-age 0, entire page becomes uncacheable
```

Reference: `/core/modules/dynamic_page_cache/src/EventSubscriber/DynamicPageCacheSubscriber.php`

## Common Mistakes

- Expecting Dynamic Page Cache for anonymous — Page Cache used instead if applicable; Dynamic Page Cache is fallback
- Not understanding auto-placeholdering — Drupal automatically creates placeholders; manual lazy builders not always needed
- Creating too many placeholders — Each placeholder adds overhead; let auto-placeholdering optimize
- Setting max-age 0 unnecessarily — Makes page uncacheable; use placeholders for variable parts instead
- Forgetting that placeholder metadata bubbles — Placeholder with max-age 0 or uncacheable context makes page uncacheable

## See Also

- [Lazy Builders](lazy-builders.md) — How to create placeholders
- [BigPipe](bigpipe.md) — Progressive rendering of placeholders
- Reference: [Dynamic Page Cache documentation](https://www.drupal.org/docs/8/core/modules/dynamic-page-cache/overview)
