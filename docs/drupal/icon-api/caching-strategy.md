---
description: Icon API caching behavior to optimize performance and troubleshoot cache-related issues
drupal_version: "11.x"
---

# Caching Strategy

## When to Use

You need to understand Icon API caching behavior to optimize performance or troubleshoot cache-related issues.

## Decision

| Cache layer | What's cached | Invalidated when... |
|---|---|---|
| Plugin definitions | Icon pack YAML | Cache cleared, `*.icons.yml` modified |
| Icon discovery | Icon file paths | Cache cleared, icon files added/removed |
| Render cache | Rendered icon markup | Settings changed, icon source modified |
| Asset library | Icon CSS/JS | Cache cleared, library definition changed |

## Pattern

Icon API cache participation:

```php
// Icon render array includes cache tags automatically
$icon = [
  '#type' => 'icon',
  '#pack' => 'my_theme',
  '#icon' => 'home',
  '#settings' => ['size' => 24],
];

// Equivalent to:
$icon = [
  '#type' => 'icon',
  '#pack' => 'my_theme',
  '#icon' => 'home',
  '#settings' => ['size' => 24],
  '#cache' => [
    'tags' => ['icon_pack_plugin'],
    'contexts' => [],
    'max-age' => Cache::PERMANENT,
  ],
];
```

Custom extractor caching:

```php
<?php
namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Theme\Icon\IconExtractorBase;

class CachedExtractor extends IconExtractorBase {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected CacheBackendInterface $cache
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public function discoverIcons(): array {
    $cid = 'my_module:icons:' . $this->getPackId();

    if ($cached = $this->cache->get($cid)) {
      return $cached->data;
    }

    $icons = $this->loadIconsFromSource();

    $this->cache->set($cid, $icons, Cache::PERMANENT, [
      'icon_pack_plugin',
      'my_module:icons',
    ]);

    return $icons;
  }
}
```

Clear icon caches:

```bash
# Clear all caches (includes icon caches)
drush cache:rebuild

# Clear specific cache bins
drush php:eval "\\Drupal::cache('discovery')->delete('icon_pack_plugin');"
```

Reference: `/core/lib/Drupal/Core/Cache/` for cache API.

## Common Mistakes

- **Wrong**: Clearing cache for every icon change → **Right**: Cache cleared automatically when source files change
- **Wrong**: Not tagging custom caches → **Right**: Use `icon_pack_plugin` tag for icon-related caches
- **Wrong**: Infinite cache age for dynamic icons → **Right**: Set appropriate `max-age` for API-sourced icons
- **Wrong**: Missing cache contexts → **Right**: Add contexts when icon rendering depends on user, URL, etc.
- **Wrong**: Rebuilding icon discovery on every request → **Right**: Cache discovery results with proper tags

## See Also

- [IconPackManager Service](iconpackmanager-service.md)
- [Performance Best Practices](performance-best-practices.md)
- Reference: [Drupal Cache API](https://www.drupal.org/docs/drupal-apis/cache-api/cache-api)
