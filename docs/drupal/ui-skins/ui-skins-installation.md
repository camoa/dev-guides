---
description: Installing UI Skins on Drupal 11.4+ or 12 — single module, no submodules, no external dependencies.
tldr: Install UI Skins with composer and drush en. Single module only — no submodules exist. Requires Drupal ^11.4 || ^12 and PHP 8.3+. Once enabled, it adds CSS variable and theme controls to every theme's settings form.
drupal_version: "11.x"
---

# UI Skins Installation

## When to Use

> Use this guide when installing UI Skins on a new site or confirming compatibility requirements.

## Decision

| Property | Value |
|---|---|
| Drupal core | `^11.4 \|\| ^12` |
| PHP | 8.3+ |
| External | None (no Composer dependencies beyond core) |

## Pattern

```bash
composer require drupal/ui_skins
drush en ui_skins
```

UI Skins has no submodule integrations — it's a single module. Once enabled, it injects new sections into every theme's settings form (`/admin/appearance/settings/{theme}`).

## Common Mistakes

- **Looking for a submodule like `ui_skins_layout_builder`** → Doesn't exist. UI Skins is theme-level only

## See Also

- [UI Skins Overview](ui-skins-overview.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- Reference: `drupal/ui_skins` on drupal.org
