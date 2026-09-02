---
description: Reference for DaisyUI layout components — drawer, hero, divider, join, indicator, stack, footer, and mask
tldr: "Page structure, sidebars, overlays, and content arrangement patterns. Use `lg:drawer-open` + `lg:hidden` for responsive sidebar. `.mask` clips visually but leaves the box model unchanged — always set explicit width and height."
---

# Layout Components

## When to Use

> Page structure, sidebars, overlays, and content arrangement patterns.

## Decision: Which Layout Component

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

## .drawer — Sidebar Navigation

**Description:** Slide-in sidebar panel. CSS-only via hidden checkbox toggle.

**Structure:**

```html
<div class="drawer lg:drawer-open">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" />

  <!-- Main content -->
  <div class="drawer-content flex flex-col">
    <div class="navbar bg-base-100">
      <label for="my-drawer" class="btn btn-ghost drawer-button lg:hidden">
        <!-- hamburger icon -->
      </label>
    </div>
    <main class="flex-1 p-6">Page content</main>
  </div>

  <!-- Sidebar -->
  <div class="drawer-side">
    <label for="my-drawer" class="drawer-overlay" aria-label="Close sidebar"></label>
    <ul class="menu bg-base-200 min-h-full w-64 p-4">
      <li><a>Dashboard</a></li>
    </ul>
  </div>
</div>
```

`drawer-open` keeps sidebar permanently visible. `drawer-end` puts sidebar on the right.

**Gotchas:**

- `lg:drawer-open` paired with `lg:hidden` on the hamburger button is the standard responsive pattern — open on large screens, toggleable on mobile
- The `drawer-side` is `position: fixed` by default — it overlays content. This is correct for mobile

## .hero — Hero Section

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

`hero-content` can be `flex-col` or `flex-col lg:flex-row` for side-by-side image + text.

## .divider — Horizontal/Vertical Divider

```html
<div class="divider">OR</div>
<div class="divider divider-vertical h-24">AND</div>
<div class="divider divider-primary">Section</div>
```

Color modifiers: `divider-primary` through `divider-error` + `divider-start` `divider-end` (text alignment).

## .join — Grouped Elements

**Description:** Joins borders between adjacent components (buttons, inputs). Removes inner border-radius.

```html
<div class="join">
  <input class="input join-item" placeholder="Email" />
  <button class="btn btn-primary join-item">Subscribe</button>
</div>

<div class="join join-vertical">
  <button class="btn join-item">Top</button>
  <button class="btn join-item">Middle</button>
  <button class="btn join-item">Bottom</button>
</div>
```

**Gotchas:** Each child needs `join-item` class. Works with `.btn`, `.input`, `.select`, `.badge`.

## .indicator — Positional Badge on Element

```html
<div class="indicator">
  <span class="indicator-item badge badge-secondary">99+</span>
  <button class="btn">Notifications</button>
</div>
```

Position modifiers: `indicator-top` `indicator-middle` `indicator-bottom` + `indicator-start` `indicator-center` `indicator-end`

## .stack — Overlapping Stack

```html
<div class="stack">
  <div class="card bg-primary text-primary-content">Card 3</div>
  <div class="card bg-secondary text-secondary-content">Card 2</div>
  <div class="card bg-base-100">Card 1 (top)</div>
</div>
```

Stacks children with offset overlap — good for card pile effects.

## .footer — Page Footer

**Description:** Structured footer layout with support for multi-column link groups. Composes with `.menu` for navigation links.

**Modifiers:** `footer-horizontal` (forces side-by-side columns regardless of viewport) `footer-center` (centers all content)

**Required structure:**

```html
<footer class="footer bg-base-200 text-base-content p-10">
  <nav>
    <h6 class="footer-title">Services</h6>
    <a class="link link-hover">Branding</a>
    <a class="link link-hover">Design</a>
    <a class="link link-hover">Marketing</a>
  </nav>
  <nav>
    <h6 class="footer-title">Company</h6>
    <a class="link link-hover">About us</a>
    <a class="link link-hover">Contact</a>
  </nav>
  <nav>
    <h6 class="footer-title">Legal</h6>
    <a class="link link-hover">Privacy policy</a>
    <a class="link link-hover">Terms of use</a>
  </nav>
</footer>

<!-- Footer with copyright bar -->
<footer class="footer footer-center bg-base-300 text-base-content p-4">
  <aside>
    <p>Copyright © 2025 — All rights reserved</p>
  </aside>
</footer>
```

**Gotchas:**

- `.footer` is `display: grid` with auto column sizing — columns form automatically based on `<nav>` or `<aside>` children
- `.footer-title` adds `opacity-60` and `uppercase` letter-spacing — don't use `.font-bold` expecting the same treatment
- Wrap in `<footer>` semantic HTML element, not a `<div>`, for landmark navigation

## .mask — Shape Clipping Mask

**Description:** Clips an element to a non-rectangular shape using CSS `mask-image`. Commonly used for avatar shapes, image crops, and decorative elements.

**Modifiers (shape):**

| Class | Shape |
|-------|-------|
| `mask-squircle` | Squircle (rounded square, iOS-style icon) |
| `mask-circle` | Circle |
| `mask-heart` | Heart shape |
| `mask-star` | 5-point star (thin) |
| `mask-star-2` | 5-point star (filled, used in `.rating`) |
| `mask-hexagon` | Regular hexagon |
| `mask-hexagon-2` | Rotated hexagon |
| `mask-decagon` | 10-sided polygon |
| `mask-pentagon` | 5-sided polygon |
| `mask-diamond` | Diamond shape |
| `mask-square` | Square (useful to override other masks) |
| `mask-triangle` | Triangle pointing up |
| `mask-triangle-2` | Triangle pointing down |
| `mask-triangle-3` | Triangle pointing left |
| `mask-triangle-4` | Triangle pointing right |
| `mask-half-1` | Left or top half of the parent shape |
| `mask-half-2` | Right or bottom half of the parent shape |

**Usage Example:**

```html
<!-- Squircle avatar -->
<div class="avatar">
  <div class="w-16 mask mask-squircle">
    <img src="/user.jpg" alt="User" />
  </div>
</div>

<!-- Star-shaped decorative image -->
<img src="/photo.jpg" class="mask mask-star-2 w-32" alt="Feature" />

<!-- Half-masks for split-color effects -->
<div class="flex">
  <div class="mask mask-star-2 mask-half-1 bg-primary w-8 h-8"></div>
  <div class="mask mask-star-2 mask-half-2 bg-base-300 w-8 h-8"></div>
</div>
```

**Gotchas:**

- `mask` uses `mask-image` CSS property — content outside the shape is clipped but the element's box model is unchanged (hover areas, spacing still reflect the original box)
- Not all shapes render correctly in Firefox — `mask-squircle` uses an SVG data URI that is broadly supported, but complex polygons may vary
- The `.rating` component uses `mask mask-star-2` internally on radio inputs — avoid applying other mask classes to rating inputs

## Common Mistakes

- Forgetting `drawer-toggle` checkbox must be direct sibling of `drawer-content` and `drawer-side` — positioning breaks if nested differently
- Using `hero` without `min-h-screen` when full-viewport height is desired — the class doesn't force height on its own
- Using `.mask` without setting explicit width/height — without dimensions, mask has nothing to clip

## See Also

- [Navigation Components](navigation-components.md) — menu inside drawer sidebar
- [Actions Components](actions-components.md) — modal for overlay dialogs
- Reference: `node_modules/daisyui/components/drawer/object.js`
