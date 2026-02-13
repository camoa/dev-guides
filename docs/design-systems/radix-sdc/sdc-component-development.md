---
description: You're creating new SDC components from scratch
drupal_version: "11.x"
---

## 7. SDC Component Development

### When to Use This Section
- You're creating new SDC components from scratch
- You need to define component props, slots, and schemas
- You're adding JavaScript to components

### 7.1 Component YAML Schema

#### Pattern: Complete Component Schema

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
      enum:
        - option1
        - option2
        - option3
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
    drupal_attribute:
      type: Drupal\Core\Template\Attribute
      title: Drupal Attributes
slots:
  slot_name:
    title: Slot Title
    description: Slot description
```

#### Decision Table: Prop Types

| Data Type | YAML Type | Example Use |
|-----------|-----------|-------------|
| String | `type: string` | Text, IDs, URLs |
| Boolean | `type: boolean` | Flags (disabled, active) |
| Number | `type: number` | Counts, measurements |
| Array | `type: array` | Lists, utility classes |
| Enum | `enum: [...]` | Fixed options (size, color) |
| Drupal Attribute | `type: Drupal\Core\Template\Attribute` | HTML attributes |

#### Common Mistakes
- **Missing $schema reference** — Enables validation
- **Not setting defaults** — Props without defaults require values
- **Wrong type definitions** — Follow JSON Schema spec
- **Not documenting props** — Use `title` and `description`

#### See Also
- [7.2 Props and Slots](#72-props-and-slots)
- Official SDC Schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json

---

### 7.2 Props and Slots

#### Pattern: Props vs Slots Usage

**Props:**
```yaml
props:
  type: object
  properties:
    title:
      type: string
      title: Title
    color:
      type: string
      enum: ['primary', 'secondary']
```

**Twig:**
```twig
<h2>{{ title }}</h2>
<div class="alert alert-{{ color }}">...</div>
```

**Slots:**
```yaml
slots:
  header:
    title: Header
  body:
    title: Body
  footer:
    title: Footer
```

**Twig:**
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

#### Decision Table: When to Use

| Feature | Props | Slots |
|---------|-------|-------|
| Simple values | ✅ Use props | ❌ |
| HTML content | ❌ | ✅ Use slots |
| Component composition | ❌ | ✅ Use slots |
| Configuration | ✅ Use props | ❌ |
| Nested components | ❌ | ✅ Use slots |

#### Common Mistakes
- **Using props for HTML** — Use slots instead
- **Not checking slot existence** — Always use `{% if slots.SLOT %}`
- **Confusing prop and slot syntax** — Props = `{{ prop }}`, Slots = `{{ slots.slot }}`
- **Missing required props** — Define in `required: []` array

#### See Also
- [4.2 Slots and Composition](#42-slots-and-composition)

---

### 7.3 SCSS Scoping

#### Pattern: Component SCSS Scoping

**Best Practice: BEM Methodology**

```scss
@import '../../src/scss/init';

// Component block
.my-component {
  // Use Bootstrap variables
  padding: $spacer;
  background: $white;
  border: 1px solid $border-color;

  // Element
  &__header {
    font-weight: $font-weight-bold;
    margin-bottom: $spacer * 0.5;
  }

  &__body {
    color: $body-color;
  }

  // Modifier
  &--highlighted {
    background: tint-color($primary, 90%);
    border-color: $primary;
  }

  // Responsive
  @include media-breakpoint-up(md) {
    padding: $spacer * 2;
  }
}
```

#### Decision Table: Scoping Strategy

| Scope | Pattern | Example |
|-------|---------|---------|
| **Component** | `.component-name` | `.card-content` |
| **Element** | `.component__element` | `.card-content__title` |
| **Modifier** | `.component--modifier` | `.card-content--featured` |
| **State** | `.component.is-state` | `.card-content.is-active` |

#### Common Mistakes
- **Not using BEM** — Leads to specificity issues
- **Global class names** — Scope to component
- **Hardcoding values** — Use Bootstrap variables
- **Not importing _init.scss** — Missing Bootstrap foundation

#### See Also
- [3.4 SCSS Integration in SDCs](#34-scss-integration-in-sdcs)

---

### 7.4 JavaScript in SDCs

#### Pattern: Component JavaScript

**File: `components/COMPONENT/COMPONENT.js`**
```javascript
/**
 * @file
 * JavaScript for COMPONENT component.
 */

((Drupal) => {
  'use strict';

  /**
   * Attaches COMPONENT behavior.
   *
   * @type {Drupal~behavior}
   */
  Drupal.behaviors.myComponent = {
    attach(context) {
      // Use once() to ensure initialization happens only once
      const components = once('my-component', '.my-component', context);

      components.forEach((component) => {
        // Component initialization logic
        const button = component.querySelector('.my-component__button');

        if (button) {
          button.addEventListener('click', () => {
            component.classList.toggle('my-component--active');
          });
        }
      });
    },
  };
})(Drupal);
```

**Auto-Loading:** If `COMPONENT.js` exists, Drupal automatically attaches it as an asset library.

#### Common Mistakes
- **Not using Drupal.behaviors** — Required for Drupal integration
- **Not using once()** — Prevents duplicate initialization
- **Not scoping to context** — Breaks AJAX compatibility
- **Missing 'use strict'** — Best practice for modern JS

#### See Also
- Drupal JavaScript API: https://www.drupal.org/docs/drupal-apis/javascript-api