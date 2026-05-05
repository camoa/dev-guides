---
description: Reference for DaisyUI navigation components — navbar, menu, tabs, breadcrumbs, steps, dock, link, and pagination composition
tldr: "Site navigation, wayfinding, and multi-section navigation patterns. Tabs require `aria-label` on radio inputs. Dock is mobile-only — use `lg:hidden`. Pagination is composed from `.join` + `.btn`, not a standalone component."
---

# Navigation Components

## When to Use

> Site navigation, wayfinding, and multi-section navigation patterns.

## Decision

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

## Pattern

### .navbar

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

`navbar-start` and `navbar-end` are each `width: 50%` by default. Add `flex-1` to adjust proportions.

### .menu

```html
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

Variants: `menu-horizontal` `menu-vertical` + sizes `menu-xs` through `menu-xl`. Nested `<details><summary>` provides CSS-only submenu toggle.

### .tabs (CSS-only radio group)

```html
<div class="tabs tabs-lift">
  <input type="radio" name="my-tabs" class="tab" aria-label="Tab 1" checked />
  <div class="tab-content bg-base-100 border-base-300 p-6">Content 1</div>

  <input type="radio" name="my-tabs" class="tab" aria-label="Tab 2" />
  <div class="tab-content bg-base-100 border-base-300 p-6">Content 2</div>
</div>
```

Container variants: `tabs-border` `tabs-lift` `tabs-box` `tabs-top` `tabs-bottom` + sizes `tabs-xs` through `tabs-xl`. `.tab-content` must immediately follow its corresponding `<input>` — CSS sibling selectors depend on this.

### .breadcrumbs

```html
<nav aria-label="Breadcrumb">
  <div class="breadcrumbs text-sm">
    <ul>
      <li><a>Home</a></li>
      <li><a>Products</a></li>
      <li>Current Page</li>
    </ul>
  </div>
</nav>
```

Separators are CSS-generated — no markup needed for `>` dividers.

### .steps

```html
<ul class="steps steps-horizontal">
  <li class="step step-primary">Register</li>
  <li class="step step-primary">Choose plan</li>
  <li class="step">Payment</li>
  <li class="step">Confirm</li>
</ul>
```

Use `steps-vertical` for vertical layout. `step-primary` marks completed/active steps. Add `aria-current="step"` on the active step.

### .dock — Bottom Navigation

```html
<div class="dock">
  <button class="dock-active">
    <svg .../>
    <span class="dock-label">Home</span>
  </button>
  <button>
    <svg .../>
    <span class="dock-label">Search</span>
  </button>
  <button>
    <svg .../>
    <span class="dock-label">Profile</span>
  </button>
</div>
```

`.dock` is `position: fixed; bottom: 0`. Add `pb-safe` or `padding-bottom: env(safe-area-inset-bottom)` for iOS home indicator clearance. `.dock-label` text is hidden at smaller dock sizes — include icons always. Use `lg:hidden` to hide on desktop.

Sizes: `dock-xs` through `dock-xl`.

### .link — Styled Hyperlink

```html
<a href="#" class="link link-primary">Read more</a>
<a href="#" class="link link-hover">Optional underline</a>
<p>Visit our <a href="#" class="link link-secondary">documentation</a> for details.</p>
```

Modifiers: `link-primary` through `link-error` + `link-hover` (underline on hover only) + `link-neutral`. Without a color modifier, `.link` uses `currentColor`.

### Pagination (Composed from .join + .btn)

DaisyUI has no `.pagination` class — compose pagination from `.join` + `.btn`:

```html
<div class="join">
  <button class="join-item btn btn-sm">«</button>
  <button class="join-item btn btn-sm">1</button>
  <button class="join-item btn btn-sm btn-active">2</button>
  <button class="join-item btn btn-sm">3</button>
  <button class="join-item btn btn-sm">»</button>
</div>
```

Use `<a>` instead of `<button>` for server-rendered pagination. Add `aria-current="page"` on the active page and `aria-label` on prev/next buttons.

## Common Mistakes

- **Wrong**: Tab `<input>` without `aria-label` — **Right**: Required for radio tabs; DaisyUI uses `attr(aria-label)` as the visible tab label
- **Wrong**: `tab-content` not immediately following its `<input>` — **Right**: CSS sibling selectors depend on DOM adjacency
- **Wrong**: `menu-horizontal` on mobile without hiding — **Right**: Use `lg:menu-horizontal` to prevent wrapping on small screens
- **Wrong**: Direct `<a>` inside `.menu` without `<li>` wrapper — **Right**: Menu items require `<li>` wrappers
- **Wrong**: `.dock` on desktop layouts without `lg:hidden` — **Right**: Dock is a mobile pattern; switch to a sidebar at larger breakpoints
- **Wrong**: `.breadcrumbs` without a `<nav aria-label="Breadcrumb">` wrapper — **Right**: Required as a landmark for screen readers

## See Also

- [Actions Components](actions-components.md) — dropdown inside navbar
- [Layout Components](layout-components.md) — drawer for mobile sidebar
- Reference: `node_modules/daisyui/components/navbar/object.js`
- Reference: `node_modules/daisyui/components/menu/object.js`
- Reference: `node_modules/daisyui/components/tab/object.js`
