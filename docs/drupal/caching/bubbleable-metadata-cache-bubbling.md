---
description: Handle cache metadata bubbling from child to parent render arrays
---

# BubbleableMetadata & Cache Bubbling

## When to Use

When you need to propagate cache metadata from child render arrays to parent. Cache bubbling ensures that when a parent element is cached, it includes all cacheability requirements from its children.

## Steps

1. **Child element sets cache metadata**
   ```php
   $child = [
     '#markup' => 'Content',
     '#cache' => [
       'tags' => ['node:123'],
       'contexts' => ['user.roles'],
       'max-age' => 3600,
     ],
   ];
   ```
   Child declares its cacheability requirements.

2. **Parent includes child**
   ```php
   $parent = [
     'title' => ['#markup' => 'Title'],
     'content' => $child,
   ];
   ```
   No manual metadata copying needed.

3. **Renderer automatically bubbles metadata**
   ```php
   $output = \Drupal::service('renderer')->render($parent);
   ```
   Renderer merges child metadata into parent:
   - Tags: union of all tags
   - Contexts: union of all contexts
   - Max-age: minimum of all max-ages

4. **Bubbled metadata reaches cache boundary** — Response, render cache, or lazy builder placeholder
   ```php
   // Metadata bubbles until it hits:
   // - HttpFoundation Response (for page-level headers)
   // - Render array with #cache keys (for render caching)
   // - Lazy builder placeholder (for BigPipe)
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Creating child element | Child has cacheability requirements | Set `#cache` on child; metadata auto-bubbles |
| Combining render arrays | Manually merging arrays | Use `BubbleableMetadata::createFromRenderArray()` and `merge()` |
| Working with objects | Object implements CacheableDependencyInterface | Call `addCacheableDependency($object)` instead of manually copying metadata |
| Setting cache keys | Want to cache parent with children | Set keys on parent; children's metadata bubbles automatically |

## Pattern

**Automatic bubbling** (preferred):
```php
$child = [
  '#cache' => [
    'tags' => ['node:123'],
    'contexts' => ['user.roles'],
    'max-age' => 3600,
  ],
];

$parent = [
  'child' => $child,
  '#cache' => ['keys' => ['parent']],
];
// Child metadata automatically bubbles to parent when rendered
```

**Manual metadata management** (when needed):
```php
$metadata = BubbleableMetadata::createFromRenderArray($child);
$metadata->applyTo($parent);
```

**Adding object dependency**:
```php
$metadata = (new BubbleableMetadata())->addCacheableDependency($entity);
$metadata->applyTo($build);
```

Reference: `/core/lib/Drupal/Core/Render/BubbleableMetadata.php`

## Common Mistakes

- Manually copying cache metadata between arrays — Use bubbling; renderer handles this automatically
- Not understanding max-age merging — Lowest max-age wins; child with `max-age = 0` makes parent uncacheable
- Setting different cache keys on child and parent — Both cached separately, but child metadata still bubbles to parent
- Forgetting to render child arrays — Metadata only bubbles during rendering, not when building arrays
- Using `array_merge()` for render arrays — Loses cache metadata; use `NestedArray::mergeDeep()` or let renderer handle it

## See Also

- [Render Caching](render-caching.md) — How bubbling enables render caching
- [Lazy Builders](lazy-builders.md) — Bubbling boundaries
- Reference: [Bubbleable metadata documentation](https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays)
