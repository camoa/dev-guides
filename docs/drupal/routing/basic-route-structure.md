---
description: Basic Drupal route structure - foundation for all route definitions in *.routing.yml files
drupal_version: "11.x"
---

# Basic Route Structure

## When to Use

> Use when defining any new route in a `*.routing.yml` file. This is the foundation for all routing definitions.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple page with controller | `_controller` | Full control over response, can return render arrays or Response objects |
| Form page | `_form` | Drupal handles form workflow automatically |
| Entity form | `_entity_form` | Leverages entity form handlers |
| Entity list | `_entity_list` | Uses entity list builder |
| Menu block page | `SystemController::systemAdminMenuBlockPage` | Standard admin landing page pattern |

## Pattern

```yaml
# Minimal route structure
my_module.example:
  path: '/example-path'
  defaults:
    _controller: '\Drupal\my_module\Controller\ExampleController::build'
    _title: 'Example Page'
  requirements:
    _permission: 'access content'

# Form route
my_module.config_form:
  path: '/admin/config/my-module/settings'
  defaults:
    _form: '\Drupal\my_module\Form\SettingsForm'
    _title: 'Module Settings'
  requirements:
    _permission: 'administer my module'
  options:
    _admin_route: TRUE
```

Reference: `core/modules/system/system.routing.yml`

## Common Mistakes

- **Wrong**: Omitting leading slash in path → **Right**: Always start paths with `/example-path`
- **Wrong**: Using underscores in URL paths → **Right**: Use hyphens for SEO and conventions
- **Wrong**: Missing `_title` or `_title_callback` → **Right**: Always provide page title
- **Wrong**: Forgetting `_admin_route: TRUE` for admin pages → **Right**: Set option for admin theme
- **Wrong**: Using non-existent permissions → **Right**: Define permissions in `permissions.yml` first

## See Also

- [YAML Escaping Rules](yaml-escaping-rules.md)
- [Route Parameters](route-parameters.md)
- Reference: [Structure of routes - Drupal.org](https://www.drupal.org/docs/drupal-apis/routing-system/structure-of-routes)
