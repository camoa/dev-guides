---
description: "Widget selection reference for all 23 custom field types with 37 available widgets, showing defaults and compatibility."
tldr: "37 widget plugins map to 23 custom field column types, each with a documented default; only override the default when UX calls for it (e.g., select/radios instead of autocomplete for small reference sets, or select_or_other for a constrained-but-extensible list)."
drupal_version: "11.x"
---

# Widget Plugins

## When to Use

You need to choose the right widget for collecting data for each sub-field in your custom field.

## Decision

**Widget selection by field type**:

| Field Type | Available Widgets | Default | Notes |
|---|---|---|---|
| string | TextWidget, HiddenWidget, SelectOrOtherWidget | TextWidget | Short text input |
| string_long | TextareaWidget | TextareaWidget | Multi-line textarea |
| email | EmailWidget | EmailWidget | Email input with validation |
| telephone | TelephoneWidget | TelephoneWidget | Tel input |
| uri | UrlWidget | UrlWidget | URL input |
| color | ColorWidget, ColorBoxesWidget | ColorWidget | Color picker |
| integer | IntegerWidget, SelectWidget, RadiosWidget, CheckboxWidget, SelectOrOtherWidget | IntegerWidget | Number input |
| float | FloatWidget, SelectOrOtherWidget | FloatWidget | Decimal number input |
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

**37 total widget plugins** -- 32 in the main module's `/src/Plugin/CustomField/FieldWidget/` (39 files; the other 7 are base classes), 5 more across the sub-modules (`LinkitWidget`, `LinkitUrlWidget`, `EntityReferenceBrowserWidget`, `MediaLibraryWidget`, `ViewfieldSelectWidget`).

**New in 5.0.2:** `SelectOrOtherWidget` (id `select_or_other`, category *Lists*), for `string`, `integer` and `float`. It renders a select list or radio buttons plus a free-text "Other" input, with settings `select_element_type` (`list`|`buttons`), `other_field_label`, `other_placeholder` and `other_option`. It is backed by three new render elements, `src/Element/SelectOrOtherBase.php`, `SelectOrOtherSelect.php` and `SelectOrOtherRadios.php`.

## Common Mistakes

- **Using wrong widget for field type** -- Custom Field validates widget compatibility; incompatible widgets won't appear in UI
- **Not configuring widget settings** -- Most widgets have settings (placeholder, size, allowed values) -- configure in field settings UI
- **Overriding default widget without reason** -- Default widgets chosen for best UX; only override when needed (e.g., select list instead of autocomplete for small sets)

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/`
