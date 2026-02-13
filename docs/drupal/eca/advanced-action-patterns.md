---
description: Integrate external APIs, YAML config, dynamic forms, and structured error handling in ECA actions
drupal_version: "11.x"
---

# Advanced Action Patterns

## When to Use

> Use advanced action patterns when integrating with external APIs, processing complex data structures with YAML configuration, validating external service responses, or implementing sophisticated error handling.

## Decision

| If you need... | Pattern | Why |
|----------------|---------|-----|
| API integration with config | Service injection + YAML config | Flexible configuration without hardcoding |
| Dynamic form options | External service in `buildConfigurationForm()` | Real-time option lists from APIs |
| Multiple related actions | Plugin deriver | Single class generates multiple plugin variants |
| Structured error responses | Token data with success/error fields | Downstream conditions can check results |

## Pattern

```php
#[Action(
  id: 'my_module_api_call',
  label: new TranslatableMarkup('My Module: API Call'),
)]
#[EcaAction(version_introduced: '1.0.0')]
class ApiCallAction extends ConfigurableActionBase {

  protected HttpClientInterface $httpClient;
  protected YamlParser $yamlParser;

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
    $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
    $instance->httpClient = $container->get('http_client');
    $instance->yamlParser = $container->get('eca.service.yaml_parser');
    return $instance;
  }

  public function execute(): void {
    try {
      $endpoint = $this->tokenService->getOrReplace($this->configuration['endpoint']);
      $api_config = $this->yamlParser->parse($this->configuration['api_config']) ?? [];

      $response = $this->httpClient->request('GET', $endpoint, $api_config);
      $data = json_decode($response->getBody()->getContents(), TRUE);

      $this->tokenService->addTokenData($this->configuration['result_token'], [
        'success' => 1,
        'data' => $data,
        'status_code' => $response->getStatusCode(),
      ]);
    }
    catch (\Exception $e) {
      $this->tokenService->addTokenData($this->configuration['result_token'], [
        'success' => 0,
        'error' => $e->getMessage(),
      ]);
      $this->logger->error('API call failed: @error', ['@error' => $e->getMessage()]);
    }
  }
}
```

## Common Mistakes

- **Wrong**: Not handling API failures → **Right**: Always use try-catch for graceful degradation
- **Wrong**: Hardcoding API configuration → **Right**: Use YAML config fields for flexibility
- **Wrong**: Missing structured error responses → **Right**: Include success/error fields for conditions
- **Wrong**: Not logging errors → **Right**: Use `$this->logger` for debugging
- **Wrong**: Injecting parent's services in child → **Right**: Parent already has them

## See Also

- [YAML Configuration](yaml-configuration.md) for config patterns
- [Access Control Patterns](access-control-patterns.md) for validation
- [Security Best Practices](security-best-practices.md) for secure API calls

**References:**
- Contrib example: Check ECA AI module for AI service integration patterns
- Core: `/modules/contrib/eca/src/Service/YamlParser.php`
