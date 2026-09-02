---
description: Reference for DaisyUI data display components — badge, alert, card, stat, table, accordion, avatar, carousel, chat, countdown, diff, kbd, list, status, timeline, toast, and tooltip
tldr: "Presenting information: status indicators, grouped content, statistics, tables, collapsible sections, avatars, chat bubbles, timelines, and tooltips. Add `role='alert'` to `.alert`, `overflow-x-auto` to `.table`, and explicit `h-*`/`w-*` on skeleton-like components."
---

# Data Display Components

## When to Use

> Presenting information: status indicators, grouped content, statistics, tables.

## Decision: Which Display Component

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

## .badge — Badge / Tag

**Modifiers:** `badge-primary` `badge-secondary` `badge-accent` `badge-neutral` `badge-info` `badge-success` `badge-warning` `badge-error` `badge-ghost` + `badge-outline` `badge-dash` `badge-soft` + sizes `badge-xs` through `badge-xl`

```html
<span class="badge badge-primary">New</span>
<span class="badge badge-success badge-lg">Active</span>
<span class="badge badge-error badge-outline badge-sm">Error</span>
```

**Gotchas:** Default badge has no color modifier — it uses `base` colors. Add a color modifier for semantic meaning.

## .alert — Alert / Notification

**Modifiers:** `alert-info` `alert-success` `alert-warning` `alert-error` + `alert-soft` `alert-outline` `alert-dash` + layout `alert-horizontal` `alert-vertical`

```html
<div role="alert" class="alert alert-success">
  <svg .../><!-- icon -->
  <span>Your changes have been saved.</span>
</div>

<div role="alert" class="alert alert-error alert-soft">
  <span>Form contains errors.</span>
  <div class="flex gap-2">
    <button class="btn btn-sm">Dismiss</button>
  </div>
</div>
```

**Gotchas:** Add `role="alert"` manually — DaisyUI does not add ARIA roles to `.alert`. Without it, screen readers won't announce alerts.

## .card — Card Container

**Sub-classes:** `.card-body` `.card-title` `.card-actions` `.card-figure`

**Variants:** `card-border` `card-dash` `card-side` `card-compact`

**Sizes:** `card-xs` `card-sm` `card-md` `card-lg` `card-xl`

```html
<div class="card card-border bg-base-100 w-96">
  <figure><img src="..." alt="Product" /></figure>
  <div class="card-body">
    <h2 class="card-title">Product Name <span class="badge badge-secondary">New</span></h2>
    <p>Description text.</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Buy Now</button>
    </div>
  </div>
</div>
```

**Gotchas:**

- `card` has no default background — add `bg-base-100` or similar
- `card-side` requires `flex-direction: row` — image goes first in DOM and appears left
- Card is `<div>` by default; for linked cards, use `<a class="card ...">` or add a stretched-link pattern

## .stat — Statistics Display

**Structure:** `.stats` (container) > `.stat` (item) > `.stat-title` `.stat-value` `.stat-desc` `.stat-figure` `.stat-actions`

```html
<div class="stats stats-horizontal shadow">
  <div class="stat">
    <div class="stat-figure text-primary"><!-- icon --></div>
    <div class="stat-title">Total Users</div>
    <div class="stat-value text-primary">31,200</div>
    <div class="stat-desc">21% more than last month</div>
  </div>
</div>
```

## .table — Table

```html
<div class="overflow-x-auto">
  <table class="table table-zebra">
    <thead><tr><th>Name</th><th>Role</th></tr></thead>
    <tbody>
      <tr><td>Alice</td><td>Admin</td></tr>
      <tr><td>Bob</td><td>User</td></tr>
    </tbody>
  </table>
</div>
```

**Modifiers:** `table-zebra` (alternating row colors) `table-xs` `table-sm` `table-md` `table-lg` `table-xl` `table-pin-rows` `table-pin-cols`

## .accordion / .collapse — Collapsible Section

```html
<!-- Accordion using radio (only one open at a time) -->
<div class="collapse collapse-arrow bg-base-200">
  <input type="radio" name="accordion-1" />
  <div class="collapse-title font-semibold">Question?</div>
  <div class="collapse-content">Answer text here.</div>
</div>
```

**Gotchas:** For `checkbox` input, multiple sections can be open. For `radio` with same `name`, only one at a time.

## .avatar — User Avatar

**Description:** Displays a user image, placeholder, or online indicator in a circular or square crop.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `avatar-online` | Green dot indicator (positioned top-right) |
| `avatar-offline` | Grey dot indicator |
| `avatar-away` | Yellow dot indicator |
| `rounded-full` | Circular crop (add to inner `<div>`) |
| `rounded-box` | Rounded square crop |

**Required structure:**

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

**Gotchas:**

- The `w-*` sizing class must go on the **inner `<div>`**, not the `.avatar` wrapper
- `rounded-full` on the inner div creates circular crop; the image itself does not need border-radius
- `avatar-placeholder` requires the `avatar-placeholder` class on the outer div to center initials text

## .carousel — Horizontal Scroll Carousel

**Description:** CSS-only horizontal scroll carousel using anchor links or snap scrolling. No JavaScript required for basic use.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `carousel-center` | Items snap to center |
| `carousel-end` | Items snap to end |
| `carousel-vertical` | Vertical scroll direction |

**Required structure:**

```html
<!-- Snap carousel with prev/next buttons -->
<div class="carousel w-full">
  <div id="slide1" class="carousel-item relative w-full">
    <img src="/img1.jpg" class="w-full" alt="Slide 1" />
    <div class="absolute inset-y-0 right-5 left-5 flex items-center justify-between">
      <a href="#slide3" class="btn btn-circle">&#10094;</a>
      <a href="#slide2" class="btn btn-circle">&#10095;</a>
    </div>
  </div>
  <div id="slide2" class="carousel-item relative w-full">
    <img src="/img2.jpg" class="w-full" alt="Slide 2" />
    <div class="absolute inset-y-0 right-5 left-5 flex items-center justify-between">
      <a href="#slide1" class="btn btn-circle">&#10094;</a>
      <a href="#slide3" class="btn btn-circle">&#10095;</a>
    </div>
  </div>
</div>
```

**Gotchas:**

- Navigation uses anchor links (`href="#slideN"`) — the `id` on each `.carousel-item` must match. JavaScript is needed for looping or auto-play
- `.carousel` is `display: flex; overflow-x: scroll` — items must be `carousel-item` with explicit width (`w-full` or `w-64`)
- No built-in pagination dots — build them separately using `flex` + `btn btn-xs btn-circle`

## .chat — Chat Bubble

**Description:** Styled conversation bubbles for chat interfaces. Two layout variants: start (received) and end (sent).

**Sub-classes:** `.chat-image` `.chat-header` `.chat-footer` `.chat-bubble`

**Modifiers:**

| Class | Effect |
|-------|--------|
| `chat-start` | Message on left (received) |
| `chat-end` | Message on right (sent) |
| `chat-bubble-primary` through `chat-bubble-error` | Bubble color |

**Required structure:**

```html
<div class="chat chat-start">
  <div class="chat-image avatar">
    <div class="w-10 rounded-full">
      <img src="/avatar.jpg" alt="Sender" />
    </div>
  </div>
  <div class="chat-header">
    Alice <time class="text-xs opacity-50">12:45</time>
  </div>
  <div class="chat-bubble">Hello! How are you?</div>
  <div class="chat-footer opacity-50">Delivered</div>
</div>

<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-primary">I'm great, thanks!</div>
</div>
```

**Gotchas:**

- `chat-image`, `chat-header`, and `chat-footer` are optional but must appear as direct children of `.chat` in the correct order
- No scrollable container provided — wrap in a `div` with `overflow-y-auto max-h-*` for scrollable chat windows

## .countdown — Animated Number Countdown

**Description:** Displays animated flip-style numbers. Uses CSS custom property `--value` to set the current number. Requires JavaScript to update.

**Required structure:**

```html
<span class="countdown font-mono text-5xl">
  <span style="--value:10;"></span>
</span>

<!-- Hours:Minutes:Seconds -->
<span class="countdown font-mono text-4xl">
  <span style="--value:02;"></span>h
  <span style="--value:48;"></span>m
  <span style="--value:33;"></span>s
</span>
```

**Gotchas:**

- `--value` must be set as an inline style (or via CSS/JS) — it cannot be set as a Tailwind utility
- The element must have `content` provided via `::before` CSS — DaisyUI does this via the `.countdown` selector
- For live countdowns, use `setInterval` to update `style="--value:X"` — the CSS animation fires whenever the value changes
- Values must be integers 0–99; no decimal support

## .diff — Side-by-Side Image/Content Comparison

**Description:** A divider-based image comparison slider using CSS. The user drags a central divider to reveal more of one side.

**Required structure:**

```html
<div class="diff aspect-video">
  <div class="diff-item-1">
    <img alt="Before" src="/before.jpg" />
  </div>
  <div class="diff-item-2">
    <img alt="After" src="/after.jpg" />
  </div>
  <div class="diff-resizer"></div>
</div>
```

**Gotchas:**

- `aspect-video` (or any explicit aspect ratio/height) is required — `.diff` is `position: relative` and needs a known height
- The `.diff-resizer` is the draggable handle — it must be the third child in DOM order
- Works purely via CSS `resize` and `overflow` — no JavaScript required, but has limited browser support for the resize handle on touch devices

## .kbd — Keyboard Key Display

**Description:** Inline element styled to look like a physical keyboard key.

**Modifiers:** `kbd-xs` `kbd-sm` `kbd-md` `kbd-lg` `kbd-xl`

```html
<kbd class="kbd">Ctrl</kbd> + <kbd class="kbd">C</kbd>
<kbd class="kbd kbd-lg">⌘</kbd>
```

**Gotchas:** Pure presentational — no keyboard event behavior. Use for documentation, shortcut guides, and command references only.

## .list — Structured List

**Description:** Vertically stacked list rows with consistent spacing and optional actions. A structured alternative to bare `<ul>` for application lists.

**Sub-classes:** `.list-row` `.list-col-wrap`

**Required structure:**

```html
<ul class="list bg-base-100 rounded-box shadow-md">
  <li class="list-row">
    <div>
      <div class="font-bold">Item Title</div>
      <div class="text-xs text-base-content/70">Subtitle or description</div>
    </div>
    <button class="btn btn-ghost btn-sm ml-auto">Action</button>
  </li>
  <li class="list-row">
    <div class="font-bold">Another Item</div>
  </li>
</ul>
```

**Gotchas:**

- `.list-row` adds padding, border-bottom, and `display: flex` — don't add `flex` manually
- For image thumbnails in list rows, use `.avatar` or an `<img class="w-10 rounded-box">` as first child

## .status — Status Indicator Dot

**Description:** A small colored dot for live status indicators (online, error, processing).

**Modifiers:**

| Class | Effect |
|-------|--------|
| `status-primary` through `status-error` | Semantic color |
| `status-xs` `status-sm` `status-md` `status-lg` `status-xl` | Size scale |

```html
<span class="status status-success"></span> Online
<span class="status status-error"></span> Disconnected
<span class="status status-warning status-lg"></span> Degraded
```

**Gotchas:** `.status` renders a `display: inline-block` dot — pair with `items-center gap-2` on the parent for proper vertical alignment with text.

## .timeline — Vertical or Horizontal Timeline

**Description:** A structured timeline of events with connector lines and optional icons.

**Modifiers:** `timeline-vertical` (default) `timeline-horizontal` `timeline-compact`

**Required structure:**

```html
<ul class="timeline timeline-vertical">
  <li>
    <div class="timeline-start text-right">2020</div>
    <div class="timeline-middle">
      <svg class="text-primary" ...><!-- checkmark icon --></svg>
    </div>
    <div class="timeline-end timeline-box">First milestone</div>
    <hr class="bg-primary" />
  </li>
  <li>
    <hr class="bg-primary" />
    <div class="timeline-start">2021</div>
    <div class="timeline-middle">
      <svg .../>
    </div>
    <div class="timeline-end timeline-box">Second milestone</div>
    <hr />
  </li>
</ul>
```

**Gotchas:**

- The `<hr>` elements between `<li>` items are the connector lines — they must be present for the connecting lines to render
- The `<hr>` color class (e.g., `bg-primary`) controls connector line color for completed steps
- `timeline-box` adds card-like styling to `.timeline-end` or `.timeline-start` content
- `timeline-compact` collapses the alternating left/right layout to one side only

## .toast — Fixed-Position Notification Stack

**Description:** A fixed-position container that stacks notification messages in a corner of the viewport.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `toast-top` `toast-middle` `toast-bottom` | Vertical position (default: bottom) |
| `toast-start` `toast-center` `toast-end` | Horizontal position (default: end/right) |

**Required structure:**

```html
<div class="toast toast-top toast-end">
  <div class="alert alert-success">
    <span>Changes saved successfully.</span>
  </div>
  <div class="alert alert-error">
    <span>Error connecting to server.</span>
  </div>
</div>
```

**Gotchas:**

- `.toast` is `position: fixed` — it always appears in the viewport corner, overlaying all content
- Children of `.toast` are typically `.alert` elements. Multiple `.alert` children stack vertically
- In React/Next.js, manage toast visibility via state and conditional rendering — DaisyUI provides no dismiss mechanism
- `z-index` is set high (`z-[1000]`) — verify it doesn't conflict with modals (`z-[999]`)

## .tooltip — Hover/Focus Tooltip

**Description:** Adds a CSS tooltip on hover or focus. No JavaScript required.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `tooltip-top` `tooltip-bottom` `tooltip-left` `tooltip-right` | Tooltip direction |
| `tooltip-open` | Force open state |
| `tooltip-primary` through `tooltip-error` | Tooltip background color |

**Required structure:**

```html
<span class="tooltip" data-tip="This is a tooltip">
  <button class="btn">Hover me</button>
</span>
```

**Gotchas:**

- Tooltip text is set via `data-tip` attribute — not inner HTML. Dynamic content requires updating the attribute via JS
- CSS-only tooltips do not trap focus and are not announced by screen readers. For accessible tooltips use `aria-describedby` pointing to a visible or visually-hidden element
- Long tooltip text in `data-tip` does not wrap automatically — use `tooltip-lg` class or constrain content

## Common Mistakes

- Missing `overflow-x-auto` wrapper on `.table` — tables overflow on mobile without it
- Using `.alert` without `role="alert"` — screen readers ignore it
- Card images not cropping correctly — the `<figure>` inside `.card` handles overflow, but the image needs `object-cover` for proper fill
- Setting `--value` on `.countdown` without inline style — Tailwind utilities cannot set CSS custom properties

## See Also

- [Navigation Components](navigation-components.md) — navigation using tabs and menu
- [Actions Components](actions-components.md) — badge + button combos in actions
- [Feedback Components](feedback-components.md)
- Reference: `node_modules/daisyui/components/card/object.js`
- Reference: `node_modules/daisyui/components/badge/object.js`
- Reference: `node_modules/daisyui/components/alert/object.js`
- Reference: `node_modules/daisyui/components/toast/object.js`
- Reference: `node_modules/daisyui/components/stat/object.js`
