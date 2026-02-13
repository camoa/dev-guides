---
description: Define structure and validation constraints for configuration
drupal_version: "11.x"
---

# Configuration Schema

## When to Use

> Use configuration schema when defining structure and validation constraints for configuration stored by ConfigFormBase.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple key-value config | type: mapping with scalar types | Most common config pattern |
| Typed config values | type: string/integer/boolean/float | Schema validation enforces types |
| Validation constraints | constraints: NotBlank/Length/etc | Drupal 11+ validates automatically |
| Nested config structure | type: mapping with nested mappings | Complex config hierarchies |
| Config arrays/sequences | type: sequence | List of items of same type |

## Pattern

**Config Schema** (config/schema/mymodule.schema.yml):
```yaml
mymodule.settings:
  type: config_object
  label: 'MyModule settings'
  mapping:
    api_key:
      type: string
      label: 'API Key'
      constraints:
        NotBlank: []
        Length:
          max: 255
    timeout:
      type: integer
      label: 'Timeout'
      constraints:
        Range:
          min: 1
          max: 300
    enabled:
      type: boolean
      label: 'Enabled status'
    options:
      type: sequence
      label: 'Options'
      sequence:
        type: string
```

**Using #config_target** (Drupal 11+):
```php
$form['api_key'] = [
  '#type' => 'textfield',
  '#title' => $this->t('API Key'),
  '#default_value' => $config->get('api_key'),
  '#config_target' => 'mymodule.settings:api_key', // Enables automatic validation
];
```

**Schema Types**:
- `boolean`, `string`, `integer`, `float` - Scalar types
- `mapping` - Key-value structure
- `sequence` - Array of items
- `config_object` - Root type for config files

**Common Constraints**:
- `NotBlank: []` - Required field
- `Length: {min: 1, max: 255}` - String length
- `Range: {min: 0, max: 100}` - Numeric range
- `Email: []` - Valid email format
- `Regex: {pattern: '/^[a-z]+$/'}` - Pattern matching

## Common Mistakes

- **Wrong**: Missing config schema entirely → **Right**: Strict validation fails in Drupal 11+
- **Wrong**: Using wrong type (string for integer) → **Right**: Type validation errors
- **Wrong**: Not using #config_target with constraints → **Right**: Validation not triggered
- **Wrong**: Forgetting sequence wrapper for arrays → **Right**: Schema validation fails
- **Wrong**: Not declaring FullyValidatable constraint → **Right**: Config not validated until explicitly checked
- **Wrong**: Typo in config name (mymodule.settings vs mymodule.setting) → **Right**: Schema not loaded

## See Also

- [ConfigFormBase Pattern](configformbase-pattern.md)
- [Common Mistakes](common-mistakes.md)
- Reference: [Configuration Schema/Metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)
- Reference: [#config_target in ConfigFormBase](https://www.drupal.org/node/3373502)
- Reference: core/config/schema/core.data_types.schema.yml
