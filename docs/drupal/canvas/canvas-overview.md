---
description: What Drupal Canvas is, when to use it, its architecture, and key version requirements for Drupal 11.2+.
drupal_version: "11.x"
---

# Canvas Overview

## When to Use

> Use Canvas when you need a visual page-building experience for non-technical editors on Drupal 11.2+. Use standard content types + SDC theming when layouts are fixed or developer-managed.

## Decision

| If your project needs... | Canvas is... | Notes |
|---|---|---|
| Visual page building for non-technical editors | The right fit | Drag-and-drop, real-time preview, in-place editing |
| A design-system-native CMS | The right fit | All pages built from SDC/Code Components |
| Drupal 10 or earlier | Not available | Requires Drupal ^11.2 |
| Developer-only content editing | Possibly overkill | Standard content types + SDC theming may be simpler |
| Existing Paragraphs-based architecture | Migration needed | Canvas replaces, not extends, Paragraphs for page composition |
| Decoupled/headless frontend | Supported but complex | See [Decoupled Frontend Patterns](decoupled-frontend-patterns.md) |

## Pattern

Canvas introduces a distinct page entity type (`canvas_page`) that stores its layout as a **component tree** — a structured JSON field referencing versioned Component config entities. This is fundamentally different from standard Drupal content types:

- **Standard Drupal content type**: Fields defined in config, rendered via Twig templates, layout via Layout Builder or theme
- **Canvas page**: Layout AND content stored as a component tree; components provide all structure and content
- **Component config entities**: Versioned configs that map SDC definitions to Canvas-aware field storage; Canvas tracks these separately from the SDC plugin itself

**Component sources**: Canvas can source components from multiple origins:

1. **SDC components** — Standard Drupal Single Directory Components in any module or theme; automatically available in Canvas once the module/theme is enabled
2. **Code Components** — React/Preact components authored in-browser or synced from a local codebase via CLI; stored as Drupal config entities
3. **External JS Components** — Components from any JS framework (Vue, Nuxt, etc.) registered via the `canvas_extjs` contrib module

**The Canvas UI**: A React-based interface running in the browser that provides:
- A component panel showing all available SDC and Code Components
- Drag-and-drop placement onto the canvas
- In-place editing of component props (text fields, image pickers, link widgets, etc.)
- Real-time preview
- Design token editing (color, typography overrides)
- AI assistant (optional `canvas_ai` submodule)

**Module version**: Canvas 1.0 stable released November 2025. Canvas 1.1.0 (February 2026) requires Drupal ^11.2. As of early 2026, ~3,253 sites report using the module. Security advisory SA-CONTRIB-2026-006 exists — update to Canvas 1.0.4+ if using unpublished Canvas pages.

## Common Mistakes

- **Wrong**: Treating Canvas pages like standard content types — they are a separate entity; standard fields cannot be added to the page entity → **Right**: Use the component tree for all content and layout
- **Wrong**: Assuming any Drupal 11 version works → **Right**: Minimum is Drupal 11.2 (Canvas 1.1.0+)
- **Wrong**: Enabling Canvas on existing sites without planning component migration → **Right**: Paragraphs content cannot be auto-converted to Canvas pages; plan migration carefully
- **Wrong**: Confusing "Canvas" (the page builder) with "canvas_page" (the entity type) and "Component" (the config entity) → **Right**: These are three distinct concepts
- **Wrong**: Forgetting that theme changes break SDC dependencies if components reference a theme's SDC → **Right**: Track component-to-theme dependencies carefully

## See Also

- Official Canvas project page: https://www.drupal.org/project/canvas
- Canvas documentation: https://project.pages.drupalcode.org/canvas/
- Release notes: https://www.drupal.org/project/canvas/releases
