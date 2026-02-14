---
description: Every recipe requires a recipe.yml file defining metadata, dependencies, extensions, configuration, inputs, and content
drupal_version: "11.x"
---

# Recipe YAML Schema

## When to Use

> Every recipe requires a `recipe.yml` file defining metadata, dependencies, extensions, configuration, inputs, and content.

## Decision

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| name | string | Yes | Human-readable recipe name |
| description | string | No | Short description of the recipe |
| type | string | No | Recipe category for organizational purposes |
| recipes | array | No | List of recipe machine names to apply before this recipe |
| install | array | No | List of module/theme machine names to install |
| config | associative_array | No | Configuration to import and config actions to apply |
| input | associative_array | No | Defines user-provided values for the recipe |
| content | array | No | Reserved for default content configuration |
| extra | associative_array | No | Extension-specific data keyed by extension name |

## Pattern

Minimal recipe.yml structure:

```yaml
name: 'My Recipe'
description: 'Example recipe.'
type: 'Feature'
install:
  - node
config:
  strict: false
  import:
    node:
      - views.view.content
  actions:
    user.role.authenticated:
      grantPermission: 'access content'
input:
  site_name:
    description: 'The name of the site'
    data_type: string
    default:
      source: config
      config: [system.site, name]
extra:
  my_module:
    custom_setting: value
```

## Common Mistakes

- **Wrong**: Omitting `name` → **Right**: Required field, validation fails without it
- **Wrong**: Using relative paths in recipes list → **Right**: Recipe names are machine names, not paths
- **Wrong**: Listing themes before modules in install → **Right**: Themes depend on modules; runner handles order automatically
- **Wrong**: Misspelling config action keys → **Right**: Actions silently fail if plugin ID doesn't exist
- **Wrong**: Forgetting to install extensions that provide config being imported → **Right**: Validation catches this for config actions, not always for imports

## See Also

- [Recipe System Overview](recipe-system-overview.md)
- [Creating Your First Recipe](creating-first-recipe.md)
- Reference: `core/lib/Drupal/Core/Recipe/Recipe.php` (parse method, validation constraints)
