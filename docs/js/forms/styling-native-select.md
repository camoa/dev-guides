---
description: Styling native <select> elements — accent-color for basic tinting, appearance:base-select for full brand control, animated pickers, and grid picker layouts.
tldr: appearance:base-select is Chrome/Edge 135+ only; degrades gracefully to OS native on other browsers. Apply to both the element AND ::picker(select) or the picker retains OS styling. Grid picker layouts do not give 2D keyboard navigation — Up/Down arrows only. Guard all animations with prefers-reduced-motion.
drupal_version: ""
---

# Styling Native Select

## When to Use

> Use `accent-color` for lightweight brand-tinting of checkboxes, radios, ranges, and progress elements. Use the Customizable Select API (`appearance: base-select`) when your design system requires pixel-perfect `<select>` styling — and you can accept Chrome/Edge-only support with native OS fallback everywhere else.

## Decision

| Need | Pattern | Browser Support |
|------|---------|-----------------|
| Brand-tint checkbox / radio / range | `accent-color` | Widely available (Chrome 93+, FF 92+, Edge 93+; limited Safari) |
| Custom dropdown arrow, basic styling | `appearance: none` + CSS | Widely available |
| Full brand control over `<select>` | `appearance: base-select` | Limited — Chrome 135+, Edge 135+ only |
| Grid/Flexbox picker layout | `appearance: base-select` + `::picker(select)` | Limited |
| Animated open/close picker | `appearance: base-select` + `@starting-style` | Limited |
| Validation state on `<select>` | `:user-invalid` / `:user-valid` | Widely available (Baseline 2023) |

## Pattern

**accent-color (widely available):**

```css
:root { --brand: #6200ee; }
body  { accent-color: var(--brand); }
@media (prefers-color-scheme: dark) { :root { --brand: #bb86fc; } }
```

**Customizable Select API opt-in:**

```css
/* Apply to BOTH element and picker */
.brand-select,
.brand-select::picker(select) { appearance: base-select; }

.brand-select {
  background: #fffaf0;
  border: 2px dashed #8b4513;
  border-radius: 4px;
  padding: 0.75rem;
}
```

**HTML with custom trigger:**

```html
<select class="brand-select" id="pref" name="pref">
  <button>
    <selectedcontent></selectedcontent>
  </button>
  <option value="standard">Standard</option>
  <option value="express" selected>Express</option>
</select>
```

**Animated picker** (requires `interpolate-size: allow-keywords` on `:root`):

```css
.animated-select::picker(select) {
  opacity: 0; height: 0;
  transition: display 0.4s allow-discrete, opacity 0.4s ease, height 0.4s ease;
}
.animated-select:open::picker(select) { opacity: 1; height: auto; }
@starting-style { .animated-select:open::picker(select) { opacity: 0; height: 0; } }

@media (prefers-reduced-motion: reduce) {
  .animated-select::picker(select) { transition: none !important; }
}
```

**Internal pseudo-elements:**

| Pseudo-element | Targets |
|---|---|
| `::picker(select)` | The dropdown options list |
| `::picker-icon` | The dropdown arrow icon |
| `option::checkmark` | Checkmark beside active option |
| `<selectedcontent>` | Trigger button content (mirrors selected option) |

## Common Mistakes

- **`appearance: base-select` only on `<select>`, not `::picker(select)`** → picker retains OS styling
- **Grid layout implying 2D keyboard navigation** → native `<select>` only navigates Up/Down; spatial grid is visual only
- **Missing `prefers-reduced-motion` guard** → motion-sensitive users experience forced animation
- **`accent-color` without checking contrast** → known bugs in Safari and Chrome Android
- **Expecting `appearance: base-select` in Firefox or Safari** → not supported; degrade gracefully

## See Also

- [Rich Media Input](rich-media-input.md) — rich HTML content inside options
- [user-valid and user-invalid](../../css/modern-css/user-valid-invalid.md) — full `:user-invalid` coverage
- Reference: MWG `branded-select-styling.md`, `custom-select-picker-layouts.md`, `animated-select-picker.md`
