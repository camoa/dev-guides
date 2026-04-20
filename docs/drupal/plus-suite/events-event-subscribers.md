---
description: Complete event catalog for Plus Suite — Navigation+, LB+, Edit+, and Twig Events with extension point reference
tldr: "Subscribe to Plus Suite events to customize behavior without overriding core module code. Check this catalog before writing new hooks or overrides."
drupal_version: "11.x"
---

# Events & Event Subscribers

## When to Use

> Subscribe to Plus Suite events to customize behavior without overriding core module code. Check this catalog before writing new hooks or overrides.

## Decision

**Quick extension point reference:**

| I Want To... | Subscribe To |
|--------------|-------------|
| Block Edit Mode for certain entities | `ShouldNotEditModeEvent` |
| Add settings to the sidebar | `SettingsSidebarEvent` |
| Add custom block properties | `BlockPropertiesEvent` |
| Set defaults on block placement | `PlaceBlockEvent` |
| Prevent inline editing on a field | `NoChangeTool` or field third-party settings |
| Add section-level actions | `SectionToolIndicatorEvent` |
| Add block-level actions | `BlockToolIndicatorEvent` |
| Intercept media replacement | `LayoutBuilderReplaceMedia` |
| Modify form item attributes | `FieldAttributes::ALTER` |

## Pattern

**Navigation+ events:**

| Event | When Dispatched |
|-------|----------------|
| `ShouldNotEditModeEvent` | Before enabling Edit Mode — allows blocking |
| `SettingsSidebarEvent` | Building settings sidebar — add settings forms |
| `EditableFieldAttributes` | Rendering fields — add editing attributes |
| `LayoutBuilderNewMedia` | New media dropped on page |
| `LayoutBuilderReplaceMedia` | Media replaced on existing block |

**LB+ events:**

| Event | When Dispatched |
|-------|----------------|
| `PlaceBlockEvent` | Block placed from sidebar |
| `PrepareLayoutEvent` | Before layout renders in edit mode |
| `SectionToolIndicatorEvent` | Building section hover actions |
| `BlockToolIndicatorEvent` | Building block hover actions |

**Edit+ events:**

| Event | When Dispatched |
|-------|----------------|
| `FieldAttributes::ALTER` | Before form items rendered |
| `FieldAttributes::AFTER_BUILD` | After form items built |
| `BlockPropertiesEvent` | Adding custom block properties |
| `NoChangeTool` | Checking if Change tool should appear |

**Twig Events:**

| Event | When Dispatched |
|-------|----------------|
| `TwigRenderTemplateEvent` | During every Twig template render |

## Common Mistakes

- **Wrong**: Subscribing to `TwigRenderTemplateEvent` without performance testing → **Right**: It fires on every template; keep subscribers extremely fast
- **Wrong**: Modifying events after stopping propagation → **Right**: Downstream subscribers won't see changes if propagation is stopped

## See Also

- [Mode Plugins](mode-plugins.md)
- [Tool Plugins](tool-plugins.md)
- [Custom Block Types](custom-block-types.md)
- [Twig Events](twig-events.md)
