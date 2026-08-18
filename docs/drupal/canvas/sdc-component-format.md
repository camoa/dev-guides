---
description: "Full file structure, YAML schema, and Twig template patterns for authoring SDC components compatible with Canvas."
tldr: "Use this when creating a Canvas-compatible component using Drupal's Single Directory Component (SDC) system. This produces a server-side-rendered Twig component with Drupal field widget integration in the Canvas editor."
drupal_version: "11.x"
---

# SDC Component Format

## When to Use

> Use this when creating a Canvas-compatible component using Drupal's Single Directory Component (SDC) system. This produces a server-side-rendered Twig component with Drupal field widget integration in the Canvas editor.

**Discovery is not eligibility.** Canvas automatically discovers every SDC from every enabled module/theme — there is no registration step. Each discovered component is then run through a requirements check, and any component that fails is silently excluded: it never appears in the Canvas panel, and nothing is logged to the page. See [SDC Props Reference](sdc-props-reference.md) for the full gate list.

## Decision

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

**Only three `$ref` URIs exist**, and they are a closed enum: `.../image`, `.../video`, `.../content-entity-reference`. There is no `json-schema-definitions://canvas.module/link` — writing one makes Canvas reject the whole component.

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

**Twig template:**

```twig
{# hero.twig #}
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

**Link prop structure**: a link prop is a **plain string** — the URL. Render it directly with `{{ cta_url }}`. There is no `.url` and no `.title`: Canvas maps URI-format string props onto Drupal's `link` field with the instance setting `title: 0`, which switches the link widget's text field off. If you want editor-supplied link text, declare a **second** `type: string` prop for it (`cta_text` above).

**Slot rendering**: Slots arrive as renderable Twig variables — render directly with `{{ slot_name }}`. No `{% block %}` needed.

## Common Mistakes

- **Wrong**: Using `.html.twig` extension → **Right**: Canvas (and SDC) only recognize `.twig`
- **Wrong**: Writing `$ref: 'json-schema-definitions://canvas.module/link'` → **Right**: that definition has never existed; Canvas fails closed and disables the whole component. Use `type: string` + `format: uri-reference`/`uri`
- **Wrong**: `<img src="{{ image }}">` — image props are objects, not URLs → **Right**: Use `canvas:image`
- **Wrong**: `{% include 'canvas:image' with {image: image} %}` — `canvas:image` takes `src`, not `image` → **Right**: Spread with `image|merge({...})`
- **Wrong**: Adding `$ref` for anything other than image, video, or content-entity-reference → **Right**: those are the only three that resolve
- **Wrong**: Forgetting `x-formatting-context` on rich text props → **Right**: without it, Canvas may not show the CKEditor widget
- **Wrong**: Putting components in `templates/` → **Right**: SDC components must be in `components/`
- **Wrong**: Using `{% embed %}` with `{% block %}` for canvas:image → **Right**: always use `{% include ... only %}`
- **Wrong**: Relying on YAML `default:` → **Right**: Canvas strips it. The stored default comes from `examples[0]`

## See Also

- [SDC Props Reference](sdc-props-reference.md) for all prop types in detail
- [SDC Slots](sdc-slots.md) for slot behavior
- [SDC Image Handling](sdc-image-handling.md) for image patterns
- Official SDC docs: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
- Canvas SDC docs: https://project.pages.drupalcode.org/canvas/sdc-components/
