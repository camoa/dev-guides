---
description: Reference for DaisyUI data display components — badge, alert, card, stat, table, accordion, avatar, carousel, chat, countdown, diff, kbd, list, status, timeline, toast, and tooltip
tldr: "Presenting information: status indicators, grouped content, statistics, tables, collapsible sections, avatars, chat bubbles, timelines, and tooltips. Add `role='alert'` to `.alert`, `overflow-x-auto` to `.table`, and explicit `h-*`/`w-*` on skeleton-like components."
---

# Data Display Components

## When to Use

> Presenting information: status indicators, grouped content, statistics, tables, collapsible sections, avatars, carousel displays, chat interfaces, and timelines.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Badge/tag | `.badge` | Status labels, counts, categories |
| Alert | `.alert` | Feedback messages, notifications |
| Card | `.card` | Grouped content with image + body |
| Statistics | `.stats` + `.stat` | Metrics and KPI displays |
| Table | `.table` | Tabular data |
| Accordion | `.collapse` | Collapsible FAQ/content sections |
| Avatar | `.avatar` | User images with status indicators |
| Carousel | `.carousel` | Horizontal scroll image/content gallery |
| Chat bubble | `.chat` | Conversation-style message display |
| Countdown | `.countdown` | Animated flip number display |
| Diff slider | `.diff` | Side-by-side image comparison |
| Keyboard key | `.kbd` | Inline keyboard shortcut display |
| Structured list | `.list` + `.list-row` | Application-style item lists |
| Status dot | `.status` | Live presence/state indicator dot |
| Timeline | `.timeline` | Chronological event list |
| Toast stack | `.toast` | Fixed-position notification container |
| Tooltip | `.tooltip` | Hover/focus tooltip on any element |

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

### .avatar

```html
<!-- Basic avatar -->
<div class="avatar">
  <div class="w-12 rounded-full">
    <img src="/avatar.jpg" alt="User Name" />
  </div>
</div>

<!-- With online indicator -->
<div class="avatar avatar-online">
  <div class="w-12 rounded-full">
    <img src="/avatar.jpg" alt="User Name" />
  </div>
</div>

<!-- Placeholder (no image) -->
<div class="avatar avatar-placeholder">
  <div class="bg-neutral text-neutral-content w-12 rounded-full">
    <span>JD</span>
  </div>
</div>
```

Status modifiers: `avatar-online` `avatar-offline` `avatar-away`. The `w-*` sizing class goes on the **inner `<div>`**, not the `.avatar` wrapper.

### .carousel

```html
<div class="carousel w-full">
  <div id="slide1" class="carousel-item relative w-full">
    <img src="/img1.jpg" class="w-full" alt="Slide 1" />
    <div class="absolute inset-y-0 right-5 left-5 flex items-center justify-between">
      <a href="#slide3" class="btn btn-circle">&#10094;</a>
      <a href="#slide2" class="btn btn-circle">&#10095;</a>
    </div>
  </div>
</div>
```

Modifiers: `carousel-center` `carousel-end` `carousel-vertical`. Navigation uses anchor links (`href="#slideN"`) — the `id` on each `.carousel-item` must match.

### .chat

```html
<div class="chat chat-start">
  <div class="chat-image avatar">
    <div class="w-10 rounded-full">
      <img src="/avatar.jpg" alt="Sender" />
    </div>
  </div>
  <div class="chat-header">Alice <time class="text-xs opacity-50">12:45</time></div>
  <div class="chat-bubble">Hello! How are you?</div>
  <div class="chat-footer opacity-50">Delivered</div>
</div>
<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-primary">I'm great, thanks!</div>
</div>
```

Layout: `chat-start` (received/left) `chat-end` (sent/right). Bubble colors: `chat-bubble-primary` through `chat-bubble-error`.

### .countdown

```html
<span class="countdown font-mono text-5xl">
  <span style="--value:10;"></span>
</span>
```

`--value` must be set as an inline style — it cannot be set as a Tailwind utility. Values must be integers 0–99.

### .diff

```html
<div class="diff aspect-video">
  <div class="diff-item-1"><img alt="Before" src="/before.jpg" /></div>
  <div class="diff-item-2"><img alt="After" src="/after.jpg" /></div>
  <div class="diff-resizer"></div>
</div>
```

`aspect-video` (or explicit height) is required. The `.diff-resizer` must be the third child.

### .kbd

```html
<kbd class="kbd">Ctrl</kbd> + <kbd class="kbd">C</kbd>
<kbd class="kbd kbd-lg">⌘</kbd>
```

Modifiers: `kbd-xs` through `kbd-xl`. Pure presentational — use for documentation, shortcut guides, and command references only.

### .list

```html
<ul class="list bg-base-100 rounded-box shadow-md">
  <li class="list-row">
    <div>
      <div class="font-bold">Item Title</div>
      <div class="text-xs text-base-content/70">Subtitle</div>
    </div>
    <button class="btn btn-ghost btn-sm ml-auto">Action</button>
  </li>
</ul>
```

`.list-row` adds padding, border-bottom, and `display: flex` — don't add `flex` manually.

### .status

```html
<span class="status status-success"></span> Online
<span class="status status-error"></span> Disconnected
<span class="status status-warning status-lg"></span> Degraded
```

Modifiers: `status-primary` through `status-error` + sizes `status-xs` through `status-xl`. Pair with `items-center gap-2` on the parent for alignment with text.

### .timeline

```html
<ul class="timeline timeline-vertical">
  <li>
    <div class="timeline-start text-right">2020</div>
    <div class="timeline-middle">
      <svg class="text-primary" ...><!-- checkmark --></svg>
    </div>
    <div class="timeline-end timeline-box">First milestone</div>
    <hr class="bg-primary" />
  </li>
  <li>
    <hr class="bg-primary" />
    <div class="timeline-start">2021</div>
    <div class="timeline-middle"><svg .../></div>
    <div class="timeline-end timeline-box">Second milestone</div>
    <hr />
  </li>
</ul>
```

The `<hr>` elements between `<li>` items are the connector lines — they must be present. `timeline-compact` collapses alternating layout to one side.

### .toast

```html
<div class="toast toast-top toast-end">
  <div class="alert alert-success">
    <span>Changes saved successfully.</span>
  </div>
</div>
```

Position modifiers: `toast-top` `toast-middle` `toast-bottom` + `toast-start` `toast-center` `toast-end`. `.toast` is `position: fixed` — it overlays all content. Manage visibility via conditional rendering in React.

### .tooltip

```html
<span class="tooltip" data-tip="This is a tooltip">
  <button class="btn">Hover me</button>
</span>
```

Position modifiers: `tooltip-top` `tooltip-bottom` `tooltip-left` `tooltip-right`. Tooltip text is set via `data-tip` attribute. CSS-only tooltips are not announced by screen readers — use `aria-describedby` for accessibility.

## Common Mistakes

- **Wrong**: `.table` without `overflow-x-auto` wrapper — **Right**: Tables overflow on mobile without it
- **Wrong**: `.alert` without `role="alert"` — **Right**: Screen readers ignore alerts without this attribute
- **Wrong**: Card without background — **Right**: `.card` has no default background; add `bg-base-100` or similar
- **Wrong**: `w-*` on the `.avatar` wrapper — **Right**: The sizing class goes on the inner `<div>`, not the outer wrapper
- **Wrong**: Setting `--value` on `.countdown` as a Tailwind class — **Right**: CSS custom properties require `style=""` inline

## See Also

- [Navigation Components](navigation-components.md)
- [Actions Components](actions-components.md)
- [Feedback Components](feedback-components.md)
- Reference: `node_modules/daisyui/components/card/object.js`
- Reference: `node_modules/daisyui/components/badge/object.js`
- Reference: `node_modules/daisyui/components/alert/object.js`
- Reference: `node_modules/daisyui/components/toast/object.js`
- Reference: `node_modules/daisyui/components/stat/object.js`
