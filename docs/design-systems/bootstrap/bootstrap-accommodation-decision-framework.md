---
description: "Core decision-making methodology for Bootstrap mapping using the 6px threshold"
tldr: "Use this framework when deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE. Use the 6px threshold to systematically evaluate visual differences."
drupal_version: "11.x"
---

# Bootstrap Accommodation Decision Framework

## When to Use

> Use this framework when deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE. Use the 6px threshold to systematically evaluate visual differences.

- You need to understand the core decision-making methodology for Bootstrap mapping
- You're deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE
- You need to apply the 6px threshold systematically
- You want to ensure proper SCSS practices and quality standards

## Core Principle

> **"Minimal visual impact justifies accommodation, significant visual differences require customization"**

## Framework Goals

- **Maximize Bootstrap ecosystem compatibility** while preserving design integrity
- **Systematic decision-making** for any design system → Bootstrap conversion
- **Minimize maintenance overhead** through strategic accommodation
- **Enable advanced features** when Bootstrap scope is exceeded
- **Maintain upgrade compatibility** by working with Bootstrap's architecture

## The 6-Pixel Rule

### When to ACCOMMODATE vs CUSTOMIZE

**ACCOMMODATE to Bootstrap When:**
- **Pixel differences < 6px** - Minimal visual impact, functionally equivalent
- **Bootstrap value achieves same design intent**
- **Single isolated value variations** (not systematic scale differences)
- **High maintenance cost** for minimal visual gain

**CUSTOMIZE When:**
- **Pixel differences ≥ 6px** - Visual impact requires attention and precision
- **Systematic differences** affecting entire design scales
- **Brand-critical measurements** (logo lockups, signature spacing)
- **Functional requirements** (accessibility, touch targets, mobile optimization)

### Application Examples

| Design System Value | Bootstrap Value | Difference | Decision | Rationale |
|---------------------|----------------|-----------|----------|-----------|
| 8px spacing | 8px (0.5rem) | 0px | ✅ ACCOMMODATE | Exact match |
| 14px spacing | 16px (1rem) | 2px | ✅ ACCOMMODATE | < 6px threshold |
| 18px spacing | 24px (1.5rem) | 6px | 🔴 CUSTOMIZE | ≥ 6px threshold |
| 2px micro-spacing | Not available | N/A | 🔶 EXTEND | Missing value |
| Advanced blur effect | Not available | N/A | 🆕 CREATE | Outside Bootstrap scope |

## Decision Categories

### ✅ ACCOMMODATE (Use Bootstrap As-Is)

**Criteria:**
- < 6px difference from Bootstrap defaults
- Same design intent achieved
- Low maintenance benefit

**Implementation:**
```scss
// Use Bootstrap variables directly
$primary: #194582;           // Override Bootstrap variable
$body-color: #141414;        // Override Bootstrap variable

// Use Bootstrap utilities in HTML
.btn-primary                 // Automatically uses $primary color
.p-2                        // Automatically uses Bootstrap 8px spacing
```

**Result:** `.p-2` class generates 8px padding automatically through Bootstrap's utility system.

### 🔶 EXTEND (Add to Bootstrap System)

**Criteria:**
- Missing values in Bootstrap
- Useful additions to existing systems
- Systematic gaps that need filling

**Implementation:**
```scss
// Add to Bootstrap's existing maps
$spacers: map-merge($spacers, (
  "3xs": 2px,               // Add missing micro-spacing
  "2xs": 6px,               // Add missing value
));

$theme-colors: map-merge($theme-colors, (
  "brand": #your-brand-color, // Add brand color to Bootstrap system
));
```

**Result:** `.p-3xs` class available alongside Bootstrap defaults. Bootstrap's utility API auto-generates classes from extended maps.

### 🔴 CUSTOMIZE (Replace Bootstrap Values)

**Criteria:**
- ≥ 6px difference from Bootstrap defaults
- Systematic scale changes
- Brand requirements

**Implementation:**
```scss
// Replace Bootstrap defaults with design system values
$spacers: (
  0: 0,
  "3xs": 2px,
  "2xs": 4px,
  "xs": 8px,
  "sm": 24px,               // Custom value ≥6px different from Bootstrap
  "md": 32px,               // Custom value ≥6px different from Bootstrap
  "lg": 40px,               // Custom value ≥6px different from Bootstrap
  "xl": 64px,
);
```

**Result:** `.p-sm` generates 24px padding using design system values, replacing Bootstrap's defaults entirely.

### 🆕 CREATE (New Advanced Features)

**Criteria:**
- Modern design features not available in Bootstrap
- Advanced visual effects outside Bootstrap's scope
- Complex functionality requiring custom systems

**Bootstrap Constraint:** Bootstrap focuses on core layout/components, not cutting-edge effects.

**Examples:**
- Advanced visual effects (backdrop-filter, advanced shadows)
- Complex animations (keyframe sequences, micro-interactions)
- Modern CSS features (advanced Grid, CSS custom properties systems)

**Implementation Strategy:**
```scss
// Modern features not available in Bootstrap
// Follow Bootstrap patterns where possible
@mixin advanced-feature($base-value, $modifier: 1) {
  // Use Bootstrap variables when applicable
  border-radius: var(--bs-border-radius);

  // Implement advanced functionality
  // Include progressive enhancement
  @supports (backdrop-filter: blur(10px)) {
    backdrop-filter: blur(#{$base-value * $modifier});
  }
}

// Generate utilities following Bootstrap methodology
@each $name, $value in $feature-map {
  .advanced-#{$name} {
    @include advanced-feature($value);
  }
}
```

**Integration:** Use Bootstrap variables, mixins, and utility patterns where possible to maintain consistency.

## Bootstrap Research Methodology

**CRITICAL: Research Bootstrap Capabilities FIRST**

Before categorizing any feature, systematically investigate Bootstrap's capabilities:

### Step 1: Bootstrap Documentation Review

**Check Bootstrap Variables:**
```scss
// Look for variables in _variables.scss
$font-size-base: 1rem !default;
$spacer: 1rem !default;
$border-radius: 0.375rem !default;
$primary: #0d6efd !default;
```

**Reference:** [https://getbootstrap.com/docs/5.3/customize/sass/](https://getbootstrap.com/docs/5.3/customize/sass/)

### Step 2: Bootstrap Mixins Investigation

**Check Available Mixins:**
```scss
// Look for mixins in mixins/_*.scss
@mixin gradient-directional($start-color, $end-color, $deg: 45deg)
@mixin border-radius($radius: $border-radius)
@mixin font-size($size)
@mixin button-variant($background, $border, $color)
```

**Reference:** `/core/scss/mixins/_*.scss` files

### Step 3: Bootstrap Maps Examination

**Check Extensible Maps:**
```scss
// Look for maps in _maps.scss
$spacers: (
  0: 0,
  1: $spacer * 0.25,
  2: $spacer * 0.5,
  // Can we add to this map?
) !default;

$theme-colors: (
  "primary": $primary,
  "secondary": $secondary,
  // Can we add brand colors here?
) !default;
```

**Reference:** [https://getbootstrap.com/docs/5.3/customize/color/](https://getbootstrap.com/docs/5.3/customize/color/)

### Step 4: Bootstrap Utilities Research

**Check Utility Generation:**
```scss
// Look in _utilities.scss and utilities/_api.scss
$utilities: (
  "margin": (
    property: margin,
    class: m,
    values: map-merge($spacers, (auto: auto))
  ),
  "color": (
    property: color,
    class: text,
    values: map-merge($theme-colors, $colors)
  ),
)
```

**Reference:** [https://getbootstrap.com/docs/5.3/utilities/api/](https://getbootstrap.com/docs/5.3/utilities/api/)

## Decision Tree After Research

1. **Bootstrap has exact feature** → ✅ **ACCOMMODATE**
2. **Bootstrap has extensible system** → 🔶 **EXTEND**
3. **Bootstrap has similar feature with ≥6px difference** → 🔴 **CUSTOMIZE**
4. **Bootstrap has no equivalent or capability** → 🆕 **CREATE**

## Common Mistakes

- **Wrong**: Customizing before researching Bootstrap capabilities → **Right**: Research Bootstrap first, then decide
- **Wrong**: Accommodating ≥6px differences → **Right**: Apply 6px threshold rigorously
- **Wrong**: Creating from scratch when Bootstrap has extensible system → **Right**: Extend existing Bootstrap maps

## See Also

- Next: [SCSS Best Practices](scss-best-practices.md)
- Related: [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
