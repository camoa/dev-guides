---
description: "Deciding between props and slots by data shape, and what schema 'validation' actually guarantees"
tldr: "Use props for structured, typed, validated data that drives logic; use slots for unstructured renderable content. Prop validation is a dev-time, assert()-gated lint that never mutates data, and slot required: is not a real key — pick the shape based on the data, not on an enforcement guarantee neither one gives you."
drupal_version: "11.x"
---

# Props vs Slots Decision Framework

## When to Use

> Use this when you're designing a component API, deciding if something should be a prop or slot, or debugging schema validation errors.

## Decision

**Use Props When:**
- Data is **structured and typed** (string, boolean, number, enum, object, array).
- Data needs **validation** against JSON Schema.
- Data drives **component logic** (variants, states, configuration).
- Data is **scalar or simple objects**.
- Example: `variant: 'primary'`, `disabled: true`, `size: 'large'`.

**Use Slots When:**
- Content is **unstructured renderables** (HTML, Drupal render arrays, nested components).
- Content type **cannot be known in advance**.
- Content implements `RenderableInterface`, `MarkupInterface`, or `Stringable`.
- No validation needed, only an existence check.
- Example: main content area, header region, action buttons area.

**What "validated" actually buys you.** Props are checked against the JSON Schema in development only — the check is `assert()`-gated (`ComponentsTwigExtension.php:106`) and off on a production `zend.assertions=-1`, and it never modifies the data. So "props are validated" means *you get a loud error in dev when you pass the wrong shape*, not *bad data cannot reach the template*. Slots get even less: `ComponentNodeVisitor::validateSlots()` reports slots you supplied but never declared, and never reports a declared slot you failed to supply. Pick props vs slots on the shape of the data, not on an enforcement guarantee neither one gives you.

## Pattern

**Props for Configuration** — Reference: `/themes/contrib/radix/components/button/button.component.yml`

```yaml
props:
  type: object
  properties:
    variant:
      type: string
      enum: [primary, secondary, danger]
      default: primary
    size:
      type: string
      enum: [small, medium, large]
      default: medium
    disabled:
      type: boolean
      default: false
```

These control button appearance and behavior — perfect for props. The `default:` lines document intent; `button.twig` is what makes them happen (`{% set variant = variant|default('primary') %}`). Check the template before you rely on any of them.

**Slots for Content** — Reference: `/core/themes/olivero/components/teaser/teaser.component.yml`

```yaml
slots:
  content:
    title: 'Content'
    description: 'Required in practice — teaser.twig has no fallback.'
  image:
    title: 'Image'
  meta:
    title: 'Metadata'
```

These accept arbitrary renderable content — perfect for slots. There is no `required:` key for slots: the schema does not define one and no code reads one, so "required" can only be a note to the next developer plus a sensible fallback inside the `{% block %}`.

**Mixed Props and Slots** — most components use both.

```yaml
# Alert component example
props:
  type: object
  properties:
    variant:
      type: string
      enum: [success, warning, danger, info]
    dismissible:
      type: boolean
      default: false

slots:
  heading:
    title: 'Alert Heading'
  message:
    title: 'Alert Message'
    description: 'Required — alert.twig renders nothing without it.'
```

## Common Mistakes

- **Wrong**: Writing `required: true` on a slot → **Right**: Nothing in core reads it. `ComponentNodeVisitor::validateSlots()` only reports *undeclared* slots. The component ships and renders an empty region in production with no warning. Handle the omission in the template.
- **Wrong**: Using props for HTML/renderable content → **Right**: Props must validate against JSON Schema. HTML/render arrays don't have predictable schemas. Use slots instead.
- **Wrong**: Using slots for simple text/boolean/enum values → **Right**: Slots bypass validation. Simple values should be validated props for better error messages and type safety.
- **Wrong**: Applying logic to slot content in templates beyond existence checks → **Right**: Slots contain arbitrary renderables. Can't reliably check their properties. Capture the block and test the rendered output (`{% set x %}{% block x %}{% endblock %}{% endset %}{% if x|trim is not empty %}`) — see [Twig Templates in SDCs](twig-templates-in-sdcs.md). Never test a slot-named variable around a `{% block %}`; it does not exist on the `{% embed %}` path.

## See Also

- [Component YAML Schema](component-yaml-schema.md)
- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Official Props and Slots Documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming)
