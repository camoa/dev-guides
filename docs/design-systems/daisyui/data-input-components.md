---
description: Reference for DaisyUI form input components — input, fieldset, select, textarea, checkbox, toggle, range, rating, file-input, floating-label, validator, calendar, and filter
tldr: "Form elements: text fields, selections, toggles, form structure, file pickers, floating labels, and CSS-driven validation display. Replace v4's `form-control` with `fieldset`. Use `.validator` only with native HTML validation attributes."
---

# Data Input Components

## When to Use

> Form elements: text fields, selections, toggles, and form structure.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Text input | `.input` | Single-line text, email, search |
| Form group | `.fieldset` | Label + input + help text grouping (v5) |
| Select | `.select` | Dropdown selection |
| Multi-line | `.textarea` | Long-form text |
| Boolean | `.checkbox` | True/false selection |
| On/off | `.toggle` | Styled boolean switch |
| Radio | `.radio` | Single-select from group |
| Range | `.range` | Numeric slider |
| Rating | `.rating` | Star rating input |
| File picker | `.file-input` | Styled file upload field |
| Animated label | `.floating-label` | Placeholder-style label that animates on focus (v5) |
| CSS validation | `.validator` | Show/hide hints using native `:valid`/`:invalid` state |
| Calendar styling | `.calendar` | Skin for third-party datepicker libraries |
| Filter chips | `.filter` | Radio/checkbox inputs styled as selectable pill chips |

## Pattern

### .input — Text Input

```html
<!-- Wrapper pattern (supports prefix/suffix icons) -->
<label class="input input-primary flex items-center gap-2">
  <svg .../>
  <input type="text" class="grow" placeholder="Search" />
</label>

<!-- Direct input -->
<input type="text" class="input w-full" placeholder="Email" />
```

Modifiers: `input-primary` through `input-error` (focus border color) + `input-ghost` + sizes `input-xs` through `input-xl`. Borders are on by default in v5 — use `input-ghost` to remove them.

### .fieldset — Form Group (v5)

```html
<fieldset class="fieldset">
  <legend class="fieldset-legend">Account Details</legend>
  <label class="fieldset-label">Email</label>
  <input type="email" class="input w-full" placeholder="you@example.com" />
  <p class="fieldset-label text-error">Enter a valid email address</p>
</fieldset>
```

Replaces the `form-control` class from v4. Do not use `form-control` in v5 projects.

### .checkbox / .radio / .toggle

```html
<input type="checkbox" class="checkbox checkbox-primary" />
<input type="checkbox" class="toggle toggle-success toggle-lg" checked />
<input type="radio" class="radio radio-primary" />
```

All accept semantic color modifiers + sizes `xs` through `xl`. Always wrap related radios with a `<fieldset>` and provide `<legend>`.

### .range / .rating

```html
<input type="range" min="0" max="100" value="40" class="range range-primary" />

<div class="rating rating-lg">
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" aria-label="1 star" />
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked aria-label="2 stars" />
</div>
```

`.rating` uses radio inputs with `.mask` to clip to star shape. `aria-label` is required on each radio input.

### .file-input — File Upload

```html
<input type="file" class="file-input file-input-primary w-full" />

<!-- Ghost variant -->
<input type="file" class="file-input file-input-ghost w-full" />
```

Modifiers: `file-input-primary` through `file-input-error` + sizes `file-input-xs` through `file-input-xl`. Always pair with a `<label>` for accessibility. The browser's native file picker UI is not replaceable.

### .floating-label — Animated Floating Label (v5)

```html
<label class="floating-label">
  <span>Email address</span>
  <input type="email" class="input" placeholder="Email address" />
</label>
```

The `placeholder` attribute must match the label text — CSS uses `:placeholder-shown` to detect the empty state. Not available in v4.

### .validator — CSS Validation Display

```html
<input
  type="email"
  class="input validator"
  required
  placeholder="user@example.com"
/>
<p class="validator-hint">Must be a valid email address</p>
```

Relies on native HTML validation attributes (`required`, `type="email"`, `pattern`, etc.). Without them, `:valid`/`:invalid` never trigger. The hint text is hidden by default and shown only on `:invalid` state.

### .calendar — Calendar Styling Skin

```html
<!-- Requires a JS library (e.g. Cally web component) -->
<calendar-date class="calendar">
  <svg slot="previous"><!-- left arrow --></svg>
  <svg slot="next"><!-- right arrow --></svg>
</calendar-date>
```

`.calendar` is a CSS skin only — it provides no calendar logic. DaisyUI's calendar CSS targets Cally web component element selectors.

### .filter — Filter Chips

```html
<div class="filter">
  <input class="btn filter-reset" type="radio" name="category" aria-label="All" checked />
  <input class="btn btn-sm" type="radio" name="category" aria-label="Electronics" />
  <input class="btn btn-sm" type="radio" name="category" aria-label="Clothing" />
</div>
```

Chip labels come from `aria-label` — rendered via `content: attr(aria-label)`. Use `type="radio"` for single-select, `type="checkbox"` for multi-select. Add JavaScript to listen for change events to filter content.

## Common Mistakes

- **Wrong**: Using old `form-control` wrapper class (v4) in v5 — **Right**: Replaced by `fieldset`
- **Wrong**: `input-bordered` in v5 — **Right**: This class no longer exists; borders are on by default. Use `input-ghost` to remove them
- **Wrong**: No `<label>` or `aria-label` for checkbox/radio/toggle — **Right**: Screen readers need explicit labels on `<input>` elements
- **Wrong**: Using `.validator` without native HTML validation attributes — **Right**: No `required`/`type`/`pattern` means `:invalid` never fires
- **Wrong**: Floating label without matching `placeholder` attribute — **Right**: `:placeholder-shown` requires the placeholder to detect the empty state

## See Also

- [Customization Patterns](customization-patterns.md)
- [Security and Accessibility](security-accessibility.md)
- Reference: `node_modules/daisyui/components/input/object.js`
- Reference: `node_modules/daisyui/components/fieldset/object.js`
