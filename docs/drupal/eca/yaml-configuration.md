---
description: Use YAML config fields for complex structured settings with YamlParser validation
drupal_version: "11.x"
---

# YAML Configuration

## When to Use

> Use YAML configuration fields when plugins need complex, structured configuration that's too cumbersome for multiple form fields, such as API client options, nested settings, or dynamic key-value pairs.

## Decision

| Configuration Type | Use YAML When | Use Form Fields When |
|--------------------|---------------|----------------------|
| API client options | 5+ related options | 1-3 simple options |
| Nested structures | Multi-level hierarchy needed | Flat structure works |
| Dynamic keys | User defines key names | Fixed set of keys |
| Optional settings | Many optional parameters | Few required parameters |

## Pattern

```php
use Drupal\eca\Plugin\FormFieldYamlTrait;
use Drupal\eca\Service\YamlParser;
use Symfony\Component\Yaml\Exception\ParseException;

class MyAction extends ConfigurableActionBase {

  use FormFieldYamlTrait;  // Provides YAML form integration

  protected YamlParser $yamlParser;

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
    $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
    $instance->setYamlParser($container->get('eca.service.yaml_parser'));
    return $instance;
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form['api_config'] = [
      '#type' => 'textarea',
      '#title' => $this->t('API Configuration'),
      '#description' => $this->t('YAML format. Example:<br><code>timeout: 30<br>headers:<br>  Authorization: Bearer token</code>'),
      '#default_value' => $this->configuration['api_config'],
      '#rows' => 10,
    ];

    return parent::buildConfigurationForm($form, $form_state);
  }

  public function access($object, ?AccountInterface $account = NULL, $return_as_object = FALSE) {
    // Validate YAML before execution
    if (!empty($this->configuration['api_config'])) {
      try {
        $this->yamlParser->parse($this->configuration['api_config']);
      } catch (ParseException $e) {
        $result = AccessResult::forbidden('Invalid YAML: ' . $e->getMessage());
        return $return_as_object ? $result : FALSE;
      }
    }

    return parent::access($object, $account, $return_as_object);
  }

  public function execute(): void {
    // Parse YAML configuration
    $config = $this->yamlParser->parse($this->configuration['api_config']) ?? [];

    // Use parsed config
    $timeout = $config['timeout'] ?? 30;
    $headers = $config['headers'] ?? [];

    $this->httpClient->request('GET', $url, [
      'timeout' => $timeout,
      'headers' => $headers,
    ]);
  }
}
```

## Common Mistakes

- **Wrong**: Not validating YAML in `access()` → **Right**: Workflow crashes during execution
- **Wrong**: Missing example in form description → **Right**: Users don't know the format
- **Wrong**: Not handling ParseException → **Right**: Uncaught exceptions crash workflows
- **Wrong**: No default value for missing keys → **Right**: Fatal errors on undefined array keys
- **Wrong**: Requiring YAML when simple fields work → **Right**: Unnecessary complexity for users

## See Also

- [Advanced Action Patterns](advanced-action-patterns.md) for API integration
- [Access Control Patterns](access-control-patterns.md) for validation
- [Reusable Traits](reusable-traits.md) for FormFieldYamlTrait

**References:**
- Core: `/modules/contrib/eca/src/Service/YamlParser.php`
- Trait: `/modules/contrib/eca/src/Plugin/FormFieldYamlTrait.php`
- Example: `/modules/contrib/eca_base/src/Plugin/Action/EcaStateWrite.php`
