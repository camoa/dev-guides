---
description: Reference for DaisyUI feedback components — loading spinner, progress bar, skeleton, and radial progress
tldr: "Communicating async operation states: loading spinners, linear progress bars, skeleton placeholders, and radial progress indicators. These components are CSS-only — show/hide logic requires JavaScript state management. Always add `aria-label` and `role='status'` to `.loading`."
---

# Feedback Components

## When to Use

> Use feedback components when communicating async operation states (loading, progress) and skeleton screens during content fetching. The CSS classes exist, but the show/hide logic requires code.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Spinner / animation | `.loading` | Loading state indicator during async operations |
| Linear progress | `.progress` | Determinate or indeterminate progress bar |
| Content placeholder | `.skeleton` | Shape-matching placeholder during content fetch |
| Circular progress | `.radial-progress` | Donut-style percentage display |

## Pattern

### .loading — Loading Spinner

```html
<!-- Default spinner -->
<span class="loading loading-spinner loading-md" aria-label="Loading" role="status"></span>

<!-- Inside a button during form submission -->
<button class="btn btn-primary" disabled>
  <span class="loading loading-spinner loading-sm"></span>
  Saving...
</button>

<!-- Full-page overlay -->
<div class="flex items-center justify-center h-screen">
  <span class="loading loading-dots loading-xl text-primary" aria-label="Loading" role="status"></span>
</div>
```

Animation styles: `loading-spinner` `loading-dots` `loading-ring` `loading-ball` `loading-bars` `loading-infinity`

Size modifiers: `loading-xs` through `loading-xl`. Color: `text-primary` through `text-error` (uses `currentColor`).

### .progress — Linear Progress Bar

```html
<!-- Determinate -->
<progress class="progress progress-primary w-56" value="60" max="100"></progress>

<!-- Indeterminate (animated sweep) — omit value attribute -->
<progress class="progress w-56"></progress>

<!-- With percentage label -->
<div class="w-56">
  <div class="flex justify-between text-sm mb-1">
    <span>Uploading</span>
    <span>60%</span>
  </div>
  <progress class="progress progress-success w-full" value="60" max="100"></progress>
</div>
```

Omitting `value` triggers the indeterminate animation — native HTML `<progress>` behavior. Width is controlled by Tailwind `w-*` utilities — `progress` has no intrinsic width.

Modifiers: `progress-primary` through `progress-error`

### .skeleton — Content Placeholder

```html
<!-- Text placeholder -->
<div class="skeleton h-4 w-48"></div>

<!-- Card skeleton -->
<div class="card w-64 bg-base-100 shadow">
  <div class="skeleton h-32 w-full"></div>
  <div class="card-body gap-3">
    <div class="skeleton h-4 w-36"></div>
    <div class="skeleton h-4 w-24"></div>
  </div>
</div>

<!-- Avatar + text row -->
<div class="flex items-center gap-4">
  <div class="skeleton w-12 h-12 rounded-full"></div>
  <div class="flex flex-col gap-2">
    <div class="skeleton h-4 w-32"></div>
    <div class="skeleton h-4 w-24"></div>
  </div>
</div>
```

`.skeleton` requires explicit `h-*` and `w-*` — it has no intrinsic size. The pulse animation uses `opacity` — do not apply `opacity` utilities to skeleton elements. Swap for real content via conditional rendering.

### .radial-progress — Circular Progress

```html
<div
  class="radial-progress text-primary"
  style="--value:70;"
  role="progressbar"
  aria-valuenow="70"
  aria-valuemin="0"
  aria-valuemax="100"
>
  70%
</div>

<div
  class="radial-progress text-success"
  style="--value:100; --size:8rem; --thickness:0.5rem;"
  role="progressbar"
  aria-valuenow="100"
  aria-valuemin="0"
  aria-valuemax="100"
>
  Done
</div>
```

CSS variables (must be set as inline styles):

| Variable | Default | Effect |
|----------|---------|--------|
| `--value` | — | **Required.** Progress percentage (0–100) |
| `--size` | `3.5rem` | Circle diameter |
| `--thickness` | derived | Ring stroke width |

Text inside is centered automatically — put the percentage label as inner content.

## Common Mistakes

- **Wrong**: `.loading` without `aria-label="Loading"` and `role="status"` — **Right**: Invisible to screen readers without these
- **Wrong**: `.skeleton` without explicit `h-*` and `w-*` — **Right**: Renders as zero-size
- **Wrong**: Setting `--value` on `.radial-progress` as a Tailwind class — **Right**: CSS custom properties require `style=""` or a `@layer` override
- **Wrong**: Leaving `.progress` in indeterminate state after operation completes — **Right**: Swap to a determinate value or hide the element
- **Wrong**: Applying `opacity-*` Tailwind utilities to `.skeleton` elements — **Right**: The pulse animation uses opacity internally; external opacity utilities break it

## See Also

- [Data Display Components](data-display-components.md) — `.toast` for success/error notifications after async operations
- [Actions Components](actions-components.md) — disabling `.btn` and adding `.loading` spinner during form submission
- Reference: https://daisyui.com/components/loading/
- Reference: https://daisyui.com/components/progress/
- Reference: https://daisyui.com/components/skeleton/
