---
description: Common SDC anti-patterns with explanations from code review perspective
drupal_version: "11.x"
---

# Anti-Patterns

## When to Use

> Use this when code reviewing component implementations, debugging component issues, or establishing component development standards.

## Decision

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Over-componentizing | Each component has discovery/loading overhead | Create components at meaningful abstraction level |
| Logic in Twig | Business logic belongs in preprocessing | Templates should be presentation-only |
| Missing schema definitions | No validation, no IDE support | Always define complete props/slots schemas |
| Slots for simple data | Slots bypass validation | Use props for typed configuration data |
| Hardcoded child components | Reduces flexibility | Use slots for variable content areas |
| Not using `with_context = false` | Creates hidden dependencies | Isolate component context |
| Complex conditionals on slots | Slots contain arbitrary renderables | Only check `if slot` for existence |
| Using `@extend` in SCSS | Bloats compiled CSS | Use mixins or utility classes |
| Not checking slot existence | Creates empty wrapper elements | Wrap optional slots in conditionals |
| Global CSS selectors | Collides with other components | Use BEM with component-specific namespace |
| Module component overrides | Only themes can use `replaces` | Override in theme, not module |
| Changing schema in `replaces` | Breaks API contract | Replacement must have identical schema |

## Pattern

**Anti-Pattern 1: Over-Componentizing**
```
❌ WRONG: Atomic-level components
components/
├── heading/
├── paragraph/
├── link/
└── image/

✓ RIGHT: Meaningful abstraction
components/
└── article-card/  ← Combines elements
```

**Anti-Pattern 3: Missing Schema**
```yaml
❌ WRONG: No schema
name: 'Button'
status: stable

✓ RIGHT: Complete schema
name: 'Button'
status: stable
props:
  type: object
  properties:
    text:
      type: string
      title: 'Button Text'
```

**Anti-Pattern 6: Variable Leakage**
```twig
❌ WRONG: Leaking context
{{ include('my_theme:button', { text: 'Click' }) }}

✓ RIGHT: Isolated context
{{ include('my_theme:button', { text: 'Click' }, with_context = false) }}
```

**Anti-Pattern 9: Empty Wrappers**
```twig
❌ WRONG: Unconditional wrapper
<header class="component__header">
  {{ header }}
</header>

✓ RIGHT: Conditional wrapper
{% if header %}
  <header class="component__header">
    {{ header }}
  </header>
{% endif %}
```

## See Also

- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Security](security.md)
- [Component Composition](component-composition.md)
