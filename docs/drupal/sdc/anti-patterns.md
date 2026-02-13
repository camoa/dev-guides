---
description: Common component development anti-patterns with WHY explanations from code review perspective
drupal_version: "11.x"
---

# Anti-Patterns

## When to Use

> Use this when code reviewing component implementations, debugging component issues, or establishing component development standards.

## Common Mistakes

**Over-Componentizing**
- **Wrong**: Creating components for heading, paragraph, link, image, text-with-heading (combines previous 4) → **Right**: Each component has discovery/loading overhead. Group elements that always appear together into single component at meaningful abstraction level.

**Logic in Twig Templates**
- **Wrong**: Complex business logic in template (checking user roles, computing values) → **Right**: Business logic belongs in preprocessing/controllers. Templates should be presentation-only.

**Missing Schema Definitions**
- **Wrong**: No props or slots defined in component YAML → **Right**: No validation, no IDE support, no documentation of component API. Integration modules require schemas.

**Using Slots for Simple Typed Data**
- **Wrong**: Using slot for boolean/enum values → **Right**: Slots bypass validation. Simple typed values should be validated props for type safety and better errors.

**Hardcoding Child Components**
- **Wrong**: Hardcoded child components in template → **Right**: Reduces flexibility. Use slot for content area. Let calling code decide what to include.

**Not Using `with_context = false`**
- **Wrong**: `{{ include('my_theme:button', { text: 'Click' }) }}` → **Right**: Component inherits all parent template variables. Creates hidden dependencies and unpredictable behavior. Use `with_context = false` to isolate context.

**Complex Conditionals on Slots**
- **Wrong**: `{% if content and content.field_name and content.field_name|render|striptags|trim %}` → **Right**: Slots contain arbitrary renderables. Can't reliably access their properties. Only check `if slot` for existence.

**Using `@extend` in SCSS**
- **Wrong**: `@extend .btn;` in Sass → **Right**: Creates unexpected selector chains, bloats compiled CSS, makes debugging difficult. Use mixins or utility classes instead.

**Not Checking Slot Existence**
- **Wrong**: Rendering wrapper element without checking if slot has content → **Right**: Creates empty wrapper elements when slot not provided. Invalid HTML and accessibility issues. Always wrap optional slots in `{% if slot %}` conditional.

**Global CSS Selectors**
- **Wrong**: Generic selectors like `.button`, `.card`, `.title` → **Right**: Collides with other components and global styles. Use BEM with component-specific namespace: `.my-component__element`.

**Trying to Override Components from Modules**
- **Wrong**: Using `replaces` directive in module component → **Right**: Only themes can use `replaces` directive. Module overrides not supported.

**Changing Schema in `replaces` Component**
- **Wrong**: Replacement with different props/slots than original → **Right**: Breaks API contract. Calling code expects original schema. Replacement must have identical schemas.

## See Also

- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Security](security.md)
- [Component Composition](component-composition.md)
