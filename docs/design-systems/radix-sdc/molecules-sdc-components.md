---
description: You've identified molecules using the Design System Recognition Guide
drupal_version: "11.x"
---

## 4. Molecules → SDC Components

### When to Use This Section
- You've identified molecules using the Design System Recognition Guide
- You need to compose multiple atoms into a reusable molecule
- You're implementing composite patterns like search bars, card content, form fields

### 4.1 Composing Atom SDCs

#### Pattern: Including Atom SDCs in Molecule

**Molecule: Search Bar** (input + button)

**File: `components/search-bar/search-bar.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Search Bar
status: stable
description: Search input with submit button
props:
  type: object
  properties:
    placeholder:
      type: string
      title: Placeholder
      default: 'Search...'
    button_text:
      type: string
      title: Button Text
      default: 'Search'
```

**File: `components/search-bar/search-bar.twig`**
```twig
<div class="search-bar input-group">
  {# Include Radix input component #}
  {% include 'radix:input' with {
    input_type: 'search',
    input_attributes: create_attribute().setAttribute('placeholder', placeholder),
  } %}

  {# Include Radix button component #}
  {% include 'radix:button' with {
    color: 'primary',
    content: button_text,
  } %}
</div>
```

**File: `components/search-bar/search-bar.scss`**
```scss
@import '../../src/scss/init';

.search-bar {
  // Bootstrap's .input-group handles most styling
  // Add molecule-specific customizations here

  max-width: 400px;

  @include media-breakpoint-up(md) {
    max-width: 600px;
  }
}
```

#### Decision Table: Component Inclusion Methods

| Method | Syntax | Use When |
|--------|--------|----------|
| **Include (Radix)** | `{% include 'radix:button' %}` | Using Radix base theme component |
| **Include (Sub-theme)** | `{% include 'THEME_NAME:button' %}` | Using sub-theme component |
| **Embed** | `{% embed 'radix:button' %}` | Need to override component blocks |
| **Direct HTML** | `<button class="btn">` | Simple, non-reusable elements |

#### Common Mistakes
- **Not using component namespace** — Use `radix:` or `THEME_NAME:` prefix
- **Duplicating component logic** — Include existing atoms instead
- **Over-composing** — Not every atom pairing needs a molecule
- **Forgetting to pass props** — Use `with {}` to pass properties

#### See Also
- [3.2 SDC Component Structure](#32-sdc-component-structure)
- [4.2 Slots and Composition](#42-slots-and-composition)

---

### 4.2 Slots and Composition

#### Pattern: Using Slots for Flexible Composition

**Molecule: Card Content** (image + title + text + button)

**File: `components/card-content/card-content.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
name: Card Content
status: stable
description: Card content molecule with flexible slots
props:
  type: object
  properties:
    title:
      type: string
      title: Card Title
    title_tag:
      type: string
      title: Title Tag
      default: 'h3'
      enum: ['h2', 'h3', 'h4', 'h5']
slots:
  image:
    title: Card Image
    description: Slot for card image
  body:
    title: Card Body
    description: Main card content
  footer:
    title: Card Footer
    description: Footer content (buttons, links)
```

**File: `components/card-content/card-content.twig`**
```twig
<div class="card-content">
  {% if slots.image %}
    <div class="card-content__image">
      {% block image %}
        {{ slots.image }}
      {% endblock %}
    </div>
  {% endif %}

  <div class="card-content__body">
    {% if title %}
      <{{ title_tag }} class="card-content__title">{{ title }}</{{ title_tag }}>
    {% endif %}

    {% block body %}
      {{ slots.body }}
    {% endblock %}
  </div>

  {% if slots.footer %}
    <div class="card-content__footer">
      {% block footer %}
        {{ slots.footer }}
      {% endblock %}
    </div>
  {% endif %}
</div>
```

**Usage:**
```twig
{% include 'THEME_NAME:card-content' with {
  title: 'Product Name',
  title_tag: 'h3',
  slots: {
    image: '<img src="/path/to/image.jpg" alt="Product">',
    body: '<p>Product description</p>',
    footer: render_button_component,
  }
} %}
```

#### Decision Table: Props vs Slots

| Use Props When | Use Slots When |
|----------------|----------------|
| Simple values (strings, booleans) | Complex markup/content |
| Component configuration | Nested components |
| Variant selection | User-generated content |
| Atomic data | Variable content structure |

#### Common Mistakes
- **Overusing props for markup** — Use slots for HTML content
- **Not checking slot existence** — Use `{% if slots.SLOT_NAME %}` before rendering
- **Confusing props and slots** — Props = configuration, Slots = content
- **Not documenting slots** — Define all slots in component.yml

#### See Also
- [7.2 Props and Slots](#72-props-and-slots)
- Official SDC Documentation: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components

---

### 4.3 Molecule vs Drupal Integration

#### Decision Table: Molecule SDC vs Drupal System

| Pattern | Create Molecule SDC | Use Drupal System |
|---------|---------------------|-------------------|
| Input + Label + Error | Maybe | **Prefer**: Field template/formatter |
| Search input + Button | **Yes** | Could use Views exposed form |
| User avatar + Name + Role | **Yes** | Could use User entity display |
| Image + Caption | Maybe | **Prefer**: Media entity with formatter |
| Breadcrumb links | Maybe | **Prefer**: Drupal breadcrumb system |
| Pagination controls | Maybe | **Prefer**: Views pager |

#### Pattern: Integration Decision Framework

```
1. Does Drupal have a built-in system for this?
   YES → Use Drupal system (field formatter, Views, entity display)
   NO → Continue to step 2

2. Is this molecule tied to a specific content type?
   YES → Consider field formatter or entity display mode
   NO → Continue to step 3

3. Is this molecule reused across multiple contexts?
   YES → Create SDC molecule
   NO → Consider template-specific implementation

4. Does this need dynamic data from Drupal?
   YES → Create SDC, populate via field formatter or preprocess
   NO → SDC with static props is fine
```

#### Common Mistakes
- **Creating SDC for everything** — Leverage Drupal's field/entity systems
- **Duplicating Drupal functionality** — Check for existing formatters/displays first
- **Not integrating with Drupal** — SDCs should work WITH Drupal, not replace it
- **Over-abstracting** — Simple molecules may not need SDCs

#### See Also
- [5.3 Layout Builder Integration](#53-layout-builder-integration)
- [6.1 Page Template Structure](#61-page-template-structure)