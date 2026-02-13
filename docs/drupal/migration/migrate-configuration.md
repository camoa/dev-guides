---
description: Migrate content types, views, and configuration from D7 to D11
drupal_version: "11.x"
---

# Migrate Configuration

## When to Use

Configuration migration transfers content types, field definitions, views, image styles from D7 to D11. Unlike content, configuration often requires manual recreation due to structural changes. Use Drupal Recipes for standardized configuration deployment.

## Decision

| Configuration type | Strategy | Reason |
|---|---|---|
| Content types with same structure | Migration or manual recreation | D11 field UI improved, manual often faster |
| Views (simple) | Migration possible | Basic views migrate reasonably well |
| Views (complex relationships) | Manual recreation | Complex views need D11 query optimization |
| Image styles | Manual recreation | D11 has responsive image styles |
| Blocks | Manual recreation | D11 block system completely different |
| Menus | Migration | Menu links migrate well |

## Pattern

**Content type migration (rarely automated):**

```yaml
# Most teams manually recreate via UI or use Drupal Recipes
# Example recipe for standardized config:
recipes/content_types/article/recipe.yml:
  name: Article content type
  type: content_type
  install:
    - field
    - node
    - text
  config:
    import:
      node_type_article: config/install/node.type.article.yml
      field_node_article_body: config/install/field.storage.node.body.yml
      field_instance_node_article_body: config/install/field.field.node.article.body.yml
```

**Manual recreation preferred:**
1. Document D7 configuration (screenshots, exports)
2. Recreate in D11 UI using modern equivalents
3. Export configuration to sync
4. Version control in config/sync/

**Reference**: `/core/modules/migrate_drupal/` for configuration migration plugins

## Common Mistakes

- **Wrong**: Attempting to migrate complex views → **Right**: Manual recreation often faster, better D11 optimization
- **Wrong**: Not using configuration management → **Right**: Export config to track changes, enable deployment
- **Wrong**: Migrating deprecated configuration → **Right**: Use D11 equivalents (responsive images vs fixed styles)
- **Wrong**: Skipping documentation → **Right**: Document D7 config decisions before migration

## See Also

- Reference: [Configuration management](https://www.drupal.org/docs/configuration-management)
- Reference: [Drupal Recipes](https://www.drupal.org/docs/extending-drupal/drupal-recipes)
