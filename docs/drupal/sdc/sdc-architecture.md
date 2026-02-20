---
description: How Drupal discovers and loads SDC components via plugin system
drupal_version: "11.x"
---

# SDC Architecture

## When to Use

> Use this when you need to understand how Drupal discovers and loads components, debug component registration issues, or plan component organization across modules/themes.

## Decision

| Situation | How SDC Discovery Works | Why |
|-----------|------------------------|-----|
| Component discovery | Plugin Manager scans `components/` directories at cache rebuild | Components auto-register without manual configuration |
| Component ID format | `provider:component-name` (e.g., `olivero:teaser`) | Namespaces components by module/theme to avoid collisions |
| Discovery precedence | 1. Active theme, 2. Base themes, 3. Modules | Theme components override module components with same name |
| Integration | Render system, asset system, theme system, template system | Components work seamlessly with existing Drupal systems |

## Pattern

```
Component ID format:
provider:component-name

Examples:
- olivero:teaser
- radix:button
- my_theme:hero-banner
- my_module:user-card

Discovery locations (in precedence order):
1. themes/{theme_name}/components/
2. themes/{base_theme}/components/
3. modules/{module_name}/components/
```

## Common Mistakes

- **Wrong**: Expecting nested directories to create namespaces → **Right**: Use flat structure in `components/` directory (Drupal scans for leaf directories containing `.component.yml`)
- **Wrong**: Manual component registration → **Right**: Let Plugin Manager auto-discover (requires cache rebuild to detect new components)

## See Also

- Reference: `/core/lib/Drupal/Core/Theme/ComponentPluginManager.php` - Discovery implementation
- [Component File Structure](component-file-structure.md)
- [Replacing Templates with SDCs](replacing-templates-with-sdcs.md)
