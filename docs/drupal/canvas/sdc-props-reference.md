---
description: Reference for all SDC prop types in Canvas — YAML syntax, Canvas editor widgets, value structures, and gotchas per type.
tldr: "Use this when defining props in a `*.component.yml` file and you need the exact YAML syntax for each prop type, what Canvas editor widget each produces, and Canvas-specific annotations (`$ref`, `contentMediaType`, `x-formatting-context`)."
drupal_version: "11.x"
---

# SDC Props Reference

## When to Use

> Use this when defining props in a `*.component.yml` file and you need the exact YAML syntax for each prop type, what Canvas editor widget each produces, and Canvas-specific annotations (`$ref`, `contentMediaType`, `x-formatting-context`).

## Decision

| Prop type | YAML key additions | Canvas widget |
|---|---|---|
| Plain string | `type: string` | Single-line text input |
| Rich text (block) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: block` | CKEditor 5 block editor |
| Rich text (inline) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: inline` | CKEditor 5 inline editor |
| Image | `type: object` + `$ref: 'json-schema-definitions://canvas.module/image'` | Media Library picker |
| Link | `type: object` + `$ref: 'json-schema-definitions://canvas.module/link'` | URL + link text input |
| Enum/select | `type: string` + `enum: [...]` + `default: value` | Select dropdown |
| Boolean | `type: boolean` + `default: false` | Toggle/checkbox |
| Integer | `type: integer` + `minimum`/`maximum` | Numeric input |
| Number (float) | `type: number` | Numeric input |
| Multi-value | `type: array` + `items: {type: object, properties: {...}}` | Repeater |

## Pattern

#### Plain String Prop

```yaml
props:
  type: object
  properties:
    headline:
      type: string
      title: Headline
      description: 'Short display text for the headline.'
      examples:
        - 'Transform Your Business'
```

Canvas widget: Single-line text input. No maximum length enforced by default; add JSON Schema `maxLength` if needed.

---

#### Rich Text Prop (Block)

```yaml
body:
  type: string
  title: Body
  contentMediaType: text/html
  x-formatting-context: block
```

Canvas widget: CKEditor 5 block editor (limited toolbar by default). Install `canvas_full_html` contrib module for full HTML format support.

- Default Canvas text format (`canvas_html_block`) has a restricted toolbar
- The `canvas_full_html` module overrides this via `hook_canvas_storable_prop_shape_alter()` to use Drupal's `full_html` format
- Block context allows block-level elements; inline context only allows inline elements

---

#### Rich Text Prop (Inline)

```yaml
caption:
  type: string
  title: Caption
  contentMediaType: text/html
  x-formatting-context: inline
```

Canvas widget: CKEditor 5 inline editor (reduced toolbar). Does not support block-level elements.

---

#### Image Prop

```yaml
image:
  type: object
  title: Image
  description: 'Component image from the media library.'
  $ref: 'json-schema-definitions://canvas.module/image'
```

Canvas widget: Media Library picker.

Value structure passed to Twig:
```
image.url         — rendered image URL
image.alt         — alt text from media entity
image.width       — pixel width
image.height      — pixel height
image.srcset      — responsive srcset string (if image styles configured)
```

Do NOT use `<img src="{{ image }}">` — the prop is an object, not a URL. Always use the `canvas:image` component (see [SDC Image Handling](sdc-image-handling.md)).

---

#### Link Prop

```yaml
cta_url:
  type: object
  title: 'Call to Action URL'
  $ref: 'json-schema-definitions://canvas.module/link'
```

Canvas widget: URL input + link text input.

Value structure:
```
cta_url.url    — the URL string
cta_url.title  — the link text (if provided)
```

Check for `cta_url` being empty before using `cta_url.url` in Twig.

---

#### Enum / Select Prop

```yaml
color_scheme:
  type: string
  title: 'Color Scheme'
  enum:
    - light
    - dark
    - brand
  default: light
```

Canvas widget: Select dropdown showing enum values. Values shown are raw enum strings.

---

#### Boolean Prop

```yaml
show_divider:
  type: boolean
  title: 'Show Divider'
  default: false
```

Canvas widget: Toggle/checkbox. In Twig, check with `{% if show_divider %}` — no casting needed.

---

#### Integer/Number Prop

```yaml
columns:
  type: integer
  title: Columns
  minimum: 1
  maximum: 6
  default: 3
```

Canvas widget: Numeric input (with min/max constraints if specified). Use `integer` for whole numbers; `number` for floats.

---

#### Multi-value Props

```yaml
items:
  type: array
  title: Items
  items:
    type: object
    properties:
      title:
        type: string
        title: Title
      body:
        type: string
        title: Body
        contentMediaType: text/html
        x-formatting-context: block
```

Canvas widget: Repeater — editors can add/remove/reorder items. Multi-value prop UI support is still maturing (tracked in Canvas issue #3571917). In Twig, iterate with `{% for item in items %}`.

## Common Mistakes

- **Wrong**: Not providing `title` on props → **Right**: Canvas uses `title` as the editor label; without it, editors see raw machine names
- **Wrong**: Not providing `description` → **Right**: Editors have no context for what the prop is for
- **Wrong**: Using `$ref` for props that don't need Media Library or link widgets → **Right**: It adds overhead and changes the editor widget
- **Wrong**: Forgetting `type: object` wrapping when using `$ref` → **Right**: `$ref` props must declare `type: object`
- **Wrong**: Defining props that don't appear in the Twig template → **Right**: Wasted editor effort and storage

## See Also

- [SDC Component Format](sdc-component-format.md) for full component YAML structure
- [SDC Slots](sdc-slots.md) for nested component areas
- [SDC Image Handling](sdc-image-handling.md) for image prop rendering
- Canvas SDC Props docs: https://project.pages.drupalcode.org/canvas/sdc-components/props/
