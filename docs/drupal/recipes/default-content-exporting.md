---
description: Export existing content entities to YAML for bundling with recipes
tldr: "Use content export when you need to bundle existing content entities with a recipe for demo or starter content."
drupal_version: "11.x"
---

# Default Content - Exporting

## When to Use

> Use content export when you need to bundle existing content entities with a recipe for demo or starter content.

Export existing content entities to YAML for bundling with recipes.

## Steps: Export Entities, Dependencies and Files

1. **Export single entity via Drush** — Export entity by ID
   ```bash
   drush content:export node 123 recipes/my_recipe/content
   ```

2. **Export with dependencies** — Export entity and all referenced entities
   ```bash
   drush content:export node 123 recipes/my_recipe/content --dependencies
   ```

3. **Programmatic export** — Use Exporter service
   ```php
   $exporter = \Drupal::service(Exporter::class);
   $entity = Node::load(123);
   $result = $exporter->exportWithDependencies($entity, '/path/to/recipe/content');
   ```

4. **Export result** — YAML file with metadata and field values
   ```yaml
   _meta:
     entity_type: node
     uuid: a1b2c3d4-5678-90ab-cdef-1234567890ab
     bundle: article
     default_langcode: en
     depends:
       uuid-of-referenced-user: user
       uuid-of-referenced-media: media
   default:
     title:
       - value: 'Article Title'
     body:
       - value: 'Article body text...'
         format: basic_html
   ```

5. **File attachments** — Media/file entities copy physical files
   ```
   content/
     media/
       uuid.yml
       photo.jpg  # Physical file copied
   ```

## Decision Points: References, Files, Translations and Serial IDs

| At this step... | If... | Then... |
|---|---|---|
| Content has references | Referenced entities matter | Use `--dependencies` flag to export full tree |
| Content has files | Media or file fields exist | Files automatically copy to content directory |
| Content has translations | Multi-language content | All translations export in same YAML under `translations:` |
| Serial IDs matter | Referencing users 0/1 | UID 0/1 export as IDs; others as UUIDs |

## Common Mistakes

- Exporting without dependencies → Referenced entities won't exist on import; causes validation failures
- Not committing physical files → Files in `content/` directory must be in version control
- Editing YAML manually without understanding structure → Breaking `_meta.depends` causes import errors
- Exporting user passwords → Passwords export as pre-hashed; secure but can't derive plaintext
- Forgetting to export dependency tree → Use `--dependencies` or manually track entity references
- Expecting bundle filtering → No way to export all nodes of a type (e.g., all articles); must export individually by entity ID

## See Also

- Previous: ← [Default Content - Overview](default-content-overview.md)
- Next: [Default Content - Importing](default-content-importing.md) →
- Reference: `core/lib/Drupal/Core/DefaultContent/Exporter.php`
- Reference: https://www.drupal.org/node/3533854 (content:export command)
