---
description: Creating atom SDC components in Radix — decision framework, component structure, button pattern, SCSS integration
drupal_version: "11.x"
---

# Atoms SDC Components

## When to Use

> Use this when deciding whether to create an atom SDC vs use Bootstrap classes, and when creating foundational UI components.

## Decision

| Atom Type | Radix Provides SDC? | Bootstrap Provides Classes? | Decision |
|-----------|---------------------|----------------------------|----------|
| Button | Yes (`button/`) | Yes (`.btn`) | **REUSE** Radix SDC or Bootstrap classes |
| Input | Yes (`input/`) | Yes (`.form-control`) | **REUSE** Radix SDC or Bootstrap classes |
| Badge | Yes (`badge/`) | Yes (`.badge`) | **REUSE** Radix SDC or Bootstrap classes |
| Heading | Yes (`heading/`) | Yes (`<h1>`-`<h6>`) | **REUSE** Radix SDC or Bootstrap classes |
| Icon | No | No | **CREATE** SDC if reusable |
| Avatar | No | No | **CREATE** SDC if reusable |
| Tag/Chip | No | Partial (`.badge`) | **CREATE** or extend Radix badge |
| Custom atom | No | No | **CREATE** SDC |

**Atom Creation Decision Process:**

```
1. Does Radix provide this atom?
   YES → Reuse Radix SDC
   NO → Continue to step 2

2. Do Bootstrap utility classes suffice?
   YES → Use Bootstrap classes in HTML (no SDC needed)
   NO → Continue to step 3

3. Is this atom reused across multiple templates?
   YES → Create SDC
   NO → Consider inline styles or template-specific CSS

4. Does this atom have configurable variants?
   YES → Create SDC with props
   NO → May not need SDC
```

## Pattern

**Complete SDC File Structure (`components/button/`):**

```
button/
├── button.component.yml    # Component metadata
├── button.twig             # Component template
├── button.scss             # Component styles (optional)
├── button.js               # Component JavaScript (optional)
└── README.mdx              # Documentation (optional)
```

**File: `button.component.yml`**

```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Button
status: experimental
description: Custom button component with design system variants
props:
  type: object
  properties:
    color:
      type: string
      title: Color
      default: ''
      enum: ['', 'primary', 'secondary', 'success']
    size:
      type: string
      title: Size
      default: ''
      enum: ['', 'sm', 'lg']
    disabled:
      type: boolean
      title: Disabled
      default: false
slots:
  content:
    title: Content
    description: Button text or content
```

**File: `button.twig`**

```twig
{%
  set button_classes = [
    'btn',
    color ? 'btn-' ~ color : '',
    size ? 'btn-' ~ size : '',
    disabled ? 'disabled' : '',
  ]
%}

<button {{ attributes.addClass(button_classes) }}>
  {% block content %}
    {{ content }}
  {% endblock %}
</button>
```

**File: `button.scss` (optional)**

```scss
// Import Bootstrap foundation
@import '../../src/scss/init';

// Component-specific styles
.btn {
  // Customizations beyond Bootstrap defaults
  // Use Bootstrap variables for consistency

  &-custom-variant {
    @include button-variant(
      $background: $custom-color,
      $border: $custom-color,
      $color: color-contrast($custom-color)
    );
  }
}
```

**Extending Radix Button:**

```yaml
# components/brand-button/brand-button.component.yml
name: Brand Button
status: stable
description: Brand-specific button with custom colors
props:
  type: object
  properties:
    variant:
      type: string
      default: 'primary'
      enum: ['primary', 'secondary', 'brand-accent']
```

```scss
// components/brand-button/brand-button.scss
@import '../../src/scss/init';

.btn-brand-accent {
  @include button-variant(
    $background: $brand-accent,
    $border: $brand-accent,
    $color: color-contrast($brand-accent),
    $hover-background: shade-color($brand-accent, 10%)
  );
}
```

## Common Mistakes

- **Wrong**: Creating SDC for every element → **Right**: Use Bootstrap classes when possible
- **Wrong**: Duplicating Radix SDCs → **Right**: Check `radix/components/` first
- **Wrong**: SDC SCSS without `@import '../../src/scss/init'` → **Right**: Import for Bootstrap access
- **Wrong**: Hardcoding colors in SCSS → **Right**: Define in `base/_variables.scss` first
- **Wrong**: Not using Bootstrap mixins → **Right**: Use `button-variant()` for consistency
- **Wrong**: Naming mismatch (directory `button/` with `btn.component.yml`) → **Right**: File prefix must match directory name
- **Wrong**: Missing schema reference → **Right**: Include `$schema` for validation
- **Wrong**: Not using slots → **Right**: Slots enable content composition
- **Wrong**: Hardcoding props → **Right**: Use props for variant configuration

## See Also

- [SDC Component Best Practices](sdc-component-best-practices.md)
- [SDC Component Development](sdc-component-development.md)
- [Radix Component Reuse Strategy](radix-component-reuse-strategy.md)
- Design System Recognition Guide: Section 2.2 (Atom Recognition)
- Official Drupal SDC Documentation: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
