---
description: Molecule SDC components — composing atoms, slots and composition, molecule vs Drupal integration
drupal_version: "11.x"
---

# Molecules SDC Components

## When to Use

> Use this when composing multiple atoms into a reusable molecule, implementing composite patterns like search bars or card content.

## Decision

| Method | Syntax | Use When |
|--------|--------|----------|
| **Include (Radix)** | `{% include 'radix:button' %}` | Using Radix base theme component |
| **Include (Sub-theme)** | `{% include 'THEME_NAME:button' %}` | Using sub-theme component |
| **Embed** | `{% embed 'radix:button' %}` | Need to override component blocks |
| **Direct HTML** | `<button class="btn">` | Simple, non-reusable elements |

**Molecule vs Drupal System:**

| Pattern | Create Molecule SDC | Use Drupal System |
|---------|---------------------|-------------------|
| Input + Label + Error | Maybe | **Prefer**: Field template/formatter |
| Search input + Button | **Yes** | Could use Views exposed form |
| User avatar + Name + Role | **Yes** | Could use User entity display |
| Image + Caption | Maybe | **Prefer**: Media entity with formatter |
| Breadcrumb links | Maybe | **Prefer**: Drupal breadcrumb system |
| Pagination controls | Maybe | **Prefer**: Views pager |

**Integration Decision Framework:**

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

## Pattern

**Composing Atoms (Search Bar):**

**File: `components/search-bar/search-bar.component.yml`**

```yaml
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
  max-width: 400px;

  @include media-breakpoint-up(md) {
    max-width: 600px;
  }
}
```

**Slots and Composition (Card Content):**

**File: `components/card-content/card-content.component.yml`**

```yaml
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

## Common Mistakes

- **Wrong**: Not using component namespace → **Right**: Use `radix:` or `THEME_NAME:` prefix
- **Wrong**: Duplicating component logic → **Right**: Include existing atoms instead
- **Wrong**: Over-composing (creating molecule for every atom pairing) → **Right**: Only when reused
- **Wrong**: Forgetting to pass props → **Right**: Use `with {}` to pass properties
- **Wrong**: Using props for markup → **Right**: Use slots for HTML content
- **Wrong**: Not checking slot existence → **Right**: Use `{% if slots.SLOT_NAME %}`
- **Wrong**: Creating SDC for everything → **Right**: Leverage Drupal's field/entity systems
- **Wrong**: Duplicating Drupal functionality → **Right**: Check for existing formatters/displays first

## See Also

- [Atoms SDC Components](atoms-sdc-components.md)
- [SDC Component Best Practices](sdc-component-best-practices.md)
- [SDC Component Development](sdc-component-development.md)
- Official SDC Documentation: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
