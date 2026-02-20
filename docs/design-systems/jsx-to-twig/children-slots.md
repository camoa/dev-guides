---
description: Convert React children and JSX props to Twig blocks and SDC slots
drupal_version: "11.x"
---

# Children & Slots to Twig Blocks

## When to Use

> Use this when converting React's children, named props that accept JSX, render props, or compound component patterns into Twig blocks and SDC slots.

## Decision: Children Pattern Mapping

| React Pattern | SDC Equivalent | Implementation |
|---|---|---|
| `{children}` (single child) | Default slot | `{% block content %}{% endblock %}` in Twig, `slots: content:` in component.yml |
| Named prop: `header={<Header />}` | Named slot | `{% block header %}{% endblock %}` in Twig, `slots: header:` in component.yml |
| Multiple named props: `icon`, `title`, `actions` | Multiple named slots | One `{% block %}` per slot; all declared in component.yml `slots:` |
| Render prop: `renderItem={(item) => ...}` | No direct equivalent | Use Twig `{% include %}` with context variables, or preprocess to prepare render arrays |
| Compound: `<Card><Card.Header /><Card.Body /></Card>` | Slots or nested includes | Parent SDC defines slots; caller fills them with include/embed |
| `{children \|\| <Default />}` (fallback) | Block with default content | `{% block content %}Default content{% endblock %}` -- Twig blocks support defaults |
| Conditional children: `{children && <Wrapper>{children}</Wrapper>}` | `{% if slot_name %}` check | Slots are truthy when filled; check before rendering wrapper |

## Pattern: Single Default Slot

**React**
```jsx
function Card({ children }) {
  return <div className="card"><div className="card-body">{children}</div></div>;
}
```

**component.yml**
```yaml
slots:
  content:
    title: Content
    description: "Card body content."
```

**Twig**
```twig
<div {{ attributes.addClass('card') }}>
  <div class="card-body">
    {% block content %}{% endblock %}
  </div>
</div>
```

## Pattern: Multiple Named Slots

**React**
```jsx
function Hero({ title, aside, button, children }) {
  return (
    <div className="hero">
      <div className="hero-content">
        {aside && <div className="aside">{aside}</div>}
        <div>
          {title && <h1>{title}</h1>}
          {children}
          {button}
        </div>
      </div>
    </div>
  );
}
```

**component.yml**
```yaml
slots:
  aside:
    title: Aside
  title:
    title: Title
  text:
    title: Text
  button:
    title: Button
```

**Twig**
```twig
<div {{ attributes.addClass('hero') }}>
  <div class="hero-content">
    {% if aside %}
      {{ aside }}
    {% endif %}
    <div>
      {% if title %}
        <h1 class="text-5xl font-bold">{{ title }}</h1>
      {% endif %}
      {{ text }}
      {{ button }}
    </div>
  </div>
</div>
```

Note: SDC slots are rendered by outputting the slot variable name directly (`{{ aside }}`), not with `{% block %}`. The `{% block %}` syntax is used when the SDC is consumed via `{% embed %}`.

## Common Mistakes

- **Wrong**: Using `{% block %}` for slots in the component template → **Right**: SDC slots arrive as render arrays in template variables; use `{{ slot_name }}` to output slot content
- **Wrong**: Creating separate SDC components for every sub-piece → **Right**: SDC registration has overhead; use slots on a single component instead
- **Wrong**: Trying to iterate over slot contents → **Right**: Slot content is an opaque render array; if you need iteration, pass data as a prop

## See Also

- [Props to Twig Variables](props-to-twig.md)
- [Component Composition](composition.md)
- Reference: [UI Suite DaisyUI Hero component](https://git.drupalcode.org/project/ui_suite_daisyui/-/tree/4.x/components/hero)
