---
description: Adding cache keys, contexts, tags, and max-age to render arrays for correct caching and invalidation.
---

# Cache Metadata in Render Arrays

## When to Use

Every render array that depends on dynamic data (entities, config, user context, time) needs cache metadata to ensure correct caching and cache invalidation.

## Cache Metadata Components

| Component | Purpose | Example |
|---|---|---|
| **keys** | Unique identifier for this render array | `#cache['keys'] => ['node', 'teaser', $node->id()]` |
| **contexts** | Vary cache by request context (user, language, URL) | `#cache['contexts'] => ['user', 'languages:language_interface']` |
| **tags** | Invalidate cache when dependencies change | `#cache['tags'] => ['node:1', 'config:system.site']` |
| **max-age** | How long cached version is valid (seconds) | `#cache['max-age'] => 3600` (1 hour) or `Cache::PERMANENT` |

## Decision: Cache Strategy

| If output depends on... | Add cache context... | Why |
|---|---|---|
| Current user's identity | `'user'` | Different users see different content |
| Current user's permissions | `'user.permissions'` | Permission checks affect visibility |
| Current user's roles | `'user.roles'` | Role-based output variations |
| URL path | `'url.path'` | Page-specific content |
| URL query string | `'url.query_args'` or `'url'` | Filter/sort parameters affect output |
| Interface language | `'languages:language_interface'` | Translated content |
| Content language | `'languages:language_content'` | Multilingual sites |
| Theme | `'theme'` | Theme-specific rendering |
| Timezone | `'timezone'` | Date/time displays |

## Pattern: Basic Caching

```php
// Simple cached block
$build = [
  '#markup' => $this->generateExpensiveContent(),
  '#cache' => [
    'keys' => ['mymodule', 'expensive_block'],
    'contexts' => ['user'],  // Different per user
    'tags' => ['config:mymodule.settings'],  // Invalidate when config changes
    'max-age' => 3600,  // Cache for 1 hour
  ],
];
```

## Pattern: Entity-Based Caching

```php
// Node teaser with proper cache metadata
$node = Node::load($nid);

$build = [
  '#theme' => 'node_teaser',
  '#node' => $node,
  '#cache' => [
    'keys' => ['node_teaser', $node->id()],
    'tags' => $node->getCacheTags(),  // 'node:123', 'node_type:article', etc.
    'contexts' => ['languages:language_interface'],
    'max-age' => Cache::PERMANENT,  // Valid until tags invalidate
  ],
];
```

**Reference:** Entities implement `CacheableDependencyInterface` -- use their cache methods:

- `$entity->getCacheTags()` -- tags to invalidate when entity changes
- `$entity->getCacheContexts()` -- contexts the entity rendering varies by
- `$entity->getCacheMaxAge()` -- max-age based on entity data

## Pattern: Using addCacheableDependency()

```php
$renderer = \Drupal::service('renderer');
$config = $this->config('mymodule.settings');

$build = ['#markup' => $config->get('message')];

// Automatically adds config's cache tags
$renderer->addCacheableDependency($build, $config);

// Result: $build['#cache']['tags'] includes 'config:mymodule.settings'
```

**Reference:** `core/lib/Drupal/Core/Render/RendererInterface.php` (lines 405-420) -- `addCacheableDependency()` method

## Pattern: Bubbling Metadata from Objects

```php
use Drupal\Core\Render\BubbleableMetadata;

$metadata = new BubbleableMetadata();
$access_result = $node->access('view', NULL, TRUE);

// Capture access check's cache metadata
$metadata->addCacheableDependency($access_result);

if ($access_result->isAllowed()) {
  $build = ['#markup' => $node->label()];
  $metadata->applyTo($build);  // Add captured metadata to render array
}
```

**Reference:** `core/lib/Drupal/Core/Render/BubbleableMetadata.php`

## Cache Max-Age Constants

```php
use Drupal\Core\Cache\Cache;

// Permanent until invalidated by tags
Cache::PERMANENT  // = -1 (infinite)

// Never cache (always regenerate)
0  // max-age = 0 seconds

// Time-based (seconds)
3600  // 1 hour
86400  // 1 day
```

## Common Mistakes

- **Setting cache keys without contexts** -- Same cached version shown to all users when it should vary
- **Not adding cache tags for dependencies** -- Stale cache persists after entity/config updates
- **Using `max-age => 0` everywhere** -- Destroys performance; find appropriate cache strategy instead
- **Forgetting to bubble metadata from access checks** -- Cached version doesn't respect permissions
- **Not understanding cache context cost** -- Too many contexts = too many cache variations = low hit rate
- **Assuming `#cache['tags']` merges automatically in custom code** -- Only automatic during rendering; use `BubbleableMetadata::merge()` in preprocess

## See Also

- [Lazy Builders & Placeholders](lazy-builders-placeholders.md) for uncacheable parts
- [Security & Performance](security-performance.md) for cache security implications
- Reference: [Cacheability of render arrays](https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays)
- Reference: [Drupal at your Fingertips: Render Arrays](https://www.drupalatyourfingertips.com/render)
