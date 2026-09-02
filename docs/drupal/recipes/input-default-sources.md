---
description: Default sources provide fallback values from literal values, config references, or environment variables
tldr: "Use default sources to provide fallback values when inputs aren't explicitly collected from users."
drupal_version: "11.x"
---

# Input System - Default Sources

## When to Use

> Use default sources to provide fallback values when inputs aren't explicitly collected from users.

Default sources provide fallback values when inputs aren't explicitly collected. Three source types: literal values, config references, environment variables.

## Items: The Three Default Sources

### source: value

**Description:** Literal default value
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | primitive | Literal string, int, bool, or float |

**Usage Example:**
```yaml
input:
  site_name:
    data_type: string
    default:
      source: value
      value: 'Default Site Name'
```
**Gotchas:** No fallback; value is the default

### source: config

**Description:** Read default from active config
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| config | array | [config_name, property_path] |
| fallback | primitive | Optional; used if config doesn't exist |

**Usage Example:**
```yaml
input:
  site_mail:
    data_type: string
    default:
      source: config
      config: [system.site, mail]
      fallback: 'admin@example.com'
```
**Gotchas:** Config must exist unless fallback provided; throws exception if config missing and no fallback

### source: env

**Description:** Read default from environment variable
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| env | string | Environment variable name |
| fallback | primitive | Optional; used if env var not set |

**Usage Example:**
```yaml
input:
  api_key:
    data_type: string
    default:
      source: env
      env: DRUPAL_API_KEY
      fallback: ''
```
**Gotchas:** Environment variables are always strings; no type coercion; missing var without fallback throws exception

## Common Mistakes

- Using config source without fallback on new installs → Config likely doesn't exist yet; provide fallback
- Forgetting environment variables are strings → `ENABLE_FEATURE=1` is string `"1"`, not boolean `true`
- Not validating fallback matches data type → Fallback should be same type as data_type (though cast happens)
- Using deeply nested config paths → Only supports `config.get('key')`, not `config.get('nested.key.path')`; use dot syntax in key
- Assuming config source works for all config → Only works for simple config, not config entity properties

## See Also

- Previous: ← [Input System - Defining Inputs](input-defining.md)
- Next: [Input Collection & Forms](input-collection-forms.md) →
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php` (getDefaultValue method)
