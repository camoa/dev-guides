---
description: "Detect swipes, pinch-to-zoom, and long-press with Pointer Events API — touch-action CSS, passive listeners, and 300ms tap delay"
tldr: "Use Pointer Events API for all gestures — it handles mouse, touch, and pen uniformly. Use `touch-action` CSS to declare which axes you own so the browser can optimize scrolling."
---

# Touch and Gesture Craft

## When to Use

> Mobile-first interfaces where swipe, pinch, or long-press are natural interactions. The Pointer Events API (not touch events) is now the right abstraction — it handles mouse, touch, and pen uniformly.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Swipe left/right detection | `pointerdown`/`pointermove`/`pointerup` | Unified across mouse + touch + pen |
| Pinch-to-zoom | Pointer Events with multi-pointer tracking | Only way to track two concurrent pointers cleanly |
| Long-press | `pointerdown` + `setTimeout` (500ms) + cancel on move | No native event; build from pointer lifecycle |
| Swipe that doesn't conflict with scroll | `touch-action: pan-x` on swipeable axis | Tells browser which axis you own; prevents passive listener conflict |
| Legacy browser touch support | `touchstart`/`touchmove`/`touchend` | Only if you cannot use Pointer Events |

**pointerType disambiguation:**

```javascript
element.addEventListener('pointerdown', (e) => {
  if (e.pointerType === 'touch') { /* finger */ }
  if (e.pointerType === 'mouse') { /* mouse — don't add delay */ }
  if (e.pointerType === 'pen')   { /* stylus — may need pressure */ }
});
```

## Pattern: Swipe Detection

```javascript
function detectSwipe(element, { threshold = 50, velocity = 0.3 } = {}) {
  let start = null;

  element.addEventListener('pointerdown', (e) => {
    start = { x: e.clientX, y: e.clientY, time: Date.now() };
    element.setPointerCapture(e.pointerId);   // Track pointer even if it leaves element
  });

  element.addEventListener('pointerup', (e) => {
    if (!start) return;
    const dx = e.clientX - start.x;
    const dy = e.clientY - start.y;
    const elapsed = Date.now() - start.time;
    const speed = Math.abs(dx) / elapsed;

    if (Math.abs(dx) > threshold && Math.abs(dx) > Math.abs(dy) && speed > velocity) {
      element.dispatchEvent(new CustomEvent('swipe', {
        bubbles: true, detail: { direction: dx > 0 ? 'right' : 'left', speed }
      }));
    }
    start = null;
  });

  element.addEventListener('pointercancel', () => { start = null; });
}
```

## Pattern: Pinch-to-Zoom

```javascript
function detectPinch(element, onScale) {
  const pointers = new Map();
  let initialDistance = null;

  function getDistance(a, b) {
    return Math.hypot(b.clientX - a.clientX, b.clientY - a.clientY);
  }

  element.addEventListener('pointerdown', (e) => {
    pointers.set(e.pointerId, e);
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()];
      initialDistance = getDistance(a, b);
    }
  });

  element.addEventListener('pointermove', (e) => {
    if (!pointers.has(e.pointerId)) return;
    pointers.set(e.pointerId, e);
    if (pointers.size === 2 && initialDistance) {
      const [a, b] = [...pointers.values()];
      onScale(getDistance(a, b) / initialDistance);
    }
  });

  ['pointerup', 'pointercancel'].forEach(type => {
    element.addEventListener(type, (e) => {
      pointers.delete(e.pointerId);
      if (pointers.size < 2) initialDistance = null;
    });
  });
}
```

## Passive Listeners and touch-action

**The passive listener problem:** `touchstart` and `touchmove` default to passive in modern browsers (Chrome 51+, Firefox 49+). If you call `preventDefault()` in a passive listener, it silently fails — the browser scrolls anyway. To prevent scroll and handle your gesture, you must explicitly opt out:

```javascript
// Must opt out of passive to call preventDefault()
element.addEventListener('touchmove', handleGesture, { passive: false });

// Better — use CSS to declare which axes you own
element.style.touchAction = 'pan-y'; // You handle horizontal; browser handles vertical scroll
```

**CSS touch-action reference:**

| Value | Meaning |
|---|---|
| `auto` | Browser controls all gestures |
| `none` | You control all gestures (preventDefault works) |
| `pan-x` | Browser handles vertical scroll; you handle horizontal swipe |
| `pan-y` | Browser handles horizontal scroll; you handle vertical swipe |
| `manipulation` | Enables panning and pinch-zoom; eliminates 300ms tap delay |
| `pinch-zoom` | Browser handles pinch-zoom; you handle everything else |

## 300ms Tap Delay

The 300ms delay was added for double-tap-to-zoom detection. Modern solution: `touch-action: manipulation` in CSS eliminates it without removing pinch-zoom. FastClick is not needed for modern browsers (Chrome 32+, iOS 9.3+).

```css
/* Eliminates 300ms delay globally */
html { touch-action: manipulation; }
```

## Touch Target Sizing

Minimum 44×44 CSS pixels for any interactive touch target (WCAG 2.5.5, Level AAA). For dense UIs, use padding rather than increasing element size — the hit area grows without changing layout. WCAG 2.5.8 (Target Size, AA) adds a 24×24px minimum in WCAG 2.2.

## Common Mistakes

- **Using `touchstart`/`touchmove` when Pointer Events work in all target browsers** — unnecessary code paths; consolidate to Pointer Events
- **Not calling `setPointerCapture()`** — pointer leaves element during fast swipe, pointerup fires on wrong target
- **Passive listener with `preventDefault()` call** — silently fails in modern browsers; set `{ passive: false }` explicitly
- **Swipe threshold too low (< 20px)** — every accidental scroll triggers swipe; use 50px minimum
- **Ignoring `pointercancel`** — gesture state machine gets stuck when phone call or context menu cancels the pointer
- **Touch targets under 44px** — fails WCAG 2.5.5 (Level AAA) and is frustrating on real devices; 24×24 under 2.5.8 is the Level AA floor

## See Also

- [Drag and Drop Craft](./drag-and-drop-craft.md) — Pointer Events for cross-device drag
- [Performance and Event Handling](./performance-and-event-handling.md) — passive event listener impact on scroll
- Reference: [MDN: Pinch Zoom Gestures with Pointer Events](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events/Pinch_zoom_gestures)
- Reference: [Chrome: 300ms tap delay gone away](https://developer.chrome.com/blog/300ms-tap-delay-gone-away)
