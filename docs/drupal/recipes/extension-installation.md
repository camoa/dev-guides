---
description: The install key declares modules and themes the recipe requires
tldr: "Use the `install:` key to declare modules and themes that your recipe requires."
drupal_version: "11.x"
---

# Extension Installation

## When to Use

> Use the `install:` key to declare modules and themes that your recipe requires.

The `install:` key declares modules and themes the recipe requires.

## Steps: Declare Extensions and Understand Install Order

1. **List extensions** — Modules and themes by machine name
   ```yaml
   install:
     - node
     - image
     - path
     - olivero  # Theme
   ```

2. **Installation order** — RecipeRunner processes in sequence
   - Modules install first (via ModuleInstaller)
   - Themes install second (via ThemeInstaller)
   - Dependencies of extensions auto-install
   - Already-installed extensions are skipped

3. **Config override during install** — Recipe config overrides extension config
   - Extension's `config/install` loaded
   - Recipe's `config/` directory overlays extension defaults
   - Uses RecipeOverrideConfigStorage to merge

## Decision Points: Extension Availability and Theme Dependencies

| At this step... | If... | Then... |
|---|---|---|
| Extension already installed | Recipe needs specific config | Use `config.actions` to modify installed extension config |
| Extension not available | Extension is custom or contrib | Ensure extension is in codebase; recipes don't download code |
| Theme needs module | Module provides theme dependency | List module in `install:` before or with theme |

## Common Mistakes

- Forgetting to install extension that provides config → Validation catches config actions, not imports; causes runtime errors
- Listing themes before modules explicitly → Runner handles order but explicit misordering is confusing
- Expecting recipes to download code → Recipes install existing extensions; use Composer for code acquisition
- Not declaring transitive dependencies → Extension dependencies auto-install but documenting helps clarity
- Installing extensions the recipe doesn't configure → Keep `install:` minimal; only list extensions recipe uses

## See Also

- Previous: ← [Recipe Composition & Dependencies](recipe-composition.md)
- Next: [Config Import & Strict Mode](config-import-strict.md) →
- Reference: `core/lib/Drupal/Core/Recipe/RecipeRunner.php` (processInstall method)
