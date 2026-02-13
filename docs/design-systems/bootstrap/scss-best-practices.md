---
description: Critical SCSS patterns and anti-patterns for Bootstrap customization
---

# SCSS Best Practices

## When to Use

> Use this when writing SCSS for Bootstrap customization. Apply these patterns to prevent technical debt and maintain upgrade compatibility.

## Philosophy

**Work WITH Bootstrap's architecture, not against it.** These practices prevent technical debt, maintain upgrade compatibility, and ensure predictable CSS output.

## Core SCSS Principles

### Variable Scoping

- **Global variables** - Define at root level for design system tokens
- **Local variables** - Define within mixins/functions for calculations
- **WHY:** Proper scoping prevents naming collisions and makes refactoring safer

### Nesting Limits (CRITICAL)

**Maximum 2-3 nesting levels:**

```scss
// ❌ WRONG: Excessive nesting
.navbar {
  .nav {
    .nav-item {
      .nav-link {
        &:hover {
          color: $primary; // 5 levels = disaster
        }
      }
    }
  }
}

// ✅ CORRECT: Limited nesting
.navbar {
  .nav-link {
    &:hover {
      color: $primary; // 3 levels = manageable
    }
  }
}
```

**WHY excessive nesting fails:**
- Overly specific CSS (specificity 0,0,4,1)
- Performance issues (browser selector matching overhead)
- Impossible to override without `!important`
- SCSS compile performance degradation

### Module System (Modern SCSS)

```scss
// ❌ OLD: @import (deprecated)
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";

// ✅ NEW: @use with namespacing
@use "bootstrap/scss/functions" as bs-fn;
@use "bootstrap/scss/variables" as bs-var;

.component {
  padding: bs-fn.map-get(bs-var.$spacers, 3);
}
```

**WHY @use is required:**
- No global scope pollution
- Performance improvement (faster compilation)
- Prevents naming conflicts
- @import is deprecated (will be removed)

### Mixin Usage

```scss
// ❌ WRONG: Mixin without arguments
@mixin button-base {
  padding: 0.5rem 1rem;
  border: none;
}

// ✅ CORRECT: Mixin WITH arguments
@mixin button-variant($bg, $color, $hover-bg) {
  background: $bg;
  color: $color;

  &:hover {
    background: $hover-bg;
  }
}

// ✅ CORRECT: Use %placeholder for static styles
%button-base {
  padding: 0.5rem 1rem;
  border: none;
}

.btn-primary { @extend %button-base; }
```

**WHY:** Mixins without arguments duplicate CSS in every output location. Use mixins ONLY when arguments provide dynamic functionality.

## Bootstrap Integration Patterns

### ✅ DO

| Pattern | Code |
|---------|------|
| Use Bootstrap variables | `padding: $btn-padding-y $btn-padding-x;` |
| Use Bootstrap mixins | `@include button-variant($bg, $border, $color);` |
| Extend Bootstrap maps | `$spacers: map-merge($spacers, ("3xs": 2px));` |

### ❌ DON'T

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| `@extend .btn` | Selector explosion, specificity chaos |
| `!important` everywhere | Specificity wars, maintenance nightmare |
| Hardcode Bootstrap values | Breaks with Bootstrap updates |
| Nesting >3 levels | Specificity issues, performance overhead |

## Critical Anti-Patterns

### Never @extend Bootstrap Classes

```scss
// ❌ WRONG
.custom-button {
  @extend .btn;
  @extend .btn-primary;
}

// ✅ CORRECT
.custom-button {
  padding: $btn-padding-y $btn-padding-x;
  background: $primary;
  border-radius: $btn-border-radius;
}
```

**WHY @extend is dangerous:**
1. Selector explosion (combinatorial nightmare)
2. Unpredictable specificity changes
3. Bootstrap class pollution
4. Maintenance nightmare
5. Performance issues
6. Debugging hell

**If you MUST use @extend:** Limit to `%placeholder` selectors ONLY, never actual CSS classes.

### Never Use !important

```scss
// ❌ WRONG
.component {
  color: #0066cc !important;
  padding: 1rem !important;
}

// ✅ CORRECT
.component {
  color: $primary;
  padding: $spacer;
}
```

**WHY !important is dangerous:**
1. Specificity wars
2. Maintenance nightmare
3. Impossible to override
4. Code smell
5. Team collaboration issues

**ONLY acceptable use:** Utility classes designed to override everything (proactive, not reactive).

### Never Hardcode Bootstrap Values

```scss
// ❌ WRONG
.component {
  padding: 0.375rem 0.75rem;
  color: #0d6efd;
  font-weight: 700;
}

// ✅ CORRECT
.component {
  padding: $btn-padding-y $btn-padding-x;
  color: $primary;
  font-weight: $font-weight-bold;
}
```

## Common Mistakes

- **Wrong**: Using @extend on Bootstrap classes → **Right**: Use Bootstrap variables and mixins
- **Wrong**: 5+ nesting levels → **Right**: Maximum 2-3 nesting levels
- **Wrong**: @import for Bootstrap modules → **Right**: @use with namespacing
- **Wrong**: Mixins without arguments → **Right**: Use %placeholders for static styles

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- Reference: [SASS Best Practices (Educative)](https://www.educative.io/blog/sass-best-practices-frontend-coding-tips)
- Reference: [Smashing Magazine: Extending In Sass](https://www.smashingmagazine.com/2015/05/extending-in-sass-without-mess/)
