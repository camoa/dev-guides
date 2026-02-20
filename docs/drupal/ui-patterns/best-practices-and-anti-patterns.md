---
description: Best practices and anti-patterns — component naming, slot vs prop decisions, and when NOT to use UI Patterns
drupal_version: "10.3+ / 11"
---

## Best Practices & Anti-Patterns

### Component Naming

**Do:** Use business-agnostic names: `Card`, `Hero`, `Accordion`, `Alert`.
**Do not:** Use business-specific names: `EventCard`, `NewsSlideshow`, `ProductHero`.
**Why:** Components should be reusable across content types. Business-specific names create artificial coupling and reduce reuse.

### Slot vs Prop Decision

| Content Type | Use | Reason |
|---|---|---|
| Block output, rendered markup | Slot | Renderables need the render pipeline |
| Plain text, numbers, booleans | Prop | Strictly typed, validated by JSON Schema |
| Images with URL + alt + title | Slot | Complex renderables with wrapper elements should not be prop-drilled |
| Navigation links | Prop (`links` type) | Structured data with a defined schema |
| CSS classes, HTML attributes | Prop (`attributes` type) | Key-value data, not renderables |

### Avoid Prop Drilling

**Anti-pattern:** Defining props in a parent component solely to pass them to a child component.

```yaml
# BAD: parent has image_url and image_alt just to pass to child
props:
  properties:
    image_url:
      type: "string"
    image_alt:
      type: "string"
```

**Better:** Use a slot and let the child component be configured independently:

```yaml
# GOOD: image is a slot, filled by a nested image component
slots:
  image:
    title: "Image"
```

**Why:** Prop drilling couples parent and child component schemas. When the child changes, the parent must change too. Slots provide decoupling.

### Avoid Prop Paradoxes

Design orthogonal props that do not create incompatible states:

```yaml
# BAD: is_link and url create a paradox (what if is_link=true but url is empty?)
props:
  properties:
    is_link:
      type: "boolean"
    url:
      type: "string"

# GOOD: use a single optional URL prop (empty = not a link)
props:
  properties:
    url:
      "$ref": "ui-patterns://url"
```

### Use `|default()` in Twig

Always handle empty/missing values in templates:

```twig
{# GOOD #}
<h2>{{ title|default('Untitled') }}</h2>
<div class="card card--{{ variant|default('default') }}">

{# BAD: breaks with empty values #}
<h2>{{ title }}</h2>
<div class="card card--{{ variant }}">
```

### Use Drupal Attributes

Always apply the `attributes` prop to the component wrapper element:

```twig
<div{{ attributes }}>
  {{ content }}
</div>
```

**Why:** Drupal modules (contextual links, quick edit, translation, SEO tools) inject attributes into the wrapper. Without `{{ attributes }}`, these features break silently.

### Mark Internal Components

Sub-components that only make sense as children of a parent should be clearly marked:

```yaml
name: "Carousel Item"
group: "Carousel"
tags: ["Internal"]
# In description or metadata, indicate this is internal
```

### When NOT to Use UI Patterns

| Situation | Better Approach |
|---|---|
| Component used only by developers in Twig templates | Use SDC directly |
| Simple text replacement in a theme | Use preprocess hooks or Twig |
| One-off page layout | Use Layout Builder with core layouts |
| Content types with fixed, predictable structure | Field formatters may be simpler than component wrappers |

**Why:** UI Patterns adds an abstraction layer (source plugins, form generation, context resolution). This is valuable when site-builders need configurability, but overhead when developers control all rendering.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Creating one component per content type | Components should be content-agnostic. A "Card" works for articles, events, and products. |
| Hardcoding component IDs in Twig templates | Components should be nested through slots or render arrays, not Twig `include()`. Hardcoded IDs prevent replacement/override. If necessary, use `include()` with `with_context = false`. |
| Hardcoding HTML IDs in components | If a component is used multiple times on a page, duplicate IDs break HTML validity and accessibility. Generate IDs with `random()` or accept them as props. |

### See Also

- [Defining Components](#defining-components)
- [Slots System](#slots-system)
- [Security & Accessibility](#security--accessibility)