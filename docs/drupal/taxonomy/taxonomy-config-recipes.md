---
description: "Package taxonomy vocabulary config for reuse or deployment via recipes"
tldr: "Use this guide when packaging taxonomy vocabulary config for reuse, distribution via modules, or deployment via recipes."
drupal_version: "11.x"
---

# Config Export & Recipes

## When to Use

> Use this guide when packaging taxonomy vocabulary config for reuse, distribution via modules, or deployment via recipes.

## Steps

**Export existing vocabulary config:**

1. **Via UI** — Configuration > Synchronize > Export > Single item > Taxonomy vocabulary
   - Select vocabulary, copy YAML

2. **Via Drush** — Export specific config
   ```bash
   drush config:get taxonomy.vocabulary.tags
   drush config:export taxonomy.vocabulary.tags --destination=/tmp/
   ```

3. **Clean exported YAML** — Remove UUIDs, dependencies if needed
   ```yaml
   # Remove this line for module config
   uuid: 12345678-1234-1234-1234-123456789abc
   ```

**Create recipe for taxonomy setup:**

Recipe pattern for vocabulary + field + display config:

```yaml
# recipe.yml
name: 'Article Tags'
description: 'Provides tags on article content'
type: 'Content field'
recipes:
  - article_content_type
  - tags_taxonomy
install:
  - views
config:
  strict:
    - field.storage.node.field_tags
  import:
    taxonomy:
      - taxonomy.vocabulary.tags
      - views.view.taxonomy_term
  actions:
    core.entity_form_display.node.article.default:
      setComponent:
        name: field_tags
        options:
          type: entity_reference_autocomplete_tags
          weight: 3
          settings:
            match_operator: CONTAINS
            size: 60
    core.entity_view_display.node.article.default:
      setComponent:
        name: field_tags
        options:
          type: entity_reference_label
          settings:
            link: true
          weight: 10
```

Reference: `/core/recipes/article_tags/recipe.yml`

**Include default terms (requires contrib):**

Terms are content, not config. Options:

1. **Default Content module** — Export terms as JSON
   ```bash
   drush dce taxonomy_term TERM_ID
   ```

2. **Content as Configuration module** — Save terms as config entities

3. **Install hook** — Create terms programmatically
   ```php
   function mymodule_install() {
     $terms = ['PHP', 'JavaScript', 'CSS'];
     foreach ($terms as $name) {
       Term::create(['vid' => 'technologies', 'name' => $name])->save();
     }
   }
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Export method | One-time manual export | Use UI export |
| Export method | Automated deployment | Use Drush in scripts |
| Recipe vs module | Reusable taxonomy pattern | Create recipe with vocabulary + field configs |
| Recipe vs module | Site-specific taxonomy | Export to sync config, deploy via config management |
| Default terms | Terms are essential for functionality | Use install hook or Default Content module |
| Default terms | Terms are sample data | Skip; let site builders create them |

## Common Mistakes

- Including UUIDs in module config → Causes conflicts on import. Remove uuid keys before committing to module
- Not using `enforced` module dependency → Vocabulary persists after module uninstall. Always add enforced dependency for module-owned config
- Exporting entire config directory for one vocabulary → Bloats repository. Export only necessary files: vocabulary, field storage, field instances
- Forgetting to include field display configs → Vocabulary + field storage aren't enough; widget/formatter configs needed for complete setup
- Trying to export terms as config → Terms are content entities. Use Default Content, install hooks, or content_as_config contrib module
- Not setting `strict: false` in recipes when optional → Recipe fails if config already exists. Use `strict: false` for optional/reusable configs like shared vocabularies

## See Also

- ← Previous: [Taxonomy with Entity Reference](entity-reference-taxonomy.md) | Next: [Best Practices & Patterns](best-practices.md) →
- Reference: `/core/recipes/tags_taxonomy/recipe.yml`
- Reference: [Drupal.org Content as Configuration module](https://www.drupal.org/project/content_as_config)
