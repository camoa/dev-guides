---
description: "Plus Suite module dependency graph, responsibilities, plugin systems, and page-building data flow"
tldr: "Reference this when you need to understand how Plus Suite's modules relate to each other and which module provides which functionality."
drupal_version: "11.x"
---

# Architecture & Module Map

## When to Use

> When you need to understand how Plus Suite's modules relate to each other and which module provides which functionality.

## Module Dependency Graph

```
plus_suite (recipe)
├── navigation_plus (2.3.4) ──── Foundation: Mode/Tool plugin system, Edit Mode toolbar
│   └── twig_events (1.0.1) ──── Template event dispatching for entity wrapping
├── lb_plus (3.6.8) ──────────── Layout Builder UI replacement with nested layouts
│   ├── navigation_plus ────────── Tools register via Navigation+ plugin system
│   ├── tempstore_plus (1.0.4) ── State management via Strategy pattern
│   └── section_library (1.2.2) ─ Reusable section templates (sub-module integration)
├── edit_plus (2.3.0) ─────────── Inline field editing with CKEditor 5
│   ├── navigation_plus ────────── "Change" tool registers via plugin system
│   ├── tempstore_plus ─────────── Entity tempstore for unsaved edits
│   └── field_sample_value (1.0.8) Sample content generation for new blocks
└── dropzonejs (2.11.0) ────────── Media drag-and-drop from desktop
```

## Module Responsibilities

| Module | Role | Key Classes |
|---|---|---|
| **navigation_plus** | UI framework, Mode/Tool plugins, hotkeys, sidebar system | `ModePluginManager`, `ToolPluginManager`, `NavigationPlusUi` |
| **lb_plus** | Layout Builder UI replacement, nested layouts, promoted blocks, drag-drop | `LayoutBuilderPlus` (element), `NestedAwareSectionStorage`, `TreeIndex` |
| **edit_plus** | Inline field editing, CKEditor integration, form alterations | `EditPlusFormTrait`, `InlineTextarea`, `ShowFieldWithErrors` |
| **tempstore_plus** | Strategy-based temporary storage for entities and layouts | `StrategySelector`, `EntityTempstoreStrategy`, `LayoutTempstoreStrategy` |
| **field_sample_value** | Pluggable placeholder content for new blocks | `SampleValueGeneratorManager`, `SampleValueEntityGenerator` |
| **twig_events** | Event dispatching during template rendering | `TwigRenderTemplateEvent` |
| **section_library** | Save and reuse Layout Builder sections | `SectionLibraryTemplate` entity |
| **dropzonejs** | JavaScript library for drag-and-drop file uploads | DropzoneJS integration |

## Data Flow: Page Building Workflow

```
1. User enables Edit Mode → Navigation+ sets cookie, renders toolbar
2. User selects tool (e.g., Place Block) → Tool plugin activates, loads JS library
3. User drags block from sidebar → lb_plus JS creates drop zone, sends AJAX
4. DropZones controller creates block → field_sample_value populates fields
5. Block rendered inline → twig_events dispatches template events
6. User clicks field to edit → edit_plus Change tool activates
7. Inline form loads → tempstore_plus stores changes
8. User saves → tempstore cleared, entity saved with all changes
```

## Plugin Systems

| Plugin Type | Manager | Provider Module | Purpose |
|---|---|---|---|
| Mode | `ModePluginManager` | navigation_plus | UI modes (Edit, Preview) |
| Tool | `ToolPluginManager` | navigation_plus | Actions (Place, Move, Trash, Configure, Duplicate) |
| SampleValueGenerator | `SampleValueGeneratorManager` | field_sample_value | Placeholder content for field types |

## Common Mistakes

- **Enabling modules in random order** — enable `field_sample_value tempstore_plus twig_events navigation_plus edit_plus lb_plus` in dependency order.
- **Assuming all features come from `lb_plus`** — inline editing is `edit_plus`, tempstore is `tempstore_plus`, toolbar is `navigation_plus`.

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Tempstore Strategy Pattern](tempstore-strategy.md)
- [Mode Plugins](mode-plugins.md)
- [Tool Plugins](tool-plugins.md)
