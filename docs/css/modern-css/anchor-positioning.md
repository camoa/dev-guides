---
description: "Position tooltips relative to anchors natively — replace Popper.js"
tldr: "Use anchor positioning for tooltips, dropdowns, and overlays that need to follow their trigger across scroll container boundaries. Use `position: relative` + `position: absolute` on a parent when there is no scroll container concern and…"
---

# CSS Anchor Positioning

## When to Use

> To position tooltips, dropdowns, and overlays relative to a trigger element — replacing Popper.js, Floating UI, and manual `position: relative` + `position: absolute` patterns, especially when the popover crosses scroll container boundaries.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Tooltip/dropdown next to its trigger | Anchor Positioning | Works across scroll containers; old pattern breaks |
| Automatic repositioning when near viewport edge | `position-try-fallbacks` | Browser tries alternative positions automatically |
| Legacy tooltip with predictable behavior | `position: relative` on parent + `position: absolute` | Simpler when no cross-scroll-container concern |
| Maximum browser compatibility now | Floating UI polyfill | Safari support only recently arrived |

## Pattern

```css
/* Step 1 — name the anchor element */
.trigger {
  anchor-name: --my-tooltip-anchor;
}

/* Step 2 — position the tooltip relative to the anchor */
.tooltip {
  position: absolute;
  position-anchor: --my-tooltip-anchor;

  /* Place below the anchor, left-aligned */
  top: anchor(bottom);
  left: anchor(left);

  /* Auto-flip above if not enough space below */
  position-try-fallbacks: flip-block;
}
```

With Popover API for light dismiss:
```css
.trigger { anchor-name: --dropdown-anchor; }

.dropdown[popover] {
  position: absolute;
  position-anchor: --dropdown-anchor;
  top: calc(anchor(bottom) + 0.5rem);
  left: anchor(left);
  min-width: anchor-size(width);
}
```

**`anchor()` function:** references the anchor's edge. Values: `top`, `right`, `bottom`, `left`, `center`, `start`, `end`.

**`anchor-size()`:** reads the anchor's dimensions. Use for `min-width: anchor-size(width)` to match dropdown to button width.

**`position-try-fallbacks`:** space-separated list of alternative positions to try if the element overflows the viewport.
- `flip-block` — try flipping on the block axis (above/below)
- `flip-inline` — try flipping on the inline axis (left/right)
- `--custom-try` — reference a named `@position-try` rule

**Browser support:** Chrome 125+, Firefox 145 (behind flag; 149+ production). Safari 26. **Significant Safari and Firefox gaps until very recently.** Use `@supports` progressive enhancement:

```css
@supports (anchor-name: --test) {
  .tooltip { /* anchor positioning styles */ }
}
```

## Common Mistakes

- Using anchor positioning without `@supports` — Safari and Firefox support only arrived in 2025; older versions need a fallback
- Setting `position: fixed` instead of `position: absolute` — anchor positioning requires `position: absolute` (or `fixed` in limited cases); check spec behavior for your use case
- Anchoring to an element that is not a sibling or ancestor in DOM order — anchor positioning works across the DOM but behavior with stacking contexts can be surprising
- Expecting the anchor to auto-follow on scroll — it does, but only within the same scroll container; test with overflowing parents

## See Also

- ← [Popover API](popover-api.md) | [View Transitions](view-transitions.md) →
- Reference: [MDN CSS Anchor Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning)
