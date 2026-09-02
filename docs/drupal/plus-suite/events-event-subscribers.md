---
description: Complete event catalog for Plus Suite — Navigation+, LB+, Edit+, and Twig Events with extension point reference
tldr: "Subscribe to Plus Suite events to customize behavior without overriding core module code. Check this catalog before writing new hooks or overrides."
drupal_version: "11.x"
---

# Events & Event Subscribers

## When to Use

> When you need to hook into Plus Suite's event system to customize behavior, or understand the complete event flow.

## Event Catalog: Navigation+ Events

| Event | Class | When Dispatched |
|---|---|---|
| `ShouldNotEditModeEvent` | `navigation_plus\Event\ShouldNotEditModeEvent` | Before enabling Edit Mode — allows blocking |
| `SettingsSidebarEvent` | `navigation_plus\Event\SettingsSidebarEvent` | Building settings sidebar — add settings forms |
| `EditableFieldAttributes` | `navigation_plus\Event\EditableFieldAttributes` | Rendering fields — add editing attributes |
| `EditableUiBuilder` | `navigation_plus\Event\EditableUiBuilder` | Building editable UI — modify UI build |
| `LayoutBuilderNewMedia` | `navigation_plus\Event\LayoutBuilderNewMedia` | New media dropped on page |
| `LayoutBuilderReplaceMedia` | `navigation_plus\Event\LayoutBuilderReplaceMedia` | Media replaced on existing block |

## Event Catalog: LB+ Events

| Event | Class | When Dispatched |
|---|---|---|
| `PlaceBlockEvent` | `lb_plus\Event\PlaceBlockEvent` | Block placed from sidebar |
| `PrepareLayoutEvent` | `lb_plus\Event\PrepareLayoutEvent` | Before layout renders in edit mode |
| `SectionToolIndicatorEvent` | `lb_plus\Event\SectionToolIndicatorEvent` | Building section hover actions |
| `BlockToolIndicatorEvent` | `lb_plus\Event\BlockToolIndicatorEvent` | Building block hover actions |

## Event Catalog: Edit+ Events

| Event | Class | When Dispatched |
|---|---|---|
| `FieldAttributes::ALTER` | `edit_plus\Event\FieldAttributes` | Before form items rendered |
| `FieldAttributes::AFTER_BUILD` | `edit_plus\Event\FieldAttributes` | After form items built |
| `BlockPropertiesEvent` | `edit_plus\Event\BlockPropertiesEvent` | Adding custom block properties |
| `AddEmptyField` | `edit_plus\Event\AddEmptyField` | Auto-generating empty field values |
| `NoChangeTool` | `edit_plus\Event\NoChangeTool` | Checking if Change tool should appear |
| `FieldProperties` | `edit_plus\Event\FieldProperties` | Managing field-level properties |

## Event Catalog: Twig Events

| Event | Class | When Dispatched |
|---|---|---|
| `TwigRenderTemplateEvent` | `twig_events\Event\TwigRenderTemplateEvent` | During every Twig template render |

## Decision: Common Extension Points

| I Want To... | Subscribe To |
|---|---|
| Block Edit Mode for certain entities | `ShouldNotEditModeEvent` |
| Add settings to the sidebar | `SettingsSidebarEvent` |
| Add custom block properties | `BlockPropertiesEvent` |
| Set defaults on block placement | `PlaceBlockEvent` |
| Prevent inline editing on a field | `NoChangeTool` or field third-party settings |
| Add section-level actions | `SectionToolIndicatorEvent` |
| Add block-level actions | `BlockToolIndicatorEvent` |
| Intercept media replacement | `LayoutBuilderReplaceMedia` |
| Modify form item attributes | `FieldAttributes::ALTER` |

## Common Mistakes

- **Do not subscribe to `TwigRenderTemplateEvent` without performance testing** — it fires on every template.
- **Do not modify events after stopping propagation** — downstream subscribers won't see changes.

## See Also

- [Mode Plugins](mode-plugins.md)
- [Tool Plugins](tool-plugins.md)
- [Custom Block Types](custom-block-types.md)
- [Twig Events](twig-events.md)
