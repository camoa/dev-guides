---
description: Native dropdowns and overlays with Popover API — built-in light dismiss
---

# Popover API

## When to Use

> Use `popover` for tooltips, dropdowns, and non-modal overlays that need light dismiss (closes on outside click or Escape key). Use `<dialog>` when you need a modal with focus trap.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Dropdown or tooltip that auto-closes on outside click | `popover` attribute | Light dismiss is built in |
| Modal dialog requiring focus trap | `<dialog>` element | Popovers do not trap focus |
| Tooltip anchored next to a trigger | Popover API + [Anchor Positioning](anchor-positioning.md) | Native positioning without Popper.js |
| Only one popover open at a time | `popover="auto"` (default) | Auto popovers close others; `popover="manual"` keeps them open |
| Complex open/close state with callbacks | JS API (`showPopover()`, `hidePopover()`, `toggle` event) | Full programmatic control available |

## Pattern

```html
<button popovertarget="my-menu" popovertargetaction="toggle">
  Open Menu
</button>

<div id="my-menu" popover>
  <nav>
    <a href="/page-1">Page 1</a>
    <a href="/page-2">Page 2</a>
  </nav>
</div>
```

```css
/* Animate popover entry and exit */
[popover] {
  opacity: 0;
  translate: 0 -0.5rem;
  transition:
    opacity 0.2s,
    translate 0.2s,
    display 0.2s allow-discrete,
    overlay 0.2s allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  translate: 0 0;

  @starting-style {
    opacity: 0;
    translate: 0 -0.5rem;
  }
}
```

**`popover` attribute values:**
- `popover` or `popover="auto"` — light dismiss, only one auto popover open at a time
- `popover="manual"` — no light dismiss, no automatic close; open/close via JS or `popovertarget`

**JS API:**
```js
const el = document.getElementById('my-menu');
el.showPopover();
el.hidePopover();
el.togglePopover();
el.addEventListener('toggle', (e) => {
  console.log(e.newState); // 'open' or 'closed'
});
```

**Browser support:** Chrome 114, Firefox 125, Safari 18.3 (full light-dismiss support). Baseline newly available January 2025. Safe to use.

## Common Mistakes

- **Wrong**: Using `popover` for modal dialogs that need focus trap → **Right**: Popover does not trap focus; use `<dialog>` with `showModal()`
- **Wrong**: Nesting a popover inside `overflow: hidden` expecting clipping → **Right**: Popovers render in the top layer; they are not clipped, but positioning can break without Anchor Positioning
- **Wrong**: Expecting `popover="auto"` to stack multiple open popovers → **Right**: It closes other auto popovers; use `popover="manual"` for nested or stacked menus
- **Wrong**: Forgetting animation requires `@starting-style` and `allow-discrete` → **Right**: The entry animation pattern is the same as `@starting-style` transitions

## See Also

- [@starting-style & Discrete Transitions](starting-style-transitions.md)
- [Anchor Positioning](anchor-positioning.md)
- Reference: [MDN Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)
