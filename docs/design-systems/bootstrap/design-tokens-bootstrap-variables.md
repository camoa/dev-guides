---
description: Map design system tokens (colors, typography, spacing, borders, shadows, breakpoints) to Bootstrap SCSS variables
---

# Design Tokens → Bootstrap Variables

## When to Use

> Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system.

## Color Tokens

| Design System Token Type | Bootstrap Variable | Bootstrap Map |
|-------------------------|-------------------|---------------|
| Primary/secondary colors | `$primary`, `$secondary` | `$theme-colors` |
| Brand colors (additional) | N/A (extend map) | Add to `$theme-colors` |
| Gray/neutral scales | `$gray-100` through `$gray-900` | `$grays` |
| Semantic colors | `$success`, `$danger`, `$warning`, `$info` | `$theme-colors` |
| Text colors | `$body-color`, `$headings-color` | N/A |
| Background colors | `$body-bg`, `$secondary-bg` | N/A |
| Border colors | `$border-color` | N/A |

### Pattern

```scss
// 1. Override BEFORE importing Bootstrap
$primary: #194582;
$secondary: #6c757d;

// 2. Extend theme colors
$theme-colors: map-merge($theme-colors, (
  "brand-blue": #0066cc,
));

// 3. Import Bootstrap
@import "bootstrap";
```

## Typography Tokens

| Design System Token | Bootstrap Variable |
|--------------------|-------------------|
| Base font size | `$font-size-base` |
| Font family (body) | `$font-family-base` |
| Font family (headings) | `$headings-font-family` |
| Font family (mono) | `$font-family-monospace` |
| Heading sizes | `$h1-font-size` through `$h6-font-size` |
| Display sizes | `$display-font-sizes` map |
| Line heights | `$line-height-base`, `$line-height-sm`, `$line-height-lg` |
| Font weights | `$font-weight-lighter`, `$font-weight-normal`, `$font-weight-bold` |

### Pattern

```scss
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.5;

// Override heading sizes if ≥6px different
$h1-font-size: $font-size-base * 2.5;  // 40px
$h2-font-size: $font-size-base * 2;    // 32px

@import "bootstrap";
```

## Spacing Tokens

| Design System Scale | Bootstrap Default | Bootstrap Map Key | Generated Utilities |
|---------------------|------------------|------------------|---------------------|
| 0px | 0px | `0: 0` | `.m-0`, `.p-0` |
| 4px | 4px (0.25rem) | `1: $spacer * 0.25` | `.m-1`, `.p-1` |
| 8px | 8px (0.5rem) | `2: $spacer * 0.5` | `.m-2`, `.p-2` |
| 16px | 16px (1rem) | `3: $spacer` | `.m-3`, `.p-3` |
| 24px | 24px (1.5rem) | `4: $spacer * 1.5` | `.m-4`, `.p-4` |
| 48px | 48px (3rem) | `5: $spacer * 3` | `.m-5`, `.p-5` |

### Pattern

```scss
// ACCOMMODATE: Use Bootstrap defaults (no override needed)
@import "bootstrap";

// EXTEND: Add missing micro-spacing
$spacers: map-merge($spacers, (
  "3xs": 2px,
  "2xs": 6px,
));

// CUSTOMIZE: Replace scale entirely (≥6px systematic differences)
$spacers: (
  0: 0,
  xs: 8px,
  sm: 24px,
  md: 32px,
  lg: 40px,
  xl: 64px,
);
```

## Surface Tokens (Border, Radius, Shadow)

| Design System Token | Bootstrap Variable |
|--------------------|-------------------|
| Border width | `$border-width` |
| Border color | `$border-color` |
| Border radius (base) | `$border-radius` |
| Border radius (small/large) | `$border-radius-sm`, `$border-radius-lg` |
| Border radius (pill) | `$border-radius-pill` |
| Box shadow (small/base/large) | `$box-shadow-sm`, `$box-shadow`, `$box-shadow-lg` |

### Pattern

```scss
$border-width: 1px;
$border-radius: 0.375rem;
$border-radius-sm: 0.25rem;
$border-radius-lg: 0.5rem;

$box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
$box-shadow-sm: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.075);
$box-shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);

@import "bootstrap";
```

## Breakpoint Tokens

| Design System Breakpoint | Bootstrap Default | Bootstrap Map Key |
|-------------------------|------------------|------------------|
| Mobile (small) | 576px | `sm: 576px` |
| Tablet | 768px | `md: 768px` |
| Desktop (small) | 992px | `lg: 992px` |
| Desktop (large) | 1200px | `xl: 1200px` |
| Desktop (extra large) | 1400px | `xxl: 1400px` |

### Pattern

```scss
$grid-breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 1024px,   // Custom (vs Bootstrap 992px)
  xl: 1280px,   // Custom (vs Bootstrap 1200px)
  xxl: 1440px   // Custom (vs Bootstrap 1400px)
);

$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1200px,
  xxl: 1320px
);

@import "bootstrap";
```

## Common Mistakes

- **Wrong**: Setting variables after Bootstrap import → **Right**: Override BEFORE importing Bootstrap (!default flag behavior)
- **Wrong**: Hardcoding hex codes in components → **Right**: Use Bootstrap variables ($primary, etc.)
- **Wrong**: Hardcoding font-weight: 700 → **Right**: Use $font-weight-bold
- **Wrong**: Mixing rem and px inconsistently → **Right**: Use Bootstrap's rem-based system
- **Wrong**: Changing breakpoints without updating container widths → **Right**: Update both $grid-breakpoints and $container-max-widths

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [SCSS Best Practices](scss-best-practices.md)
- [Token to Utility Flow](token-to-utility-flow.md)
- Reference: [Bootstrap Typography](https://getbootstrap.com/docs/5.3/content/typography/)
- Reference: [Bootstrap Spacing Utilities](https://getbootstrap.com/docs/5.3/utilities/spacing/)
- Reference: [Bootstrap Breakpoints](https://getbootstrap.com/docs/5.3/layout/breakpoints/)
