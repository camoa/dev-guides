---
description: Export existing content entities to YAML for bundling with recipes
drupal_version: "11.x"
---

# Default Content - Exporting

## When to Use

> Use content export when you need to bundle existing content entities with a recipe for demo or starter content.

## Decision

| At this step | Choose | Why |
|--------------|--------|-----|
| Content has references | Use `--dependencies` flag | Exports full dependency tree |
| Content has files | Files automatically copy | Media or file fields include physical files |
| Content has translations | All translations export | In same YAML under `translations:` |
| Serial IDs matter (users 0/1) | UID 0/1 export as IDs | Others as UUIDs |

## Pattern

Export single entity via Drush:

```bash
drush content:export node 123 recipes/my_recipe/content
```

Export with dependencies:

```bash
drush content:export node 123 recipes/my_recipe/content --dependencies
```

Programmatic export:

```php
$exporter = \Drupal::service(Exporter::class);
$entity = Node::load(123);
$result = $exporter->exportWithDependencies($entity, '/path/to/recipe/content');
```

Export result YAML structure:

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

File attachments (physical files copied):

```
content/
  media/
    uuid.yml
    photo.jpg  # Physical file copied
```

## Common Mistakes

- **Wrong**: Exporting without dependencies → **Right**: Referenced entities won't exist on import; causes validation failures
- **Wrong**: Not committing physical files → **Right**: Files in `content/` directory must be in version control
- **Wrong**: Editing YAML manually without understanding structure → **Right**: Breaking `_meta.depends` causes import errors
- **Wrong**: Exporting user passwords → **Right**: Passwords export as pre-hashed; secure but can't derive plaintext
- **Wrong**: Forgetting to export dependency tree → **Right**: Use `--dependencies` or manually track entity references
- **Wrong**: Expecting bundle filtering → **Right**: No way to export all nodes of a type; must export individually by entity ID

## See Also

- [Default Content - Overview](default-content-overview.md)
- [Default Content - Importing](default-content-importing.md)
- Reference: `core/lib/Drupal/Core/DefaultContent/Exporter.php`
- Reference: https://www.drupal.org/node/3533854 (content:export command)
