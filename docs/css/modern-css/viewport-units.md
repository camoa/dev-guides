---
description: "Fix 100vh on mobile with dvh, svh, lvh dynamic viewport units"
tldr: "Use `dvh` for hero sections that should fill the visible screen on mobile. Use `svh` for the app shell root container."
---

# Dynamic Viewport Units

## When to Use

> For layouts that need to fill the screen on mobile devices where the browser chrome (address bar) collapses and expands, causing classic `100vh` to overflow or shift the layout.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Hero section filling the visible screen on mobile | `100dvh` | Adjusts dynamically as browser chrome shows/hides |
| App shell that always fits — no overflow | `100svh` | Conservative — accounts for full chrome always visible |
| Desktop-only full-height element | `100vh` | Still fine; mobile chrome issue doesn't apply |
| Element height based on largest possible viewport | `100lvh` | Equal to viewport with chrome fully retracted |
| Same but for widths | `dvw`, `svw`, `lvw` | Same logic, inline axis |

## Pattern

```css
/* Hero — fills screen, adjusts as address bar shows/hides */
.hero {
  min-height: 100dvh;
}

/* App shell — conservative, always fits regardless of chrome state */
.app-layout {
  height: 100svh;
  display: flex;
  flex-direction: column;
}

/* Old pattern — causes overflow on iOS Safari when address bar is visible */
/* .hero { min-height: 100vh; } */
```

**Unit reference:**
| Unit | Meaning | Use case |
|---|---|---|
| `dvh` / `dvw` | Dynamic — updates as chrome shows/hides | Hero sections, fullscreen layouts |
| `svh` / `svw` | Small — assumes chrome always visible | App shells, fixed bottom bars |
| `lvh` / `lvw` | Large — assumes chrome always hidden | Background elements, max-size calculations |

**`dvh` caveat:** because `dvh` changes as the user scrolls (address bar retracts), content can shift. For most hero sections this is acceptable; avoid it for elements where layout shift is jarring.

**Browser support:** Chrome 108, Firefox 101, Safari 15.4. Widely available since 2022–2023. Safe to use.

## Common Mistakes

- Using `dvh` for the app shell root — the dynamic resizing causes layout shifts when the address bar moves; use `svh` for the root container
- Mixing `vh` and `dvh` in the same layout — creates inconsistent sizing between elements; choose one system per layout
- Not testing on real mobile devices — emulators often do not simulate address bar behavior accurately

## See Also

- Reference: [web.dev: Large, small, and dynamic viewport units](https://web.dev/blog/viewport-units)
