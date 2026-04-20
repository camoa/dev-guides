---
description: Decide between SDC (Twig), Code Component (React), and External JS Component types when building for Canvas.
tldr: "Use this when creating a new component for Canvas and you need to decide which component type to use. Canvas supports three distinct types, each with different authoring patterns, capabilities, and tradeoffs."
drupal_version: "11.x"
---

# Component Types Decision

## When to Use

> Use this when creating a new component for Canvas and you need to decide which component type to use. Canvas supports three distinct types, each with different authoring patterns, capabilities, and tradeoffs.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Server-side rendered Twig + Drupal field integration | SDC Component | Works with Drupal's render system; props map to Drupal field widgets; integrates with Drupal's caching |
| Interactive React UI, Tailwind styling, browser-only rendering | Code Component | Built-in browser editor; full React/Preact + Tailwind; syncs to external codebase via CLI |
| Vue / Nuxt / other JS framework components | External JS Component (canvas_extjs) | Register pre-built external components; Canvas editor shows them as available components |
| Simple static layout structure (dividers, spacers, grids) | SDC Component | Less overhead than React for non-interactive structure |
| Complex interactive widgets (sliders, tabs, carousels) | Code Component | React state management, hooks, event handling |
| CKEditor-style rich text with full HTML | SDC Component + canvas_full_html | SDC with `contentMediaType: text/html` prop; canvas_full_html module extends the text format |
| Reusing existing design system components | Code Component | Import from `preact`, use Tailwind; mirrors React component patterns |

## Pattern

The canonical decision flowchart:

```
Does the component need server-side Drupal field integration?
  → YES: Use SDC Component
    Does it need rich text? → Add contentMediaType: text/html prop
    Does it need images? → Use $ref: json-schema-definitions://canvas.module/image

Does the component need React state / interactivity?
  → YES: Use Code Component
    Start with @drupal-canvas/create (Nebula template)
    Author in browser editor OR local codebase + CLI sync

Is it an existing Vue/Nuxt component?
  → YES: Use canvas_extjs module
```

## Common Mistakes

- **Wrong**: Defaulting to Code Components for everything → **Right**: SDC is simpler for most content components, has better Drupal field integration, and server-renders
- **Wrong**: Using Code Components for components that only display static text → **Right**: Unnecessary React overhead; use SDC
- **Wrong**: Mixing SDC and Code Component patterns in one component definition → **Right**: Pick one type per component
- **Wrong**: Expecting Code Components to have access to Drupal's full PHP/Twig API → **Right**: Code Components are browser-only React components

## See Also

- [SDC Component Format](sdc-component-format.md) for the SDC authoring guide
- [Code Component Format](code-component-format.md) for the React authoring guide
- External JS Components: https://www.drupal.org/project/canvas_extjs
