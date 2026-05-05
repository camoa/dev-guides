---
description: Reference for DaisyUI layout components — drawer, hero, divider, join, indicator, stack, footer, and mask
tldr: "Page structure, sidebars, overlays, and content arrangement patterns. Use `lg:drawer-open` + `lg:hidden` for responsive sidebar. `.mask` clips visually but leaves the box model unchanged — always set explicit width and height."
---

# Layout Components

## When to Use

> Page structure, sidebars, overlays, and content arrangement patterns.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Sidebar | `.drawer` | Slide-in navigation panel |
| Landing section | `.hero` | Full-width hero/banner area |
| Separator | `.divider` | Horizontal or vertical dividers with optional label |
| Grouped elements | `.join` | Merge adjacent borders between components |
| Positional badge | `.indicator` | Overlay a badge on a component |
| Overlapping stack | `.stack` | Card pile / layered effect |
| Page footer | `.footer` | Multi-column link groups and copyright bar |
| Shape clip | `.mask` | Clip an element to a non-rectangular shape |

## Pattern

### .drawer — Sidebar Navigation

```html
<div class="drawer lg:drawer-open">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" />

  <div class="drawer-content flex flex-col">
    <div class="navbar bg-base-100">
      <label for="my-drawer" class="btn btn-ghost drawer-button lg:hidden">
        <!-- hamburger icon -->
      </label>
    </div>
    <main class="flex-1 p-6">Page content</main>
  </div>

  <div class="drawer-side">
    <label for="my-drawer" class="drawer-overlay" aria-label="Close sidebar"></label>
    <ul class="menu bg-base-200 min-h-full w-64 p-4">
      <li><a>Dashboard</a></li>
    </ul>
  </div>
</div>
```

`lg:drawer-open` + `lg:hidden` on hamburger is the standard responsive pattern. `drawer-end` puts sidebar on the right.

### .hero

```html
<div class="hero min-h-screen bg-base-200">
  <div class="hero-content text-center">
    <div class="max-w-md">
      <h1 class="text-5xl font-bold">Hello</h1>
      <p class="py-6">Description text.</p>
      <button class="btn btn-primary">Get Started</button>
    </div>
  </div>
</div>
```

`hero-content` can be `flex-col lg:flex-row` for side-by-side image + text.

### .divider

```html
<div class="divider">OR</div>
<div class="divider divider-primary">Section</div>
<div class="divider divider-vertical h-24">AND</div>
```

Color modifiers: `divider-primary` through `divider-error` + `divider-start` `divider-end`

### .join — Group Adjacent Components

```html
<div class="join">
  <input class="input join-item" placeholder="Email" />
  <button class="btn btn-primary join-item">Subscribe</button>
</div>
```

Each child needs `join-item`. Works with `.btn`, `.input`, `.select`, `.badge`.

### .indicator

```html
<div class="indicator">
  <span class="indicator-item badge badge-secondary">99+</span>
  <button class="btn">Notifications</button>
</div>
```

Position modifiers: `indicator-top` `indicator-middle` `indicator-bottom` + `indicator-start` `indicator-center` `indicator-end`

### .stack — Overlapping Cards

```html
<div class="stack">
  <div class="card bg-primary text-primary-content">Card 3</div>
  <div class="card bg-secondary text-secondary-content">Card 2</div>
  <div class="card bg-base-100">Card 1 (top)</div>
</div>
```

Stacks children with offset overlap — good for card pile effects.

### .footer

```html
<footer class="footer bg-base-200 text-base-content p-10">
  <nav>
    <h6 class="footer-title">Services</h6>
    <a class="link link-hover">Branding</a>
    <a class="link link-hover">Design</a>
  </nav>
  <nav>
    <h6 class="footer-title">Company</h6>
    <a class="link link-hover">About us</a>
    <a class="link link-hover">Contact</a>
  </nav>
</footer>

<!-- Copyright bar -->
<footer class="footer footer-center bg-base-300 text-base-content p-4">
  <aside>
    <p>Copyright © 2025 — All rights reserved</p>
  </aside>
</footer>
```

`.footer` is `display: grid` with auto column sizing — columns form based on `<nav>` or `<aside>` children. `.footer-title` adds `opacity-60` and uppercase letter-spacing. Modifiers: `footer-horizontal` `footer-center`.

### .mask — Shape Clipping

```html
<!-- Squircle avatar -->
<div class="avatar">
  <div class="w-16 mask mask-squircle">
    <img src="/user.jpg" alt="User" />
  </div>
</div>

<!-- Half-masks for split-color effects -->
<div class="flex">
  <div class="mask mask-star-2 mask-half-1 bg-primary w-8 h-8"></div>
  <div class="mask mask-star-2 mask-half-2 bg-base-300 w-8 h-8"></div>
</div>
```

Shape modifiers: `mask-squircle` `mask-circle` `mask-heart` `mask-star` `mask-star-2` `mask-hexagon` `mask-hexagon-2` `mask-decagon` `mask-pentagon` `mask-diamond` `mask-square` `mask-triangle` (+ `-2` `-3` `-4`) `mask-half-1` `mask-half-2`

`mask` clips content visually but the element's box model (hover areas, spacing) is unchanged. Always set explicit width and height.

## Common Mistakes

- **Wrong**: `drawer-toggle` checkbox not a direct sibling of `drawer-content` and `drawer-side` — **Right**: DOM structure must be exact; nesting breaks CSS positioning
- **Wrong**: `hero` without `min-h-screen` when full viewport height is desired — **Right**: The class doesn't force height on its own
- **Wrong**: `.mask` without explicit `w-*` and `h-*` — **Right**: Without dimensions, mask has nothing to clip
- **Wrong**: `<div class="footer">` — **Right**: Use `<footer>` semantic HTML for landmark navigation

## See Also

- [Navigation Components](navigation-components.md) — menu inside drawer
- [Actions Components](actions-components.md) — modal for overlay dialogs
- Reference: `node_modules/daisyui/components/drawer/object.js`
