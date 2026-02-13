---
description: SDC component best practices — granularity decisions, props vs slots, SCSS scoping, schema definitions
drupal_version: "11.x"
---

# SDC Component Best Practices

## When to Use

> Use this when deciding component granularity (too small vs too large), needing guidance on props vs slots architecture, or questioning whether a Bootstrap class suffices vs creating an SDC.

## Decision

**Component Granularity:**

| Create SDC When | Don't Create SDC When |
|----------------|----------------------|
| Reused across multiple templates (3+ places) | Just applying 1-3 Bootstrap classes |
| Has configurable variants | Bootstrap utility classes suffice (`.d-flex`, `.mb-3`) |
| Contains custom markup structure | Simple spacing/layout needs |
| Represents design system atom/molecule | Template-specific one-off element |

**Component Size:**

| Too Small | Sweet Spot | Too Large |
|-----------|-----------|-----------|
| Wrapper for `.d-flex .gap-2` | Icon button with configurable position | Hero with 30+ props for all variants |
| Spacer component (`.mb-3`) | Card with image/title/footer slots | Monolithic component with unused props |
| Single Bootstrap class wrapper | Search bar (input + button) | 200+ lines of Twig with complex conditionals |

**Props vs Slots:**

| Scenario | Use Props | Use Slots | WHY |
|----------|-----------|-----------|-----|
| Simple text/string | ✅ | ❌ | Props are validated, typed, documented in schema |
| HTML content | ❌ | ✅ | Props can't contain markup safely |
| Number/boolean config | ✅ | ❌ | Props provide type validation |
| Nested components | ❌ | ✅ | Slots enable composition |
| User-generated content | ❌ | ✅ | Props shouldn't trust user HTML |
| Design system token | ✅ | ❌ | Props enforce valid values via enum |

## Pattern

**Props for Configuration:**

```yaml
props:
  type: object
  properties:
    size:
      type: string
      enum: ['sm', 'md', 'lg']  # Enforce valid values
      default: 'md'
    color:
      type: string
      enum: ['primary', 'secondary', 'success']
      default: 'primary'
```

**Slots for Content:**

```yaml
slots:
  header:
    title: Card Header
    description: Optional header content with custom markup
  body:
    title: Card Body
    description: Main card content
  footer:
    title: Card Footer
    description: Optional footer with buttons or links
```

**BEM Inside Components (SCSS Scoping):**

```scss
// components/card-teaser/card-teaser.scss
@import '../../src/scss/init';

.card-teaser {
  background: $white;
  border-radius: $border-radius;

  &__image {
    width: 100%;
    height: auto;
  }

  &__title {
    font-size: $h3-font-size;
    color: $headings-color;
  }

  &--featured {
    border: 2px solid $primary;
    box-shadow: $box-shadow-lg;
  }
}
```

**Schema Best Practices:**

```yaml
props:
  type: object
  required:
    - title  # Only require what's necessary
  properties:
    title:
      type: string
      title: Title
    description:
      type: string
      title: Description
      default: ''  # Optional, has default
    size:
      type: string
      enum: ['sm', 'md', 'lg']  # Use enums for fixed options
      default: 'md'
    show_icon:
      type: boolean
      default: false  # Explicit default for everything optional
```

## Common Mistakes

- **Wrong**: Creating SDC for simple flex container → **Right**: Use Bootstrap classes (`.d-flex .gap-2`)
- **Wrong**: Monolithic hero with 30+ props → **Right**: Split into focused components (hero-simple, hero-video, hero-carousel)
- **Wrong**: Using props for HTML content → **Right**: Use slots for markup
- **Wrong**: Not checking slot existence → **Right**: `{% if slots.header %}` before rendering
- **Wrong**: Hardcoded classes in Twig → **Right**: Merge with attributes object (`{{ attributes.addClass(classes) }}`)
- **Wrong**: Duplicating Radix components → **Right**: Check `radix/components/` before creating
- **Wrong**: Generic class names (`.title`) → **Right**: Namespace with BEM (`.hero-section__title`)
- **Wrong**: Hardcoding values in SCSS → **Right**: Use Bootstrap variables (`$primary`, `$spacer`)
- **Wrong**: Global styles in component SCSS → **Right**: Keep scoped to component
- **Wrong**: Over-requiring props → **Right**: Only require what's actually required

## See Also

- [Atoms SDC Components](atoms-sdc-components.md)
- [Molecules SDC Components](molecules-sdc-components.md)
- [SDC Component Development](sdc-component-development.md)
- [Radix Component Reuse Strategy](radix-component-reuse-strategy.md)
