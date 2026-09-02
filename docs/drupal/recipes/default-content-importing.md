---
description: Recipes automatically import default content from content directory during application
tldr: "Recipes automatically import default content from the `content/` directory during recipe application via RecipeRunner."
drupal_version: "11.x"
---

# Default Content - Importing

## When to Use

> Recipes automatically import default content from the `content/` directory during recipe application via RecipeRunner.

Recipes automatically import default content from `content/` directory during application.

## Steps: Automatic Import, Manual Import and Dependency Resolution

1. **Automatic import** — RecipeRunner calls Importer during processContent
   ```php
   // Happens automatically when applying recipe
   RecipeRunner::processRecipe($recipe);
   ```

2. **Manual import** — Use Importer service directly
   ```php
   $importer = \Drupal::service(Importer::class);
   $content = new Finder('/path/to/recipe/content');
   $importer->importContent($content, Existing::Skip);
   ```

3. **Dependency resolution** — Finder sorts entities by dependency graph
   - Graph analysis finds entity references in `_meta.depends`
   - Entities sorted so dependencies import first
   - References by UUID resolve to entity IDs after import

4. **Existing entity handling** — Two strategies via Existing enum
   ```php
   Existing::Error  // Throw exception if entity exists (default)
   Existing::Skip   // Skip existing entities silently
   ```

5. **AdminAccountSwitcher** — Import runs as admin user
   - Bypasses access control during import
   - Ensures all entities can be created
   - Switches back to original user after import

## Decision Points: Existing Entities, Missing References and Languages

| At this step... | If... | Then... |
|---|---|---|
| Entity already exists | UUID collision detected | Error by default; use Skip in recipe application context |
| Referenced entity missing | Dependency not in content dir | Validation fails; export dependencies or create manually |
| Language not installed | Default langcode unavailable | Importer switches to installed translation or site default |
| File missing | File entity references non-existent file | Warning logged; entity imports without file |

## Common Mistakes

- Not understanding Existing::Skip default in recipes → Recipes use Skip to be re-runnable; manual imports default to Error
- Forgetting file directory structure → Files must be alongside YAML in same entity type subdirectory
- Assuming content updates → Existing entities skip; no update mechanism; delete and re-import to update
- Not handling validation failures → InvalidEntityException thrown if entity doesn't validate; fix YAML or entity definition
- Ignoring import order → Finder handles order but manual YAML edits can create circular dependencies
- Reapplying recipes expecting idempotent content → Content with same UUID is skipped (Existing::Skip), but if UUIDs were changed or removed, duplicate content is created; default content has no deduplication by title or path

## See Also

- Previous: ← [Default Content - Exporting](default-content-exporting.md)
- Next: [Composer Integration & Publishing](composer-integration.md) →
- Reference: `core/lib/Drupal/Core/DefaultContent/Importer.php`
