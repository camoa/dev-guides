---
description: Config actions that work on ANY config entity or simple config for generic config updates
drupal_version: "11.x"
---

# Config Actions - Universal

## When to Use

> Use universal config actions when you need to update simple config or config entities without entity-type-specific methods.

## Decision

| Action | Use For | Parameters |
|--------|---------|------------|
| simpleConfigUpdate | Simple (non-entity) configuration | `value`: associative array of config keys → values |
| setProperties | Config entity properties | `value`: associative array of entity properties → values |
| createIfNotExists | Create config entity if missing | `value`: entity property values; ID from config name |
| setThirdPartySetting(s) | Third-party settings on config entities | `module`, `key`, `value` for single; object for multiple |
| entity_clone | Clone existing config entity | `id`: entity ID to clone |

## Pattern

Update simple config:

```yaml
config:
  actions:
    system.site:
      simpleConfigUpdate:
        page.front: /node
        name: 'My Site'
```

Set config entity properties:

```yaml
config:
  actions:
    node.type.article:
      setProperties:
        name: 'Article'
        description: 'Use articles for news.'
```

Create if not exists (idempotent):

```yaml
config:
  actions:
    user.role.editor:
      createIfNotExists:
        label: 'Editor'
        weight: 5
```

Third-party settings:

```yaml
config:
  actions:
    node.type.article:
      setThirdPartySetting:
        scheduler:
          publish_enable: true
      setThirdPartySettings:
        metatag:
          tags:
            title: '[node:title] | [site:name]'
```

Clone entity:

```yaml
config:
  actions:
    user.role.custom_editor:
      entity_clone:
        id: content_editor
```

## Common Mistakes

- **Wrong**: Using simpleConfigUpdate on config entities → **Right**: Deprecated; use setProperties or entity-specific actions
- **Wrong**: Forgetting createIfNotExists is idempotent → **Right**: Safe to run multiple times; only creates if missing
- **Wrong**: Not understanding action order → **Right**: Actions apply in YAML order; later actions override earlier ones
- **Wrong**: Applying actions to non-existent config → **Right**: Prefix with `?` to make optional: `?user.role.maybe_exists:`
- **Wrong**: Hardcoding values that should be inputs → **Right**: Use `${input_name}` syntax to reference input values

## See Also

- [Config Import & Strict Mode](config-import-strict.md)
- [Config Actions - Entity-Specific](config-actions-entity-specific.md)
- Reference: `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/`
- Reference: https://project.pages.drupalcode.org/distributions_recipes/config_action_list.html
