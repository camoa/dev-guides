---
description: "Inline editing with Edit+ — field handle types, data attributes, FieldAttributes events, InlineTextarea, and tempstore save flow"
tldr: "Use Edit+ to let users click on any field and edit it directly. Enable inline editing on fields editors change frequently; disable it on computed, read-only, or complex-validation fields."
drupal_version: "11.x"
---

# Inline Editing (Edit+)

## When to Use

> When you need to understand or configure the inline WYSIWYG editing experience that lets users click on any field and edit it directly.

## How Inline Editing Works

Edit+ adds the "Change" tool (`edit_plus` plugin, hotkey `c`) to the toolbar. When active:

1. Fields render with `data-edit-plus-*` attributes identifying them
2. User clicks a field → form loads inline replacing the field display
3. CKEditor 5 activates for text fields (`inline_textarea` element)
4. Changes stored in entity tempstore (via Tempstore+)
5. User saves via top bar → tempstore flushed, entity saved

## Field Attribute Correlation

Edit+ adds correlation attributes to both the rendered field and the form element:

**Rendered field attributes** (from `RenderEditableFieldAttributes`):
```
data-edit-plus-field-value-wrapper
data-edit-plus-id="{entity_type}.{bundle}.{entity_id}.{field_name}.{delta}.{language}.{formatter}"
data-edit-plus-page-element-id
```

**Form element attributes** (from `FormDefaultFieldAttributes`):
```
data-edit-plus-form-element
data-edit-plus-field-name="{field_name}"
```

JavaScript matches these to swap display → form when the user clicks.

## FieldAttributes Event System

Edit+ dispatches events during form preparation:

```php
// ALTER phase — modify form items before rendering
$event = new FieldAttributes(FieldAttributes::ALTER, $form, $view_mode, $field_name, $entity, $form_state);
$this->eventDispatcher->dispatch($event, FieldAttributes::ALTER);

// AFTER_BUILD phase — modify form items after Drupal's form building
$event = new FieldAttributes(FieldAttributes::AFTER_BUILD, ...);
$this->eventDispatcher->dispatch($event, FieldAttributes::AFTER_BUILD);
```

## Event Subscriber Priority Chain

| Subscriber | Priority | Purpose |
|---|---|---|
| `FormInlineEditorFieldAttributes` | 200 | Maps text_textarea → inline_textarea |
| `FormMediaFieldAttributes` | 100 | Handles media reference fields |
| `FormHandleFieldAttribute` | default | Determines handle type (form_item vs wrapper) |
| `FormDefaultFieldAttributes` | -1 | Adds data attributes, CSS classes |

## Per-Field Configuration

On **Manage Fields → Field Settings** (`field_config_edit` form), Edit+ adds:

| Setting | Purpose | Stored As |
|---|---|---|
| Disable inline editing | Prevent inline editing for this field | `edit_plus.disable` third-party setting |
| Form Item Handle | Whether to replace form_item or wrapper | `edit_plus.handle` third-party setting |

## Handle Types

| Handle | Behavior | Use For |
|---|---|---|
| `form_item` | Replace the individual form element | Single-value fields (text, select) |
| `wrapper` | Replace the entire field wrapper | Entity reference, multi-value fields |

## InlineTextarea Element

For text fields, Edit+ replaces the standard textarea with `inline_textarea`:
- Extends core's `TextFormat` render element
- Integrates CKEditor 5 with the text format
- Applies XSS filtering during editing
- Tracks original value for change detection
- Adds `data-inline-editor-for` attribute for JS correlation

## Tempstore Save Flow

```
1. User edits field inline
2. Form submitted via AJAX
3. InlineEntityFormAlter::update() stores in tempstore
4. `UpdateElement` AJAX command (defined by navigation_plus) refreshes the rendered field
5. Top bar shows "unsaved changes" indicator
6. User clicks Save → Tempstore controller applies changes to real entity
```

## NoChangeTool Event

Controls when the Change tool should not appear for a field:

```php
// Prevent Change tool for media_library view mode
$event = new NoChangeTool($entity, $field_name, $view_mode);
$this->eventDispatcher->dispatch($event);
if ($event->shouldNotChange()) {
  // Don't show inline editing for this field
}
```

## Non-Layout Builder Editing

The `edit_plus_non_lb_node` sub-module enables inline editing on regular (non-LB) node pages. It uses entity tempstore to track changes without Layout Builder's section storage.

## Decision

| Field Type | Enable? | Handle |
|---|---|---|
| Plain text, formatted text | Yes | `form_item` |
| Entity reference | Yes | `wrapper` |
| Image/Media | Yes (with media library) | `wrapper` |
| Computed/read-only fields | No (disable) | N/A |
| Fields with complex validation | Consider disabling | N/A |
| Password/sensitive fields | No (disable) | N/A |

## Common Mistakes

- **Do not** enable inline editing on fields with complex server-side validation that can't be shown inline.
- **Do not** forget to set the handle type — wrong handle causes JS to target the wrong element.

## See Also

- [Tempstore Strategy Pattern](tempstore-strategy.md)
- [Custom Block Types](custom-block-types.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `edit_plus/src/Element/InlineTextarea.php`
