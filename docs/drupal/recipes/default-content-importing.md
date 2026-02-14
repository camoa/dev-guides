---
description: Recipes automatically import default content from content directory during application
drupal_version: "11.x"
---

# Default Content - Importing

## When to Use

> Recipes automatically import default content from the `content/` directory during recipe application via RecipeRunner.

## Decision

| At this step | Situation | Resolution |
|--------------|-----------|------------|
| Entity already exists | UUID collision detected | Error by default; use Skip in recipe application context |
| Referenced entity missing | Dependency not in content dir | Validation fails; export dependencies or create manually |
| Language not installed | Default langcode unavailable | Importer switches to installed translation or site default |
| File missing | File entity references non-existent file | Warning logged; entity imports without file |

## Pattern

Automatic import (happens during recipe application):

```php
// Happens automatically when applying recipe
RecipeRunner::processRecipe($recipe);
```

Manual import (use Importer service):

```php
$importer = \Drupal::service(Importer::class);
$content = new Finder('/path/to/recipe/content');
$importer->importContent($content, Existing::Skip);
```

Dependency resolution:
- Finder analyzes entity references in `_meta.depends`
- Entities sorted so dependencies import first
- References by UUID resolve to entity IDs after import

Existing entity handling (Existing enum):

```php
Existing::Error  // Throw exception if entity exists (default)
Existing::Skip   // Skip existing entities silently
```

AdminAccountSwitcher:
- Import runs as admin user
- Bypasses access control during import
- Switches back to original user after import

## Common Mistakes

- **Wrong**: Not understanding Existing::Skip default in recipes → **Right**: Recipes use Skip to be re-runnable; manual imports default to Error
- **Wrong**: Forgetting file directory structure → **Right**: Files must be alongside YAML in same entity type subdirectory
- **Wrong**: Assuming content updates → **Right**: Existing entities skip; no update mechanism; delete and re-import to update
- **Wrong**: Not handling validation failures → **Right**: InvalidEntityException thrown if entity doesn't validate; fix YAML or entity definition
- **Wrong**: Ignoring import order → **Right**: Finder handles order but manual YAML edits can create circular dependencies
- **Wrong**: Reapplying recipes expecting idempotent content → **Right**: Content with same UUID is skipped (Existing::Skip), but if UUIDs were changed or removed, duplicate content is created

## See Also

- [Default Content - Exporting](default-content-exporting.md)
- [Composer Integration & Publishing](composer-integration.md)
- Reference: `core/lib/Drupal/Core/DefaultContent/Importer.php`
