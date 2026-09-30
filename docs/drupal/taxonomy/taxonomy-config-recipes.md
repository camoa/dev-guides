---
description: "Package taxonomy vocabulary config for reuse or deployment via recipes"
tldr: "Package taxonomy vocabulary config into a recipe for reuse or deployment; ship default terms through the recipe's content folder using core's content:export, not a contrib module, unless the recipe route doesn't fit."
drupal_version: "11.x"
---

# Config Export & Recipes

## When to Use

> When packaging taxonomy vocabulary config for reuse, distribution via modules, or deployment via recipes.

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

**Include default terms:**

Terms are content, not config. A recipe ships them in its `content/` folder:

1. **Create the terms on a working site.**
2. **Export them** with core's `content:export` Drush command. This needs Drupal 11.3 or later — recipes import `content/` from 10.3, but the export command lands in 11.3. On earlier versions, export with the contrib Default Content module instead:
   ```bash
   drush content:export taxonomy_term --bundle=VOCAB_ID --dir=recipes/RECIPE_NAME/content
   ```
   The command is core's (`core/lib/Drupal/Core/DefaultContent/Command/ContentExportCommand.php` on 11.4), and is marked experimental. It writes one YAML file per term under `content/taxonomy_term/`.
3. **List the vocabulary's recipe under `recipes:`** in the term recipe, so the vocabulary exists before the terms import.
4. **Apply the recipe.** Core imports `content/` with `Existing::Skip`: a term whose UUID already exists is left as-is, so re-applying the recipe is safe. A child term names its parent by UUID under `_meta.depends`, so the importer creates the parent first.

Use an install hook instead when a module, not a recipe, owns the vocabulary:
```php
function mymodule_install() {
  $terms = ['PHP', 'JavaScript', 'CSS'];
  foreach ($terms as $name) {
    Term::create(['vid' => 'technologies', 'name' => $name])->save();
  }
}
```

Default Content and Content as Configuration are contrib alternatives, not the default — reach for them only when the recipe route above doesn't fit:

1. **Default Content module** — Export terms as JSON
   ```bash
   drush dce taxonomy_term TERM_ID
   ```

2. **Content as Configuration module** — Save terms as config entities

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Export method | One-time manual export | Use UI export |
| Export method | Automated deployment | Use Drush in scripts |
| Recipe vs module | Reusable taxonomy pattern | Create recipe with vocabulary + field configs |
| Recipe vs module | Site-specific taxonomy | Export to sync config, deploy via config management |
| Default terms | Terms are essential for functionality | Ship them in the recipe's `content/` folder; use an install hook only when a module, not a recipe, owns the vocabulary |
| Default terms | Terms are sample data | Skip; let site builders create them |

## Common Mistakes

- Including UUIDs in module config → Causes conflicts on import. Remove uuid keys before committing to module
- Not using `enforced` module dependency → Vocabulary persists after module uninstall. Always add enforced dependency for module-owned config
- Exporting entire config directory for one vocabulary → Bloats repository. Export only necessary files: vocabulary, field storage, field instances
- Forgetting to include field display configs → Vocabulary + field storage aren't enough; widget/formatter configs needed for complete setup
- Trying to export terms as config → Terms are content entities. Ship terms in a recipe's `content/` folder, or create them in an install hook
- Not setting `strict: false` in recipes when optional → Recipe fails if config already exists. Use `strict: false` for optional/reusable configs like shared vocabularies
- Keeping the empty `path` item that `content:export` writes → A term with no alias still exports `path: [{langcode: en, alias: null}]`, because `PathItem::isEmpty()` returns FALSE whenever `langcode` is set, and export always sets it. Importing that item requires the Path module. Remove it when no term has an alias, or add `path` to the recipe's `install:` when terms do
- Leaving out Views → Core's `/core/recipes/tags_taxonomy/recipe.yml` installs `views` beside `taxonomy`, with a comment citing drupal.org issue 3479980: taxonomy has no fallback to display terms without Views. Copy that line and its comment into any recipe that ships a vocabulary
- Committing `config/sync` vocabulary files exported from another database → A vocabulary in `config/sync` carries the UUID of the site it was exported from. If the live vocabulary has a different UUID, `drush config:import` deletes and recreates it, and deleting a vocabulary deletes its terms. Export `config/sync` from the site that will import it, not from a scratch database

## See Also

- ← Previous: [Taxonomy with Entity Reference](entity-reference-taxonomy.md) | Next: [Best Practices & Patterns](best-practices.md) →
- Reference: `/core/recipes/tags_taxonomy/recipe.yml`
- Reference: `/core/recipes/basic_shortcuts/content/` — a core recipe that ships content
- Reference: [Drupal.org Content as Configuration module](https://www.drupal.org/project/content_as_config)
