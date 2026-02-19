---
description: Reference for DaisyUI data display components — badge, alert, card, stat, table, and accordion
---

# Data Display Components

## When to Use

> Presenting information: status indicators, grouped content, statistics, tables, and collapsible sections.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Badge/tag | `.badge` | Status labels, counts, categories |
| Alert | `.alert` | Feedback messages, notifications |
| Card | `.card` | Grouped content with image + body |
| Statistics | `.stats` + `.stat` | Metrics and KPI displays |
| Table | `.table` | Tabular data |
| Accordion | `.collapse` | Collapsible FAQ/content sections |

## Pattern

### .badge

```html
<span class="badge badge-primary">New</span>
<span class="badge badge-success badge-lg">Active</span>
<span class="badge badge-error badge-outline badge-sm">Error</span>
```

Modifiers: semantic colors + `badge-outline` `badge-dash` `badge-soft` + sizes `badge-xs` through `badge-xl`

### .alert

```html
<div role="alert" class="alert alert-success">
  <svg .../>
  <span>Your changes have been saved.</span>
</div>
```

Modifiers: `alert-info` `alert-success` `alert-warning` `alert-error` + `alert-soft` `alert-outline` `alert-dash`

### .card

```html
<div class="card card-border bg-base-100 w-96">
  <figure><img src="..." alt="Product" /></figure>
  <div class="card-body">
    <h2 class="card-title">Product Name</h2>
    <p>Description text.</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
    </div>
  </div>
</div>
```

Sub-classes: `.card-body` `.card-title` `.card-actions` `.card-figure`
Variants: `card-border` `card-dash` `card-side` `card-compact`

### .stats

```html
<div class="stats stats-horizontal shadow">
  <div class="stat">
    <div class="stat-title">Total Users</div>
    <div class="stat-value text-primary">31,200</div>
    <div class="stat-desc">21% more than last month</div>
  </div>
</div>
```

### .table

```html
<div class="overflow-x-auto">
  <table class="table table-zebra">
    <thead><tr><th>Name</th><th>Role</th></tr></thead>
    <tbody>
      <tr><td>Alice</td><td>Admin</td></tr>
    </tbody>
  </table>
</div>
```

Modifiers: `table-zebra` + sizes `table-xs` through `table-xl` + `table-pin-rows` `table-pin-cols`

### .collapse (Accordion)

```html
<!-- Radio: only one open at a time -->
<div class="collapse collapse-arrow bg-base-200">
  <input type="radio" name="accordion-1" />
  <div class="collapse-title font-semibold">Question?</div>
  <div class="collapse-content">Answer text here.</div>
</div>
```

Use `checkbox` input for independent multi-open sections; `radio` with same `name` for single-open accordion.

## Common Mistakes

- **Wrong**: `.table` without `overflow-x-auto` wrapper — **Right**: Tables overflow on mobile without it
- **Wrong**: `.alert` without `role="alert"` — **Right**: Screen readers ignore alerts without this attribute
- **Wrong**: Card without background — **Right**: `.card` has no default background; add `bg-base-100` or similar
- **Wrong**: Card image not cropping — **Right**: `<figure>` handles overflow but the image needs `object-cover` for proper fill

## See Also

- [Navigation Components](navigation-components.md)
- [Actions Components](actions-components.md)
- Reference: `node_modules/daisyui/components/card/object.js`
- Reference: `node_modules/daisyui/components/badge/object.js`
- Reference: `node_modules/daisyui/components/alert/object.js`
