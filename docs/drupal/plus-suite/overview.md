---
description: "Plus Suite overview — WYSIWYG page builder recipe on top of Layout Builder with drag-and-drop, inline editing, and nested layouts"
tldr: "Use Plus Suite when you need a WYSIWYG page builder on top of core Layout Builder with drag-and-drop, inline editing, and nested layouts. Use core Layout Builder when you only need basic block placement via the sidebar form."
drupal_version: "11.x"
---

# Plus Suite Overview

## When to Use

> When you need a WYSIWYG page builder experience in Drupal that improves on Layout Builder's UX with drag-and-drop block placement, inline editing, nested layouts, and a Photoshop-like toolbar — while staying native to Drupal's rendering pipeline.

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

## What Plus Suite Is

Plus Suite is a **Drupal recipe** (not a single module) that orchestrates 7+ contributed modules into a cohesive page-building experience built on top of core Layout Builder. Created by Tim Bozeman and backed by Tag1 Consulting.

**Philosophy**: "Drag. Drop. Done." — get content on screen fast with auto-generated content, then refine inline. The inline editing, entity forms, widgets, tools, sidebars, and modes are all pluggable.

## Key Architectural Principles

1. **Drupal-native**: Uses PHP/Twig rendering pipeline, not React. Standard entity forms, standard field API, standard caching.
2. **Drop-in replacement**: Replaces Layout Builder's UI element (`layout_builder` → `layout_builder_plus`) while keeping the same data model.
3. **Pluggable everything**: Modes, Tools, Sidebars, Sample Value Generators, and Block Properties are all plugin systems.
4. **Enhances, doesn't replace**: Layout Builder data models, entity displays, and configuration remain unchanged. Other LB contrib modules should work.

## Common Mistakes

- **Treating Plus Suite as a React-based page builder** — it's fully Drupal PHP/Twig native.
- **Assuming it requires React knowledge** — PHP developers can use it without frontend framework skills.
- **Confusing it with Canvas/Experience Builder** — Plus Suite enhances Layout Builder; Canvas is a ground-up rebuild.

## See Also

- [Installation & Setup](installation-setup.md)
- [Architecture & Module Map](architecture-module-map.md)
- [Plus Suite vs Canvas](plus-suite-vs-canvas.md)
- Reference: [https://www.drupal.org/project/plus_suite](https://www.drupal.org/project/plus_suite)
