---
description: Reference for DaisyUI action components — button, dropdown, modal, and swap
tldr: "Interactive elements that trigger actions: buttons, dropdowns, modals, and content swap toggles."
---

# Actions Components

## When to Use

> Interactive elements that trigger actions: buttons, dropdowns, modals, and swap.

## Decision: Which Action Component

| Component | Class | Use for |
|-----------|-------|---------|
| Button | `.btn` | Any interactive trigger |
| Dropdown | `.dropdown` | Contextual menus, CSS-only |
| Modal | `.modal` | Overlay dialogs |
| Swap | `.swap` | Toggle between two visual states |

## .btn — Button

**Description:** Primary interactive element. Highly configurable via modifier classes.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `btn-primary` `btn-secondary` `btn-accent` `btn-neutral` `btn-info` `btn-success` `btn-warning` `btn-error` | Semantic color |
| `btn-ghost` | Transparent, no background until hover |
| `btn-link` | Styled as hyperlink with underline |
| `btn-outline` | Border + text color only, fills on hover |
| `btn-dash` | Dashed border variant |
| `btn-soft` | Muted/tinted background, less emphasis than solid |
| `btn-xs` `btn-sm` `btn-md` `btn-lg` `btn-xl` | Size scale |
| `btn-square` | Equal width/height (icon buttons) |
| `btn-circle` | Circular icon button |
| `btn-wide` | Max 16rem width |
| `btn-block` | Full width |
| `btn-active` | Force active state appearance |
| `btn-disabled` | Disabled styling (use `:disabled` attr for real disable) |

**Usage Example:**

```html
<button class="btn btn-primary btn-lg">Save Changes</button>
<button class="btn btn-ghost btn-sm">Cancel</button>
<button class="btn btn-outline btn-error">Delete</button>
<!-- Icon button -->
<button class="btn btn-circle btn-sm btn-ghost">
  <svg .../>
</button>
```

**Gotchas:**

- `btn-disabled` only adds visual styles — it does NOT set `disabled` attribute. Always add both `class="btn btn-disabled"` AND `disabled` attribute for real form buttons
- `btn-link` text color is `--color-primary` by default — pair with color modifiers for other colors: `btn-link btn-error`
- `btn` works on `<a>`, `<button>`, `<input type="submit">` equally

## .dropdown — Dropdown

**Description:** Positional container for dropdown menus. CSS-only by default; no JavaScript required.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `dropdown-top` `dropdown-bottom` `dropdown-left` `dropdown-right` | Position direction |
| `dropdown-start` `dropdown-center` `dropdown-end` | Alignment within direction |
| `dropdown-hover` | Open on hover instead of focus/click |
| `dropdown-open` | Force open state |

**Required structure:**

```html
<div class="dropdown">
  <div tabindex="0" role="button" class="btn">Open Menu</div>
  <ul class="dropdown-content menu bg-base-100 rounded-box shadow-lg w-52 p-2">
    <li><a>Option 1</a></li>
    <li><a>Option 2</a></li>
  </ul>
</div>
```

**Gotchas:**

- `tabindex="0"` on the trigger is required for CSS-only focus-based opening
- The `.menu` class inside `.dropdown-content` gives the list styling
- For React/JS-controlled dropdowns, use `dropdown-open` class toggled programmatically instead of relying on focus state

## .modal — Modal Dialog

**Description:** Full-screen overlay dialog. Supports CSS-only (checkbox), anchor (`#id`), and JS (`.modal-open`) activation methods.

**Required structure:**

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

**Position modifiers:** `modal-top` `modal-middle` `modal-bottom` `modal-start` `modal-end`

**Gotchas:**

- The `.modal-backdrop` click-outside-to-close requires the backdrop element with `for` attribute matching the toggle
- For `<dialog>` element usage: `<dialog class="modal">` opened via `dialog.showModal()` — the `[open]` attribute triggers DaisyUI's open state styles
- `z-index: 999` — stacks above most content, but below browser UI

## .swap — Swap Toggle

**Description:** Toggles between two elements using a hidden checkbox. Common use: sun/moon dark mode toggle icons.

```html
<label class="swap swap-rotate">
  <input type="checkbox" class="theme-controller" value="dark" />
  <svg class="swap-on ..."><!-- moon icon --></svg>
  <svg class="swap-off ..."><!-- sun icon --></svg>
</label>
```

`swap-rotate` `swap-flip` control the animation style.

## Common Mistakes

- Modals with `pointer-events: none` on closed state — if modal is not closing, check for missing `modal-toggle` id/for pair
- Dropdown not closing on mobile — add `tabindex="-1"` focus trap or use JS-controlled version
- Missing `role="dialog"` on modal — DaisyUI applies visual styles but NOT ARIA roles automatically

## See Also

- [Data Input Components](data-input-components.md) — form inputs
- [Security and Accessibility](security-accessibility.md)
- Reference: `react-design-system.md` Section 7 — dialog/modal patterns in React
- Reference: `node_modules/daisyui/components/button/object.js`
- Reference: `node_modules/daisyui/components/modal/object.js`
- Reference: `node_modules/daisyui/components/dropdown/object.js`
