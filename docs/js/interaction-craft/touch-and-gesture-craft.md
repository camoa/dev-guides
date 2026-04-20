---
description: Detect swipes, pinch-to-zoom, and long-press with Pointer Events API — touch-action CSS, passive listeners, and 300ms tap delay
tldr: "Use Pointer Events API for all gestures — it handles mouse, touch, and pen uniformly. Use `touch-action` CSS to declare which axes you own so the browser can optimize scrolling."
---

# Touch and Gesture Craft

## When to Use

> Use Pointer Events API for all gestures — it handles mouse, touch, and pen uniformly. Use `touch-action` CSS to declare which axes you own so the browser can optimize scrolling.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Swipe left/right detection | `pointerdown`/`pointermove`/`pointerup` | Unified across mouse + touch + pen |
| Pinch-to-zoom | Pointer Events with multi-pointer tracking | Only way to track two concurrent pointers cleanly |
| Long-press | `pointerdown` + `setTimeout` (500ms) + cancel on move | No native event; build from pointer lifecycle |
| Swipe that doesn't conflict with scroll | `touch-action: pan-x` on swipeable axis | Tells browser which axis you own; prevents passive listener conflict |
| Legacy browser touch support | `touchstart`/`touchmove`/`touchend` | Only if Pointer Events cannot be used |

**CSS touch-action reference:**

| Value | Meaning |
|---|---|
| `auto` | Browser controls all gestures |
| `none` | You control all gestures |
| `pan-x` | Browser handles vertical scroll; you handle horizontal swipe |
| `pan-y` | Browser handles horizontal scroll; you handle vertical swipe |
| `manipulation` | Enables panning and pinch-zoom; eliminates 300ms tap delay |

## Pattern

```javascript
// Swipe detection
function detectSwipe(element, { threshold = 50, velocity = 0.3 } = {}) {
  let start = null;
  element.addEventListener('pointerdown', (e) => {
    start = { x: e.clientX, y: e.clientY, time: Date.now() };
    element.setPointerCapture(e.pointerId); // Track even if pointer leaves element
  });
  element.addEventListener('pointerup', (e) => {
    if (!start) return;
    const dx = e.clientX - start.x, dy = e.clientY - start.y;
    const speed = Math.abs(dx) / (Date.now() - start.time);
    if (Math.abs(dx) > threshold && Math.abs(dx) > Math.abs(dy) && speed > velocity) {
      element.dispatchEvent(new CustomEvent('swipe', { bubbles: true, detail: { direction: dx > 0 ? 'right' : 'left', speed } }));
    }
    start = null;
  });
  element.addEventListener('pointercancel', () => { start = null; });
}

// Pinch-to-zoom
function detectPinch(element, onScale) {
  const pointers = new Map();
  let initialDistance = null;
  const dist = (a, b) => Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY);
  element.addEventListener('pointerdown', (e) => {
    pointers.set(e.pointerId, e);
    if (pointers.size === 2) { const [a, b] = [...pointers.values()]; initialDistance = dist(a, b); }
  });
  element.addEventListener('pointermove', (e) => {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, e);
    if (pointers.size === 2 && initialDistance) {
      const [a, b] = [...pointers.values()]; onScale(dist(a, b) / initialDistance);
    }
  });
  ['pointerup', 'pointercancel'].forEach(type =>
    element.addEventListener(type, (e) => { pointers.delete(e.pointerId); if (pointers.size < 2) initialDistance = null; })
  );
}
```

```css
/* Eliminate 300ms tap delay globally */
html { touch-action: manipulation; }
```

## Common Mistakes

- **Wrong**: Using `touchstart`/`touchmove` when Pointer Events work in target browsers → **Right**: Consolidate to Pointer Events
- **Wrong**: Not calling `setPointerCapture()` → **Right**: Without it, fast swipes lose the pointer when it leaves the element
- **Wrong**: `preventDefault()` in a passive listener → **Right**: Set `{ passive: false }` explicitly; it silently fails otherwise
- **Wrong**: Swipe threshold below 20px → **Right**: Use 50px minimum; low thresholds trigger on accidental scroll
- **Wrong**: Ignoring `pointercancel` → **Right**: Always handle it; phone calls and context menus can cancel mid-gesture
- **Wrong**: Touch targets under 44px → **Right**: WCAG failure; use padding to grow hit area without changing layout

## See Also

- [Drag and Drop Craft](./drag-and-drop-craft.md) — Pointer Events for cross-device drag
- [Performance and Event Handling](./performance-and-event-handling.md) — passive event listener impact on scroll
- Reference: [MDN: Pinch Zoom Gestures with Pointer Events](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events/Pinch_zoom_gestures)
- Reference: [Chrome: 300ms tap delay gone away](https://developer.chrome.com/blog/300ms-tap-delay-gone-away)
