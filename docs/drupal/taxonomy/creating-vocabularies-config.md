---
description: Create vocabularies for deployment via config management or module installation
drupal_version: "11.x"
---

# Creating Vocabularies via Config

## When to Use

> Use config-first approach for vocabularies to ensure consistent structure across environments. Create YAML files for module installation or config sync.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Vocabulary ships with module | `config/install/` directory | Imports on module enable |
| Vocabulary is site-specific config | Export to sync directory | Import via config management |
| Vocabulary is essential to module functionality | Add enforced module dependency | Ensures cleanup on module uninstall |
| Creating reusable taxonomy setup | Use recipe.yml with config import | Packages vocabulary + field + display configs |

## Pattern

**Create YAML file** — Place in `MODULE_NAME/config/install/taxonomy.vocabulary.VOCAB_ID.yml`:
```yaml
langcode: en
status: true
dependencies:
  enforced:
    module:
      - my_content_module
name: Topics
vid: topics
description: 'Article topics'
weight: 0
new_revision: false
```

**Install module** — Vocabulary imports automatically:
```bash
drush en my_content_module
```

**Or import config directly** — For config changes after installation:
```bash
drush config:import --partial --source=modules/custom/my_module/config/install/
```

## Common Mistakes

- **Wrong**: Placing config in `config/optional/` when it should be required → **Right**: Use `install/` for required config, `optional/` only when dependencies might not exist
- **Wrong**: Not enforcing module dependencies → **Right**: Always add enforced dependency for module-owned vocabularies
- **Wrong**: Using `drush cex` instead of hand-crafting config → **Right**: For module config, write YAML manually following schema
- **Wrong**: Forgetting to clear cache after config import → **Right**: Run `drush cr` after importing vocabulary config
- **Wrong**: Mixing content (terms) with config (vocabulary) → **Right**: Vocabularies are config, terms are content. Export vocabularies as YAML, manage terms separately

## See Also

- [Vocabulary Configuration Schema](vocabulary-config-schema.md)
- [Term Reference Field Configuration](term-reference-config.md)
- Reference: `/core/recipes/tags_taxonomy/config/taxonomy.vocabulary.tags.yml`
- Reference: [Drupal.org Configuration Management](https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration)
