---
description: Bootstrap Accommodation Decision Framework — systematic methodology for deciding when to accommodate, extend, customize, or create
---

# Bootstrap Accommodation Decision Framework

## When to Use

> Use this framework when mapping any design system element to Bootstrap. Apply the 6px threshold to decide between ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Pixel difference < 6px | ACCOMMODATE | Minimal visual impact, functionally equivalent |
| Bootstrap has extensible system | EXTEND | Add missing values to existing maps |
| Pixel difference ≥ 6px | CUSTOMIZE | Visual impact requires precision |
| No Bootstrap equivalent | CREATE | Outside Bootstrap scope |

## Pattern

**ACCOMMODATE** (Use Bootstrap As-Is):
```scss
// Override Bootstrap variable
$primary: #194582;
$body-color: #141414;

@import "bootstrap";
// .p-2 class generates 8px padding automatically
```

**EXTEND** (Add to Bootstrap System):
```scss
$spacers: map-merge($spacers, (
  "3xs": 2px,   // Add missing micro-spacing
  "2xs": 6px,
));

@import "bootstrap";
// .p-3xs class now available
```

**CUSTOMIZE** (Replace Bootstrap Values):
```scss
$spacers: (
  0: 0,
  "xs": 8px,
  "sm": 24px,   // ≥6px different from Bootstrap
  "md": 32px,
  "lg": 40px,
);

@import "bootstrap";
```

**CREATE** (New Advanced Features):
```scss
@mixin advanced-feature($base-value, $modifier: 1) {
  border-radius: var(--bs-border-radius);

  @supports (backdrop-filter: blur(10px)) {
    backdrop-filter: blur(#{$base-value * $modifier});
  }
}
```

## Common Mistakes

- **Wrong**: Skipping Bootstrap research → **Right**: Systematically investigate variables, mixins, maps, and utilities first
- **Wrong**: Overriding 16px with 14px (2px difference) → **Right**: Accommodate to Bootstrap's 16px (< 6px threshold)
- **Wrong**: Creating custom system when Bootstrap has extensible map → **Right**: Extend Bootstrap's existing map

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap 5.3 Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
- Reference: [Bootstrap 5.3 Utility API](https://getbootstrap.com/docs/5.3/utilities/api/)
