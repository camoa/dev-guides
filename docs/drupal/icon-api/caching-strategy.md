---
description: "Icon pack cache layers — nothing watches *.icons.yml for changes, and the icon render element carries zero cache metadata of its own"
tldr: "Icon pack definitions cache in cache.discovery under cid icon_pack (icon_pack_plugin is a tag, not the cid); nothing watches *.icons.yml file changes, and the icon render element itself adds no #cache — add your own on the parent."
drupal_version: "11.x"
---

# Caching Strategy

## When to Use

You need to understand Icon API caching behavior to optimize performance or troubleshoot cache-related issues.

## Decision

| Cache layer | Where | Invalidated when... |
|---|---|---|
| Pack definitions **and** the full icon list | `cache.discovery`, cid `icon_pack`, tags `icon_pack_plugin` + `icon_pack_collector` | Cache rebuild, or those tags invalidated. **Not** on `*.icons.yml` file change |
| Loaded `IconDefinition` objects | `IconCollector`, bin `cache.default`, cid `icon_info`, tag `icon_pack_collector` | Same tags |
| Render cache | Whatever the surrounding render array declares | The icon element itself contributes nothing |

Discovery is eager: `IconPackManager::processDefinition()` runs the extractor and stores the whole icon list inside the cached plugin definition. That means a pack with thousands of icons is paid for once per cache rebuild, and that editing an `.icons.yml` or dropping a new SVG into a source directory has **no effect until you rebuild** — `DefaultPluginManager` does not watch file mtimes.

## Pattern

The icon render element carries **no cache metadata**. `getIconRenderable()` returns four keys and `preRenderIcon()` adds `inline-template` and, if the pack declares one, `#attached['library']` — there is no `#cache` anywhere in the path. If an icon's visibility depends on something cacheable, declare it on the parent element:

```php
$build['maybe_icon'] = [
  '#type' => 'icon',
  '#pack_id' => 'my_theme',
  '#icon_id' => 'home',
  '#settings' => ['size' => 24],
  // Yours to add; nothing in Icon API supplies this.
  '#cache' => [
    'tags' => ['icon_pack_plugin'],
    'contexts' => ['user.permissions'],
  ],
];
```

Custom extractor caching:

```php
<?php
namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\Cache\Cache;
use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Theme\Icon\IconDefinition;
use Drupal\Core\Theme\Icon\IconExtractorBase;

class CachedExtractor extends IconExtractorBase {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected CacheBackendInterface $cache,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public function discoverIcons(): array {
    // There is no getPackId() on the base class. The pack ID is the plugin
    // definition's own id, which arrives in the configuration array.
    $pack_id = $this->configuration['id'];
    $cid = 'my_module:icons:' . $pack_id;

    if ($cached = $this->cache->get($cid)) {
      return $cached->data;
    }

    $icons = [];
    foreach ($this->loadIconsFromSource() as $icon_id => $data) {
      // Keys MUST be the full "pack_id:icon_id". IconCollector looks icons up
      // by full ID; a bare icon_id key discovers fine and never renders.
      $icons[IconDefinition::createIconId($pack_id, $icon_id)] = $data;
    }

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

# Targeted: invalidate the icon tags. `icon_pack_plugin` is a cache TAG,
# not a cache ID -- the discovery cid is 'icon_pack'.
drush php:eval "\\Drupal::service('cache_tags.invalidator')->invalidateTags(['icon_pack_plugin', 'icon_pack_collector']);"
```

Reference: `/core/lib/Drupal/Core/Cache/` for cache API.

## Common Mistakes

- Expecting a cache clear on `*.icons.yml` change → Nothing watches those files; run `drush cr` (or invalidate the tags) after every edit
- Deleting a cid named `icon_pack_plugin` → That is a tag. The cid is `icon_pack` in `cache.discovery`
- Calling `$this->getPackId()` in an extractor → No such method; use `$this->configuration['id']`
- Keying `discoverIcons()` by bare icon ID → Must be `pack_id:icon_id`; use `IconDefinition::createIconId()`
- Infinite cache age for dynamic icons → Set an appropriate expiry for API-sourced icons

## See Also

- [IconPackManager Service](iconpackmanager-service.md)
- [Performance Best Practices](performance-best-practices.md)
- Reference: [Drupal Cache API](https://www.drupal.org/docs/drupal-apis/cache-api/cache-api)
