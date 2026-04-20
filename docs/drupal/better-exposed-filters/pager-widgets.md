---
description: BEF pager widgets — radio buttons and links for items-per-page controls, enabling exposed pager
tldr: "Use this guide when you have an exposed pager (items per page) and want to render it as radio buttons or links instead of a dropdown."
drupal_version: "11.x"
---

# Pager Widgets

## When to Use

> Use this guide when you have an exposed pager (items per page) and want to render it as radio buttons or links instead of a dropdown.

## Decision

| Plugin ID | Class | Title |
|---|---|---|
| `default` | `DefaultWidget` | Default (select dropdown) |
| `bef` | `RadioButtons` | Radio Buttons |
| `bef_links` | `Links` | Links |

Pager widgets have minimal configuration — only the secondary panel option:

| Option | Config Key | Default |
|---|---|---|
| Is secondary | `advanced.is_secondary` | FALSE |

## Pattern

```
# Enable exposed pager in Views UI:
1. Edit the View → Pager settings
2. Check "Allow people to choose the number of items displayed"
3. Save → BEF pager widget options appear in BEF settings
```

The pager elements (`items_per_page`, `offset`) are transformed to the selected widget type.

## Common Mistakes

- **Wrong**: Expecting pager widget options in BEF settings without exposing the pager → **Right**: Enable "Allow people to choose the number of items displayed" in the View's pager settings first.

## See Also

- [Sort Widgets](sort-widgets.md)
- [General Settings](general-settings.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/pager/`
