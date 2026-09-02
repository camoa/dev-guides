---
description: Default content ships demo or starter content with recipes as YAML files for initial site setup
tldr: "Use default content when you need demo or starter content bundled with your recipe. For ongoing content staging, use Workspaces or Migrate API."
drupal_version: "11.x"
---

# Default Content - Overview

## When to Use

> Use default content when you need demo or starter content bundled with your recipe. For ongoing content staging, use Workspaces or Migrate API.

Default content (demo content, starter content) ships with recipes as YAML files. Understand when to use default content vs other approaches.

## Decision: Default Content vs Migrate vs Config Management

| If you need... | Use... | Why |
|---|---|---|
| Demo/starter content bundled with recipe | Default Content | Ships with recipe, dependency-sorted, UUIDs stable |
| One-time data migration | Migrate API | Complex transformations, external sources, replayable |
| Config vs content sync | Config Management | Config entities, not content entities |
| Large datasets | Migrate API or custom import | Default content loads all at once; memory-intensive |

## Pattern: Directory Structure and Supported Entity Types

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

Supported entity types: `node`, `taxonomy_term`, `file`, `media`, `menu_link_content`, `block_content`, `shortcut`. Not config entities. Other content entity types may work but these seven are the tested/documented set.

**Use for bootstrapping** — default content is designed for initial site setup (demo content, starter pages, initial taxonomy terms). It is not a content deployment pipeline — no updates, no sync, no rollback for content. For ongoing content staging, use Workspaces or Migrate API.

Reference: `core/lib/Drupal/Core/DefaultContent/Finder.php`

## Common Mistakes

- Exporting config entities → Default content is for content entities only; config goes in `config/`
- Not sorting dependencies → Finder handles this automatically but manual YAML edits can break references
- Using serial IDs → Export references entities by UUID; serial IDs won't match across installs
- Forgetting files → Media/file entities need physical files in `content/` directory alongside YAML
- Assuming content updates → Default content imports once; existing entities (by UUID) are skipped or error based on Existing enum

## See Also

- Next: [Default Content - Exporting](default-content-exporting.md) →
- Reference: https://project.pages.drupalcode.org/distributions_recipes/default_content.html
- Reference: https://kanopi.com/blog/default-content-in-drupal/
