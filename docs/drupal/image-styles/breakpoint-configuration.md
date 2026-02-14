---
description: Define breakpoints in your theme
drupal_version: "11.x"
---

# Breakpoint Configuration

## When to Use

> Use this when defining breakpoints in your theme or module for responsive image style mappings.

## Pattern

1. **Create breakpoint definition file** at `{theme_or_module_name}.breakpoints.yml`

   ```yaml
   # olivero.breakpoints.yml
   olivero.sm:
     label: Small
     mediaQuery: 'all and (min-width: 500px)'
     weight: 0
     multipliers:
       - 1x
   olivero.md:
     label: Medium
     mediaQuery: 'all and (min-width: 700px)'
     weight: 1
     multipliers:
       - 1x
   olivero.lg:
     label: Large
     mediaQuery: 'all and (min-width: 1000px)'
     weight: 2
     multipliers:
       - 1x
       - 2x
   ```

2. **Clear cache**

   ```bash
   drush cr
   ```

3. **Verify**

   ```bash
   drush php-eval "print_r(\Drupal::service('breakpoint.manager')->getGroups());"
   ```

## Schema

| Property | Type | Required | Description |
|---|---|---|---|
| `{group}.{id}` | mapping | Yes | Key is `{extension_name}.{breakpoint_id}` |
| `label` | string | Yes | Human-readable name for admin UI |
| `mediaQuery` | string | Yes | CSS media query (can be empty for viewport_sizing) |
| `weight` | integer | Yes | Controls order (lower = higher priority in sorting) |
| `multipliers` | sequence | Yes | List of pixel densities: `['1x']`, `['1x', '2x']`, etc. |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Standard responsive images | min-width media queries with 1x multiplier | Mobile-first, browser picks best match |
| Retina support | Add 2x multiplier to breakpoints | Provides high-DPI derivatives |
| Sizes attribute (resolution switching) | Empty mediaQuery with viewport_sizing breakpoint | Triggers sizes-based srcset generation |
| Art direction (different crops) | Multiple breakpoints with distinct image styles | Full control over which image at which viewport |

## Common Mistakes

- **Wrong**: Using max-width instead of min-width → **Right**: Use min-width (desktop-first approach, harder to maintain, conflicts with mobile-first CSS)
- **Wrong**: Breakpoints don't match CSS breakpoints → **Right**: Align with theme CSS (images switch at different points than layout, jarring UX)
- **Wrong**: Missing 1x multiplier → **Right**: Always include 1x (no images generated for standard DPI screens)
- **Wrong**: Too many breakpoints → **Right**: Use 3-5 breakpoints maximum (excessive derivatives, storage bloat, marginal UX gains)
- **Wrong**: Wrong weight ordering → **Right**: Set weights in ascending order (breakpoints applied in unexpected order, wrong image selected)

## See Also

- [Responsive Image Style Config](responsive-image-config.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/themes/olivero/olivero.breakpoints.yml
- Reference: core/lib/Drupal/Core/Breakpoint/BreakpointManager.php
