---
description: Cache render arrays and understand how render caching stores rendered HTML
---

# Render Caching

## When to Use

When you need to cache rendered output of render arrays. Render caching stores the final rendered HTML along with cache metadata, avoiding expensive re-rendering on subsequent requests.

## Steps

1. **Add cache keys to render array** — Define unique identifier for this cacheable content
   ```php
   $build = [
     '#theme' => 'my_template',
     '#cache' => [
       'keys' => ['my_module', 'component', $entity->id()],
     ],
   ];
   ```
   Cache keys must uniquely identify the render array. Contexts will create variations automatically.

2. **Add cache metadata** (tags, contexts, max-age)
   ```php
   $build['#cache']['tags'] = ['node:' . $entity->id()];
   $build['#cache']['contexts'] = ['user.roles'];
   $build['#cache']['max-age'] = Cache::PERMANENT;
   ```
   All three metadata properties required for proper caching.

3. **Render the array** — Renderer checks cache, serves cached if available
   ```php
   $output = \Drupal::service('renderer')->render($build);
   ```
   Renderer handles cache lookup, storage, and metadata bubbling automatically.

4. **Cache metadata bubbles up** — Child metadata merges with parent
   ```php
   $parent = [
     'child' => $build,  // Child metadata automatically bubbles to parent
   ];
   ```
   No manual metadata copying needed; renderer handles bubbling.

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Defining cache keys | Content varies by parameter | Include parameter in keys array: `['my_module', $type, $id]` |
| Defining cache keys | Content varies by context (user, language) | Use cache contexts, not keys: contexts create variations automatically |
| Adding cache tags | Using entity data | Add entity cache tags: `$entity->getCacheTags()` |
| Adding cache contexts | Content differs per user/URL/language | Add appropriate contexts: `['user.roles', 'url.path']` |
| Setting max-age | Content updates on schedule | Set expiration in seconds: `max-age => 3600` |
| Setting max-age | Content updates when entity changes | Use `Cache::PERMANENT` and rely on cache tags |

## Common Mistakes

- Forgetting cache keys — Render cache not used (no unique identifier to look up)
- Using contexts in keys — Creates separate cache entry per variation instead of using Drupal's context system
- Manually copying child cache metadata to parent — Renderer does this automatically through bubbling
- Rendering without cache metadata — Content cached with wrong tags/contexts, serves stale data
- Setting cache keys on non-cacheable elements — Waste (elements like `#markup` without `#cache` keys don't cache)

## See Also

- [BubbleableMetadata & Cache Bubbling](bubbleable-metadata-cache-bubbling.md) — How metadata bubbles
- [Cache Metadata Trinity](cache-metadata-trinity.md) — Required metadata properties
- Reference: `/core/lib/Drupal/Core/Render/RenderCache.php`
