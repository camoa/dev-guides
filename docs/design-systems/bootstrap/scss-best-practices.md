---
description: SCSS Best Practices — critical anti-patterns and why they're harmful when customizing Bootstrap
---

# SCSS Best Practices

## When to Use

> Use when writing SCSS for Bootstrap customization. Understand critical anti-patterns and why they're harmful.

## Decision

| Situation | Wrong Approach | Right Approach |
|-----------|----------------|----------------|
| Sharing static styles | Mixin without arguments | CSS class or `%placeholder` |
| Need Bootstrap button styles | `@extend .btn` | Use `.btn` class in HTML or Bootstrap mixins |
| Override styles | `!important` everywhere | Solve specificity properly |
| Deep nesting | 5+ levels | Limit to 2-3 levels |
| Module imports | `@import` (deprecated) | `@use` with namespacing |

## Pattern

**Nesting Limits** (2-3 levels max):
```scss
// ✅ CORRECT
.navbar {
  .nav-link {
    &:hover {
      color: $primary;
    }
  }
}
```

**Module System** (Dart Sass):
```scss
// ✅ CORRECT: @use with namespacing
@use "bootstrap/scss/functions" as bs-fn;
@use "bootstrap/scss/variables" as bs-var;

.component {
  padding: bs-fn.map-get(bs-var.$spacers, 3);
}
```

**Bootstrap Integration**:
```scss
// ✅ CORRECT: Use Bootstrap variables and mixins
.custom-button {
  padding: $btn-padding-y $btn-padding-x;
  background: $primary;
  border-radius: $border-radius;

  @include button-variant(
    $background: $custom-bg,
    $border: $custom-border,
    $color: $custom-color
  );
}
```

## Common Mistakes

- **Wrong**: `@extend .btn` → **Right**: Use Bootstrap mixins or HTML classes (combinatorial explosion, unpredictable specificity)
- **Wrong**: `color: #0066cc !important` → **Right**: Solve specificity properly (creates maintenance nightmare)
- **Wrong**: `font-family: "Helvetica Neue"` → **Right**: `font-family: $font-family-base` (enables global updates)
- **Wrong**: 5 levels of nesting → **Right**: 2-3 levels max (overly specific CSS, performance issues)
- **Wrong**: `@import` (deprecated) → **Right**: `@use` with namespacing (no global scope pollution)

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- Reference: [Smashing Magazine: Extending In Sass Without Creating A Mess](https://www.smashingmagazine.com/2015/05/extending-in-sass-without-mess/)
- Reference: [CSS-Tricks: Code Smells in CSS](https://css-tricks.com/css-code-smells/)
- Reference: [Educative: SASS Best Practices](https://www.educative.io/blog/sass-best-practices-frontend-coding-tips)
