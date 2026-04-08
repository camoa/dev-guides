---
description: Inline editing with Edit+ — field handle types, data attributes, FieldAttributes events, InlineTextarea, and tempstore save flow
drupal_version: "11.x"
---

# Inline Editing (Edit+)

## When to Use

> Enable inline editing on fields that editors change frequently. Disable it on computed, read-only, or complex-validation fields.

## Decision

| Field Type | Enable? | Handle |
|------------|---------|--------|
| Plain text, formatted text | Yes | `form_item` |
| Entity reference | Yes | `wrapper` |
| Image/Media | Yes (with media library) | `wrapper` |
| Computed/read-only fields | No (disable) | N/A |
| Fields with complex validation | Consider disabling | N/A |
| Password/sensitive fields | No (disable) | N/A |

## Pattern

Edit+ adds the "Change" tool (`edit_plus` plugin, hotkey `c`). When active, fields render with `data-edit-plus-*` attributes; clicking a field loads the form inline.

**Handle types:**

| Handle | Behavior | Use For |
|--------|----------|---------|
| `form_item` | Replace the individual form element | Single-value fields (text, select) |
| `wrapper` | Replace the entire field wrapper | Entity reference, multi-value fields |

**Field third-party settings** (via Manage Fields → Field Settings):

```yaml
third_party_settings:
  edit_plus:
    disable: false
    handle: form_item  # or 'wrapper'
```

**Tempstore save flow:**
```
1. User edits field inline
2. Form submitted via AJAX
3. InlineEntityFormAlter::update() stores in tempstore
4. UpdateMarkup AJAX command refreshes the rendered field
5. Top bar shows "unsaved changes" indicator
6. User clicks Save → Tempstore applies changes to real entity
```

**InlineTextarea** — for text fields, replaces textarea with CKEditor 5 inline editing:
- Extends core's `TextFormat` render element
- Applies XSS filtering during editing
- Adds `data-inline-editor-for` attribute for JS correlation

**FieldAttributes events** for customizing form preparation:
- `FieldAttributes::ALTER` — modify form items before rendering (priority chain: 200, 100, default, -1)
- `FieldAttributes::AFTER_BUILD` — modify form items after Drupal's form building

## Common Mistakes

- **Wrong**: Setting wrong handle type → **Right**: Use `wrapper` for entity reference and multi-value fields; `form_item` for simple single-value fields
- **Wrong**: Enabling inline editing on complex-validation fields → **Right**: Inline validation errors can't display fully; disable for those fields

## See Also

- [Tempstore Strategy Pattern](tempstore-strategy.md)
- [Custom Block Types](custom-block-types.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `edit_plus/src/Element/InlineTextarea.php`, `edit_plus/src/Ajax/UpdateMarkup.php`
