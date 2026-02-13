---
description: Design Tokens to Bootstrap Variables — mapping color, typography, spacing, surface, and breakpoint tokens
---

# Design Tokens to Bootstrap Variables

## When to Use

> Use when mapping design tokens (colors, typography, spacing) to Bootstrap's SCSS variable system. Use after identifying tokens via Design System Recognition Guide.

## Decision

| Token Type | Bootstrap Variable | Bootstrap Map | Strategy |
|-----------|-------------------|---------------|----------|
| Primary/secondary colors | `$primary`, `$secondary` | `$theme-colors` | Override variables |
| Brand colors (additional) | N/A | Add to `$theme-colors` | Extend map |
| Gray/neutral scales | `$gray-100` through `$gray-900` | `$grays` | Override variables |
| Typography base | `$font-family-base`, `$font-size-base` | N/A | Override variables |
| Spacing scale | `$spacer` | `$spacers` map | Override or extend |
| Border/radius/shadow | `$border-radius`, `$box-shadow` | N/A | Override variables |
| Breakpoints | N/A | `$grid-breakpoints` | Override map |

## Pattern

**Color Tokens**:
```scss
// Override Bootstrap color variables
$primary: #194582;
$secondary: #6c757d;

// Extend theme colors map
$theme-colors: map-merge($theme-colors, (
  "brand-blue": #0066cc,
  "brand-teal": #20c997
));

@import "bootstrap";
```

**Typography Tokens**:
```scss
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.5;

// Override heading sizes if ≥6px different
$h1-font-size: $font-size-base * 2.5;
$h2-font-size: $font-size-base * 2;

@import "bootstrap";
```

**Spacing Tokens** (EXTEND strategy):
```scss
$spacers: map-merge($spacers, (
  "3xs": 2px,
  "2xs": 6px,
));

@import "bootstrap";
```

**Spacing Tokens** (CUSTOMIZE strategy):
```scss
$spacers: (
  0: 0,
  xs: 8px,
  sm: 24px,
  md: 32px,
  lg: 40px,
  xl: 64px,
);

@import "bootstrap";
```

**Surface Tokens**:
```scss
$border-width: 1px;
$border-radius: 0.375rem;
$box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);

@import "bootstrap";
```

**Breakpoint Tokens**:
```scss
$grid-breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 1024px,
  xl: 1280px,
  xxl: 1440px
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

- **Wrong**: Setting colors after Bootstrap import → **Right**: Override variables BEFORE import (`!default` flag)
- **Wrong**: Hardcoding `#0066cc` in components → **Right**: Use `$primary` (enables global updates)
- **Wrong**: Hardcoding font families → **Right**: Use `$font-family-base` (ONE variable change updates entire site)
- **Wrong**: Mixing rem and px inconsistently → **Right**: Use rem for accessibility
- **Wrong**: Not updating container widths when changing breakpoints → **Right**: Update `$container-max-widths` too

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Token to Utility Flow](token-to-utility-flow.md)
- Reference: [Bootstrap 5.3 Sass Variables](https://getbootstrap.com/docs/5.3/customize/sass/)
- Reference: [Bootstrap 5.3 Color System](https://getbootstrap.com/docs/5.3/customize/color/)
- Reference: [Bootstrap 5.3 Typography](https://getbootstrap.com/docs/5.3/content/typography/)
- Reference: [Bootstrap 5.3 Spacing](https://getbootstrap.com/docs/5.3/utilities/spacing/)
