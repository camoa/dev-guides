---
description: Package taxonomy vocabulary config for reuse or deployment via recipes
drupal_version: "11.x"
---

# Config Export & Recipes

## When to Use

> Use this guide when packaging taxonomy vocabulary config for reuse, distribution via modules, or deployment via recipes.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| One-time manual export | UI export | Simple, visual |
| Automated deployment | Drush in scripts | Scriptable, repeatable |
| Reusable taxonomy pattern | Recipe with vocabulary + field configs | Packages complete setup |
| Site-specific taxonomy | Export to sync config | Deploy via config management |
| Essential default terms | Install hook or Default Content module | Terms are content, not config |
| Sample data terms | Skip | Let site builders create them |

## Pattern

**Export existing vocabulary config:**

Via UI — Configuration > Synchronize > Export > Single item > Taxonomy vocabulary

Via Drush:
```bash
drush config:get taxonomy.vocabulary.tags
drush config:export taxonomy.vocabulary.tags --destination=/tmp/
```

Clean exported YAML — Remove UUIDs:
```yaml
# Remove this line for module config
# uuid: 12345678-1234-1234-1234-123456789abc
```

**Create recipe for taxonomy setup:**
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

**Include default terms (install hook):**
```php
function mymodule_install() {
  $terms = ['PHP', 'JavaScript', 'CSS'];
  foreach ($terms as $name) {
    Term::create(['vid' => 'technologies', 'name' => $name])->save();
  }
}
```

## Common Mistakes

- **Wrong**: Including UUIDs in module config → **Right**: Remove uuid keys before committing
- **Wrong**: Not using `enforced` module dependency → **Right**: Always add enforced dependency for module-owned config
- **Wrong**: Exporting entire config directory for one vocabulary → **Right**: Export only necessary files
- **Wrong**: Forgetting to include field display configs → **Right**: Widget/formatter configs needed for complete setup
- **Wrong**: Trying to export terms as config → **Right**: Terms are content entities; use Default Content or install hooks
- **Wrong**: Not setting `strict: false` in recipes when optional → **Right**: Recipe fails if config already exists

## See Also

- [Taxonomy with Entity Reference](entity-reference-taxonomy.md)
- [Best Practices & Patterns](best-practices.md)
- Reference: `/core/recipes/tags_taxonomy/recipe.yml`
- Reference: `/core/recipes/article_tags/recipe.yml`
- Reference: [Drupal.org Content as Configuration module](https://www.drupal.org/project/content_as_config)
