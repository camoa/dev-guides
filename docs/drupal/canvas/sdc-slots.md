---
description: "When and how to use SDC slots in Canvas — defining drop zones where editors can nest other Canvas components."
tldr: "Use slots when a component has a region where editors should nest other Canvas components, not just edit text or pick an image. Use props for discrete editable values instead."
drupal_version: "11.x"
---

# SDC Slots

## When to Use

> Your component has a region where editors should place other components — not just edit text or pick an image, but nest whole other Canvas components inside. Examples: a card component with an "Actions" slot accepting button components, a grid layout with column slots accepting any content component.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Nesting other Canvas components inside a component | Slot | Enables full component composition in Canvas editor |
| Editable text/images/links | Props | Props map to discrete editor widgets |
| Simple text that editors type directly | Prop with type: string | Less overhead than a slot for text content |
| A list of repeated items with sub-components | Slot (preferred over array props) | More flexible composition than array props |

## Pattern

Define slots in `*.component.yml`:

```yaml
slots:
  content:
    title: Content
    description: 'Main content area — accepts any Canvas component.'
  actions:
    title: Actions
    description: 'Button area — intended for button components.'
```

Render slots in Twig with `{{ slot_name }}`:

```twig
<div class="card">
  <div class="card__content">
    {{ content }}
  </div>
  {% if actions is not empty %}
    <div class="card__actions">
      {{ actions }}
    </div>
  {% endif %}
</div>
```

**Slot behavior in Canvas:**
- Slots appear as drop zones in the Canvas editor
- Editors drag other components into slots
- Slots accept any Canvas component (SDC or Code Component). No `allowedComponents` / `allowed_components` key exists in Canvas 1.10.1 — there is currently no per-slot component allow-list
- **Every slot must have a `title`.** A slot without one disqualifies the entire component from Canvas (see [Component Eligibility](sdc-props-reference.md))
- Slot keys are used **exactly as authored** in the YAML — Canvas does not rename them. The camelCase you see on Code Component slots comes from the in-browser editor generating a machine name from the human-readable name you type, not from a transform applied at render

## Common Mistakes

- Using `{% block %}` for slots — Canvas slots render via `{{ slot_name }}`, not `{% block %}` / `{% embed %}`
- Expecting slots to accept raw HTML from editors — slots only accept Canvas component instances, not arbitrary HTML
- Not checking `{% if slot is not empty %}` before rendering slot wrappers — an empty slot with a wrapper div can break layouts
- Defining slots when you actually want a text prop — if it's just text, use a string prop

## See Also

- [SDC Component Format](sdc-component-format.md)
- Canvas SDC Slots docs: https://project.pages.drupalcode.org/canvas/sdc-components/slots/
