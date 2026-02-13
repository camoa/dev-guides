---
description: SDC component development — YAML schema, props and slots, SCSS scoping, JavaScript in components
drupal_version: "11.x"
---

# SDC Component Development

## When to Use

> Use this when creating new SDC components from scratch, defining component props/slots/schemas, or adding JavaScript to components.

## Decision

**Prop Types:**

| Data Type | YAML Type | Example Use |
|-----------|-----------|-------------|
| String | `type: string` | Text, IDs, URLs |
| Boolean | `type: boolean` | Flags (disabled, active) |
| Number | `type: number` | Counts, measurements |
| Array | `type: array` | Lists, utility classes |
| Enum | `enum: [...]` | Fixed options (size, color) |
| Drupal Attribute | `type: Drupal\Core\Template\Attribute` | HTML attributes |

**Props vs Slots:**

| Feature | Props | Slots |
|---------|-------|-------|
| Simple values | ✅ Use props | ❌ |
| HTML content | ❌ | ✅ Use slots |
| Component composition | ❌ | ✅ Use slots |
| Configuration | ✅ Use props | ❌ |
| Nested components | ❌ | ✅ Use slots |

## Pattern

**Complete Component Schema:**

**File: `components/COMPONENT/COMPONENT.component.yml`**

```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Component Name
status: stable
description: Detailed component description
group: Component Group
props:
  type: object
  required:
    - required_prop
  properties:
    required_prop:
      type: string
      title: Required Property
      description: This prop is required
    optional_prop:
      type: string
      title: Optional Property
      default: 'default value'
    enum_prop:
      type: string
      title: Enumerated Property
      enum: ['option1', 'option2', 'option3']
      default: 'option1'
    boolean_prop:
      type: boolean
      title: Boolean Property
      default: false
    array_prop:
      type: array
      items:
        type: string
      title: Array Property
      default: []
slots:
  slot_name:
    title: Slot Title
    description: Slot description
```

**Props in Twig:**

```twig
<h2>{{ title }}</h2>
<div class="alert alert-{{ color }}">...</div>
```

**Slots in Twig:**

```twig
{% if slots.header %}
  <div class="component__header">
    {{ slots.header }}
  </div>
{% endif %}

<div class="component__body">
  {{ slots.body }}
</div>
```

**SCSS Scoping:**

```scss
// components/my-component/my-component.scss
@import '../../src/scss/init';

.my-component {
  // Component-scoped styles only
  padding: $spacer;
  background: $white;

  &__title {
    color: $primary;
  }

  &--featured {
    border: 2px solid $primary;
  }

  // Don't style global elements
  // h2 { } ← BAD
  // .container { } ← BAD
}
```

**JavaScript in Components:**

**File: `components/my-component/my-component.js`**

```javascript
((Drupal, once) => {
  Drupal.behaviors.myComponent = {
    attach(context) {
      once('my-component', '.my-component', context).forEach((element) => {
        // Component-specific JavaScript
        element.addEventListener('click', () => {
          console.log('Component clicked');
        });
      });
    },
  };
})(Drupal, once);
```

**Auto-loading:** SDC automatically attaches `my-component.js` when component renders.

**Component Library (Optional):**

```yaml
# components/my-component/my-component.component.yml
libraryOverrides:
  dependencies:
    - core/drupal
    - core/once
```

## Common Mistakes

- **Wrong**: Missing `$schema` reference → **Right**: Include for validation
- **Wrong**: Props without defaults → **Right**: Set defaults for all optional props
- **Wrong**: Wrong type definitions → **Right**: Follow JSON Schema spec
- **Wrong**: Not documenting props → **Right**: Use `title` and `description`
- **Wrong**: Using props for HTML → **Right**: Use slots instead
- **Wrong**: Not checking slot existence → **Right**: Always `{% if slots.SLOT %}`
- **Wrong**: Confusing prop and slot syntax → **Right**: Props = `{{ prop }}`, Slots = `{{ slots.slot }}`
- **Wrong**: Global styles in component SCSS → **Right**: Keep scoped to component
- **Wrong**: Not importing `_init.scss` → **Right**: Import for Bootstrap access
- **Wrong**: Plain JavaScript without Drupal.behaviors → **Right**: Use Drupal.behaviors pattern
- **Wrong**: Not using `once()` → **Right**: Prevents duplicate initialization

## See Also

- [Atoms SDC Components](atoms-sdc-components.md)
- [Molecules SDC Components](molecules-sdc-components.md)
- [SDC Component Best Practices](sdc-component-best-practices.md)
- Official SDC Schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
- Official SDC Documentation: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
