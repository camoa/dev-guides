---
description: Injecting services into media source plugins for HTTP, logging, caching
drupal_version: "11.x"
---

# Dependency Injection

## When to Use

> Use dependency injection when media source plugin needs services like HTTP client, logger, cache, file system, or custom services.

## Decision

| Service | Use When | Container Service ID |
|---------|----------|---------------------|
| **http_client** | Fetching remote resources, API calls | `http_client` |
| **logger.factory** | Error logging, debugging | `logger.factory` → get('yourmodule') |
| **cache.default** | Caching API responses, metadata | `cache.default` |
| **file_system** | Thumbnail downloads, file operations | `file_system` |
| **token** | Directory paths with tokens | `token` |
| Custom service | Module-specific logic | `yourmodule.service_name` |

## Pattern

Service injection in plugin (15 lines):
```php
use Drupal\Core\Cache\CacheBackendInterface;
use GuzzleHttp\ClientInterface;
use Psr\Log\LoggerInterface;

class CustomApi extends MediaSourceBase {
  protected ClientInterface $httpClient;
  protected LoggerInterface $logger;
  protected CacheBackendInterface $cache;

  public function __construct(
    array $configuration, $plugin_id, $plugin_definition,
    EntityTypeManagerInterface $entity_type_manager,
    EntityFieldManagerInterface $entity_field_manager,
    FieldTypePluginManagerInterface $field_type_manager,
    ConfigFactoryInterface $config_factory,
    ClientInterface $http_client,
    LoggerInterface $logger,
    CacheBackendInterface $cache,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition,
      $entity_type_manager, $entity_field_manager, $field_type_manager, $config_factory);
    $this->httpClient = $http_client;
    $this->logger = $logger;
    $this->cache = $cache;
  }

  public static function create(ContainerInterface $container, array $configuration,
    $plugin_id, $plugin_definition): static {
    return new static(
      $configuration, $plugin_id, $plugin_definition,
      $container->get('entity_type.manager'),
      $container->get('entity_field.manager'),
      $container->get('plugin.manager.field.field_type'),
      $container->get('config.factory'),
      $container->get('http_client'),
      $container->get('logger.factory')->get('yourmodule'),
      $container->get('cache.default'),
    );
  }
}
```

## Common Mistakes

- **Wrong**: Using `\Drupal::service()` in plugins → **Right**: Inject via constructor
- **Wrong**: Not calling parent constructor → **Right**: Call parent with base services
- **Wrong**: Forgetting `create()` method → **Right**: Implement static factory method
- **Wrong**: Wrong parent constructor signature → **Right**: Match MediaSourceBase signature
- **Wrong**: Injecting unnecessary services → **Right**: Only inject what's needed

## See Also

- Previous: [Thumbnail Generation](thumbnail-generation.md)
- Next: [Validation Constraints](validation-constraints.md)
- Reference: https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block
- Reference: https://drupalize.me/topic/dependency-injection
