---
description: Full file structure, YAML schema, and Twig template patterns for authoring SDC components compatible with Canvas.
drupal_version: "11.x"
---

# SDC Component Format

## When to Use

> Use this when creating a Canvas-compatible component using Drupal's Single Directory Component (SDC) system. This produces a server-side-rendered Twig component with Drupal field widget integration in the Canvas editor.

## Decision

| Prop type | YAML definition | Canvas editor widget |
|---|---|---|
| Plain text | `type: string` | Single-line text input |
| Rich text (block) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: block` | CKEditor block editor |
| Rich text (inline) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: inline` | CKEditor inline editor |
| Image | `type: object` + `$ref: 'json-schema-definitions://canvas.module/image'` | Media Library picker |
| Link | `type: object` + `$ref: 'json-schema-definitions://canvas.module/link'` | URL + link text input |
| Number | `type: integer` or `type: number` | Numeric input |
| Boolean | `type: boolean` | Toggle |
| Enum/select | `type: string` + `enum: [value1, value2]` | Select dropdown |

## Pattern

An SDC component for Canvas follows standard Drupal SDC conventions, organized in a single directory:

```
my_theme/
  components/
    hero/
      hero.component.yml    ← required: metadata, props, slots
      hero.twig             ← required: Twig template (NOT .html.twig)
      hero.css              ← optional: component styles
      hero.js               ← optional: component JS behaviors
```

Canvas automatically discovers ALL SDC components from all enabled modules and themes. There is no registration step.

**`*.component.yml` schema:**

```yaml
# hero.component.yml
$schema: 'https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json'
name: Hero
status: stable
group: Marketing               # Groups components in Canvas panel
description: 'Full-width hero with headline, subtext, CTA, and background image.'

props:
  type: object
  properties:
    headline:
      type: string
      title: Headline
      description: 'Main hero headline text.'
      examples:
        - 'Welcome to our platform'
    image:
      type: object
      title: Background Image
      $ref: 'json-schema-definitions://canvas.module/image'
    cta_text:
      type: string
      title: 'Button Label'
    cta_url:
      type: object
      title: 'Button URL'
      $ref: 'json-schema-definitions://canvas.module/link'
    body:
      type: string
      title: Description
      contentMediaType: text/html
      x-formatting-context: block

slots:
  badge:
    title: Badge
    description: 'Optional badge component above the headline.'
```

**Twig template:**

```twig
{# hero.twig #}
{% set image_attrs = create_attribute() %}

<section class="hero">
  {% if badge is not empty %}
    <div class="hero__badge">{{ badge }}</div>
  {% endif %}

  <div class="hero__content">
    {% if headline %}
      <h1 class="hero__headline">{{ headline }}</h1>
    {% endif %}
    {% if body %}
      <div class="hero__body">{{ body }}</div>
    {% endif %}
    {% if cta_text and cta_url %}
      <a href="{{ cta_url.url }}" class="btn btn-primary">
        {{ cta_text }}
      </a>
    {% endif %}
  </div>

  {% if image %}
    {% include 'canvas:image' with {
      image: image,
      loading: 'eager',
      fetchpriority: 'high',
    } only %}
  {% endif %}
</section>
```

**Link prop structure**: When a `$ref: canvas.module/link` prop is passed to Twig, it has `.url` and `.title` (link text) keys.

**Slot rendering**: Slots arrive as renderable Twig variables — render directly with `{{ slot_name }}`. No `{% block %}` needed.

## Common Mistakes

- **Wrong**: Using `.html.twig` extension → **Right**: Canvas (and SDC) only recognize `.twig`
- **Wrong**: `<img src="{{ image }}">` — image props are objects, not URLs → **Right**: Use `canvas:image` component
- **Wrong**: Adding `$ref` for text strings that don't need the Media Library → **Right**: Use `$ref` only for image and link prop types
- **Wrong**: Forgetting `x-formatting-context` on rich text props → **Right**: Without it, Canvas may not show the CKEditor widget
- **Wrong**: Putting components in `templates/` → **Right**: SDC components must be in `components/`
- **Wrong**: Using `{% embed %}` with `{% block %}` for Canvas:image → **Right**: Always use `{% include ... only %}`

## See Also

- [SDC Props Reference](sdc-props-reference.md) for all prop types in detail
- [SDC Slots](sdc-slots.md) for slot behavior
- [SDC Image Handling](sdc-image-handling.md) for image patterns
- Official SDC docs: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
- Canvas SDC docs: https://project.pages.drupalcode.org/canvas/sdc-components/
