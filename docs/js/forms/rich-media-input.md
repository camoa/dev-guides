---
description: Rich HTML content inside <option> elements using the Customizable Select API — icons, images, and descriptions without JavaScript custom select widgets.
tldr: Use appearance:base-select + HTML in <option> for icon-and-label options. Older browsers strip HTML tags and render only text nodes — always include meaningful plain text. Add aria-label to options whose rich HTML would read badly when concatenated. Mark decorative SVGs aria-hidden="true".
drupal_version: ""
---

# Rich Media Input

## When to Use

> Use the Customizable Select API (`appearance: base-select`) when `<option>` elements need to display icons, images, descriptions, or other rich HTML content — replacing heavy JavaScript custom select widgets. Accept limited browser support (Chrome/Edge 135+) with plain-text graceful fallback.

## Decision

| Need | Pattern | Notes |
|------|---------|-------|
| Icon + label inside each option | `appearance: base-select` + HTML in `<option>` | Older browsers render text nodes only |
| Selected option mirrored in trigger | `<selectedcontent>` inside `<button>` | No JS needed to update the trigger |
| Hide description in button state | CSS on `selectedcontent .desc { display: none }` | Keeps trigger compact |
| Decorative SVG in option | `aria-hidden="true"` on the `<svg>` | Prevents redundant screen reader announcement |
| Accessible option name | `aria-label` on `<option>` | Overrides concatenated text read by AT |

**Baseline status: Limited availability.** Chrome 135+, Edge 135+. Not supported in Firefox or Safari.

## Pattern

```html
<label for="role-picker">Select your role</label>
<select class="rich-select" name="role" id="role-picker">
  <button>
    <selectedcontent></selectedcontent>
  </button>
  <option value="frontend" aria-label="Frontend Developer">
    <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24">
      <rect x="2" y="3" width="20" height="14" rx="2"></rect>
    </svg>
    <div class="opt-text">
      <span class="opt-title">Frontend Developer</span>
      <span class="opt-desc">React, Vue, CSS</span>
    </div>
  </option>
</select>
```

```css
.rich-select,
.rich-select::picker(select) { appearance: base-select; }

.rich-select option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
}

/* Hide description in trigger but keep in picker list */
.rich-select selectedcontent .opt-desc { display: none; }

/* Multiple indicators for checked state */
.rich-select option:checked {
  background-color: #3b82f6;
  color: #fff;
}
.rich-select option:checked .opt-title { font-weight: 700; }
```

**Fallback** — older browsers strip HTML tags and render only text nodes. Design option content so plain text is meaningful:

```html
<!-- Good: plain text readable without SVG -->
<option value="frontend" aria-label="Frontend Developer">
  <svg aria-hidden="true">…</svg>
  Frontend Developer
</option>

<!-- Bad: only an SVG — older browsers render nothing -->
<option value="frontend"><svg>…</svg></option>
```

**Top-layer rendering:** `::picker(select)` renders in the browser's top layer — no z-index conflicts. Positioned using native Anchor Positioning relative to trigger button width.

## Common Mistakes

- **No `aria-label` on options with icons and description text** → AT reads SVG + title + description as a concatenated string
- **Decorative SVG without `aria-hidden="true"`** → screen reader announces "image" before each option
- **Overriding ARIA roles on `<select>` or `<option>`** → breaks native keyboard navigation and AT semantics
- **No plain text in `<option>` as fallback** → older browsers render empty options
- **Missing `name` attribute on `<select>`** → form submission sends nothing

## See Also

- [Styling Native Select](styling-native-select.md) — `appearance: base-select` setup and branded styling
- Reference: MWG `rich-media-picker.md`
