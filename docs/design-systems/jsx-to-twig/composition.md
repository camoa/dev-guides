---
description: Convert React component composition patterns to Twig includes and embeds
drupal_version: "11.x"
---

# Component Composition

## When to Use

> Use this when converting React patterns for combining components -- nesting, polymorphic elements, higher-order components, context providers, and compound component APIs.

## Decision

| React Pattern | Twig/SDC Equivalent | Example |
|---|---|---|
| `<Parent><Child /></Parent>` | Slots (named blocks) | Parent defines slots; child content fills them |
| `<Component as="section">` | Dynamic tag: `{% set tag = tag\|default('div') %}` then `<{{ tag }}>` | Polymorphic element |
| `<Component as={Link}>` | Conditional wrapping with `{% if url %}<a>{% else %}<div>{% endif %}` | Cannot pass component types; use conditional tags |
| `React.cloneElement(child, extraProps)` | No equivalent | Pass data via include/embed context instead |
| HOC: `withAuth(Component)` | Preprocess function | Access control and data injection happen in PHP preprocess |
| `forwardRef` | Not needed | Drupal's `attributes` variable passes through all HTML attributes naturally |
| Context/Provider | Preprocess variables or Twig globals | Data flows from PHP to Twig; no client-side context tree |
| Compound: `<Tabs><Tab /><TabPanel /></Tabs>` | Single SDC with slots, or parent + include for items | Flatten into one component with an `items` slot |
| Portal: `createPortal(<Modal />, body)` | Render in Drupal region or use `<dialog>` | No DOM teleportation; use page-level regions |

## Pattern: Dynamic HTML Tag (Polymorphic Component)

**React**
```jsx
function Box({ as: Tag = 'div', className, children, ...rest }) {
  return <Tag className={cn('box', className)} {...rest}>{children}</Tag>;
}
// Usage: <Box as="section">, <Box as="a" href="/link">
```

**Twig**
```twig
{% set tag_name = 'div' %}
{% if url %}
  {% set tag_name = 'a' %}
  {% set attributes = attributes.setAttribute('href', url) %}
{% endif %}
<{{ tag_name }} {{ attributes.addClass('box') }}>
  {% block content %}{% endblock %}
</{{ tag_name }}>
```

## Pattern: Component Composition via Include

**React**
```jsx
function StatGroup({ stats }) {
  return (
    <div className="stats">
      {stats.map(stat => (
        <StatItem key={stat.id} title={stat.title} value={stat.value} />
      ))}
    </div>
  );
}
```

**Twig** (caller assembles the composition)
```twig
{% embed 'ui_suite_daisyui:stat' %}
  {% block items %}
    {% include 'ui_suite_daisyui:stat_item' with {
      title: 'Downloads', value: '31K', description: '+21% this month'
    } %}
    {% include 'ui_suite_daisyui:stat_item' with {
      title: 'Users', value: '4,200', description: '+14% this month'
    } %}
  {% endblock %}
{% endembed %}
```

## Pattern: Wrapper Component (HOC Equivalent)

**React**
```jsx
function withCard(Component) {
  return function CardWrapped(props) {
    return (
      <div className="card">
        <div className="card-body">
          <Component {...props} />
        </div>
      </div>
    );
  };
}
```

**Twig** (using `{% embed %}`)
```twig
{% embed 'ui_suite_daisyui:card' with { size: 'lg' } %}
  {% block text %}
    {% include 'my_theme:custom_content' with { data: data } %}
  {% endblock %}
{% endembed %}
```

`{% embed %}` is Twig's answer to HOCs and wrapper components. It includes a template and overrides specific blocks.

## Common Mistakes

- **Wrong**: Creating deeply nested SDC includes (5+ levels) → **Right**: Flatten the hierarchy where possible
- **Wrong**: Trying to pass a Twig template name as a prop → **Right**: SDC props do not support component references; use conditional logic or separate component variants
- **Wrong**: Using `{% include %}` when `{% embed %}` is needed → **Right**: `{% include %}` cannot override blocks; use `{% embed %}` when you need to fill slots from the caller

## See Also

- [Children & Slots](children-slots.md)
- [Props to Twig Variables](props-to-twig.md)
- Reference: [Twig Embed Tag](https://twig.symfony.com/doc/3.x/tags/embed.html)
