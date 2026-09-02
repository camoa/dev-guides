---
description: Config actions that work on ANY config entity or simple config for generic config updates
tldr: "Use universal config actions when you need to update simple config or config entities without entity-type-specific methods."
drupal_version: "11.x"
---

# Config Actions - Universal

## When to Use

> Use universal config actions when you need to update simple config or config entities without entity-type-specific methods.

Config actions that work on ANY config entity or simple config. Use these for generic config updates.

## Items: Universal Config Actions

### simpleConfigUpdate

**Description:** Updates simple (non-entity) configuration
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | associative array | Keys are config keys, values are new values |

**Usage Example:**
```yaml
config:
  actions:
    system.site:
      simpleConfigUpdate:
        page.front: /node
        name: 'My Site'
```
**Gotchas:** Deprecated for config entities (use setProperties instead); config must exist before update

### setProperties

**Description:** Sets properties on config entities
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | associative array | Keys are entity properties, values are new values |

**Usage Example:**
```yaml
config:
  actions:
    node.type.article:
      setProperties:
        name: 'Article'
        description: 'Use articles for news.'
```
**Gotchas:** Only works on config entities; for simple config use simpleConfigUpdate

### entity_create:createIfNotExists

**Description:** Creates config entity if it doesn't exist
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | associative array | Entity property values; ID derived from config name |

**Usage Example:**
```yaml
config:
  actions:
    user.role.editor:
      createIfNotExists:
        label: 'Editor'
        weight: 5
```
**Gotchas:** Shorthand is `createIfNotExists`; full ID is `entity_create:createIfNotExists`

### setThirdPartySetting / setThirdPartySettings

**Description:** Sets third-party settings on config entities (used by contrib modules)
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| module | string | Module providing the third-party setting |
| key | string | Setting key |
| value | mixed | Setting value |

**Usage Example:**
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
**Gotchas:** Module providing the third-party setting must be installed; `setThirdPartySetting` for single setting, `setThirdPartySettings` for multiple

### entity_clone

**Description:** Clones an existing config entity to new ID
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| id | string | ID of entity to clone |

**Usage Example:**
```yaml
config:
  actions:
    user.role.custom_editor:
      entity_clone:
        id: content_editor
```
**Gotchas:** Target entity must exist; new entity ID from config name

## Common Mistakes

- Using simpleConfigUpdate on config entities → Deprecated; use setProperties or entity-specific actions
- Forgetting createIfNotExists is idempotent → Safe to run multiple times; only creates if missing
- Not understanding action order → Actions apply in YAML order; later actions override earlier ones
- Applying actions to non-existent config → Prefix with `?` to make optional: `?user.role.maybe_exists:`
- Hardcoding values that should be inputs → Use `${input_name}` syntax to reference input values

## See Also

- Previous: ← [Config Import & Strict Mode](config-import-strict.md)
- Next: [Config Actions - Entity-Specific](config-actions-entity-specific.md) →
- Reference: `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/`
- Reference: https://project.pages.drupalcode.org/distributions_recipes/config_action_list.html
