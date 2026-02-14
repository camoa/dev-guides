---
description: Develop custom extractor plugins for icon sources not supported by core extractors
drupal_version: "11.x"
---

# Custom Extractor Development

## When to Use

Core extractors (SVG, SVG Sprite, Path, Font) don't support your icon source (API, database, generated icons, external service).

## Decision

| Icon source | Extractor approach | Complexity |
|---|---|---|
| REST API | HTTP client in discoverIcons() | Medium |
| Database table | Entity query in discoverIcons() | Low-Medium |
| Generated/computed | Logic in discoverIcons() | Medium |
| External service (Iconify, etc.) | API client with caching | Medium-High |
| Conditional icons | Runtime logic in loadIcon() | Low |

## Pattern

Custom extractor plugin structure:

```php
<?php
namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Http\ClientFactory;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Theme\Icon\Attribute\IconExtractor;
use Drupal\Core\Theme\Icon\IconExtractorBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[IconExtractor(
  id: 'api_icons',
  label: 'API Icon Extractor',
  description: 'Loads icons from external API.'
)]
class ApiIconExtractor extends IconExtractorBase implements ContainerFactoryPluginInterface {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected ClientFactory $httpClientFactory,
    protected CacheBackendInterface $cache
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(
    ContainerInterface $container,
    array $configuration,
    $plugin_id,
    $plugin_definition
  ) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('http_client_factory'),
      $container->get('cache.default')
    );
  }

  /**
   * Discover all available icons from the API.
   */
  public function discoverIcons(): array {
    $cid = 'api_icons:' . $this->getPackId();

    if ($cached = $this->cache->get($cid)) {
      return $cached->data;
    }

    $icons = [];
    $api_url = $this->configuration['api_url'] ?? '';

    try {
      $client = $this->httpClientFactory->fromOptions();
      $response = $client->get($api_url);
      $data = json_decode($response->getBody(), TRUE);

      foreach ($data['icons'] ?? [] as $icon) {
        $icons[$icon['id']] = [
          'source' => $icon['svg_url'],
          'label' => $icon['name'],
        ];
      }

      // Cache for 1 hour
      $this->cache->set($cid, $icons, time() + 3600, [
        'icon_pack_plugin',
        'api_icons',
      ]);

    } catch (\Exception $e) {
      \Drupal::logger('my_module')->error(
        'Failed to load icons from API: @error',
        ['@error' => $e->getMessage()]
      );
    }

    return $icons;
  }

  /**
   * Load a specific icon.
   */
  public function loadIcon(string $icon_id): ?array {
    $icons = $this->discoverIcons();
    return $icons[$icon_id] ?? NULL;
  }
}
```

Icon pack using custom extractor:

```yaml
api_icons:
  label: "API Icons"
  extractor: api_icons
  config:
    api_url: "https://api.example.com/icons"
  template: >-
    <img src="{{ source }}"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         alt="{{ alt|default('') }}">
```

Usage:

```twig
{{ icon('api_icons:home', { size: 32 }) }}
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorInterface.php`

## Common Mistakes

- **Wrong**: Not implementing caching → **Right**: API called on every icon render, massive performance hit
- **Wrong**: Missing error handling → **Right**: API failures break entire site rendering
- **Wrong**: No cache invalidation strategy → **Right**: Stale icons when API updates
- **Wrong**: Synchronous API calls → **Right**: Use queue for icon discovery if API is slow
- **Wrong**: Not using dependency injection → **Right**: Inject services properly for testability

## See Also

- [Migration Patterns](migration-patterns.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorBase.php`
- Reference: [Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
