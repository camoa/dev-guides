---
description: "Reference for all SDC prop types in Canvas — YAML syntax, Canvas editor widgets, value structures, defaults, and the hard eligibility gates."
tldr: "Use this when writing `*.component.yml` props: exact YAML per type, the Canvas widget each produces, that `default:` is stripped (use `examples[0]`), and the eligibility gates that silently exclude a component from the panel."
drupal_version: "11.x"
---

# SDC Props Reference

## When to Use

> You are defining props in a `*.component.yml` file and need to know the exact YAML syntax for each prop type, what Canvas editor widget each produces, and Canvas-specific annotations (`$ref`, `contentMediaType`, `x-formatting-context`, `meta:enum`). Read [Defaults](#defaults-canvas-ignores-default) and [Component Eligibility](#component-eligibility-hard-gates) at the end of this section before you write any YAML — Canvas ignores `default:`, and a prop that breaks an eligibility rule removes the whole component from the editor with no visible error — with one exception, a `$ref` to a definition that does not exist, which takes the entire site down instead (see [The One Failure That Is Not Silent](#the-one-failure-that-is-not-silent)).

## Decision

| Prop type | YAML key additions | Canvas widget |
|---|---|---|
| Plain string | `type: string` | Single-line text input |
| Rich text (block) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: block` | CKEditor 5 block editor |
| Rich text (inline) | `type: string` + `contentMediaType: text/html` + `x-formatting-context: inline` | CKEditor 5 inline editor |
| Image | `type: object` + `$ref: 'json-schema-definitions://canvas.module/image'` | Media Library picker |
| Link (any URL) | `type: string` + `format: uri-reference` | Link field, URL only |
| Link (external only) | `type: string` + `format: uri` | Link field, URL only |
| Enum/select | `type: string` + `enum: [...]` + `meta:enum:` for labels | Select dropdown |
| Boolean | `type: boolean` | Toggle/checkbox |
| Integer | `type: integer` + `minimum`/`maximum` | Numeric input |
| Number (float) | `type: number` | Numeric input |
| Multi-value | `type: array` + `items:` (scalar or recognized `$ref` only) | Repeater |

**All defaults come from `examples[0]`, never from `default:`.** See [Defaults](#defaults-canvas-ignores-default).

## Pattern

#### Plain String Prop

**Description:** Simple text field. Single-line in Canvas editor.
**YAML:**
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
**Canvas widget:** Single-line text input.
**Gotchas:** No maximum length enforced by default; add JSON Schema `maxLength` if needed.

---

#### Rich Text Prop (Block)

**Description:** Multi-paragraph rich text with CKEditor. For body text, descriptions, long-form content.
**YAML:**
```yaml
body:
  type: string
  title: Body
  contentMediaType: text/html
  x-formatting-context: block
```
**Canvas widget:** CKEditor 5 block editor (limited toolbar by default). Install `canvas_full_html` contrib module for full HTML format support.
**Gotchas:**
- Default Canvas text format (`canvas_html_block`) has a restricted toolbar — limited to basic formatting
- The `canvas_full_html` module (`drupal.org/project/canvas_full_html`) overrides this via `hook_canvas_storable_prop_shape_alter()` to use Drupal's `full_html` format instead
- Block context allows block-level elements (headings, paragraphs, lists); inline context only allows inline elements

---

#### Rich Text Prop (Inline)

**Description:** Single-line rich text for captions, labels, or short text where inline HTML is needed.
**YAML:**
```yaml
caption:
  type: string
  title: Caption
  contentMediaType: text/html
  x-formatting-context: inline
```
**Canvas widget:** CKEditor 5 inline editor (reduced toolbar).
**Gotchas:** Does not support block-level elements; use `x-formatting-context: block` for multi-paragraph content.

---

#### Image Prop

**Description:** Drupal Media Library image reference. Produces a structured object with image metadata.
**YAML:**
```yaml
image:
  type: object
  title: Image
  description: 'Component image from the media library.'
  $ref: 'json-schema-definitions://canvas.module/image'
```
**Canvas widget:** image field widget (Media Library integration is layered on top via `hook_canvas_storable_prop_shape_alter()`).
**Value structure passed to Twig** — exactly four keys, no more:
```
image.src         — the image URL (NOT `image.url` — that key does not exist)
image.alt         — alt text
image.width       — pixel width
image.height      — pixel height
```
**Gotchas:**
- Do NOT use `<img src="{{ image }}">` — the prop is an object, not a URL
- There is no `image.url` and no `image.srcset`. `srcset` is computed *inside* `canvas:image` from the `|toSrcSet` Twig filter; it is never a value on the prop
- Always use the `canvas:image` component to render image props, and spread the object into the include context (see [SDC Image Handling](sdc-image-handling.md))
- `examples:` on an image prop must be a list of objects with those same keys — e.g. `- {src: hero.jpg, alt: 'Hero', width: 640, height: 427}`. An invalid example disqualifies the whole component

---

#### Link Prop

**Description:** A URL. In Canvas a link is a **plain string with a `format`**, not an object and not a `$ref`.
**YAML — internal *or* external URLs:**
```yaml
cta_url:
  type: string
  format: uri-reference   # accepts /node/1, /contact, and https://example.com
  title: 'Call to Action URL'
  examples:
    - '/contact'
```
**YAML — external URLs only:**
```yaml
cta_url:
  type: string
  format: uri             # absolute URLs only; relative paths are rejected
  title: 'Call to Action URL'
  examples:
    - 'https://www.drupal.org'
```
**Canvas widget:** Drupal's `link_default` widget, URL field only. Canvas sets the link field's `title` instance setting to `0`, so the widget shows **no link-text input**.
**Value passed to Twig:** the URL string itself. Render it with `{{ cta_url }}`.
**Gotchas:**
- `$ref: 'json-schema-definitions://canvas.module/link'` does not exist and never has. This is **not** a disqualification — it is fatal. The stream wrapper behind `json-schema-definitions://` throws when the named definition is absent, and that resolution runs inside SDC plugin discovery for every component on the site, so the next cache rebuild 500s the site. See [Component Eligibility](#component-eligibility-hard-gates)
- There is no `.url` and no `.title`. `url` is the *link field item* property Canvas reads from; `title` is the link field's *instance setting*, which Canvas pins to `0`. Neither is a key on the value your Twig receives
- Need editor-editable link text? Declare a separate `type: string` prop for it and pair the two in your Twig
- `format: uri` vs `format: uri-reference` is the *only* thing that decides internal-links-allowed. `uri` maps to `LinkItemInterface::LINK_EXTERNAL`, `uri-reference` to `LINK_GENERIC`
- Check for emptiness before rendering the anchor — an optional link prop may be unset

---

#### Enum / Select Prop

**Description:** Constrained choice from a fixed list of options.
**YAML:**
```yaml
color_scheme:
  type: string
  title: 'Color Scheme'
  enum:
    - light
    - dark
    - brand
  meta:enum:              # human-readable labels for the dropdown
    light: 'Light'
    dark: 'Dark'
    brand: 'Brand'
  x-translation-context: 'Color scheme'   # optional; makes the labels translatable
  examples:
    - light               # ← this, not `default:`, is the effective default
```
**Canvas widget:** Select dropdown (`options_select` over a `list_string` field).
**Gotchas:**
- **Do not write `default: light`.** Canvas strips `default` from every prop schema. The value Canvas seeds the prop with is `examples[0]`
- The extension key for labels is `meta:enum`, not `enumNames`. `enumNames` appears nowhere in Canvas. Without `meta:enum` the dropdown shows the raw enum strings, which is legal for SDCs (for Code Components `meta:enum` is required and validated)
- An `enum` containing `""` disqualifies the component. To express "no choice", make the prop optional instead

---

#### Boolean Prop

**Description:** On/off toggle for conditional rendering.
**YAML:**
```yaml
show_divider:
  type: boolean
  title: 'Show Divider'
  examples:
    - false             # ← this, not `default:`, is the effective default
```
**Canvas widget:** Toggle/checkbox (`boolean_checkbox`).
**Gotchas:**
- `default: false` is stripped by Canvas. Use `examples: [false]`
- In Twig, check with `{% if show_divider %}` — no casting needed

---

#### Integer/Number Prop

**Description:** Numeric value for quantities, column counts, sizes.
**YAML:**
```yaml
columns:
  type: integer
  title: Columns
  minimum: 1
  maximum: 6
  examples:
    - 3                 # ← this, not `default:`, is the effective default
```
**Canvas widget:** Numeric input (`number` widget), with min/max passed through as field instance settings.
**Gotchas:**
- `default: 3` is stripped by Canvas. Use `examples: [3]`
- Use `integer` for whole numbers; `number` for floats. `minimum`/`maximum` become the widget's min/max
- `multipleOf` has no Drupal core equivalent — a prop that uses it gets no storable shape and disqualifies the component

---

#### Multi-value Props

**Description:** Arrays of a repeated **single** prop shape (e.g., a list of URLs, a gallery of images). An array prop is Canvas's mapping onto a multi-value Drupal field: `type: array` → cardinality, `items:` → the field type.
**YAML — array of strings (optional, unlimited):**
```yaml
tags:
  type: array
  title: Tags
  items:
    type: string
  examples:
    - ['Alpha', 'Beta']
```
**YAML — array of images (required, capped at 4):**
```yaml
images:
  type: array
  title: 'Gallery images'
  minItems: 1        # required arrays MUST have this, and it must be exactly 1
  maxItems: 4        # optional; if present must be >= 2
  items:
    $ref: json-schema-definitions://canvas.module/image
    type: object
  examples:
    - - {src: a.jpg, alt: 'A', width: 601, height: 402}
      - {src: b.jpg, alt: 'B', width: 601, height: 402}
```
**Canvas widget:** the item type's own widget, repeated — editors add/remove/reorder items.
**Gotchas:**
- **`items` must be a scalar type or a recognized `$ref`.** An inline `items: {type: object, properties: {...}}` — the obvious "repeater of sub-fields" shape — is *not* supported: Canvas finds no storable shape for an anonymous object and disqualifies the entire component. For repeated compound content, use a **slot** and let editors nest real components
- The array schema may carry only `type`, `items`, `minItems`, `maxItems`. Any other keyword (`uniqueItems`, `contains`, …) makes the prop unstorable and disqualifies the component. `title`, `description`, `examples`, `meta:enum` are stripped before this check, so those are safe
- `minItems` is allowed only on a **required** array, and only with the value `1`. An optional array with `minItems`, or a required array without it, disqualifies the component
- `maxItems`, if present, must be at least `2`. For a single value, do not use an array
- Multi-value/array prop UI configuration landed in Canvas 1.3.0 (2026-03-20, issue #3571917 — front-end/UI scope); value persistence across reloads was completed in Canvas 1.4.0 (issue #3572553)
- In Canvas 1.10.1 the **Code Component builder** offers its "Allow multiple values" checkbox for nine of its twelve prop types: Text, Link, Image, Video, Date, Integer, Number, List (Text) and List (Integer). It is hidden for **Formatted Text, Boolean and Content Entity Reference**. That is a builder-UI restriction on Code Components only; it says nothing about SDC `type: array` props, which are governed by the array rules above
- The required-field-validation gap for multi-value props is **closed**: issue #3576124 ("Enforce required validation for multi-value props in code component editor") was closed 2026-05-01, so a prop marked both Required and Multi-value enforces at least one value in the Code Component editor
- In Twig, iterate with `{% for item in items %}` — items arrives as an array of objects
- Nesting complex objects in arrays increases component storage complexity; prefer slots for nested components where possible

## Defaults: Canvas Ignores `default:`

This is the single most surprising thing about Canvas props, and it inverts what plain SDC authors expect.

**Canvas deletes `default:` from every prop schema** before deciding how to store the prop, and never reads it again. The value Canvas actually seeds a new component instance with is **`examples[0]`** — the same list you write for documentation and Storybook. Canvas validates `examples[0]` against the prop's own schema precisely because it uses it as the default; an example that does not validate disqualifies the component.

- Write the default you want as the **first** entry of `examples:`. Additional entries are documentation only
- Do not also write `default:` — it is inert, and having two disagreeing "defaults" in one file is a maintenance trap
- On a **required** prop, `examples[0]` is mandatory — no example, no component
- On an **optional** prop with no `examples`, Canvas stores nothing. The effective runtime default is then whatever your Twig supplies via `??` or `|default()`. That is where a fallback belongs
- Content-entity-reference props are the exception in the other direction: they must **not** carry `examples`, because the referenced entity is resolved at runtime

## Component Eligibility (Hard Gates)

Canvas discovers every SDC automatically, then checks it against a fixed list of requirements. **A component that fails any of these is disqualified: it is never offered in the component panel, and if a Component config entity already existed it gets disabled.** For every gate in the table below the failure mode is silence — no error on the page, no exception in the log. One mistake escapes this table entirely and is anything but silent; it is covered immediately after.

See [The One Failure That Is Not Silent](#the-one-failure-that-is-not-silent) below.

| The gate | Failing it means |
|---|---|
| Every prop has a `title` | Component excluded — editors do **not** just see machine names |
| Every slot has a `title` | Component excluded |
| Every required prop has `examples[0]` | Component excluded |
| `examples[0]` validates against the prop's own schema | Component excluded |
| `group:` is not `Elements` | `Elements` is reserved; component excluded |
| No `enum` contains `""` (including inside `items`) | Component excluded |
| Required `type: array` props have `minItems: 1` | Component excluded |
| Optional `type: array` props have **no** `minItems` | Component excluded |
| `maxItems`, if present, is ≥ 2 | Component excluded |
| Every prop resolves to a field type + widget Canvas knows | Component excluded — this is what an inline object array item, an unsupported `format`, or a `$ref` to an *existing* object definition Canvas cannot store trips |
| Content-entity-reference props are optional and carry no `examples` | Component excluded |
| Not flagged `noUi: true` | Filtered out before discovery even runs — deliberately hidden, and it will **not** be listed on the status page. This is how the built-in `canvas:image` stays out of the panel |
| Not `status: obsolete` | Component excluded |

Props typed `Drupal\Core\Template\Attribute` are skipped by all of the above — that is the standard SDC `attributes` prop, and it needs no `title` or `examples`.

## The One Failure That Is Not Silent

Everything in the table above is the *eligibility* gate, and it fails quietly. `$ref` resolution happens **earlier**, during SDC plugin discovery, and it fails loudly. Canvas swaps its own class into core's `plugin.manager.sdc` service, so its `processDefinition()` resolves every `$ref` in every component's props for **every SDC on the site**, Canvas-facing or not. Resolution goes through the `json-schema-definitions://` stream wrapper, which throws an `InvalidArgumentException` when the named definition is not in the target extension's `schema.json`. Nothing on that path catches it — the nearest `catch` handles `ComponentDoesNotMeetRequirementsException`, a different exception on a later step.

The two outcomes are worlds apart:

| What you wrote | What happens |
|---|---|
| A `$ref` that **exists** but whose shape Canvas cannot store — `.../shoe-icon`, or `.../date-range` on a site without the `datetime_range` module | Graceful. That one component is disqualified with *"Drupal Canvas does not know of a field type/widget to allow populating the `X` prop"*, and nothing else is affected |
| A `$ref` naming a definition that does **not** exist — `.../link`, or any typo in the name or the extension | Fatal. The next cache rebuild throws an `InvalidArgumentException` — *"… does not contain a `link` definition."* — out of SDC discovery. Every component fails to build and the site returns 500 |

Canvas has no upstream test covering the fatal case, so do not expect it to be caught for you. Treat every `$ref` you type as a spelling test.

**Where to see why a component is missing:** Canvas records every disqualification reason. Visit **`/admin/appearance/component/status`** (permission: *administer themes*) for a table of every excluded component and the exact message. Check this page first whenever a component you just wrote does not show up — it is faster and more reliable than re-reading your YAML.

**If that page itself 500s, you are looking at the fatal `$ref` case, not a disqualification.** The status page is served by the same Drupal that can no longer build its SDC plugin definitions, so it goes down with everything else, and the page this guide sends you to will not load. Diagnose from the log instead of the UI: the exception message names the extension path and the missing definition, which is enough to find the offending `*.component.yml`. Then grep the codebase for `$ref` and check every name against the target extension's `schema.json` before rebuilding caches.

## Common Mistakes

- Writing `default:` and expecting Canvas to honour it — it is stripped; use `examples[0]`
- Omitting `title` on a prop or slot — this does not degrade the label, it removes the component
- Omitting `examples` on a required prop — same, the component disappears
- Inventing a `$ref` — a name absent from the target extension's `schema.json` is **fatal**, not a disqualification. And `image`/`video`/`content-entity-reference` are only the storable *object* refs; string and integer refs such as `heading-element` and `column-width` resolve as well
- Using `enumNames` — the real key is `meta:enum`
- Forgetting `type: object` alongside `$ref` — SDC's own validator needs it, so `$ref` props must declare both
- Defining props that don't appear in the Twig template — wasted editor effort and storage
- Debugging a missing component by re-reading YAML instead of opening `/admin/appearance/component/status` — and, if that page is down too, still assuming it is a disqualification rather than a fatal `$ref`

## See Also

- [SDC Component Format](sdc-component-format.md) for full component YAML structure
- [SDC Slots](sdc-slots.md) for nested component areas
- [SDC Image Handling](sdc-image-handling.md) for image prop rendering
- Canvas SDC Props docs: https://project.pages.drupalcode.org/canvas/sdc-components/props/
