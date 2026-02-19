---
description: Reference for DaisyUI layout components — drawer, hero, divider, join, indicator, and stack
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

## Common Mistakes

- **Wrong**: `drawer-toggle` checkbox not a direct sibling of `drawer-content` and `drawer-side` — **Right**: DOM structure must be exact; nesting breaks CSS positioning
- **Wrong**: `hero` without `min-h-screen` when full viewport height is desired — **Right**: The class doesn't force height on its own

## See Also

- [Navigation Components](navigation-components.md) — menu inside drawer
- [Actions Components](actions-components.md) — modal for overlay dialogs
- Reference: `node_modules/daisyui/components/drawer/object.js`
