---
description: Stacked and flexbox layout widgets for controlling how the entire custom field displays on the edit form.
---

# Field-Level Widgets

## When to Use

You need to control how the entire custom field (all sub-fields together) is laid out on the edit form.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Vertical stacking (default) | CustomStackedWidget | Simplest layout, sub-fields stack vertically |
| Responsive flexbox layout | CustomFlexWidget | Bootstrap 5 flexbox with configurable columns per breakpoint |

## CustomStackedWidget

Stacks sub-field widgets vertically (default field widget).

- **Plugin ID:** `custom_stacked`
- **Settings:** None (uses sub-field widget settings)
- **Layout:** Each sub-field renders full-width, one below the other

```yaml
# In field display config
type: custom_stacked
settings:
  fields:
    street:
      type: text
      weight: 0
    city:
      type: text
      weight: 1
```

**Gotchas:** Sub-field order controlled by weight in field settings. No responsive control.

## CustomFlexWidget

Bootstrap 5 flexbox layout with responsive column sizing.

- **Plugin ID:** `custom_flex`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| column_classes | array | [] | Responsive classes per sub-field (xs/sm/md/lg/xl/xxl) |
| column_gap | string | '' | Gap utility class (gap-0 through gap-5) |
| row_gap | string | '' | Row gap utility class |

**Layout:** Wraps sub-fields in Bootstrap `.row` with per-field column classes.

```yaml
type: custom_flex
settings:
  fields:
    first_name:
      column_classes:
        md: col-md-6
        sm: col-sm-12
    last_name:
      column_classes:
        md: col-md-6
        sm: col-sm-12
  column_gap: gap-3
```

**Gotchas:** Requires Bootstrap 5 theme. Column classes must be valid Bootstrap grid classes. Default is full-width if no classes set.

## Common Mistakes

- **Using FlexWidget without Bootstrap theme** -- Flexbox layout requires Bootstrap 5 CSS; won't work with non-Bootstrap themes
- **Not setting responsive column classes** -- Without column classes, all fields full-width; defeats purpose of flex layout
- **Mixing incompatible gap utilities** -- gap-* requires flexbox; doesn't work with non-flex layouts

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/Field/FieldWidget/CustomFlexWidget.php`
