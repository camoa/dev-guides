---
description: When to use UI Suite DaisyUI vs alternatives like Radix, custom Tailwind themes, or UI Suite Bootstrap
---

# Overview & Decision

## What UI Suite DaisyUI Is

UI Suite DaisyUI is a Drupal theme that integrates [DaisyUI](https://daisyui.com/) (a component class library for Tailwind CSS) with Drupal's component system via the [UI Suite Initiative](https://www.drupal.org/project/ui_suite) modules. It exposes 51 DaisyUI components as Single Directory Components (SDCs) through UI Patterns 2, 10 style plugins (with dozens of CSS class options) through UI Styles, 35 themes through UI Skins, and 25 CSS variables for design token customization -- all accessible from the Drupal admin UI without writing code.

Version 5.0.x targets **DaisyUI 5** (built on Tailwind CSS 4). The 4.0.x branch is minimally maintained. All new development focuses on 5.0.x.

## When to Use

| Scenario | Use UI Suite DaisyUI? | Alternative |
|---|---|---|
| Site-builder-first project, low-code approach | Yes | -- |
| Need DaisyUI's 35 themes (dark, retro, cyberpunk...) | Yes | -- |
| Rapid prototyping with component-based layouts | Yes | -- |
| Deep Bootstrap integration required | No | UI Suite Bootstrap or Radix |
| Need Layout Builder + DaisyUI components | Yes (with UI Styles LB) | -- |
| Existing Radix sub-theme to maintain | No | Stay with Radix |
| Custom design system, no DaisyUI dependency | No | Custom Tailwind theme |
| Need full control over Tailwind build pipeline | Yes (starterkit has Vite + Tailwind 4 + DaisyUI 5) | Custom theme with own build config |

## The UI Suite Ecosystem

UI Suite DaisyUI relies on four companion modules:

| Module | Purpose | Required? |
|---|---|---|
| `ui_patterns` (2.x) | Component discovery, props, slots, SDC integration | Yes (dependency) |
| `ui_styles` | Utility class styles applied to blocks, Layout Builder sections | Recommended (not a dependency since alpha6) |
| `ui_skins` | Theme switching (data-theme), CSS variable overrides | Recommended |
| `ui_icons` | Icon pack integration (Heroicons) | Yes (dependency) |

## See Also

- `design-system-daisyui.md` -- DaisyUI components, themes, tokens (framework-level)
- `drupal-ui-patterns.md` -- UI Patterns module (props, slots, sources, component API)
- `design-system-tailwind.md` -- Tailwind CSS fundamentals
- `drupal-twig-theming.md` -- Drupal Twig patterns
