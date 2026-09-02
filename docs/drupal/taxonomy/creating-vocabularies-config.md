---
description: "Create vocabularies for deployment via config management or module installation"
tldr: "Use config-first approach for vocabularies to ensure consistent structure across environments. Create YAML files for module installation or config sync."
drupal_version: "11.x"
---

# Creating Vocabularies via Config

## When to Use

> Use this workflow when creating vocabularies for deployment via config management or module installation.

Config-first approach ensures consistent vocabulary structure across environments.

## Steps

1. **Create YAML file** — Place in `MODULE_NAME/config/install/taxonomy.vocabulary.VOCAB_ID.yml`
   ```yaml
   langcode: en
   status: true
   name: Topics
   vid: topics
   description: 'Article topics'
   weight: 0
   new_revision: false
   ```

2. **Add dependencies** — Enforce module dependency if vocabulary is module-specific
   ```yaml
   dependencies:
     enforced:
       module:
         - my_content_module
   ```

3. **Install module** — On module enable, vocabulary imports automatically from `config/install/`
   ```bash
   drush en my_content_module
   ```

4. **Or import config directly** — For config changes after installation
   ```bash
   drush config:import --partial --source=modules/custom/my_module/config/install/
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| File location | Vocabulary ships with module | `config/install/` (imports on enable) |
| File location | Vocabulary is site-specific config | Export to sync directory, import via config management |
| Dependencies | Vocabulary is essential to module functionality | Add enforced module dependency |
| Recipe pattern | Creating reusable taxonomy setup | Use recipe.yml with config import (see Recipes section) |

## Common Mistakes

- Placing config in `config/optional/` when it should be required → Use `install/` for required config, `optional/` only when dependencies might not exist
- Not enforcing module dependencies → Vocabulary persists after module uninstall, becomes orphaned config. Always add enforced dependency for module-owned vocabularies
- Using `drush cex` instead of hand-crafting config → Exports include UUIDs and unnecessary metadata. For module config, write YAML manually following schema
- Forgetting to clear cache after config import → Drupal caches entity definitions. Run `drush cr` after importing vocabulary config
- Mixing content (terms) with config (vocabulary) → Vocabularies are config, terms are content. Export vocabularies as YAML, manage terms separately (or use content_as_config contrib)

## See Also

- ← Previous: [Vocabulary Configuration Schema](vocabulary-config-schema.md) | Next: [Term Reference Field Configuration](term-reference-config.md) →
- Reference: `/core/recipes/tags_taxonomy/config/taxonomy.vocabulary.tags.yml`
- Reference: [Drupal.org Configuration Management](https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration)
