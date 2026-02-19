---
description: Reference for DaisyUI action components — button, dropdown, modal, and swap
---

# Actions Components

## When to Use

> Interactive elements that trigger actions: buttons, dropdowns, modals, and content swap toggles.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Button | `.btn` | Any interactive trigger |
| Dropdown | `.dropdown` | Contextual menus, CSS-only |
| Modal | `.modal` | Overlay dialogs |
| Swap | `.swap` | Toggle between two visual states |

## Pattern

### .btn — Button

```html
<button class="btn btn-primary btn-lg">Save Changes</button>
<button class="btn btn-ghost btn-sm">Cancel</button>
<button class="btn btn-outline btn-error">Delete</button>
<!-- Icon button -->
<button class="btn btn-circle btn-sm btn-ghost">
  <svg .../>
</button>
```

**Color modifiers:** `btn-primary` `btn-secondary` `btn-accent` `btn-neutral` `btn-info` `btn-success` `btn-warning` `btn-error`
**Style modifiers:** `btn-ghost` `btn-link` `btn-outline` `btn-dash` `btn-soft`
**Size modifiers:** `btn-xs` `btn-sm` `btn-md` `btn-lg` `btn-xl`
**Shape modifiers:** `btn-square` `btn-circle` `btn-wide` `btn-block`

### .dropdown — Dropdown

```html
<div class="dropdown">
  <div tabindex="0" role="button" class="btn">Open Menu</div>
  <ul class="dropdown-content menu bg-base-100 rounded-box shadow-lg w-52 p-2">
    <li><a>Option 1</a></li>
    <li><a>Option 2</a></li>
  </ul>
</div>
```

Position modifiers: `dropdown-top` `dropdown-bottom` `dropdown-left` `dropdown-right` + `dropdown-hover` `dropdown-open`

### .modal — Modal Dialog

```html
<!-- CSS-only checkbox method -->
<input type="checkbox" id="my-modal" class="modal-toggle" />
<label for="my-modal" class="btn btn-primary">Open Modal</label>

<div class="modal" role="dialog">
  <div class="modal-box">
    <h3 class="text-lg font-bold">Title</h3>
    <p class="py-4">Content here.</p>
    <div class="modal-action">
      <label for="my-modal" class="btn">Close</label>
    </div>
  </div>
  <label class="modal-backdrop" for="my-modal">Close</label>
</div>
```

### .swap — Toggle Between Two States

```html
<label class="swap swap-rotate">
  <input type="checkbox" class="theme-controller" value="dark" />
  <svg class="swap-on ..."><!-- moon icon --></svg>
  <svg class="swap-off ..."><!-- sun icon --></svg>
</label>
```

## Common Mistakes

- **Wrong**: Using `btn-disabled` without the `disabled` attribute — **Right**: Add both `class="btn btn-disabled"` AND `disabled` attribute; the class only adds visual styles
- **Wrong**: Dropdown without `tabindex="0"` on trigger — **Right**: `tabindex="0"` is required for CSS-only focus-based opening
- **Wrong**: Modal without `role="dialog"` — **Right**: DaisyUI applies visual styles but NOT ARIA roles; add `role="dialog"` manually
- **Wrong**: CSS-only modal for focus-critical flows — **Right**: CSS-only modal does not trap focus; use `<dialog>` element with `showModal()` or Radix UI Dialog

## See Also

- [Security and Accessibility](security-accessibility.md)
- [Data Input Components](data-input-components.md)
- Reference: `node_modules/daisyui/components/button/object.js`
- Reference: `node_modules/daisyui/components/modal/object.js`
- Reference: `node_modules/daisyui/components/dropdown/object.js`
