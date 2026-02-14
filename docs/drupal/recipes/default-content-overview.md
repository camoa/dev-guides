---
description: Default content ships demo or starter content with recipes as YAML files for initial site setup
drupal_version: "11.x"
---

# Default Content - Overview

## When to Use

> Use default content when you need demo or starter content bundled with your recipe. For ongoing content staging, use Workspaces or Migrate API.

## Decision

| Need | Use | Why |
|------|-----|-----|
| Demo/starter content bundled with recipe | Default Content | Ships with recipe, dependency-sorted, UUIDs stable |
| One-time data migration | Migrate API | Complex transformations, external sources, replayable |
| Config vs content sync | Config Management | Config entities, not content entities |
| Large datasets | Migrate API or custom import | Default content loads all at once; memory-intensive |

## Pattern

Default content directory structure:

```
recipes/my_recipe/
  recipe.yml
  content/
    node/
      uuid1.yml
      uuid2.yml
    media/
      uuid3.yml
    file/
      image1.png
      image2.jpg
```

Supported entity types: `node`, `taxonomy_term`, `file`, `media`, `menu_link_content`, `block_content`, `shortcut`. Not config entities.

**Use for bootstrapping** — default content is designed for initial site setup (demo content, starter pages, initial taxonomy terms). It is not a content deployment pipeline — no updates, no sync, no rollback for content.

## Common Mistakes

- **Wrong**: Exporting config entities → **Right**: Default content is for content entities only; config goes in `config/`
- **Wrong**: Not sorting dependencies → **Right**: Finder handles this automatically but manual YAML edits can break references
- **Wrong**: Using serial IDs → **Right**: Export references entities by UUID; serial IDs won't match across installs
- **Wrong**: Forgetting files → **Right**: Media/file entities need physical files in `content/` directory alongside YAML
- **Wrong**: Assuming content updates → **Right**: Default content imports once; existing entities (by UUID) are skipped or error based on Existing enum

## See Also

- [Default Content - Exporting](default-content-exporting.md)
- Reference: `core/lib/Drupal/Core/DefaultContent/Finder.php`
- Reference: https://project.pages.drupalcode.org/distributions_recipes/default_content.html
- Reference: https://kanopi.com/blog/default-content-in-drupal/
