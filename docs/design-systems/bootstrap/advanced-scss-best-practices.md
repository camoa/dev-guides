---
description: Advanced SCSS patterns for complex Bootstrap customizations including Dart Sass, maps, and accessibility
---

# Advanced SCSS Best Practices

## When to Use

> Use this for complex Bootstrap customizations requiring Dart Sass features, deep map merging, performance optimization, or accessibility patterns.

## Dart Sass vs LibSass (CRITICAL)

| Tool | Status | Action |
|------|--------|--------|
| LibSass (node-sass) | DEPRECATED | Never use |
| Dart Sass (sass) | REQUIRED | Always use |

```bash
# ❌ WRONG
npm install node-sass

# ✅ CORRECT
npm install sass
```

**Why Dart Sass is required:**
- LibSass officially deprecated (2020)
- Missing modern CSS features (`:is()`, `:where()`, container queries)
- Module system (`@use`, `@forward`) only works in Dart Sass
- Future Bootstrap versions require Dart Sass
- Only Dart Sass receives security updates

## Map Manipulation Gotchas

### Deep Merge Problem

```scss
// ❌ WRONG: map-merge() doesn't deep merge
$base: ( button: ( padding: 1rem, color: blue ) );
$custom: ( button: ( color: red ) );
$merged: map-merge($base, $custom);
// Result: button.padding LOST

// ✅ CORRECT: Use map.deep-merge() (Dart Sass 1.27+)
@use "sass:map";
$merged: map.deep-merge($base, $custom);
// Result: button.padding preserved, color overridden
```

**Bootstrap implication:** When extending Bootstrap maps with nested structures, ALWAYS use `map.deep-merge()`.

## Import Order (CRITICAL)

| Step | Import | Why |
|------|--------|-----|
| 1 | Functions | Required for color operations |
| 2 | Custom variables | Overrides before Bootstrap reads them |
| 3 | Bootstrap variables | Reads your overrides via `!default` |
| 4 | Custom map extensions | After Bootstrap maps loaded |
| 5 | Bootstrap core | Maps, mixins, root |
| 6 | Bootstrap components | Full framework |
| 7 | Custom utilities | Before API generation |
| 8 | Utilities API | Generates classes from maps |
| 9 | Custom components | Last |

```scss
// ✅ CORRECT ORDER
@import "bootstrap/scss/functions";
$primary: #0066cc;                                    // Override
@import "bootstrap/scss/variables";                   // Reads override
$theme-colors: map-merge($theme-colors, ("brand": ...)); // Extend
@import "bootstrap/scss/maps";
@import "bootstrap/scss/bootstrap";
$utilities: map-merge($utilities, (...));
@import "bootstrap/scss/utilities/api";
@import "custom-components";                          // Last
```

## CSS Custom Properties vs SCSS Variables

| Use Case | Tool | Why |
|----------|------|-----|
| Brand colors (never change) | SCSS | Compile-time calculation |
| Media queries | SCSS | CSS vars don't work in `@media` |
| Bootstrap overrides | SCSS | Bootstrap uses SCSS vars |
| Light/dark mode | CSS vars | Runtime theming |
| Component customization | CSS vars | Local overrides |
| JS-driven updates | CSS vars | Dynamic values |

**Best: Hybrid approach**

```scss
// SCSS variables as source
$primary: #0066cc;

// Generate CSS custom properties
:root {
  --primary: #{$primary};
  --primary-rgb: #{red($primary), green($primary), blue($primary)};
}

// Use CSS vars in components (runtime)
.component {
  background: var(--primary);
  color: rgba(var(--primary-rgb), 0.5);
}

// Use SCSS for compile-time operations
.component-hover {
  background: darken($primary, 10%); // Can't use CSS vars
}
```

## Performance Best Practices

### Bundle Size Optimization

```scss
// ❌ WRONG: Import entire Bootstrap (200KB+)
@import "bootstrap/scss/bootstrap";

// ✅ CORRECT: Import only what you need (~50KB)
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/buttons";
@import "bootstrap/scss/forms";
```

### JavaScript Tree-Shaking

```javascript
// ❌ WRONG
import 'bootstrap';

// ✅ CORRECT
import { Modal, Dropdown } from 'bootstrap';
```

### PurgeCSS

```javascript
// purgecss.config.js
module.exports = {
  content: ['./src/**/*.html', './src/**/*.js'],
  css: ['./dist/css/bootstrap.css'],
  safelist: ['show', 'collapse', 'collapsing', /^modal/, /^dropdown/]
};
```

**Real-world impact:** PurgeCSS reduces Bootstrap from 227KB to ~6KB.

## Accessibility Best Practices

### Color Contrast

```scss
// ✅ CORRECT: Use Bootstrap's contrast functions
$bg: #0066cc;
$text: color-contrast($bg); // Auto-selects white/black for 4.5:1

// WCAG 2.2 requirements:
// - Normal text: 4.5:1 minimum
// - Large text: 3:1 minimum
// - UI components: 3:1 minimum
```

**Tool:** WebAIM Contrast Checker

### Focus Indicators (CRITICAL)

```scss
// ❌ WRONG: Never remove focus
button:focus {
  outline: none; // NEVER DO THIS
}

// ✅ CORRECT: Customize focus ring
$focus-ring-width: 0.25rem;
$focus-ring-color: rgba($primary, 0.25);

// OR: Keyboard-only focus
button:focus-visible {
  outline: 2px solid $primary;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none; // Remove for mouse only
}
```

**WHY:** Focus rings are essential for keyboard navigation.

### Reduced Motion

```scss
// Bootstrap respects prefers-reduced-motion automatically

// ✅ Your custom animations should too
@media (prefers-reduced-motion: reduce) {
  .custom-animation {
    animation: none;
    transition: none;
  }
}

// Bootstrap variable
$enable-transitions: true; // Set false to disable globally
```

### Screen Reader Utilities

```scss
// ✅ CORRECT: .visually-hidden (accessible)
.visually-hidden {
  // Invisible visually, accessible to screen readers
  // Bootstrap provides this
}

// ❌ WRONG: display:none (inaccessible)
.hidden {
  display: none; // NOT accessible
}
```

## Common Mistakes

- **Wrong**: Using LibSass/node-sass → **Right**: Use Dart Sass (sass package)
- **Wrong**: map-merge() for nested maps → **Right**: map.deep-merge()
- **Wrong**: Importing custom vars after Bootstrap → **Right**: Custom vars before Bootstrap variables
- **Wrong**: outline: none on focus → **Right**: Customize focus-visible

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Quality Assurance Framework](quality-assurance-framework.md)
- Reference: [Sass: LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- Reference: [Bootstrap Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
