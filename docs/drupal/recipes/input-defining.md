---
description: Define user-provided values that vary per environment to enable recipe portability
drupal_version: "11.x"
---

# Input System - Defining Inputs

## When to Use

> Use inputs when you need to externalize site-specific data that varies per environment, making recipes portable and reusable.

## Decision

| Need | Default Source | Why |
|------|----------------|-----|
| Value varies per environment | `source: env` | Different staging/prod values from environment variables |
| Value comes from existing config | `source: config` | Recipe extends existing site config |
| Value is fixed | `source: value` | All sites use same literal value |
| Validation needed | Add `constraints` | Input format validation (email, URL, regex patterns) |

## Pattern

Define input structure (description, data_type, default required):

```yaml
input:
  site_name:
    description: 'The name of the site'
    data_type: string
    default:
      source: value
      value: 'My Site'
```

Supported data types (primitives only):

```yaml
input:
  enable_feature:
    description: 'Enable experimental feature'
    data_type: boolean
    default: { source: value, value: false }
  cache_lifetime:
    description: 'Cache lifetime in seconds'
    data_type: integer
    default: { source: value, value: 3600 }
```

Add validation constraints:

```yaml
input:
  admin_email:
    description: 'Administrator email address'
    data_type: string
    constraints:
      Email: ~
    default: { source: value, value: 'admin@example.com' }
```

Configure CLI prompts:

```yaml
input:
  site_name:
    description: 'Site name'
    data_type: string
    prompt:
      method: ask
      arguments:
        question: 'What is your site name?'
    default: { source: value, value: 'Default Site' }
```

Configure form elements:

```yaml
input:
  site_name:
    description: 'Site name'
    data_type: string
    form:
      '#title': 'Site name'
      '#required': true
    default: { source: value, value: 'My Site' }
```

## Common Mistakes

- **Wrong**: Using complex data types → **Right**: Only primitives (string, integer, boolean, float) supported; no arrays or objects
- **Wrong**: Forgetting default is required → **Right**: Every input must have default source defined; no default = validation error
- **Wrong**: Not validating inputs → **Right**: Add constraints for format validation (email, URL, regex patterns)
- **Wrong**: Assuming inputs persist → **Right**: Inputs are apply-time only; not stored in config after recipe runs
- **Wrong**: Using Form API child elements in form definition → **Right**: Inputs are primitives; no child elements allowed

## See Also

- [Config Actions - Advanced Patterns](config-actions-advanced.md)
- [Input System - Default Sources](input-default-sources.md)
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php`
