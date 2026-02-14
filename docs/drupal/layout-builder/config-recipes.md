---
description: Exporting and deploying Layout Builder configuration
drupal_version: "11.x"
---

# Configuration Export & Recipes

### When to Use

When deploying Layout Builder configuration across environments, creating reusable layout patterns, or managing LB config in version control.

### Steps

1. **Export Layout Builder Config**
   ```bash
   # Export all config
   drush cex

   # LB config stored in entity_view_display
   # Example: config/sync/core.entity_view_display.node.article.default.yml
   ```

2. **Review Exported Config**
   ```yaml
   # core.entity_view_display.node.article.default.yml
   uuid: abc-123
   langcode: en
   status: true
   dependencies:
     config:
       - field.field.node.article.body
       - node.type.article
     module:
       - layout_builder
       - user
   third_party_settings:
     layout_builder:
       enabled: true
       allow_custom: false
       sections:
         - layout_id: layout_twocol_section
           layout_settings:
             label: ''
           components:
             - uuid: component-uuid-1
               region: first
               configuration:
                 id: 'field_block:node:article:body'
                 # ... full block config
               weight: 0
   ```

3. **Create Recipe for Reusable Pattern**
   ```yaml
   # recipes/article_layout/recipe.yml
   name: 'Article Two-Column Layout'
   description: 'Applies two-column layout to article content type'
   type: Content
   recipes:
     - core/recipes/article_with_body
   install:
     - layout_builder
   config:
     import:
       core.entity_view_display.node.article.default: '*'
   ```

4. **Import on Target Environment**
   ```bash
   # Import all config
   drush cim

   # Or apply recipe
   drush recipe recipes/article_layout
   ```

5. **Handle Inline Blocks**
   - Inline blocks stored as content (in block_content entities), not config
   - Default layouts can include inline blocks via serialized data in config
   - Per-entity overrides with inline blocks require content sync (not config-only)

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Planning export | Using defaults only | Clean config export, no content dependencies |
| Planning export | Using overrides with inline blocks | Need content sync (structure_sync, default_content, migrate) |
| Creating recipe | Layout for single bundle | Include entity_view_display config in recipe |
| Creating recipe | Layout for multiple bundles | Include all relevant view displays or use config actions |
| Version control | UUIDs change on re-export | Not an issue — UUIDs in component config, not entity config UUID |
| Multi-environment | Different inline block IDs | Use serialized blocks in defaults, avoid per-entity overrides in recipes |

### Common Mistakes

- **Forgetting dependencies** → LB config depends on fields, entity types, modules. Export dependencies or target import fails
- **Not testing import on fresh site** → Test recipe on clean install to verify all dependencies included
- **Mixing config and content** → Defaults are config (exportable). Overrides are content (harder to deploy). Document which is used
- **Hardcoding UUIDs** → Component UUIDs can be arbitrary. Don't depend on specific UUID values in custom code
- **Ignoring inline block complexity** → Inline blocks in defaults use serialized data (portable). In overrides, they're separate entities (not portable via config)
- **Not using recipes for distribution** → Recipes make LB config reusable across sites. Don't manually copy YAML files
- **Exporting with overrides enabled** → `allow_custom: true` in config affects all environments. Consider per-environment config splits

### See Also

- Section 3: Config Schema (understanding YAML structure)
- Section 7: Inline vs Reusable (portability considerations)
- Section 9: Defaults vs Overrides (config vs content)
- Reference: [Drupal Recipes documentation](https://www.drupal.org/docs/extending-drupal/drupal-recipes)
