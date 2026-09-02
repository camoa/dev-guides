---
description: "Map design system tokens (colors, typography, spacing, borders, shadows, breakpoints) to Bootstrap SCSS variables"
tldr: "Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system."
drupal_version: "11.x"
---

# Design Tokens → Bootstrap Variables

## When to Use

> Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system.

- You've identified design tokens (colors, typography, spacing, etc.) using the Design System Recognition Guide
- You need to map these tokens to Bootstrap's SCSS variable system
- You're implementing a design system's foundation layer in Bootstrap

## Color Tokens

### Decision Table: Color Token Mapping

| Design System Token Type | Bootstrap Variable | Bootstrap Map | CSS Custom Property |
|-------------------------|-------------------|---------------|---------------------|
| Primary/secondary colors | `$primary`, `$secondary` | `$theme-colors` | `--bs-primary` |
| Brand colors (additional) | N/A (extend map) | Add to `$theme-colors` | `--bs-brand-color` |
| Gray/neutral scales | `$gray-100` through `$gray-900` | `$grays` | `--bs-gray-100` |
| Semantic colors | `$success`, `$danger`, `$warning`, `$info` | `$theme-colors` | `--bs-success` |
| Text colors | `$body-color`, `$headings-color` | N/A | `--bs-body-color` |
| Background colors | `$body-bg`, `$secondary-bg` | N/A | `--bs-body-bg` |
| Border colors | `$border-color`, `$border-color-translucent` | N/A | `--bs-border-color` |

### Pattern: Color Token Implementation

```scss
// 1. Override Bootstrap color variables BEFORE importing Bootstrap
$primary: #194582;        // Design system primary
$secondary: #6c757d;      // Design system secondary

// 2. Extend theme colors map with brand colors
$theme-colors: map-merge($theme-colors, (
  "brand-blue": #0066cc,  // Additional brand color
  "brand-teal": #20c997   // Additional brand color
));

// 3. Import Bootstrap to apply changes
@import "bootstrap";
```

### Common Mistakes (WHY Each Matters)

- **Setting colors after Bootstrap import** - WHY: Bootstrap variables use `!default` flag, which means "only set if not already defined." If you import Bootstrap first, your colors are ignored because Bootstrap already defined them.
- **Using hex codes directly in components** - WHY: Hardcoded colors break when design system changes. Using `$primary` means ONE update changes all instances; hardcoded `#0066cc` requires finding/replacing everywhere.
- **Ignoring RGB variants** - WHY: Bootstrap auto-generates `--bs-primary-rgb` (e.g., `0, 102, 204`) for rgba operations. You can use `rgba(var(--bs-primary-rgb), 0.5)` for opacity without manually extracting RGB values.
- **Not considering dark mode** - WHY: Bootstrap 5.3+ supports `[data-bs-theme=dark]` attribute for automatic color inversion. If you hardcode colors, dark mode won't work without manual overrides.

### See Also

- [Section 1: Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) - 6px threshold and decision categories
- [Design System Recognition Guide](../recognition/foundation-layer-design-tokens.md) - Identifying color tokens

## Typography Tokens

### Decision Table: Typography Mapping

| Design System Token | Bootstrap Variable | Bootstrap Map | Generated Utility |
|--------------------|-------------------|---------------|-------------------|
| Base font size | `$font-size-base` | N/A | N/A (affects rem calc) |
| Font family (body) | `$font-family-base` | N/A | `--bs-body-font-family` |
| Font family (headings) | `$headings-font-family` | N/A | N/A (inherits base) |
| Font family (mono) | `$font-family-monospace` | N/A | `--bs-font-monospace` |
| Font size scale | `$font-size-sm`, `$font-size-lg` | N/A | `.fs-*` utilities |
| Heading sizes | `$h1-font-size` through `$h6-font-size` | N/A | `<h1>` through `<h6>` |
| Display sizes | N/A | `$display-font-sizes` | `.display-1` through `.display-6` |
| Line heights | `$line-height-base`, `$line-height-sm`, `$line-height-lg` | N/A | N/A (applied in components) |
| Font weights | `$font-weight-lighter`, `$font-weight-normal`, `$font-weight-bold` | N/A | `.fw-light`, `.fw-normal`, `.fw-bold` |

### Pattern: Typography Token Implementation

```scss
// 1. Set base typography before Bootstrap import
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
$font-size-base: 1rem;      // 16px base
$line-height-base: 1.5;

// 2. Override heading sizes if design system differs by ≥6px
$h1-font-size: $font-size-base * 2.5;  // 40px
$h2-font-size: $font-size-base * 2;    // 32px

// 3. Extend display sizes map if needed
$display-font-sizes: map-merge($display-font-sizes, (
  7: 5rem,  // Additional large display size
));

@import "bootstrap";
```

### Common Mistakes (WHY Each Matters)

- **Hardcoding font families in components** - WHY: `font-family: "Helvetica Neue", sans-serif` scattered throughout code means changing the typeface requires global find/replace. Using `$font-family-base` means ONE variable change updates entire site.
- **Using numeric font weights** - WHY: `font-weight: 700` breaks when font changes (new font's bold might be 600 or 800). Using `$font-weight-bold` ensures consistency and allows global weight adjustments.
- **Not accounting for rem-based scaling** - WHY: `$font-size-base: 1rem` affects ALL rem calculations. If you change it to `0.875rem`, all spacing/sizing based on rem scales proportionally. Hardcoded rem values (`padding: 1rem`) don't respect this relationship.
- **Ignoring responsive fluid typography** - WHY: Bootstrap's RFS (Responsive Font Size) system automatically scales typography based on viewport width. Hardcoded sizes (`font-size: 24px`) stay static on mobile, while `$h1-font-size` scales down for better mobile UX.

### See Also

- Bootstrap 5.3 Typography Variables: [https://getbootstrap.com/docs/5.3/content/typography/](https://getbootstrap.com/docs/5.3/content/typography/)
- [Section 1.4: SCSS Best Practices](scss-best-practices.md) - Variable consistency requirements

## Spacing Tokens

### Decision Table: Spacing System Mapping

| Design System Scale | Bootstrap Default | Bootstrap Variable | Bootstrap Map Key | Generated Utilities |
|---------------------|------------------|-------------------|------------------|---------------------|
| 0px | 0px | N/A | `0: 0` | `.m-0`, `.p-0` |
| 4px | 4px (0.25rem) | `$spacer * 0.25` | `1: $spacer * 0.25` | `.m-1`, `.p-1` |
| 8px | 8px (0.5rem) | `$spacer * 0.5` | `2: $spacer * 0.5` | `.m-2`, `.p-2` |
| 16px | 16px (1rem) | `$spacer` | `3: $spacer` | `.m-3`, `.p-3` |
| 24px | 24px (1.5rem) | `$spacer * 1.5` | `4: $spacer * 1.5` | `.m-4`, `.p-4` |
| 48px | 48px (3rem) | `$spacer * 3` | `5: $spacer * 3` | `.m-5`, `.p-5` |
| Custom values | N/A | N/A | Add to `$spacers` | `.m-custom`, `.p-custom` |

### Pattern: Spacing Token Implementation

**ACCOMMODATE Strategy** (≤6px difference from Bootstrap defaults):
```scss
// Use Bootstrap defaults directly - no override needed
@import "bootstrap";
```

**EXTEND Strategy** (add missing micro-spacing):
```scss
$spacers: map-merge($spacers, (
  "3xs": 2px,   // Add 2px micro-spacing
  "2xs": 6px,   // Add 6px spacing
));

@import "bootstrap";
```

**CUSTOMIZE Strategy** (≥6px systematic differences):
```scss
// Replace Bootstrap's spacing scale entirely
$spacers: (
  0: 0,
  xs: 8px,
  sm: 24px,    // 8px different from Bootstrap's 24px
  md: 32px,
  lg: 40px,
  xl: 64px,
);

@import "bootstrap";
```

### Common Mistakes (WHY Each Matters)

- **Mixing rem and px inconsistently** - WHY: Bootstrap uses rem for accessibility (respects user font size preferences). Mixing `padding: 16px` with `margin: 1rem` breaks proportional scaling when users change browser font size.
- **Not using spacing variables in components** - WHY: `padding: 24px` is inflexible; `padding: $spacer * 1.5` or `padding: map-get($spacers, 4)` ties to design system. When spacing scale changes, variable-based spacing updates automatically.
- **Overriding when accommodation works** - WHY: Overriding 16px with custom 14px (2px difference) creates maintenance burden for minimal visual gain. The 6px threshold (see [Section 1.1: The 6-Pixel Rule](bootstrap-accommodation-decision-framework.md)) balances design precision vs. system compatibility.
- **Forgetting negative margins** - WHY: Bootstrap auto-generates `.m-n1`, `.m-n2`, etc. for negative margins from `$spacers` map. Using custom `margin: -8px` misses these utilities and breaks spacing consistency.

### See Also

- Bootstrap 5.3 Spacing Utilities: [https://getbootstrap.com/docs/5.3/utilities/spacing/](https://getbootstrap.com/docs/5.3/utilities/spacing/)
- [Section 1.1: The 6-Pixel Rule](bootstrap-accommodation-decision-framework.md) - Decision framework for spacing

## Surface Tokens

### Decision Table: Border, Radius, Shadow Mapping

| Design System Token | Bootstrap Variable | Bootstrap Map | Generated Utility |
|--------------------|-------------------|---------------|-------------------|
| Border width | `$border-width` | N/A | `.border`, `.border-2` |
| Border color | `$border-color` | N/A | `--bs-border-color` |
| Border radius (base) | `$border-radius` | N/A | `.rounded` |
| Border radius (small) | `$border-radius-sm` | N/A | `.rounded-sm` |
| Border radius (large) | `$border-radius-lg` | N/A | `.rounded-lg` |
| Border radius (pill) | `$border-radius-pill` | N/A | `.rounded-pill` |
| Box shadow (base) | `$box-shadow` | N/A | `.shadow` |
| Box shadow (small) | `$box-shadow-sm` | N/A | `.shadow-sm` |
| Box shadow (large) | `$box-shadow-lg` | N/A | `.shadow-lg` |
| Elevation system | N/A (CREATE) | Custom map | Custom utilities |

### Pattern: Surface Token Implementation

```scss
// 1. Override border and radius tokens
$border-width: 1px;
$border-radius: 0.375rem;   // 6px
$border-radius-sm: 0.25rem; // 4px
$border-radius-lg: 0.5rem;  // 8px

// 2. Override shadow tokens
$box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
$box-shadow-sm: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.075);
$box-shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);

@import "bootstrap";
```

### Common Mistakes

- **Not considering component-specific overrides** - Some components have their own radius variables (e.g., `$btn-border-radius`)
- **Hardcoding shadow values** - Use Bootstrap's shadow variables for consistency
- **Ignoring elevation systems** - If design system has numbered elevation (1-5), use CREATE category (see [Section 1.2: CREATE Category](bootstrap-accommodation-decision-framework.md))
- **Mixing border utilities without considering responsive needs** - Border utilities support responsive variants

### See Also

- Bootstrap 5.3 Borders: [https://getbootstrap.com/docs/5.3/utilities/borders/](https://getbootstrap.com/docs/5.3/utilities/borders/)
- [Section 1.2: CREATE Category](bootstrap-accommodation-decision-framework.md) - Advanced elevation systems

## Breakpoint Tokens

### Decision Table: Responsive Breakpoint Mapping

| Design System Breakpoint | Bootstrap Default | Bootstrap Map Key | Media Query | Container Max Width |
|-------------------------|------------------|------------------|-------------|---------------------|
| Mobile (small) | 576px | `sm: 576px` | `@media (min-width: 576px)` | 540px |
| Tablet | 768px | `md: 768px` | `@media (min-width: 768px)` | 720px |
| Desktop (small) | 992px | `lg: 992px` | `@media (min-width: 992px)` | 960px |
| Desktop (large) | 1200px | `xl: 1200px` | `@media (min-width: 1200px)` | 1140px |
| Desktop (extra large) | 1400px | `xxl: 1400px` | `@media (min-width: 1400px)` | 1320px |
| Custom breakpoint | N/A | Add to `$grid-breakpoints` | Custom mixin | Add to `$container-max-widths` |

### Pattern: Breakpoint Implementation

```scss
// Override Bootstrap breakpoints if design system differs significantly
$grid-breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 1024px,   // Custom breakpoint (vs Bootstrap 992px)
  xl: 1280px,   // Custom breakpoint (vs Bootstrap 1200px)
  xxl: 1440px   // Custom breakpoint (vs Bootstrap 1400px)
);

// Update container max widths to match
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1200px,
  xxl: 1320px
);

@import "bootstrap";
```

### Common Mistakes

- **Using CSS variables in media queries** - Media queries cannot use CSS variables (CSS spec limitation)
- **Not updating container widths** - When changing breakpoints, update `$container-max-widths` too
- **Breaking Bootstrap grid** - Changing breakpoints affects ALL responsive utilities (`.col-md-*`, `.d-lg-block`, etc.)
- **Forgetting mobile-first approach** - Bootstrap uses `min-width` media queries (mobile-first)

### See Also

- Bootstrap 5.3 Breakpoints: [https://getbootstrap.com/docs/5.3/layout/breakpoints/](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
- Bootstrap 5.3 Grid: [https://getbootstrap.com/docs/5.3/layout/grid/](https://getbootstrap.com/docs/5.3/layout/grid/)

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [SCSS Best Practices](scss-best-practices.md)
- [Token to Utility Flow](token-to-utility-flow.md)
