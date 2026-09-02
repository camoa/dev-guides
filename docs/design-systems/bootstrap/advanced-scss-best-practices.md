---
description: "Advanced SCSS patterns for complex Bootstrap customizations including Dart Sass, maps, and accessibility"
tldr: "Use this for complex Bootstrap customizations requiring Dart Sass features, deep map merging, performance optimization, or accessibility patterns."
drupal_version: "11.x"
---

# Advanced SCSS Best Practices

## When to Use

> Use this for complex Bootstrap customizations requiring Dart Sass features, deep map merging, performance optimization, or accessibility patterns.

- You need advanced SCSS patterns for complex Bootstrap customizations
- You're working with Dart Sass vs LibSass compatibility
- You need performance optimization techniques
- You're implementing accessibility features in SCSS

## Dart Sass vs LibSass (CRITICAL REQUIREMENT)

**Status as of 2025:** LibSass is DEPRECATED. Dart Sass is REQUIRED.

```bash
# ❌ WRONG: Using deprecated LibSass/Node Sass
npm install node-sass

# ✅ CORRECT: Using Dart Sass
npm install sass
```

**Why Dart Sass is Required:**
1. **LibSass officially deprecated** - No new features since 2020, maintenance-only mode
2. **Missing CSS features** - LibSass doesn't support modern CSS (`:is()`, `:where()`, container queries, etc.)
3. **Module system** - `@use` and `@forward` only work in Dart Sass
4. **Bootstrap compatibility** - Future Bootstrap versions may require Dart Sass features
5. **Security** - Only Dart Sass receives security updates

**What breaks with LibSass:**
- Modern SCSS module system (`@use`, `@forward`)
- Deep map merge operations (`map.deep-merge()`)
- Advanced color functions (`color.scale()`, `color.adjust()`)
- Modern CSS feature support

**Migration Path:** Replace `node-sass` with `sass` package in build tools (Webpack, Gulp, Vite).

**Reference:** [Sass: LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/) - Official deprecation announcement

## Map Manipulation Gotchas (CRITICAL)

### Problem: Deep Merge Doesn't Exist by Default

```scss
// ❌ WRONG: map-merge() doesn't deep merge nested maps
$base-config: (
  button: (
    padding: 1rem,
    color: blue
  )
);

$custom-config: (
  button: (
    color: red  // Want to override just color, keep padding
  )
);

$merged: map-merge($base-config, $custom-config);
// Result: button.padding is LOST (entire button map replaced)
```

**✅ CORRECT Solution 1: Use map.deep-merge() (Dart Sass 1.27+)**
```scss
@use "sass:map";

$merged: map.deep-merge($base-config, $custom-config);
// Result: button.padding preserved, button.color overridden
```

**✅ CORRECT Solution 2: Manual Nested Merge (Pre-1.27)**
```scss
$merged: map-merge($base-config, (
  button: map-merge(
    map-get($base-config, button),
    map-get($custom-config, button)
  )
));
```

**Bootstrap Implication:** When extending Bootstrap maps with nested structures, ALWAYS use `map.deep-merge()` or manually merge each level.

**Reference:** [Sass: sass:map Documentation](https://sass-lang.com/documentation/modules/map/) - Deep merge functions

## Import Order Matters (CRITICAL)

**Why Order is Critical:**
1. **Variables before Bootstrap** - Bootstrap variables use `!default` flag (only set if undefined)
2. **Maps before utilities** - Utility API reads from maps to generate classes
3. **Custom after Bootstrap** - Your overrides must come after Bootstrap definitions

```scss
// ❌ WRONG ORDER: Custom imports before Bootstrap
@import "custom-components";        // TOO EARLY
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables"; // Custom already compiled

// ✅ CORRECT ORDER: Bootstrap foundation, then customizations
// 1. Functions first (required for color operations)
@import "bootstrap/scss/functions";

// 2. Custom variable OVERRIDES (before Bootstrap variables)
$primary: #0066cc;

// 3. Bootstrap variables (reads your overrides)
@import "bootstrap/scss/variables";

// 4. Custom map EXTENSIONS (after Bootstrap maps loaded)
$theme-colors: map-merge($theme-colors, ("brand": #ff0000));

// 5. Bootstrap core
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";

// 6. Bootstrap components
@import "bootstrap/scss/bootstrap";

// 7. Custom utilities (before API)
$utilities: map-merge($utilities, (...));

// 8. Utilities API (generates classes)
@import "bootstrap/scss/utilities/api";

// 9. Custom components LAST
@import "custom-components";
```

**Reference:** [Bootstrap Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/) - Official import order guide

## CSS Custom Properties vs SCSS Variables (Decision Framework)

**When to Use SCSS Variables:**
- Design system tokens that NEVER change (brand colors, base typography)
- Compile-time calculations (math operations, color manipulation)
- Values needed in media queries (CSS custom properties don't work in `@media`)
- Bootstrap variable overrides (Bootstrap uses SCSS variables)

**When to Use CSS Custom Properties:**
- Runtime theming (light/dark mode, user preferences)
- Component-scoped customization (local overrides)
- JavaScript-driven updates (dynamic values)
- Values with fallbacks (`var(--color, fallback)`)

**✅ BEST: Hybrid Approach**
```scss
// SCSS variables as source of truth
$primary: #0066cc;
$secondary: #6c757d;

// Generate CSS custom properties from SCSS
:root {
  --primary: #{$primary};
  --secondary: #{$secondary};
  --primary-rgb: #{red($primary), green($primary), blue($primary)};
}

// Use CSS custom properties in components (runtime flexibility)
.component {
  background: var(--primary);
  color: rgba(var(--primary-rgb), 0.5); // Opacity adjustment at runtime
}

// Use SCSS variables for compile-time operations
.component-hover {
  background: darken($primary, 10%); // Can't use CSS variables for darken()
}
```

**Reference:** [CSS Custom Properties vs SCSS Variables](https://codilime.com/blog/css-vs-scss-main-defferences-use-cases/) - Practical comparison

## Performance Best Practices

### Bundle Size Optimization

```scss
// ❌ WRONG: Import entire Bootstrap
@import "bootstrap/scss/bootstrap"; // 200KB+ CSS

// ✅ CORRECT: Import only what you need
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";

// Only import components you use
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/buttons";
@import "bootstrap/scss/forms";
// Result: ~50KB CSS (75% reduction)
```

### JavaScript Tree-Shaking

```javascript
// ❌ WRONG: Import entire Bootstrap JS
import 'bootstrap';

// ✅ CORRECT: Import only components needed
import { Modal, Dropdown } from 'bootstrap';
```

### Unused CSS Removal (PurgeCSS)

```javascript
// purgecss.config.js
module.exports = {
  content: ['./src/**/*.html', './src/**/*.js'],
  css: ['./dist/css/bootstrap.css'],
  // Safelist Bootstrap dynamic classes
  safelist: ['show', 'collapse', 'collapsing', /^modal/, /^dropdown/]
};
```

**Real-world impact:** PurgeCSS reduces Bootstrap CSS from 227KB to ~6KB in production.

**Reference:** [PurgeCSS with Bootstrap](https://purgecss.com/) - Unused CSS removal guide

## Accessibility Best Practices

### Color Contrast (Bootstrap Limitations)

```scss
// ⚠️ WARNING: Some Bootstrap color combinations fail WCAG 2.2
// Bootstrap default: 4.5:1 minimum for text
// Test your custom colors

@use "sass:color";

// ✅ CORRECT: Use Bootstrap's contrast functions
$bg: #0066cc;
$text: color-contrast($bg); // Auto-selects white or black for 4.5:1 ratio

// Verify contrast manually for brand colors
// WCAG 2.2 requires:
// - Normal text: 4.5:1 minimum (AA)
// - Large text: 3:1 minimum (AA)
// - UI components: 3:1 minimum (AA)
```

**Tools:** Use WebAIM Contrast Checker to validate before deployment.

### Focus Indicators (CRITICAL - Never Remove)

```scss
// ❌ WRONG: Removing focus styles breaks keyboard navigation
button:focus {
  outline: none; // NEVER DO THIS
}

// ✅ CORRECT: Customize Bootstrap focus ring
$focus-ring-width: 0.25rem;
$focus-ring-color: rgba($primary, 0.25);
$focus-ring-blur: 0;

// OR: Use :focus-visible for keyboard-only focus
button:focus-visible {
  outline: 2px solid $primary;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none; // Remove for mouse users, keep for keyboard
}
```

**WHY:** Focus rings are essential for keyboard navigation. Removing them makes sites inaccessible for sighted keyboard users.

**Reference:** [Bootstrap Focus Ring](https://getbootstrap.com/docs/5.3/helpers/focus-ring/) - Accessible focus customization

### Reduced Motion (Bootstrap Built-in Support)

```scss
// Bootstrap automatically respects user preferences
// prefers-reduced-motion: reduce disables most CSS transitions

// ✅ Your custom animations should too
@media (prefers-reduced-motion: reduce) {
  .custom-animation {
    animation: none;
    transition: none;
  }
}

// Bootstrap variable for motion control
$enable-transitions: true; // Set false to disable globally
```

**Reference:** [How to Achieve Accessibility Compliance with Bootstrap 5](https://www.batoi.com/blogs/developers/how-achieve-accessibility-compliance-bootstrap-5-6645baaae29d1) - Motion accessibility

### Screen Reader Utilities

```scss
// ✅ CORRECT: .visually-hidden vs display:none
.visually-hidden {
  // Accessible to screen readers, invisible visually
  // Bootstrap provides this utility
}

// ❌ WRONG: display:none hides from screen readers too
.hidden {
  display: none; // NOT accessible
}

// Use .visually-hidden for:
// - Skip navigation links
// - Form labels when visual label exists
// - Additional context for screen readers
```

## Common Mistakes

- **Wrong**: Using LibSass/node-sass → **Right**: Use Dart Sass (sass package)
- **Wrong**: map-merge() for nested maps → **Right**: map.deep-merge()
- **Wrong**: Importing custom vars after Bootstrap → **Right**: Custom vars before Bootstrap variables
- **Wrong**: outline: none on focus → **Right**: Customize focus-visible

## See Also

- ← Previous: [SCSS Best Practices](scss-best-practices.md)
- Next: [Quality Assurance Framework](quality-assurance-framework.md)
- Reference: [Sass: LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- Reference: [Bootstrap Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
