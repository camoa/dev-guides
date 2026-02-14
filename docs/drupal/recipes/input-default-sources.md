---
description: Default sources provide fallback values from literal values, config references, or environment variables
drupal_version: "11.x"
---

# Input System - Default Sources

## When to Use

> Use default sources to provide fallback values when inputs aren't explicitly collected from users.

## Decision

| Source Type | Parameters | Use For |
|-------------|------------|---------|
| source: value | `value`: primitive | Literal default value, no fallback needed |
| source: config | `config`: [config_name, property], `fallback`: optional | Read from active config with optional fallback |
| source: env | `env`: variable name, `fallback`: optional | Read from environment variable with optional fallback |

## Pattern

Literal default value:

```yaml
input:
  site_name:
    data_type: string
    default:
      source: value
      value: 'Default Site Name'
```

Read from active config:

```yaml
input:
  site_mail:
    data_type: string
    default:
      source: config
      config: [system.site, mail]
      fallback: 'admin@example.com'
```

Read from environment variable:

```yaml
input:
  api_key:
    data_type: string
    default:
      source: env
      env: DRUPAL_API_KEY
      fallback: ''
```

## Common Mistakes

- **Wrong**: Using config source without fallback on new installs → **Right**: Config likely doesn't exist yet; provide fallback
- **Wrong**: Forgetting environment variables are strings → **Right**: `ENABLE_FEATURE=1` is string `"1"`, not boolean `true`
- **Wrong**: Not validating fallback matches data type → **Right**: Fallback should be same type as data_type (though cast happens)
- **Wrong**: Using deeply nested config paths → **Right**: Only supports `config.get('key')`, not `config.get('nested.key.path')`; use dot syntax in key
- **Wrong**: Assuming config source works for all config → **Right**: Only works for simple config, not config entity properties

## See Also

- [Input System - Defining Inputs](input-defining.md)
- [Input Collection & Forms](input-collection-forms.md)
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php` (getDefaultValue method)
