---
description: Standard Migrate API rebuild vs wizard vs retrofit for D7 to D11 migrations
drupal_version: "11.x"
---

# Choose Migration Approach

## When to Use

Drupal 7 to 11 is a complete rebuild, not an upgrade. No 1:1 mapping exists for core modules, themes, content types, or custom code. Choose your approach based on development resources, timeline constraints, and code preservation needs.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Clean codebase, zero technical debt | Standard Migrate API rebuild | Modern architecture, optimized for Symfony 6/PHP 8.2+, API-first design |
| Quick migration, limited PHP expertise | Migrate Wizard (UI-driven) | No programming required, visual interface, selective migration by node ID/date |
| Preserve D7 custom modules unchanged | Retrofit Drupal | Runs D7 code in D11 without rewrites, temporary bridge solution |
| Complex content with AI-assisted cleanup | AI Migration module | Automated content quality improvements, unstructured data handling |

## Pattern

**Standard Migrate API approach (most common):**

```yaml
# config/install/migrate_plus.migration.d7_node_article.yml
id: d7_node_article
label: D7 Article nodes
source:
  plugin: d7_node
  node_type: article
process:
  nid: nid
  type:
    plugin: default_value
    default_value: article
  title: title
  body/value: body
  body/format:
    plugin: default_value
    default_value: basic_html
destination:
  plugin: entity:node
migration_dependencies:
  required:
    - d7_user
```

**Reference**: `/core/modules/migrate_drupal/src/Plugin/migrate/source/d7/Node.php`

## Common Mistakes

- **Wrong**: Starting migration without full D7 site assessment → **Right**: Run inventory first (content types, custom modules, integrations)
- **Wrong**: Treating as simple upgrade instead of rebuild → **Right**: Budget 3-12 months, plan for custom code rewrites
- **Wrong**: Using Retrofit as permanent solution → **Right**: Use as temporary bridge, plan modernization sprints
- **Wrong**: Skipping test migrations with sample data → **Right**: Always test with small batches before full migration

## See Also

- [Assess migration scope](assess-migration-scope.md) for inventory and planning
- [Create migration definitions](create-migration-definitions.md) for YAML patterns
- Reference: [Drupal Migrate API overview](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-api-overview)
- Reference: [Migrate Wizard module](https://www.drupal.org/project/migrate_wizard)
- Reference: [Retrofit Drupal](https://retrofit-drupal.com/)
