---
description: Inject services into ECA plugins using parent::create pattern (NEVER new static)
drupal_version: "11.x"
---

# Service Injection

## When to Use

> Inject services when your plugin needs functionality beyond what the base class provides, such as HTTP clients, external APIs, database access, or custom business logic services.

## Decision

**CRITICAL:** EcaPluginBase has a FINAL constructor. You MUST use the `parent::create()` pattern.

| Service Need | Injection Pattern | Why |
|--------------|-------------------|-----|
| Parent's services | DO NOT inject | Parent already has them (entity_type.manager, eca.token_services, logger, etc.) |
| Your custom services | Use `parent::create()` + inject | Extends parent's service set |
| Optional services | Inject + NULL default | Service may not exist |

## Pattern

```php
use Symfony\Component\DependencyInjection\ContainerInterface;
use GuzzleHttp\ClientInterface;
use Drupal\eca\Service\YamlParser;

class MyAction extends ConfigurableActionBase {

  // Typed properties (PHP 8)
  protected ClientInterface $httpClient;
  protected YamlParser $yamlParser;
  protected ?MyCustomService $customService;

  /**
   * CRITICAL: Use parent::create(), NOT new static()
   */
  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
    // Create instance with parent's services
    $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);

    // Inject ONLY your new services
    $instance->httpClient = $container->get('http_client');
    $instance->yamlParser = $container->get('eca.service.yaml_parser');

    // Optional service with NULL fallback
    $instance->customService = $container->has('my_module.custom_service')
      ? $container->get('my_module.custom_service')
      : NULL;

    return $instance;
  }

  public function execute(): void {
    // Use injected services
    $response = $this->httpClient->request('GET', $url);
    $config = $this->yamlParser->parse($yaml_string);

    if ($this->customService) {
      $this->customService->performOperation();
    }
  }
}
```

## Common Mistakes

- **Wrong**: Using `new static()` with parent constructor args → **Right**: Fatal error (parent constructor is FINAL)
- **Wrong**: Injecting parent's services again → **Right**: Duplicate dependencies, breaks when parent changes
- **Wrong**: No typed properties → **Right**: Harder to debug, no IDE autocomplete
- **Wrong**: Injecting in constructor instead of `create()` → **Right**: Bypasses Drupal's service container
- **Wrong**: Not checking optional service existence → **Right**: Crashes when service not available

## See Also

- [Reusable Traits](reusable-traits.md) for trait-based service access
- [Advanced Action Patterns](advanced-action-patterns.md) for API client injection
- [Mandatory Rules](mandatory-rules.md) for create() rules

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/EcaPluginBase.php` (FINAL constructor)
- Example: `/modules/contrib/eca_base/src/Plugin/Action/EcaStateWrite.php`
