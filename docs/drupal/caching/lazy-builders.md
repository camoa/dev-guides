---
description: Defer expensive rendering with placeholders using lazy builders
---

# Lazy Builders

## When to Use

When you need to defer expensive or user-specific rendering until after the main page is cached. Lazy builders create placeholders in cached content that are replaced with personalized or dynamic content during rendering.

## Steps

1. **Create lazy builder callback** — Static method that returns render array
   ```php
   class MyController {
     public static function lazyBuild($entity_id) {
       $entity = Entity::load($entity_id);
       return [
         '#markup' => $entity->label(),
         '#cache' => [
           'tags' => $entity->getCacheTags(),
           'contexts' => ['user'],
           'max-age' => 3600,
         ],
       ];
     }
   }
   ```
   Must be public static method; receives parameters from #lazy_builder array.

2. **Add lazy builder to render array**
   ```php
   $build = [
     '#lazy_builder' => ['MyController::lazyBuild', [$entity_id]],
     '#create_placeholder' => TRUE,
   ];
   ```
   `#lazy_builder` is `[callback, [arguments]]`; `#create_placeholder` forces placeholder creation.

3. **Page cached with placeholder** — Placeholder is special token in cached HTML
   ```html
   <!-- Cached HTML contains placeholder token -->
   <drupal-render-placeholder callback="MyController::lazyBuild" arguments="123"></drupal-render-placeholder>
   ```

4. **On request, placeholder replaced** — Lazy builder executes, replaces placeholder with real content
   ```php
   // During rendering:
   // 1. Main page served from cache
   // 2. Placeholder detected
   // 3. Lazy builder callback executed
   // 4. Placeholder replaced with rendered output
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Deciding to use lazy builder | Content varies per-user and is expensive | Use lazy builder to cache page structure, defer user-specific parts |
| Deciding to use lazy builder | Content varies by uncommon context | Use lazy builder; avoids creating many cache variations |
| Passing parameters | Need entity data in callback | Pass entity ID, not entity object (arguments must be scalar/serializable) |
| Setting create_placeholder | Want to control placeholder creation | Set `#create_placeholder = TRUE` to force, or let auto-placeholdering decide |

## Pattern

**Basic lazy builder**:
```php
// In controller or service
public static function buildUserGreeting($uid) {
  $user = User::load($uid);
  return [
    '#markup' => t('Hello, @name', ['@name' => $user->getDisplayName()]),
    '#cache' => [
      'tags' => $user->getCacheTags(),
      'contexts' => ['user'],
    ],
  ];
}

// In render array
$build = [
  'greeting' => [
    '#lazy_builder' => ['MyController::buildUserGreeting', [$user->id()]],
    '#create_placeholder' => TRUE,
  ],
];
```

**Auto-placeholdering** (Drupal decides if placeholder needed):
```php
// High-cardinality cache context triggers auto-placeholdering
$build = [
  '#markup' => $personalized_content,
  '#cache' => [
    'contexts' => ['user'],  // High-cardinality; may trigger placeholder
  ],
];
// Drupal creates placeholder automatically if max-age low or context high-cardinality
```

Reference: `/core/lib/Drupal/Core/Render/Placeholder/`, `/core/modules/big_pipe/`

## Common Mistakes

- Passing non-scalar arguments — Only pass scalars (int, string); pass IDs, not objects
- Expensive logic in lazy builder — Lazy builder should still be fast; use caching within builder if needed
- Forgetting cache metadata in lazy builder — Builder must return cache metadata; placeholder result needs cacheability
- Creating too many lazy builders — Each placeholder adds overhead; use sparingly for truly variable content
- Not understanding auto-placeholdering — Drupal creates placeholders automatically based on cache metadata; explicit `#lazy_builder` not always needed

## See Also

- [BigPipe](bigpipe.md) — Progressive rendering of lazy builders
- [Dynamic Page Cache](dynamic-page-cache.md) — How placeholders enable caching for authenticated users
- Reference: [Lazy building documentation](https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering)
