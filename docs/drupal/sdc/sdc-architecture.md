---
description: How Drupal discovers and loads SDC components using the plugin system
drupal_version: "11.x"
---

# SDC Architecture

## When to Use

> Use this when you need to understand how Drupal discovers and loads components, debug component registration issues, or plan component organization across modules/themes.

## Decision: How SDC Discovery Works

| Aspect | Pattern | Why |
|--------|---------|-----|
| Architecture | Plugin-based component discovery | Component Plugin Manager scans at cache rebuild |
| File requirement | `*.component.yml` matching directory name | Discovery matches files by directory name |
| Component ID | `provider:component-name` format | Namespace prevents collisions between providers |
| Caching | Component definitions cached | Performance optimization for production |

**Discovery Locations (in order of precedence):**
1. Active theme: `themes/{theme_name}/components/`
2. Base themes: `themes/{base_theme}/components/`
3. Modules: `modules/{module_name}/components/`

**Integration Points:**
- **Render System**: `#type => 'component'` render element
- **Asset System**: Automatic library generation per component
- **Theme System**: Component replacement via `replaces` directive (themes only)
- **Template System**: `include()` and `embed` functions

## Pattern

Component ID format:

```
provider:component-name

Examples:
- olivero:teaser
- radix:button
- my_theme:hero-banner
- my_module:user-card
```

## Common Mistakes

- **Wrong**: Expecting nested directories to create namespaces → **Right**: Drupal scans for leaf directories containing `.component.yml`, not nested hierarchies. Use flat structure in `components/` directory.

## See Also

- Reference: `/core/lib/Drupal/Core/Theme/ComponentPluginManager.php` - Discovery implementation
- [Component File Structure](component-file-structure.md)
- [Replacing Templates with SDCs](replacing-templates-with-sdcs.md)
