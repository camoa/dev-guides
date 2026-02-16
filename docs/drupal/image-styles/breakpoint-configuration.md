---
description: Define breakpoints in theme/module YAML files with media queries, weights, and multipliers for responsive image mappings
---

# Breakpoint Configuration

## When to Use

> Use this when you need to define breakpoints in your theme or module for responsive image style mappings.

## Steps

### 1. Create breakpoint definition file

At `{theme_or_module_name}.breakpoints.yml` in theme/module root

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

### 2. Clear cache to register breakpoints

```bash
drush cr
```

### 3. Verify breakpoints registered

```bash
# List all breakpoint groups
drush config:get breakpoint.breakpoint.*

# Check programmatically
drush php-eval "print_r(\Drupal::service('breakpoint.manager')->getGroups());"
```

## Breakpoint Schema

| Property | Type | Required | Description |
|---|---|---|---|
| `{group}.{id}` | mapping | Yes | Key is `{extension_name}.{breakpoint_id}` |
| `label` | string | Yes | Human-readable name for admin UI |
| `mediaQuery` | string | Yes | CSS media query (can be empty for viewport_sizing) |
| `weight` | integer | Yes | Controls order (lower = higher priority in sorting) |
| `multipliers` | sequence | Yes | List of pixel densities: `['1x']`, `['1x', '2x']`, etc. |

## Media Query Patterns

**Viewport width (most common):**
```yaml
mediaQuery: 'all and (min-width: 768px)'
```

**Viewport sizing (no media query, for sizes attribute):**
```yaml
mediaQuery: ''
```

**Max-width (less common, mobile-first is preferred):**
```yaml
mediaQuery: 'all and (max-width: 1199px)'
```

**Orientation:**
```yaml
mediaQuery: 'all and (orientation: landscape)'
```

**Retina/HiDPI:**
```yaml
mediaQuery: 'all and (min-resolution: 192dpi)'
multipliers:
  - 2x
```

## Decision Points

| If you need... | Use... | Why |
|---|---|---|
| Standard responsive images | min-width media queries with 1x multiplier | Mobile-first, browser picks best match |
| Retina support | Add 2x multiplier to breakpoints | Provides high-DPI derivatives |
| Sizes attribute (resolution switching) | Empty mediaQuery with viewport_sizing breakpoint | Triggers sizes-based srcset generation |
| Art direction (different crops) | Multiple breakpoints with distinct image styles | Full control over which image at which viewport |

## Common Mistakes

- Using max-width instead of min-width → Desktop-first approach, harder to maintain, conflicts with mobile-first CSS
- Breakpoints don't match CSS breakpoints → Images switch at different points than layout, jarring UX
- Missing 1x multiplier → No images generated for standard DPI screens
- Too many breakpoints → Excessive derivatives, storage bloat, marginal UX gains
- Wrong weight ordering → Breakpoints applied in unexpected order, wrong image selected
- Forgetting to clear cache after changes → Old breakpoint definitions cached, changes ignored

## See Also

- [Responsive Image Style Config](responsive-image-config.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/themes/olivero/olivero.breakpoints.yml
- Reference: core/lib/Drupal/Core/Breakpoint/BreakpointManager.php
