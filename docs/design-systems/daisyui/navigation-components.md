---
description: Reference for DaisyUI navigation components — navbar, menu, tabs, breadcrumbs, steps, dock, link, and pagination composition
tldr: "Site navigation, wayfinding, and multi-section navigation patterns. Tabs require `aria-label` on radio inputs. Dock is mobile-only — use `lg:hidden`. Pagination is composed from `.join` + `.btn`, not a standalone component."
---

# Navigation Components

## When to Use

> Site navigation, wayfinding, and multi-section navigation patterns.

## Decision: Which Navigation Component

| Component | Class | Use for |
|-----------|-------|---------|
| Top bar | `.navbar` | Primary site header navigation |
| Sidebar/inline menu | `.menu` | Vertical or horizontal nav lists |
| Tab navigation | `.tabs` | Multi-panel content switching |
| Path trail | `.breadcrumbs` | Hierarchical location indicator |
| Progress track | `.steps` | Multi-step wizard/form progress |
| Bottom dock | `.dock` | Mobile-first fixed bottom navigation |
| Hyperlink style | `.link` | Consistent underline and color on `<a>` |
| Pagination | `.join` + `.btn` | Page navigation (composition — no `.pagination` class) |

## .navbar — Top Navigation Bar

**Structure:** `.navbar` > `.navbar-start` + `.navbar-center` + `.navbar-end`

```html
<div class="navbar bg-base-100 shadow-sm">
  <div class="navbar-start">
    <a class="btn btn-ghost text-xl">Brand</a>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal">
      <li><a>Home</a></li>
      <li><a>About</a></li>
    </ul>
  </div>
  <div class="navbar-end">
    <button class="btn btn-primary btn-sm">Sign In</button>
  </div>
</div>
```

**Gotchas:** `navbar-start` and `navbar-end` are each `width: 50%` by default. Add `flex-1` to adjust proportions.

## .menu — Navigation Menu

**Structure:** `.menu` > `<li>` > `<a>` or `<details>` for nested

**Variants:** `menu-horizontal` `menu-vertical` (default) + sizes `menu-xs` through `menu-xl`

```html
<!-- Vertical sidebar menu with nested submenu -->
<ul class="menu bg-base-200 w-56 rounded-box">
  <li><a class="menu-active">Dashboard</a></li>
  <li>
    <details open>
      <summary>Settings</summary>
      <ul>
        <li><a>Profile</a></li>
        <li><a>Account</a></li>
      </ul>
    </details>
  </li>
  <li class="menu-disabled"><a>Disabled Item</a></li>
</ul>
```

**Gotchas:**

- `menu-active` class highlights the active item — not automatically applied, must be set programmatically
- Nested `<details><summary>` provides CSS-only toggle for submenus; the caret/arrow animates
- `.menu` items use `<li>` wrappers — direct `<a>` inside `.menu` without `<li>` breaks layout

## .tabs — Tab Navigation

**Container:** `.tabs` with variant `tabs-border` `tabs-lift` `tabs-box` `tabs-top` `tabs-bottom`

**Item:** `.tab` with `tab-active` or `aria-selected="true"`

**Sizes:** `tabs-xs` through `tabs-xl`

```html
<!-- CSS-only radio tab group -->
<div class="tabs tabs-lift">
  <input type="radio" name="my-tabs" class="tab" aria-label="Tab 1" checked />
  <div class="tab-content bg-base-100 border-base-300 p-6">Content 1</div>

  <input type="radio" name="my-tabs" class="tab" aria-label="Tab 2" />
  <div class="tab-content bg-base-100 border-base-300 p-6">Content 2</div>
</div>
```

**Gotchas:**

- `tabs-lift` and `tabs-top` are visually different — `tabs-lift` has elevated active tab effect; `tabs-top` has bottom border
- `tab-content` must immediately follow its corresponding `input[type=radio]` in DOM order — CSS sibling selectors depend on this

## .breadcrumbs — Breadcrumb Trail

```html
<div class="breadcrumbs text-sm">
  <ul>
    <li><a>Home</a></li>
    <li><a>Products</a></li>
    <li>Current Page</li>
  </ul>
</div>
```

Separators are CSS-generated — no markup needed for the `>` dividers. Wrap the whole thing in `<nav aria-label="Breadcrumb">` so screen readers get the landmark.

## .steps — Progress Steps

```html
<ul class="steps steps-horizontal">
  <li class="step step-primary">Register</li>
  <li class="step step-primary">Choose plan</li>
  <li class="step">Payment</li>
  <li class="step">Confirm</li>
</ul>
```

`steps-vertical` for vertical layout. `step-primary` marks completed/active steps. Add `aria-current="step"` on the active step.

## .dock — Bottom Navigation Dock

**Description:** Fixed bottom navigation bar for mobile-first apps. Replaces traditional tab bars.

**Modifiers:** `dock-xs` `dock-sm` `dock-md` `dock-lg` `dock-xl`

**Required structure:**

```html
<div class="dock">
  <button class="dock-active">
    <svg .../><!-- Home icon -->
    <span class="dock-label">Home</span>
  </button>
  <button>
    <svg .../><!-- Search icon -->
    <span class="dock-label">Search</span>
  </button>
  <button>
    <svg .../><!-- Profile icon -->
    <span class="dock-label">Profile</span>
  </button>
</div>
```

**Gotchas:**

- `.dock` is `position: fixed; bottom: 0` — it always sticks to the bottom of the viewport
- Add `pb-safe` or `padding-bottom: env(safe-area-inset-bottom)` for iPhone notch/home indicator clearance
- `dock-active` highlights the currently selected item — set it programmatically based on current route
- `.dock-label` text is hidden at smaller dock sizes — include icons always

## .link — Styled Hyperlink

**Description:** Applies consistent underline and color styling to `<a>` elements. Removes the need for per-link utility repetition.

**Modifiers:**

| Class | Effect |
|-------|--------|
| `link-primary` through `link-error` | Link color |
| `link-hover` | Underline only on hover (not by default) |
| `link-neutral` | Neutral color (uses `--color-base-content`) |

```html
<a href="#" class="link link-primary">Read more</a>
<a href="#" class="link link-hover">Optional underline</a>
<p>Visit our <a href="#" class="link link-secondary">documentation</a> for details.</p>
```

**Gotchas:**

- `.link` without a color modifier uses `currentColor` — inherits from parent text color
- Use `link-hover` inside body text where permanent underlines would be visually noisy

## .pagination — Page Navigation (Composition Pattern)

**Description:** DaisyUI has no dedicated `.pagination` component — pagination is composed using `.join` + `.btn` utilities.

**Required structure:**

```html
<div class="join">
  <button class="join-item btn btn-sm">«</button>
  <button class="join-item btn btn-sm">1</button>
  <button class="join-item btn btn-sm btn-active">2</button>
  <button class="join-item btn btn-sm">3</button>
  <button class="join-item btn btn-sm">»</button>
</div>

<!-- With ellipsis for large page ranges -->
<div class="join">
  <button class="join-item btn btn-sm">«</button>
  <button class="join-item btn btn-sm">1</button>
  <button class="join-item btn btn-sm btn-disabled">...</button>
  <button class="join-item btn btn-sm btn-active">10</button>
  <button class="join-item btn btn-sm btn-disabled">...</button>
  <button class="join-item btn btn-sm">50</button>
  <button class="join-item btn btn-sm">»</button>
</div>
```

**Gotchas:**

- `btn-active` marks the current page — set programmatically based on current page state
- Use `<a>` instead of `<button>` for server-rendered pagination to preserve native link behavior
- Add `aria-current="page"` on the active page button and `aria-label` on prev/next buttons for accessibility

## Common Mistakes

- Not providing `aria-label` on tab `<input>` elements — required for radio tabs since the `<input>` has no visible text; DaisyUI uses `attr(aria-label)` as the tab label
- Using `menu-horizontal` for mobile nav without hiding on small screens — horizontal menus wrap badly; use Tailwind responsive prefix `lg:menu-horizontal`
- Using `.dock` on desktop layouts without responsive hiding — dock is a mobile pattern; use `lg:hidden` or switch to a sidebar at larger breakpoints

## See Also

- [Actions Components](actions-components.md) — dropdown inside navbar
- [Layout Components](layout-components.md) — drawer for mobile sidebar navigation
- Reference: `node_modules/daisyui/components/navbar/object.js`
- Reference: `node_modules/daisyui/components/menu/object.js`
- Reference: `node_modules/daisyui/components/tab/object.js`
