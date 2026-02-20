---
description: When to translate JSX 1:1 vs restructure for Drupal SDC
drupal_version: "11.x"
---

# Overview & When to Use

## When to Use

> Use this when you have an existing React/JSX design system and need to build equivalent Drupal SDC components. This applies whether the React source uses Tailwind, DaisyUI, Radix UI, shadcn/ui, MUI, or any other component library.

## Decision

| Situation | Strategy | Why |
|---|---|---|
| Simple presentational component (Card, Badge, Alert) | Translate 1:1 | Props map cleanly to component.yml, markup translates directly |
| Component with complex client state (Combobox, DatePicker) | Restructure: static Twig + JS behavior | Twig cannot manage state -- move state logic to `Drupal.behaviors` |
| Component wrapping a JS library (Chart, Map, Editor) | Skip Twig template; use JS-only component | Twig just renders a container div; the library handles everything |
| Layout/container component (Grid, Stack, Flex) | Translate 1:1 as wrapper with slots | These are pure markup -- ideal for SDCs |
| Component relying on React Context/Provider | Restructure with preprocess | Data that React passes via context must flow through Drupal's preprocess layer |
| Component with portal/teleportation (Modal, Toast) | Restructure with Drupal patterns | Drupal has no portal system -- use `<dialog>`, off-canvas, or page-level regions |
| Compound component (Tabs + Tab + TabPanel) | Flatten or use parent + slot pattern | SDCs do not support nested component namespaces; use slots or includes |

## Pattern

```
React world                          Drupal world
-----------                          ------------
Props (data)                   -->   component.yml props + Twig variables
Children / Slots               -->   SDC slots ({% block %})
TypeScript interface           -->   component.yml JSON Schema
useState / useReducer          -->   Server state (preprocess / controller)
useEffect / event handlers     -->   Drupal.behaviors + data-* attributes
Context / Provider             -->   Preprocess variables / Twig globals
CSS Modules / Tailwind         -->   SDC scoped CSS / Tailwind classes
Dynamic className (cn/cva)     -->   Twig conditionals for class lists
```

## Common Mistakes

- **Wrong**: Trying to replicate client-side state in Twig → **Right**: Twig renders once on the server; all interactivity must use JS behaviors or HTMX
- **Wrong**: Creating one SDC per React sub-component → **Right**: Drupal SDCs have overhead; flatten compound components where possible
- **Wrong**: Passing arrays of complex objects as props → **Right**: SDC props are best for primitives and simple enums; use slots for repeated complex content

## See Also

- [Conditional Rendering](conditional-rendering.md)
- [Props to Twig Variables](props-to-twig.md)
- Reference: [Single Directory Components (SDC) Development Guide](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)
