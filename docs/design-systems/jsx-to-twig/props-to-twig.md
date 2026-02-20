---
description: Map React component props to SDC component.yml and Twig variables
drupal_version: "11.x"
---

# Props to Twig Variables

## When to Use

> Use this when mapping React component props to SDC `component.yml` properties and Twig template variables. This is the core translation step for every component.

## Decision: Prop Type Mapping

| React Prop Type | component.yml Type | Twig Usage | Notes |
|---|---|---|---|
| `string` | `type: string` | `{{ title }}` | Direct output |
| `boolean` | `type: boolean` | `{% if active %}` | Conditional logic |
| `number` | `type: integer` or `type: number` | `{{ count }}`, `{% if count > 0 %}` | Use `integer` for whole numbers |
| `'sm' \| 'md' \| 'lg'` (union) | `type: string` + `enum` | `{% if size == 'lg' %}` | Add `meta:enum` for UI labels |
| `string \| undefined` (optional) | Omit from `required` | `{{ value\|default('fallback') }}` | Optional props use `default` filter |
| `ReactNode` (children) | Use `slots:` not props | `{% block content %}{% endblock %}` | Renderable content always goes in slots |
| `() => void` (callback) | No equivalent | N/A | Event callbacks become JS behaviors |
| `Record<string, string>` (object) | `type: object` | `{% for key, val in obj %}` | Avoid complex objects; prefer flat props |
| `string[]` (array) | `type: array` + `items` | `{% for item in items %}` | Prefer slots for repeated complex content |
| `React.HTMLAttributes` | `attributes` variable | `{{ attributes }}` | Drupal's Attribute object handles all HTML attributes |

## Pattern: String Prop with Default

**React**
```jsx
interface AlertProps {
  message: string;
  heading?: string;
}
function Alert({ message, heading = 'Notice' }: AlertProps) {
  return (
    <div className="alert">
      <h3>{heading}</h3>
      <p>{message}</p>
    </div>
  );
}
```

**component.yml**
```yaml
props:
  type: object
  required:
    - message
  properties:
    heading:
      title: Heading
      type: string
slots:
  message:
    title: Message
```

**Twig**
```twig
{% set heading = heading|default('Notice') %}
<div {{ attributes.addClass('alert') }}>
  <h3>{{ heading }}</h3>
  <div>{{ message }}</div>
</div>
```

## Pattern: Enum Prop (Variant)

**React**
```jsx
type Variant = 'primary' | 'secondary' | 'accent' | 'error';
function Badge({ variant = 'primary', children }) {
  return <span className={`badge badge-${variant}`}>{children}</span>;
}
```

**component.yml**
```yaml
variants:
  default: { title: Default }
  primary: { title: Primary }
  secondary: { title: Secondary }
  accent: { title: Accent }
  error: { title: Error }
slots:
  label:
    title: Label
```

**Twig**
```twig
{% set classes = [
  'badge',
  variant and variant != 'default' ? 'badge-' ~ variant,
] %}
<div {{ attributes.addClass(classes) }}>{{ label }}</div>
```

## Common Mistakes

- **Wrong**: Creating a `classes` prop of type `string` → **Right**: Drupal's `attributes` variable already handles this
- **Wrong**: Making renderable content (HTML) a `string` prop → **Right**: String props get escaped; slots preserve render arrays and cache metadata
- **Wrong**: Omitting `meta:enum` on enum props → **Right**: Without labels, site builders see raw values (`sm`, `md`, `lg`) instead of human-readable names

## See Also

- [Children & Slots](children-slots.md)
- [TypeScript to Component.yml](typescript-to-component-yml.md)
- Reference: [SDC component.yml](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml)
