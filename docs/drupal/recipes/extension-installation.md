---
description: The install key declares modules and themes the recipe requires
drupal_version: "11.x"
---

# Extension Installation

## When to Use

> Use the `install:` key to declare modules and themes that your recipe requires.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Extension already installed, need specific config | Use `config.actions` | Modify installed extension config |
| Extension not available | Ensure extension is in codebase | Recipes don't download code |
| Theme needs module | List module in `install:` | Module provides theme dependency |

## Pattern

List extensions by machine name:

```yaml
install:
  - node
  - image
  - path
  - olivero  # Theme
```

Installation order:
- Modules install first (via ModuleInstaller)
- Themes install second (via ThemeInstaller)
- Dependencies of extensions auto-install
- Already-installed extensions are skipped

Config override during install:
- Extension's `config/install` loaded
- Recipe's `config/` directory overlays extension defaults
- Uses RecipeOverrideConfigStorage to merge

## Common Mistakes

- **Wrong**: Forgetting to install extension that provides config → **Right**: Validation catches config actions, not imports; causes runtime errors
- **Wrong**: Listing themes before modules explicitly → **Right**: Runner handles order but explicit misordering is confusing
- **Wrong**: Expecting recipes to download code → **Right**: Recipes install existing extensions; use Composer for code acquisition
- **Wrong**: Not declaring transitive dependencies → **Right**: Extension dependencies auto-install but documenting helps clarity
- **Wrong**: Installing extensions the recipe doesn't configure → **Right**: Keep `install:` minimal; only list extensions recipe uses

## See Also

- [Recipe Composition & Dependencies](recipe-composition.md)
- [Config Import & Strict Mode](config-import-strict.md)
- Reference: `core/lib/Drupal/Core/Recipe/RecipeRunner.php` (processInstall method)
