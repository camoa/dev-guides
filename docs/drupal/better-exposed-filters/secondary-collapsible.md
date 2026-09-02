---
description: "BEF secondary options panel and per-filter collapsible details — configuration, nesting, and auto-open behavior"
tldr: "Use secondary options when you have many exposed filters and want to group less-used ones into a collapsible Advanced options panel, or wrap individual filters in collapsible details elements."
drupal_version: "11.x"
---

# Secondary & Collapsible Options

## When to Use

> When you have many exposed filters and want to group less-used ones into a collapsible "Advanced options" panel, or wrap individual filters in collapsible details elements.

## Decision: Secondary Options Panel

**Enable:** General Settings → "Allow secondary options" (`allow_secondary: TRUE`)

Then per filter/sort/pager, check "This is a secondary option" (`is_secondary: TRUE`) to move it into the secondary panel.

**Configuration:**
| Option | Config Key | Default |
|---|---|---|
| Enable | `general.allow_secondary` | FALSE |
| Label | `general.secondary_label` | 'Advanced options' |
| Open by default | `general.secondary_open` | FALSE |

The secondary panel renders as a `<details>` element with the configured label.

## Decision: Per-Filter Collapsible

Any filter can be wrapped in its own collapsible `<details>` element:

| Option | Config Key | Default |
|---|---|---|
| Make collapsible | `advanced.collapsible` | FALSE |
| Disable auto-open | `advanced.collapsible_disable_automatic_open` | FALSE |
| Open by default | `advanced.open_by_default` | FALSE |

**Auto-open behavior:** By default, if a collapsible filter has a selected value, it opens automatically. Set `collapsible_disable_automatic_open` to TRUE to prevent this.

## Pattern: Nesting

A filter can be both collapsible AND secondary — it will be a `<details>` element inside the secondary `<details>` panel:

```
[Advanced options] ← secondary panel
  [Category ▶] ← collapsible filter
    □ Option 1
    □ Option 2
  [Tags ▶] ← collapsible filter
    □ Tag A
    □ Tag B
```

## Common Mistakes

- **"Is secondary" checkbox not visible** — Enable "Allow secondary" in the general settings first. The per-filter option is hidden via `#states` until then.
- **Collapsible filter with active value not opening** — This is the default behavior (auto-open). If you disabled it with `collapsible_disable_automatic_open`, the user must click to see their selection.

## See Also

- [General Settings](general-settings.md) — enabling secondary options
- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md) — combining with collapsible
