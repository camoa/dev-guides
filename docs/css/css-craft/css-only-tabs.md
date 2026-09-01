---
description: CSS-only tabs and toggles — radio input tab patterns, toggle switches, dark mode toggle with :has()
tldr: "Use radio inputs + `:checked` + sibling selectors for CSS-only tab interfaces. Add ARIA roles for accessibility."
---

# CSS-Only Tabs & Toggles

## When to Use

> Use radio inputs + `:checked` + sibling selectors for CSS-only tab interfaces. Add ARIA roles for accessibility. Switch to JavaScript when you have more than 5 panels.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Tab interface | Radio inputs + `:checked` + sibling selectors | CSS-only state management |
| Toggle panel (show/hide) | `<details>` or checkbox + `:checked` | Built-in toggle |
| Segmented control | Radio inputs styled as buttons | Same pattern as tabs |
| Content switcher (A/B) | Checkbox `:checked` + sibling selectors | Binary toggle |
| Dark mode toggle | Checkbox `:checked` + `:has()` on `html` | Parent-based state |

## Pattern: Toggle Switch

```css
.toggle {
  position: relative;
  width: 48px;
  height: 28px;
}

.toggle__input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.toggle__track {
  width: 100%;
  height: 100%;
  background: oklch(80% 0 0);
  border-radius: 14px;
  transition: background 0.2s;
}

.toggle__input:checked + .toggle__track {
  background: var(--color-primary);
}

.toggle__track::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 1px 3px oklch(0% 0 0 / 0.2);
  transition: transform 0.2s var(--ease-standard);
}

.toggle__input:checked + .toggle__track::after {
  transform: translateX(20px);
}
```

## Pattern

```html
<div class="tabs">
  <input type="radio" name="tab" id="tab1" checked class="tabs__input">
  <label for="tab1" class="tabs__label">Tab 1</label>
  <input type="radio" name="tab" id="tab2" class="tabs__input">
  <label for="tab2" class="tabs__label">Tab 2</label>
  <div class="tabs__panel" id="panel1">Content 1</div>
  <div class="tabs__panel" id="panel2">Content 2</div>
</div>
```
```css
.tabs__input { position: absolute; opacity: 0; pointer-events: none; }
.tabs__label {
  display: inline-block; padding: 0.75rem 1.5rem;
  cursor: pointer; border-bottom: 2px solid transparent;
  transition: border-color 0.2s, color 0.2s;
}
.tabs__input:checked + .tabs__label {
  border-bottom-color: var(--color-primary); color: var(--color-primary);
}
.tabs__input:focus-visible + .tabs__label {
  outline: 2px solid var(--color-primary); outline-offset: 2px;
}
.tabs__panel { display: none; }
#tab1:checked ~ #panel1,
#tab2:checked ~ #panel2 { display: block; }

/* Dark mode toggle with :has() */
html:has(#dark-toggle:checked) {
  color-scheme: dark;
  --bg: oklch(15% 0 0);
  --text: oklch(90% 0 0);
}
```

**Accessibility:** Add `role="tablist"` on container, `role="tab"` on labels, `role="tabpanel"` on panels. Toggle switches need `role="switch"` and `aria-checked`.

## Common Mistakes

- **Using `display: none` on radio inputs** — breaks keyboard navigation; use `opacity: 0` with positioning
- **Missing focus styles** — hidden radio inputs need `:focus-visible + label` styling
- **Not adding ARIA roles** — CSS-only tabs need ARIA attributes for screen readers
- **Too many tabs** — CSS-only tabs with >5 panels get unwieldy; use JS at that point

## See Also

- [CSS-Only Accordions](css-only-accordions.md) → vertical show/hide
- [CSS-Only Popovers](css-only-popovers.md) → click-triggered panels
- [Modern CSS Craft Patterns](modern-css-craft-patterns.md) → `@starting-style` panel entry animations
