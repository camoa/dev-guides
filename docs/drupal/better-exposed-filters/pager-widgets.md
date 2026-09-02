---
description: "BEF pager widgets — radio buttons and links for items-per-page controls, enabling exposed pager"
tldr: "Use this guide when you have an exposed pager (items per page) and want to render it as radio buttons or links."
drupal_version: "11.x"
---

# Pager Widgets

## When to Use

> When you have an exposed pager (items per page) and want to render it as radio buttons or links.

## Decision: Available Pager Widgets

| Plugin ID | Class | Title |
|---|---|---|
| `default` | `DefaultWidget` | Default (select dropdown) |
| `bef` | `RadioButtons` | Radio Buttons |
| `bef_links` | `Links` | Links |

## Decision: Pager Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Is secondary | `advanced.is_secondary` | FALSE | Move to secondary options panel |

Pager widgets have minimal configuration — just the secondary option. The pager elements (`items_per_page`, `offset`) are transformed to the selected widget type.

## Pattern: Enabling Exposed Pager

The pager widget options only appear when the View's pager is exposed:
1. Edit the View → Pager settings
2. Check "Allow people to choose the number of items displayed"
3. Save → BEF pager options appear in the BEF settings

## Common Mistakes

- **Pager options not showing in BEF settings** — The pager must be exposed in the View first. BEF only shows options for exposed pagers.

## See Also

- [Sort Widgets](sort-widgets.md) — similar widget types for sorts
- [General Settings](general-settings.md) — general BEF configuration
