---
description: Plus Suite overview — WYSIWYG page builder recipe on top of Layout Builder with drag-and-drop, inline editing, and nested layouts
drupal_version: "11.x"
---

# Plus Suite Overview

## When to Use

> Use Plus Suite when you need a WYSIWYG page builder on top of core Layout Builder with drag-and-drop, inline editing, and nested layouts. Use core Layout Builder when you only need basic block placement via the sidebar form.

## Decision

| Feature | Core Layout Builder | Plus Suite |
|---------|--------------------|-----------| 
| Block placement | Sidebar form, multi-step | Drag-and-drop from sidebar |
| Editing | Off-canvas forms | Inline WYSIWYG editing |
| Preview | Must toggle preview mode | Always WYSIWYG |
| Nested layouts | Not supported | Layout blocks with blocks inside |
| Tooling | Edit/layout tabs | Photoshop-style toolbar with hotkeys |
| Placeholder content | Empty blocks | Auto-generated sample content |
| Media handling | Form-based upload | Drag from desktop onto page |
| Section reuse | Not built-in | Section Library integration |
| Workspace support | Limited | Full Tempstore+ strategy pattern |

## Pattern

Plus Suite is a **Drupal recipe** (not a single module) orchestrating 7+ contributed modules on top of core Layout Builder.

**Key architectural principles:**

- **Drupal-native**: PHP/Twig rendering pipeline, not React. Standard entity forms, field API, caching.
- **Drop-in replacement**: Replaces `layout_builder` element with `layout_builder_plus`, same data model.
- **Pluggable everything**: Modes, Tools, Sidebars, Sample Value Generators — all plugin systems.
- **Enhances, doesn't replace**: Layout Builder data models and configuration remain unchanged.

## Common Mistakes

- **Wrong**: Treating Plus Suite as a React-based page builder — **Right**: It's fully Drupal PHP/Twig native
- **Wrong**: Assuming it requires React knowledge — **Right**: PHP developers can use it without frontend framework skills
- **Wrong**: Confusing it with Canvas/Experience Builder — **Right**: Plus Suite enhances Layout Builder; Canvas is a ground-up rebuild

## See Also

- [Installation & Setup](installation-setup.md)
- [Architecture & Module Map](architecture-module-map.md)
- [Plus Suite vs Canvas](plus-suite-vs-canvas.md)
- Reference: [https://www.drupal.org/project/plus_suite](https://www.drupal.org/project/plus_suite)
