---
description: Reference for DaisyUI form input components — input, fieldset, select, textarea, checkbox, toggle, range, and rating
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
| Range | `.range` | Numeric slider |
| Rating | `.rating` | Star rating input |

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

Modifiers: `input-primary` through `input-error` (focus border color) + `input-ghost` + sizes `input-xs` through `input-xl`

### .fieldset — Form Group (v5)

```html
<fieldset class="fieldset">
  <legend class="fieldset-legend">Account Details</legend>
  <label class="fieldset-label">Email</label>
  <input type="email" class="input w-full" placeholder="you@example.com" />
  <p class="fieldset-label text-error">Enter a valid email address</p>
</fieldset>
```

### .checkbox / .radio / .toggle

```html
<input type="checkbox" class="checkbox checkbox-primary" />
<input type="checkbox" class="toggle toggle-success toggle-lg" checked />
<input type="radio" class="radio radio-primary" />
```

All accept semantic color modifiers + sizes `xs` through `xl`.

### .range / .rating

```html
<input type="range" min="0" max="100" value="40" class="range range-primary" />

<div class="rating rating-lg">
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" aria-label="1 star" />
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked aria-label="2 stars" />
</div>
```

## Common Mistakes

- **Wrong**: Using old `form-control` wrapper class (v4) in v5 — **Right**: Replaced by `fieldset`
- **Wrong**: `input-bordered` in v5 — **Right**: This class no longer exists; borders are on by default. Use `input-ghost` to remove them
- **Wrong**: No `<label>` or `aria-label` for checkbox/radio/toggle — **Right**: Screen readers need explicit labels on `<input>` elements
- **Wrong**: Wrapper `<label class="input">` used in v4 style — **Right**: v5 changed the primary pattern to a wrapper label containing `<input>` for icon prefix/suffix support

## See Also

- [Customization Patterns](customization-patterns.md)
- Reference: `node_modules/daisyui/components/input/object.js`
- Reference: `node_modules/daisyui/components/fieldset/object.js`
