---
description: Reference for DaisyUI feedback components — loading spinner, progress bar, skeleton, and radial progress
tldr: "Communicating async operation states: loading spinners, linear progress bars, skeleton placeholders, and radial progress indicators. These components are CSS-only — show/hide logic requires JavaScript state management. Always add `aria-label` and `role='status'` to `.loading`."
---

# Feedback Components

## When to Use

> Communicating async operation states (loading, progress) and skeleton screens during content fetching. These components are almost always paired with JavaScript state management — the CSS classes exist, but the show/hide logic requires code.

## Decision: Which Feedback Component

| Component | Class | Use for |
|-----------|-------|---------|
| Spinner / animation | `.loading` | Loading state indicator during async operations |
| Linear progress | `.progress` | Determinate or indeterminate progress bar |
| Content placeholder | `.skeleton` | Shape-matching placeholder during content fetch |
| Circular progress | `.radial-progress` | Donut-style percentage display |

## .loading — Loading Spinner / Animation

**Description:** An animated indicator for loading states. Six animation styles available.

**Modifiers:**

| Class | Animation style |
|-------|----------------|
| `loading-spinner` | Rotating circle (default) |
| `loading-dots` | Three bouncing dots |
| `loading-ring` | Rotating ring (thinner than spinner) |
| `loading-ball` | Bouncing ball |
| `loading-bars` | Vertical equalizer bars |
| `loading-infinity` | Infinity loop |

**Size modifiers:** `loading-xs` `loading-sm` `loading-md` `loading-lg` `loading-xl`

**Color modifiers:** `text-primary` through `text-error` (uses `currentColor`)

```html
<!-- Default spinner -->
<span class="loading loading-spinner loading-md"></span>

<!-- Inside a button -->
<button class="btn btn-primary" disabled>
  <span class="loading loading-spinner loading-sm"></span>
  Saving...
</button>

<!-- Full-page overlay -->
<div class="flex items-center justify-center h-screen">
  <span class="loading loading-dots loading-xl text-primary"></span>
</div>
```

**Gotchas:**

- `.loading` renders an `<span>` — it is an inline element. Use inside `flex` or `grid` containers for centering
- No `aria-label` is added automatically — always add `aria-label="Loading"` and `role="status"` for screen readers
- The animation plays immediately on render — control visibility via conditional rendering or `hidden` class, not by removing the animation class

## .progress — Linear Progress Bar

**Description:** A styled progress bar element. Supports both determinate (known value) and indeterminate (unknown duration) states.

**Modifiers:** `progress-primary` through `progress-error`

```html
<!-- Determinate -->
<progress class="progress progress-primary w-56" value="60" max="100"></progress>

<!-- Indeterminate (animated sweep) -->
<progress class="progress w-56"></progress>

<!-- With label -->
<div class="w-56">
  <div class="flex justify-between text-sm mb-1">
    <span>Uploading</span>
    <span>60%</span>
  </div>
  <progress class="progress progress-success w-full" value="60" max="100"></progress>
</div>
```

**Gotchas:**

- Omitting `value` attribute triggers the indeterminate animation — this is native HTML `<progress>` behavior
- `<progress>` is a void element — do not put content inside it
- The progress bar width is controlled by Tailwind `w-*` utilities — `progress` has no intrinsic width

## .skeleton — Content Placeholder

**Description:** A pulsing grey placeholder that mimics content shape during loading. Pure CSS — apply the class to any element with explicit dimensions.

```html
<!-- Text placeholder -->
<div class="skeleton h-4 w-48"></div>

<!-- Card skeleton -->
<div class="card w-64 bg-base-100 shadow">
  <div class="skeleton h-32 w-full"></div>
  <div class="card-body gap-3">
    <div class="skeleton h-4 w-36"></div>
    <div class="skeleton h-4 w-24"></div>
    <div class="flex gap-2 mt-2">
      <div class="skeleton h-8 w-20"></div>
      <div class="skeleton h-8 w-20"></div>
    </div>
  </div>
</div>

<!-- Avatar + text row skeleton -->
<div class="flex items-center gap-4">
  <div class="skeleton w-12 h-12 rounded-full"></div>
  <div class="flex flex-col gap-2">
    <div class="skeleton h-4 w-32"></div>
    <div class="skeleton h-4 w-24"></div>
  </div>
</div>
```

**Gotchas:**

- `.skeleton` requires explicit dimensions (`h-*` and `w-*`) — it has no intrinsic size
- The pulse animation uses `opacity` — do not set `opacity` utilities on skeleton elements
- Swap skeleton elements for real content by conditional rendering (React) or CSS class toggling — DaisyUI provides no show/hide mechanism
- Use `rounded-full` on skeleton avatar circles to match the real content's border-radius

## .radial-progress — Circular Progress Indicator

**Description:** A circular/donut progress indicator. Value is set via CSS custom property `--value`.

**Modifiers:** `text-primary` through `text-error` (track and indicator color)

**CSS variables:**

| Variable | Default | Effect |
|----------|---------|--------|
| `--value` | — | **Required.** Progress percentage (0–100) |
| `--size` | `3.5rem` | Circle diameter |
| `--thickness` | derived | Ring stroke width |

```html
<div class="radial-progress text-primary" style="--value:70;" role="progressbar" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100">
  70%
</div>

<div class="radial-progress text-success" style="--value:100; --size:8rem; --thickness:0.5rem;" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
  Done
</div>
```

**Gotchas:**

- `--value` must be set as an inline style (or CSS) — not a Tailwind class
- Text inside `.radial-progress` is centered automatically — put the percentage label as inner content
- Always add `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax` — DaisyUI does not add ARIA attributes
- The color modifier (`text-primary`) sets both the ring color and the track color — use `[--tw-ring-color:...]` overrides to separate them if needed

## Common Mistakes

- Rendering `.loading` without `aria-label="Loading"` and `role="status"` — invisible to screen readers
- Using `.skeleton` without explicit `h-*` and `w-*` — it renders as zero-size
- Setting `--value` on `.radial-progress` as a Tailwind class instead of inline style — CSS custom properties require `style=""` or a `@layer` override
- Leaving `.progress` in indeterminate state when the operation is complete — swap to a determinate value or hide the element

## See Also

- [Data Display Components](data-display-components.md) — `.toast` for success/error notifications after async operations complete
- [Actions Components](actions-components.md) — disabling `.btn` and adding `.loading` spinner inside it during form submission
- Reference: https://daisyui.com/components/loading/
- Reference: https://daisyui.com/components/progress/
- Reference: https://daisyui.com/components/skeleton/
