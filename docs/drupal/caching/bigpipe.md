---
description: Progressively render expensive content with BigPipe streaming
---

# BigPipe

## When to Use

When you need to progressively render expensive content. BigPipe sends page skeleton immediately, then streams placeholder replacements as they become ready, improving perceived performance.

## Steps

1. **Enable BigPipe module** — Core module, disabled by default
   ```bash
   drush en big_pipe
   ```

2. **Create lazy builders for expensive content**
   ```php
   public static function expensiveContent() {
     $data = expensive_api_call();  // Takes 2 seconds
     return [
       '#markup' => render_data($data),
       '#cache' => ['max-age' => 3600],
     ];
   }
   ```

3. **Add lazy builder to render array**
   ```php
   $build = [
     'content' => [
       '#lazy_builder' => ['MyController::expensiveContent', []],
       '#create_placeholder' => TRUE,
     ],
   ];
   ```

4. **BigPipe renders progressively**
   - Page HTML sent immediately with placeholder
   - Expensive content renders in background
   - JavaScript replaces placeholder when ready
   - Process repeats for all placeholders

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing BigPipe | Content is expensive (>100ms) | Use BigPipe to improve perceived performance |
| Choosing BigPipe | Content varies per-user | Use BigPipe to cache page structure, stream personalized content |
| Choosing BigPipe | Layout shift is concern | Add placeholder preview to avoid CLS (Cumulative Layout Shift) |
| Setting placeholder strategy | Want no-JS fallback | Use SingleFlushStrategy (default in BigPipe) for progressive enhancement |

## Pattern

**Basic BigPipe usage**:
```php
// Expensive content as lazy builder
$build = [
  'header' => ['#markup' => 'Fast header'],  // Sent immediately
  'expensive' => [
    '#lazy_builder' => ['MyController::expensiveContent', []],
    '#create_placeholder' => TRUE,  // BigPipe streams this
  ],
  'footer' => ['#markup' => 'Fast footer'],  // Sent immediately
];
```

**Placeholder with preview** (prevents layout shift):
```php
$build = [
  '#lazy_builder' => ['MyController::expensiveContent', []],
  '#create_placeholder' => TRUE,
  'preview' => [
    '#markup' => '<div class="placeholder-preview">Loading...</div>',
  ],
];
```

**Drupal 11.3+ optimization** — CachedPlaceholderStrategy reduces BigPipe overhead:
```php
// If placeholder render cache is warm, BigPipe skips streaming
// and serves cached result immediately (no JavaScript needed)
```

Reference: `/core/modules/big_pipe/src/Render/BigPipe.php`

## Common Mistakes

- Using BigPipe for fast content — Only use for content taking >100ms; overhead not worth it for fast renders
- Not providing placeholder preview — Causes layout shift (CLS); add preview skeleton for better UX
- Creating too many BigPipe placeholders — Each placeholder adds overhead; use sparingly (2-5 per page)
- Forgetting about no-JS users — BigPipe degrades gracefully but test without JavaScript
- Not monitoring BigPipe overhead — Drupal 11.3+ optimizations reduce overhead; upgrade if using older versions

## See Also

- [Lazy Builders](lazy-builders.md) — How to create placeholders for BigPipe
- [Dynamic Page Cache](dynamic-page-cache.md) — How BigPipe integrates with caching
- Reference: [Drupal BigPipe documentation](https://www.drupal.org/docs/8/core/modules/big-pipe)
