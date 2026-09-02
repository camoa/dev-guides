---
description: "discoverIcons() must key by the full pack_id:icon_id, and loadIcon()'s signature is fixed — a wrong override fails at class load"
tldr: "Core/contrib extractors don't cover your source; discoverIcons() must key by the full pack_id:icon_id or the icon lists but never renders, and overriding loadIcon() with a different signature is fatal at class load."
drupal_version: "11.x"
---

# Custom Extractor Development

## When to Use

The core extractors (`svg`, `svg_sprite`, `path`) and the contrib `font` extractor don't support your icon source (API, database, generated icons, external service).

## Decision

| Icon source | Extractor approach | Complexity |
|---|---|---|
| REST API | HTTP client in discoverIcons() | Medium |
| Database table | Entity query in discoverIcons() | Low-Medium |
| Generated/computed | Logic in discoverIcons() | Medium |
| External service (Iconify, etc.) | API client with caching | Medium-High |
| Conditional icons | Runtime logic in loadIcon() | Low |

Two contracts from `IconExtractorInterface` that are easy to get wrong, and both fail hard:

- `discoverIcons(): array` must return an array **keyed by the full `pack_id:icon_id`**. `IconCollector::getIconFromExtractor()` looks up `$definition['icons'][$icon_full_id]`; a bare `icon_id` key means the icon is listed in the admin UI and never renders. Build keys with `IconDefinition::createIconId($this->configuration['id'], $icon_id)`.
- `loadIcon(array $icon_data): ?IconDefinitionInterface` takes the discovery **array** and returns an `IconDefinition`, not a string ID and an array. Declaring `loadIcon(string $icon_id): ?array` is a fatal signature incompatibility at class load. If your discovery payload needs no extra work, inherit `IconExtractorBase::loadIcon()` and do not override it at all.

Extend `IconExtractorBase` for a source you resolve yourself; extend `IconExtractorWithFinder` if you want core's path/URL `config: sources` handling.

## Pattern

Custom extractor plugin structure:

```php
<?php
namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\Http\ClientFactory;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\Core\Theme\Icon\Attribute\IconExtractor;
use Drupal\Core\Theme\Icon\IconDefinition;
use Drupal\Core\Theme\Icon\IconExtractorBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[IconExtractor(
  id: 'api_icons',
  // label and description are TranslatableMarkup in every core extractor;
  // IconExtractorBase::label() casts to string.
  label: new TranslatableMarkup('API Icon Extractor'),
  description: new TranslatableMarkup('Loads icons from external API.'),
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
    // There is no getPackId(); the pack ID arrives as configuration['id'].
    $pack_id = $this->configuration['id'];
    $cid = 'api_icons:' . $pack_id;

    if ($cached = $this->cache->get($cid)) {
      return $cached->data;
    }

    $icons = [];
    // Extractor config lives under `config:` in the pack definition.
    $api_url = $this->configuration['config']['api_url'] ?? '';

    try {
      $client = $this->httpClientFactory->fromOptions();
      $response = $client->get($api_url);
      $data = json_decode((string) $response->getBody(), TRUE);

      foreach ($data['icons'] ?? [] as $icon) {
        // Keys MUST be the full "pack_id:icon_id" or IconCollector never
        // finds the icon and it renders as nothing.
        $full_id = IconDefinition::createIconId($pack_id, $icon['id']);
        $icons[$full_id] = [
          // loadIcon() receives this array; icon_id is injected by
          // IconCollector, source and any extra keys are yours.
          'source' => $icon['svg_url'],
        ];
      }

      // Cache for 1 hour.
      $this->cache->set($cid, $icons, time() + 3600, [
        'icon_pack_plugin',
        'api_icons',
      ]);
    }
    catch (\Exception $e) {
      \Drupal::logger('my_module')->error(
        'Failed to load icons from API: @error',
        ['@error' => $e->getMessage()]
      );
    }

    return $icons;
  }

  // No loadIcon() override. IconExtractorBase::loadIcon(array $icon_data)
  // already builds the IconDefinition from icon_id + source + group.
  // Override it only to add extractor data, and keep the interface's
  // signature: loadIcon(array $icon_data): ?IconDefinitionInterface.
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
{{ icon('api_icons', 'home', { size: 32 }) }}
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorInterface.php`

## Common Mistakes

- Keying `discoverIcons()` by bare icon ID → Icons appear in the admin listing and render as nothing
- Overriding `loadIcon()` with a different signature → Fatal at class load; the interface is `loadIcon(array $icon_data): ?IconDefinitionInterface`
- Calling `$this->getPackId()` → No such method on `IconExtractorBase`; use `$this->configuration['id']`
- Reading config from `$this->configuration['my_key']` → Extractor config is nested under `config:`
- Not implementing caching → `discoverIcons()` runs on every cache rebuild, and for an HTTP source that is a slow, failure-prone rebuild
- Missing error handling → An uncaught exception in `discoverIcons()` propagates out of `processDefinition()` and takes down the cache rebuild
- Not using dependency injection → Inject services properly for testability

## See Also

- [Migration Patterns](migration-patterns.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorBase.php`, `/core/lib/Drupal/Core/Theme/Icon/IconExtractorWithFinder.php`
- Reference: `/core/modules/system/tests/modules/icon_test/src/Plugin/IconExtractor/TestExtractor.php` for a minimal working example in core
- Reference: [Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
