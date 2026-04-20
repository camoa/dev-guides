---
description: When and how to use SDC slots in Canvas — defining drop zones where editors can nest other Canvas components.
tldr: "Use slots when your component has a region where editors should place other components — not just edit text or pick an image, but nest whole other Canvas components inside. Use props when you want editors to type text, pick an image, or…"
drupal_version: "11.x"
---

# SDC Slots

## When to Use

> Use slots when your component has a region where editors should place other components — not just edit text or pick an image, but nest whole other Canvas components inside. Use props when you want editors to type text, pick an image, or toggle a setting.

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
- Slots accept any Canvas component (SDC or Code Component) unless you add `allowedComponents` constraints (check current Canvas docs for this feature's status)
- Slot names are **camelCased** when passed as parameters in Code Components (e.g., slot `call_to_action` becomes `callToAction` in Code Component props)

## Common Mistakes

- **Wrong**: Using `{% block %}` for slots → **Right**: Canvas slots render via `{{ slot_name }}`, not `{% block %}` / `{% embed %}`
- **Wrong**: Expecting slots to accept raw HTML from editors → **Right**: Slots only accept Canvas component instances, not arbitrary HTML
- **Wrong**: Not checking `{% if slot is not empty %}` before rendering slot wrappers → **Right**: An empty slot with a wrapper div can break layouts
- **Wrong**: Defining slots when you actually want a text prop → **Right**: If it's just text, use a string prop

## See Also

- [SDC Component Format](sdc-component-format.md)
- Canvas SDC Slots docs: https://project.pages.drupalcode.org/canvas/sdc-components/slots/
