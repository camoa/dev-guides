---
description: Config import specifies config to copy from extensions, strict mode controls validation of existing config
drupal_version: "11.x"
---

# Config Import & Strict Mode

## When to Use

> Use `config.import` to specify config files to copy from extensions. Use `config.strict` to control validation of existing config.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Config may already exist, adding to existing site | Use `strict: false` | Skips existing config, flexible application |
| Config must be exact, enforcing schema (fields) | Use `strict: true` or array | Validates critical config matches expectations |
| Import conflicts with actions | Actions run after import | Last action wins |

## Pattern

Import all extension config with wildcard:

```yaml
config:
  import:
    node: '*'
```

Import specific config:

```yaml
config:
  import:
    node:
      - views.view.content
      - core.entity_view_mode.node.teaser
    image:
      - image.style.medium
```

Strict mode - boolean:

```yaml
config:
  strict: true  # All config must match exactly
  strict: false # Only import config that doesn't exist
```

Strict mode - array (validate only listed config):

```yaml
config:
  strict:
    - field.storage.node.field_image  # Database schema must match
    - node.type.article
```

## Common Mistakes

- **Wrong**: Using `strict: true` on sites with existing config → **Right**: Recipe fails if any config doesn't match; use array or false
- **Wrong**: Forgetting strict mode defaults to true → **Right**: Implicit `strict: true` causes failures on existing sites
- **Wrong**: Importing config then modifying via actions without strict awareness → **Right**: Strict validates imported config, not action results
- **Wrong**: Listing config that doesn't exist in extension → **Right**: Runtime error; validate extension provides config being imported
- **Wrong**: Not understanding UUID/dependencies are stripped in comparison → **Right**: UUIDs and empty dependencies ignored; only real differences trigger strict failures

## See Also

- [Extension Installation](extension-installation.md)
- [Config Actions - Universal](config-actions-universal.md)
- Reference: `core/lib/Drupal/Core/Recipe/ConfigConfigurator.php`
