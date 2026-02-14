---
description: Complete schema for taxonomy.vocabulary.*.yml config files
drupal_version: "11.x"
---

# Vocabulary Configuration Schema

## When to Use

> Use this schema when creating or modifying vocabulary YAML config files. These are the complete properties for `taxonomy.vocabulary.*.yml`.

## Decision

| Property | Type | Required | Default | When to Use |
|----------|------|----------|---------|-------------|
| `langcode` | string | Yes | — | Language code (e.g., `en`) |
| `status` | boolean | Yes | — | `true` = enabled, `false` = disabled |
| `dependencies` | mapping | No | `{}` | When vocabulary is owned by a module (use enforced dependency) |
| `name` | string | Yes | — | Human-readable label (translatable) |
| `vid` | string | Yes | — | Machine name, max 32 characters, unique |
| `description` | string | No | `null` | Plain text description, nullable |
| `weight` | integer | No | `0` | Sort order in vocabulary list |
| `new_revision` | boolean | No | `false` | Create new term revision by default |

## Pattern

Minimal vocabulary config (`taxonomy.vocabulary.categories.yml`):
```yaml
langcode: en
status: true
dependencies: {}
name: Categories
vid: categories
description: 'Content categorization'
weight: 0
new_revision: false
```

With module dependency:
```yaml
langcode: en
status: true
dependencies:
  enforced:
    module:
      - my_module
name: Product Types
vid: product_types
description: ''
weight: 1
new_revision: true
```

## Common Mistakes

- **Wrong**: Exceeding 32-character limit on `vid` → **Right**: Keep machine names short and descriptive
- **Wrong**: Using special characters in `vid` → **Right**: Must follow machine name rules: lowercase, numbers, underscores only
- **Wrong**: Omitting `dependencies` when vocabulary is module-owned → **Right**: Add enforced module dependency so it deletes when module uninstalls
- **Wrong**: Setting `description` to empty string instead of null → **Right**: Use `description: ''` or omit the key entirely for no description
- **Wrong**: Forgetting `status: true` → **Right**: Always explicitly set status

## See Also

- [Taxonomy System Overview](taxonomy-overview.md)
- [Creating Vocabularies via Config](creating-vocabularies-config.md)
- Reference: `/core/modules/taxonomy/config/schema/taxonomy.schema.yml` (lines 22-52)
