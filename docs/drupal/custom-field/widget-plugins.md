---
description: Widget selection reference for all 27 custom field types with 39 available widgets, showing defaults and compatibility.
---

# Widget Plugins

## When to Use

You need to choose the right widget for collecting data for each sub-field in your custom field.

## Decision

**Widget selection by field type**:

| Field Type | Available Widgets | Default | Notes |
|---|---|---|---|
| string | TextWidget, HiddenWidget | TextWidget | Short text input |
| string_long | TextareaWidget | TextareaWidget | Multi-line textarea |
| email | EmailWidget | EmailWidget | Email input with validation |
| telephone | TelephoneWidget | TelephoneWidget | Tel input |
| uri | UrlWidget | UrlWidget | URL input |
| color | ColorWidget, ColorBoxesWidget | ColorWidget | Color picker |
| integer | IntegerWidget, SelectWidget, RadiosWidget, CheckboxWidget | IntegerWidget | Number input |
| float | FloatWidget | FloatWidget | Decimal number input |
| decimal | DecimalWidget | DecimalWidget | Fixed precision input |
| boolean | CheckboxWidget, SelectWidget, RadiosWidget | CheckboxWidget | On/off widget |
| datetime | DateTimeDefaultWidget, DateTimeDatelistWidget, DateTimeLocalWidget | DateTimeDefaultWidget | Date/time picker |
| daterange | DateRangeDefaultWidget | DateRangeDefaultWidget | Start/end date picker |
| time | TimeWidget | TimeWidget | Time picker |
| time_range | TimeRangeWidget | TimeRangeWidget | Start/end time |
| duration | DurationWidget | DurationWidget | Duration with granularity |
| entity_reference | EntityReferenceAutocompleteWidget, EntityReferenceSelectWidget, EntityReferenceRadiosWidget, HierarchicalSelectWidget | EntityReferenceAutocompleteWidget | Varies by use case |
| file | FileWidget | FileWidget | File upload |
| image | ImageWidget | ImageWidget | Image upload with alt/title |
| link | LinkWidget | LinkWidget | URL + title + options |
| map | MapKeyValueWidget | MapKeyValueWidget | Key-value pairs |
| map_string | MapTextWidget | MapTextWidget | Text key-value |
| uuid | UuidWidget | UuidWidget | Auto-generated, hidden |

**39 total widget plugins** in `/src/Plugin/CustomField/FieldWidget/`.

## Common Mistakes

- **Using wrong widget for field type** -- Custom Field validates widget compatibility; incompatible widgets won't appear in UI
- **Not configuring widget settings** -- Most widgets have settings (placeholder, size, allowed values) -- configure in field settings UI
- **Overriding default widget without reason** -- Default widgets chosen for best UX; only override when needed (e.g., select list instead of autocomplete for small sets)

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/`
