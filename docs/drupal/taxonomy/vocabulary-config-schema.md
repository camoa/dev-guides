---
description: "Complete schema for taxonomy.vocabulary.*.yml config files"
tldr: "Use this schema when creating or modifying vocabulary YAML config files. These are the complete properties for `taxonomy.vocabulary.*.yml`."
drupal_version: "11.x"
---

# Vocabulary Configuration Schema

## When to Use

> Use this schema when creating or modifying vocabulary YAML config files.

This is the complete schema for `taxonomy.vocabulary.*.yml`.

## Config Properties

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `langcode` | string | Yes | — | Language code (e.g., `en`) |
| `status` | boolean | Yes | — | `true` = enabled, `false` = disabled |
| `dependencies` | mapping | No | `{}` | Config dependencies (modules, config entities) |
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

Reference: `/core/modules/taxonomy/config/schema/taxonomy.schema.yml`

## Common Mistakes

- Exceeding 32-character limit on `vid` → Validation error on config import. Keep machine names short and descriptive
- Using special characters in `vid` → Must follow machine name rules: lowercase, numbers, underscores only. No spaces, hyphens, or uppercase
- Omitting `dependencies` when needed → If vocabulary is defined by a custom module, add enforced module dependency so it deletes when module uninstalls
- Setting `description` to empty string instead of null → Schema allows null; use `description: ''` or omit the key entirely for no description
- Forgetting `status: true` → Vocabulary won't be active. Always explicitly set status

## See Also

- ← Previous: [Taxonomy System Overview](taxonomy-overview.md) | Next: [Creating Vocabularies via Config](creating-vocabularies-config.md) →
- Reference: `/core/modules/taxonomy/config/schema/taxonomy.schema.yml` (lines 22-52)
