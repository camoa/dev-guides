---
description: Complex config action scenarios including wildcards, optional config, chaining, and input substitution
drupal_version: "11.x"
---

# Config Actions - Advanced Patterns

## When to Use

> Use advanced config action patterns when you need wildcards for bulk operations, optional config handling, chaining multiple actions, or input substitution.

## Decision

| Pattern | Use For | Syntax |
|---------|---------|--------|
| Wildcards | Bulk operations on multiple entities | `user.role.*:` or `core.entity_view_display.node.*.default:` |
| Optional config | Actions that should skip if config doesn't exist | `?block.block.legacy_block:` |
| Input substitution | Environment-specific values in config | `${input_name}` in config names or values |
| Chaining | Multiple actions on same entity | Multiple action keys under same config name |
| Drupal tokens | Runtime token replacement in config values | `[node:title]`, `[site:url]` (config must support tokens) |

## Pattern

Wildcards for bulk operations:

```yaml
config:
  actions:
    user.role.*:
      grantPermission: 'access content'
    core.entity_view_display.node.*.default:
      setComponent:
        name: created
        options: { type: timestamp, weight: 10 }
```

Optional config actions:

```yaml
config:
  actions:
    ?block.block.legacy_block:
      setProperties:
        status: false
```

Input substitution:

```yaml
input:
  theme_name:
    data_type: string
    default: { source: value, value: olivero }
config:
  actions:
    block.block.${theme_name}_search:
      placeBlockInRegion:
        region: header
        theme: ${theme_name}
```

Chaining actions:

```yaml
config:
  actions:
    user.role.editor:
      createIfNotExists:
        label: 'Editor'
      grantPermissions:
        - 'access content'
        - 'access toolbar'
      setProperties:
        weight: 5
```

Drupal token substitution (for config that supports tokens):

```yaml
config:
  actions:
    metatag.metatag_defaults.node:
      simpleConfigUpdate:
        tags.og_title: '[node:title]'
        tags.og_url: '[site:url]/node/[node:nid]'
```

Create entities then configure:

```yaml
config:
  actions:
    core.entity_form_display.node.article.default:
      createIfNotExists:
        targetEntityType: node
        bundle: article
        mode: default
      setComponents:
        - name: body
          options: { type: text_textarea_with_summary }
```

## Common Mistakes

- **Wrong**: Using wildcards with optional prefix → **Right**: `?user.role.*` is invalid; wildcards and optional are mutually exclusive
- **Wrong**: Forgetting input values are strings → **Right**: `${site_name}` is always string; no type coercion for integers/booleans
- **Wrong**: Not testing wildcard patterns → **Right**: Wildcards only match existing config; create first, then wildcard-modify
- **Wrong**: Assuming action order doesn't matter → **Right**: YAML dict order is preserved; actions run in declaration order
- **Wrong**: Missing createIfNotExists before entity-specific actions → **Right**: Entity must exist or be created in same recipe

## See Also

- [Config Actions - Entity-Specific](config-actions-entity-specific.md)
- [Input System - Defining Inputs](input-defining.md)
- Reference: `core/lib/Drupal/Core/Config/Action/ConfigActionManager.php` (applyAction method)
