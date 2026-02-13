---
description: Advanced SCSS Best Practices — Dart Sass requirements, performance optimization, and accessibility features
---

# Advanced SCSS Best Practices

## When to Use

> Use when working with complex Bootstrap customizations, Dart Sass vs LibSass compatibility, performance optimization, or accessibility features.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Sass compiler | Dart Sass | LibSass deprecated, missing modern features |
| Deep map merging | `map.deep-merge()` | Preserves nested values |
| Import order matters | Functions → Variables → Bootstrap | Variables use `!default` flag |
| Runtime theming | CSS custom properties | JavaScript-driven updates |
| Compile-time calculations | SCSS variables | Math operations, color manipulation |

## Pattern

**Dart Sass Requirement**:
```bash
# ✅ CORRECT
npm install sass
```

**Deep Map Merge**:
```scss
@use "sass:map";

$merged: map.deep-merge($base-config, $custom-config);
// Preserves nested values, doesn't replace entire maps
```

**Import Order**:
```scss
// 1. Functions first
@import "bootstrap/scss/functions";

// 2. Custom variable overrides
$primary: #0066cc;

// 3. Bootstrap variables
@import "bootstrap/scss/variables";

// 4. Custom map extensions
$theme-colors: map-merge($theme-colors, ("brand": #ff0000));

// 5. Bootstrap core
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";
@import "bootstrap/scss/bootstrap";

// 6. Custom utilities
$utilities: map-merge($utilities, (...));

// 7. Utilities API
@import "bootstrap/scss/utilities/api";

// 8. Custom components last
@import "custom-components";
```

**Hybrid CSS/SCSS Variables**:
```scss
// SCSS variables as source
$primary: #0066cc;

// Generate CSS custom properties
:root {
  --primary: #{$primary};
  --primary-rgb: #{red($primary), green($primary), blue($primary)};
}

// Runtime flexibility
.component {
  background: var(--primary);
  color: rgba(var(--primary-rgb), 0.5);
}

// Compile-time operations
.component-hover {
  background: darken($primary, 10%);
}
```

**Performance Optimization**:
```scss
// ✅ CORRECT: Import only what you need
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/reboot";
@import "bootstrap/scss/grid";
@import "bootstrap/scss/buttons";
// Result: ~50KB CSS (75% reduction from 200KB+)
```

**Accessibility — Focus Indicators**:
```scss
// ✅ CORRECT: Customize focus ring
$focus-ring-width: 0.25rem;
$focus-ring-color: rgba($primary, 0.25);

// OR: Use :focus-visible for keyboard-only
button:focus-visible {
  outline: 2px solid $primary;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none;
}
```

## Common Mistakes

- **Wrong**: Using LibSass/node-sass → **Right**: Use Dart Sass (LibSass deprecated, missing modern features)
- **Wrong**: `map-merge()` on nested maps → **Right**: `map.deep-merge()` (preserves nested values)
- **Wrong**: Bootstrap import before overrides → **Right**: Custom variables before Bootstrap (`.!default` flag)
- **Wrong**: Import entire Bootstrap → **Right**: Import only needed components (75% bundle reduction)
- **Wrong**: `outline: none` on focus → **Right**: Customize or use `:focus-visible` (accessibility)

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Quality Assurance Framework](quality-assurance-framework.md)
- Reference: [Sass: LibSass is Deprecated](https://sass-lang.com/blog/libsass-is-deprecated/)
- Reference: [Sass: sass:map Documentation](https://sass-lang.com/documentation/modules/map/)
- Reference: [Bootstrap Focus Ring](https://getbootstrap.com/docs/5.3/helpers/focus-ring/)
- Reference: [PurgeCSS](https://purgecss.com/)
