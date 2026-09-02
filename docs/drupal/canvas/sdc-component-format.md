---
description: "Full file structure, YAML schema, and Twig template patterns for authoring SDC components compatible with Canvas."
tldr: "Use this when creating a Canvas-compatible component using Drupal's Single Directory Component (SDC) system. This produces a server-side-rendered Twig component with Drupal field widget integration in the Canvas editor."
drupal_version: "11.x"
---

# SDC Component Format

## When to Use

> You are creating a Canvas-compatible component using Drupal's Single Directory Component (SDC) system. This produces a server-side-rendered Twig component with Drupal field widget integration in the Canvas editor — content editors get proper input widgets (text fields, image pickers, link pickers, rich text editors) rather than raw JSON inputs.

## File Structure

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

The directory can live in any Drupal module or theme under a `components/` folder.

**Important**: Canvas automatically *discovers* all SDC components from all enabled modules and themes — there is no registration step. **Discovery is not eligibility.** Every discovered component is then run through a requirements check, and any component that fails is silently excluded: it never appears in the Canvas component panel, and nothing is logged to the page. One class of mistake is the exception to that rule and is not silent at all — a `$ref` naming a definition that does not exist throws out of SDC discovery and takes the whole site down. See [Component Eligibility](sdc-props-reference.md) for the gate list, for both failure modes, and for where Canvas records the reason.

## YAML Schema

The `*.component.yml` file defines the component for both Drupal's SDC system and Canvas's editor:

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
      examples:
        - 'Get started'
    cta_url:
      # A link prop is a plain STRING with a `format` — NOT an object with a $ref.
      # `uri-reference` accepts internal (/node/1) and external URLs;
      # `uri` accepts absolute URLs only.
      type: string
      format: uri-reference
      title: 'Button URL'
      examples:
        - '/contact'
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

**Key prop types:**

| Prop type | YAML definition | Canvas editor widget |
|---|---|---|
| Plain text | `type: string` | Single-line text input |
| Rich text (block) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: block` | CKEditor block editor |
| Rich text (inline) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: inline` | CKEditor inline editor |
| Image | `type: object` + `$ref: 'json-schema-definitions://canvas.module/image'` | Media Library / image picker |
| Video | `type: object` + `$ref: 'json-schema-definitions://canvas.module/video'` | File upload (mp4) |
| Entity reference | `type: object` + `$ref: 'json-schema-definitions://canvas.module/content-entity-reference'` + `x-allowed-entity-type-id` | Entity autocomplete |
| Link (any URL) | `type: string` + `format: uri-reference` | Link field, URL only — no link-text input |
| Link (external only) | `type: string` + `format: uri` | Link field, URL only — no link-text input |
| Number | `type: integer` or `type: number` | Numeric input |
| Boolean | `type: boolean` | Toggle |
| Enum/select | `type: string` + `enum: [value1, value2]` (+ `meta:enum` for labels) | Select dropdown |

**About `$ref`:** the three URIs in the table above are a closed enum of the only `type: object` refs Canvas knows how to store. They are *not* the only `$ref`s that exist. Canvas's `schema.json` ships **fourteen** `$defs`, and the string- and integer-typed ones resolve through the ordinary scalar path and produce real storable shapes — `.../heading-element` (string enum), `.../column-width` (integer enum), `.../image-uri`, `.../stream-wrapper-uri` and `.../stream-wrapper-image-uri` all work. So does a `$ref` into another extension's own `schema.json`, addressed as `json-schema-definitions://{extension}.{module|theme}/{definition}`.

What does not exist is `json-schema-definitions://canvas.module/link`. Writing a `$ref` to a definition that is not in the target extension's `schema.json` is **fatal, not silent** — see [Component Eligibility](sdc-props-reference.md).

## Twig Template

Canvas-compatible Twig templates follow standard SDC conventions:

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
      <a href="{{ cta_url }}" class="btn btn-primary">
        {{ cta_text }}
      </a>
    {% endif %}
  </div>

  {# canvas:image reads `src` at top level — SPREAD the image object into the
     include context with |merge. Passing `{image: image}` throws a TypeError. #}
  {% if image %}
    {% include 'canvas:image' with image|merge({
      loading: 'eager',
      class: 'hero__image',
    }|filter((value) => value is not null)) only %}
  {% endif %}
</section>
```

**Link prop structure**: a link prop is a **plain string** — the URL. Render it directly with `{{ cta_url }}`. There is no `.url` and no `.title`: Canvas maps URI-format string props onto Drupal's `link` field with the instance setting `title: 0`, which switches the link widget's text field off. If you want editor-supplied link text, declare a **second** `type: string` prop for it (the `cta_text` above).

**Image rendering**: Use the `canvas:image` built-in SDC component for images (see [SDC Image Handling](sdc-image-handling.md)).

**Slot rendering**: Slots arrive as renderable Twig variables — render directly with `{{ slot_name }}`. No `{% block %}` needed.

## Common Mistakes

- Using `.html.twig` extension instead of `.twig` — Canvas (and SDC) only recognize `.twig`
- Writing `$ref: 'json-schema-definitions://canvas.module/link'` — that definition has never existed, and a `$ref` to a missing definition is **fatal**: the next cache rebuild throws out of SDC plugin discovery and the site returns 500. It does not quietly disable one component
- Referencing image props directly with `<img src="{{ image }}">` — image props are objects, not URLs; use `canvas:image`
- Passing an image prop as `{% include 'canvas:image' with {image: image} %}` — `canvas:image` takes `src`, not `image`; spread with `image|merge({...})`
- Assuming `$ref` is limited to image, video and content-entity-reference — those three are only the storable `type: object` refs. String- and integer-typed refs such as `heading-element`, `column-width` and `stream-wrapper-uri` resolve too
- Forgetting `x-formatting-context` on rich text props — without it, Canvas may not show the CKEditor widget
- Putting components in `templates/` instead of `components/` — SDC components must be in `components/`
- Using `{% embed %}` with `{% block %}` for Canvas:image — always use `{% include ... only %}`
- Relying on YAML `default:` — Canvas strips it. The stored default comes from `examples[0]`

## See Also

- [SDC Props Reference](sdc-props-reference.md) for all prop types in detail
- [SDC Slots](sdc-slots.md) for slot behavior
- [SDC Image Handling](sdc-image-handling.md) for image patterns
- Official SDC docs: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
- Canvas SDC docs: https://project.pages.drupalcode.org/canvas/sdc-components/
