---
description: "Critical SCSS patterns and anti-patterns for Bootstrap customization"
tldr: "Use this when writing SCSS for Bootstrap customization. Apply these patterns to prevent technical debt and maintain upgrade compatibility."
drupal_version: "11.x"
---

# SCSS Best Practices

## When to Use

> Use this when writing SCSS for Bootstrap customization. Apply these patterns to prevent technical debt and maintain upgrade compatibility.

- You're writing SCSS for Bootstrap customization
- You need to understand critical SCSS anti-patterns and why they're harmful
- You want to ensure proper variable usage and maintainability
- You're establishing team coding standards for SCSS development

## Philosophy

Work WITH Bootstrap's architecture, not against it. These practices prevent technical debt, maintain upgrade compatibility, and ensure predictable CSS output.

## Core SCSS Principles

### Variable Scoping

- **Global variables** - Define at root level for design system tokens (colors, typography, spacing)
- **Local variables** - Define within mixins/functions for calculations and temporary values
- **WHY:** Proper scoping prevents naming collisions and makes refactoring safer

### Nesting Limits (CRITICAL)

```scss
// ❌ WRONG: Excessive nesting creates specificity nightmares
.navbar {
  .nav {
    .nav-item {
      .nav-link {
        &:hover {
          color: $primary; // 5 levels deep = disaster
        }
      }
    }
  }
}

// ✅ CORRECT: Limit nesting to 2-3 levels maximum
.navbar {
  .nav-link {
    &:hover {
      color: $primary; // 3 levels deep = manageable
    }
  }
}
```

**WHY:** Excessive nesting (>3 levels) leads to:
- Overly specific CSS (`.navbar .nav .nav-item .nav-link:hover` = specificity 0,0,4,1)
- Performance issues (browser selector matching overhead)
- Maintenance nightmares (impossible to override without `!important`)
- SCSS compile performance degradation

**Reference:** [SASS Best Practices (Educative)](https://www.educative.io/blog/sass-best-practices-frontend-coding-tips) - Nesting depth guidelines

### Module System (Modern SCSS)

```scss
// ❌ OLD: @import pollutes global scope (deprecated)
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";

// ✅ NEW: @use with namespacing (Dart Sass 1.23+)
@use "bootstrap/scss/functions" as bs-fn;
@use "bootstrap/scss/variables" as bs-var;

// Access with namespace
.component {
  padding: bs-fn.map-get(bs-var.$spacers, 3);
}
```

**WHY @use is required:**
- **No global scope pollution** - Variables/mixins exist only in module namespace
- **Performance improvement** - Faster compilation and better debugging
- **Prevents naming conflicts** - Multiple modules can have same variable names
- **@import is deprecated** - Will be removed in future Sass versions

**Reference:** [The Latest in SCSS 2025](https://medium.com/@vrutika.premani12/the-latest-in-scss-features-best-practices-and-trends-in-2025-244921be6724) - @use optimization

### Mixin Usage Best Practices

```scss
// ❌ WRONG: Mixin without arguments (just use CSS)
@mixin button-base {
  padding: 0.5rem 1rem;
  border: none;
}

// ✅ CORRECT: Mixin WITH arguments (dynamic functionality)
@mixin button-variant($bg, $color, $hover-bg) {
  background: $bg;
  color: $color;

  &:hover {
    background: $hover-bg;
  }
}

// ❌ WRONG: Mixin without parameters used everywhere (code bloat)
.btn-primary { @include button-base; }
.btn-secondary { @include button-base; }
// Result: Duplicate CSS in output

// ✅ CORRECT: CSS class or %placeholder for static styles
%button-base {
  padding: 0.5rem 1rem;
  border: none;
}

.btn-primary { @extend %button-base; } // Only %placeholders, never .classes
```

**WHY:** Mixins without arguments duplicate CSS in every output location. Use mixins ONLY when arguments provide dynamic functionality, otherwise use CSS classes or `%placeholder` selectors.

**Reference:** [SASS Best Practices Tools](https://evnedev.com/blog/development/sass-best-practices-tips-and-tools-you-should-know/) - Mixin optimization

## Bootstrap Integration Patterns

### Use Bootstrap Variables

```scss
// ✅ GOOD: Reference Bootstrap variables
.custom-component {
  padding: $btn-padding-y $btn-padding-x;
  background: $primary;
  border-radius: $border-radius;
}
```

### Use Bootstrap Mixins

```scss
// ✅ GOOD: Use Bootstrap mixins with custom values
.custom-gradient {
  @include gradient-directional($custom-start, $custom-end, 45deg);
}

.custom-button {
  @include button-variant(
    $background: $custom-bg,
    $border: $custom-border,
    $color: $custom-color
  );
}
```

### Extend Bootstrap Maps

```scss
// ✅ GOOD: Add to Bootstrap's existing systems
$theme-colors: map-merge($theme-colors, (
  'brand': #your-brand-color,
));

$spacers: map-merge($spacers, (
  "3xs": 2px,
));
```

## Bootstrap Anti-Patterns

### Never @extend Bootstrap Classes

```scss
// ❌ WRONG: This breaks Bootstrap's architecture
.custom-button {
  @extend .btn;           // DON'T DO THIS
  @extend .btn-primary;   // DON'T DO THIS
}

// ✅ CORRECT: Use mixins or HTML classes
.custom-button {
  // Use Bootstrap variables instead
  padding: $btn-padding-y $btn-padding-x;
  background: $primary;
  border-radius: $btn-border-radius;
}

// OR: Use HTML classes directly
// <button class="btn btn-primary">Button</button>
```

**Why @extend is Dangerous:**
1. **Selector explosion (combinatorial nightmare)** - When selectors with ancestors extend other selectors with ancestors, all permutations must be accounted for, causing exponential CSS growth
2. **Unpredictable specificity changes** - Specificity shifts unexpectedly; for example, `@extend .btn` from `#goog-wm-sb` generates `:not(#goog-wm-sb)` with ID selector specificity making overrides impossible without `!important`
3. **Bootstrap class pollution** - Breaks Bootstrap's intended usage patterns and component isolation
4. **Maintenance nightmare** - Changes to Bootstrap cascade into your extended components unpredictably
5. **Performance issues** - Bloated CSS output with duplicate declarations and massive selector chains
6. **Debugging hell** - Can't trace where styles originate in compiled CSS output

**CRITICAL: If you MUST use @extend** - Limit it to Sass `%placeholder` selectors ONLY, never actual CSS selectors (classes, tags, IDs). Define relationships once, keep them one-sided, and always use placeholders to reduce CSS output.

**Reference:** [Smashing Magazine: Extending In Sass Without Creating A Mess](https://www.smashingmagazine.com/2015/05/extending-in-sass-without-mess/) - Deep dive into @extend problems and solutions

### Never Use !important (Code Smell)

```scss
// ❌ WRONG: !important creates specificity wars
.component {
  color: #0066cc !important;  // Maintenance nightmare
  padding: 1rem !important;   // Impossible to override
}

// ✅ CORRECT: Solve specificity properly
.component {
  color: $primary;
  padding: $spacer;
}
```

**Why !important is Dangerous:**
1. **Specificity wars** - When multiple `!important` declarations compete, the one with higher specificity wins, creating a vicious loop of ever-increasing specificity
2. **Maintenance nightmare** - Makes code untidy, difficult to understand, and extends debugging time
3. **Impossible to override** - Forces you to use more `!important` declarations, creating technical debt
4. **Code smell** - Using `!important` reactively to escape specificity problems is a symptom of ill-formed CSS; it only fixes symptoms, not root causes
5. **Team collaboration issues** - Multiple developers using `!important` creates unmaintainable stylesheets

**ONLY acceptable use:** When you know UP FRONT that a style will ALWAYS take precedence (proactive, not reactive). Example: utility classes designed to override everything.

**Better alternative:** Import third-party CSS into cascade layers rather than using `!important` to override external libraries.

**Reference:** [CSS-Tricks: Code Smells in CSS](https://css-tricks.com/css-code-smells/) - Harry Roberts on CSS anti-patterns

### Never Hardcode Bootstrap Values

```scss
// ❌ WRONG: Hardcoded values break with Bootstrap updates
.component {
  padding: 0.375rem 0.75rem; // DON'T hardcode Bootstrap values
  color: #0d6efd;            // DON'T hardcode Bootstrap colors
}

// ✅ CORRECT: Use Bootstrap variables
.component {
  padding: $btn-padding-y $btn-padding-x;
  color: $primary;
}
```

### Never Hardcode Font/Weight Values

```scss
// ❌ WRONG: Hardcoded values lose design system consistency
.component {
  font-family: "Helvetica Neue", sans-serif;  // DON'T hardcode fonts
  font-weight: 700;                           // DON'T hardcode weights
  line-height: 1.5;                           // DON'T hardcode line heights
}

// ✅ CORRECT: Use established variables
.component {
  font-family: $font-family-base;
  font-weight: $font-weight-bold;
  line-height: $line-height-base;
}
```

## Common Mistakes

- **Wrong**: Using @extend on Bootstrap classes → **Right**: Use Bootstrap variables and mixins
- **Wrong**: 5+ nesting levels → **Right**: Maximum 2-3 nesting levels
- **Wrong**: @import for Bootstrap modules → **Right**: @use with namespacing
- **Wrong**: Mixins without arguments → **Right**: Use %placeholders for static styles

## See Also

- ← Previous: [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- Next: [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- Reference: [SASS Best Practices (Educative)](https://www.educative.io/blog/sass-best-practices-frontend-coding-tips)
- Reference: [Smashing Magazine: Extending In Sass](https://www.smashingmagazine.com/2015/05/extending-in-sass-without-mess/)
