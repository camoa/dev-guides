---
description: BEF secondary options panel and per-filter collapsible details — configuration, nesting, and auto-open behavior
drupal_version: "11.x"
---

# Secondary & Collapsible Options

## When to Use

> Use secondary options when you have many exposed filters and want to group less-used ones into a collapsible "Advanced options" panel. Use per-filter collapsible when you want individual filters wrapped in their own toggleable details element.

## Decision

**Secondary options panel:**

| Option | Config Key | Default |
|---|---|---|
| Enable | `general.allow_secondary` | FALSE |
| Label | `general.secondary_label` | 'Advanced options' |
| Open by default | `general.secondary_open` | FALSE |

Enable with "Allow secondary options" in general settings, then per filter/sort/pager check "This is a secondary option" (`is_secondary: TRUE`). The secondary panel renders as a `<details>` element.

**Per-filter collapsible:**

| Option | Config Key | Default |
|---|---|---|
| Make collapsible | `advanced.collapsible` | FALSE |
| Disable auto-open | `advanced.collapsible_disable_automatic_open` | FALSE |
| Open by default | `advanced.open_by_default` | FALSE |

**Auto-open behavior:** By default, a collapsible filter with a selected value opens automatically. Set `collapsible_disable_automatic_open` to TRUE to prevent this.

## Pattern

```
# Nesting: collapsible filter inside secondary panel
[Advanced options] ← secondary panel <details>
  [Category ▶] ← collapsible filter <details>
    □ Option 1
    □ Option 2
  [Tags ▶] ← collapsible filter <details>
    □ Tag A
    □ Tag B
```

A filter can be both `is_secondary: TRUE` and `collapsible: TRUE`.

## Common Mistakes

- **Wrong**: Enabling "is_secondary" on a filter when "Allow secondary" is not enabled in general settings → **Right**: The per-filter "is secondary" checkbox is hidden via `#states` until "Allow secondary" is enabled.
- **Wrong**: Expecting a collapsible filter with an active value to open automatically when `collapsible_disable_automatic_open` is TRUE → **Right**: With that setting, the user must click to see their active selection.

## See Also

- [General Settings](general-settings.md)
- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/views/exposed_form/BetterExposedFilters.php`
