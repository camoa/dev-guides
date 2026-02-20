---
description: Step-by-step workflow for converting TypeScript interfaces to component.yml schemas
drupal_version: "11.x"
---

# TypeScript to Component.yml

## When to Use

> Use this when you have a TypeScript interface or Props type definition and need to produce a complete SDC `component.yml` schema. This is a step-by-step workflow for the most common translation task.

## Decision: Type Mapping

| TypeScript Type | JSON Schema Type | Notes |
|---|---|---|
| `string` | `type: string` | |
| `number` | `type: number` | Use `integer` if always whole numbers |
| `boolean` | `type: boolean` | |
| `'a' \| 'b' \| 'c'` | `type: string` + `enum: [a, b, c]` | Add `meta:enum` for labels |
| `2 \| 3 \| 4 \| 5 \| 6` | `type: integer` + `enum: [2, 3, 4, 5, 6]` | Numeric union |
| `string \| undefined` (optional `?`) | Omit from `required` list | |
| `Record<string, string>` | `type: object` | Rarely used in SDCs |
| `string[]` | `type: array` + `items: { type: string }` | Prefer slots for complex arrays |
| `React.ReactNode` | Move to `slots:` | Renderable content is always a slot |
| `() => void` / functions | **SKIP** | Use behaviors for interactivity |
| `React.HTMLAttributes<T>` | **SKIP** | Handled by Drupal's `attributes` variable |

## Pattern: Complete Workflow

**Step 1: Extract the TypeScript interface**

```typescript
interface CardProps {
  title: string;
  description?: string;
  variant?: 'default' | 'compact' | 'side';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  bordered?: boolean;
  url?: string;
  onClick?: () => void;
  className?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}
```

**Step 2: Classify each property**

| Property | Category | SDC Mapping |
|---|---|---|
| `title` | String data | `props` -- string type |
| `description` | Optional string data | `props` -- string type (not required) |
| `variant` | String union (styling) | `variants` section |
| `size` | String union (sizing) | `props` with enum + meta:enum |
| `bordered` | Boolean flag | `props` -- boolean type |
| `url` | URL string | `props` -- use `$ref: "ui-patterns://url"` |
| `onClick` | Callback function | **SKIP** -- no Twig equivalent |
| `className` | CSS classes | **SKIP** -- handled by `attributes` |
| `children` | Renderable content | `slots` -- default content slot |
| `actions` | Renderable content | `slots` -- named actions slot |

**Step 3: Write the component.yml**

```yaml
name: Card
description: "Cards display content in a contained, flexible format."
group: "Data display"

variants:
  default: { title: Default }
  compact: { title: Compact }
  side: { title: Side }

slots:
  title:
    title: Title
  description:
    title: Description
  content:
    title: Content
  actions:
    title: Actions

props:
  type: object
  properties:
    size:
      title: Size
      type: string
      enum: [sm, md, lg, xl]
      meta:enum:
        sm: Small
        md: Medium
        lg: Large
        xl: Extra large
    bordered:
      title: Bordered
      type: boolean
    url:
      title: URL
      $ref: "ui-patterns://url"
```

**Step 4: Write the Twig template**

```twig
{% set classes = [
  'card',
  variant and variant == 'compact' ? 'card-compact',
  variant and variant == 'side' ? 'card-side',
  size ? 'card-' ~ size,
  bordered ? 'card-bordered',
] %}

{% set tag_name = 'div' %}
{% if url %}
  {% set tag_name = 'a' %}
  {% set attributes = attributes.setAttribute('href', url) %}
{% endif %}

<{{ tag_name }} {{ attributes.addClass(classes) }}>
  {% if title %}
    <h2 class="card-title">{{ title }}</h2>
  {% endif %}
  {% if description %}
    <p>{{ description }}</p>
  {% endif %}
  {{ content }}
  {% if actions %}
    <div class="card-actions">{{ actions }}</div>
  {% endif %}
</{{ tag_name }}>
```

## Workflow Checklist

1. **Extract** -- Copy the full interface/Props type
2. **Classify** -- Mark each property as: prop, slot, variant, skip, or preprocess
3. **Skip these** -- `React.Ref`, callbacks (`() => void`), `className`, `style`, `React.HTMLAttributes`
4. **Convert to slots** -- Any `React.ReactNode` or `JSX.Element` type becomes a named slot
5. **Convert variants** -- String unions that control CSS modifier classes go in `variants:`
6. **Convert enums** -- Other string/number unions become `enum` with `meta:enum` labels
7. **Set required** -- Only props that the component cannot function without
8. **Add defaults** -- Use `|default()` in Twig for any prop that has a default value in React
9. **Handle URL props** -- Use `$ref: "ui-patterns://url"` for URL-type props
10. **Handle ID props** -- Use `$ref: "ui-patterns://identifier"` for ID-type props

## Common Mistakes

- **Wrong**: Trying to represent `React.ReactNode` as `type: string` → **Right**: Renderable content must be a slot to preserve HTML and cache metadata
- **Wrong**: Putting `className` as a prop → **Right**: Drupal's `attributes` variable already handles class merging
- **Wrong**: Making every prop `required` → **Right**: Only truly required props (those that break the component if missing)
- **Wrong**: Forgetting `meta:enum` labels → **Right**: Site builders see raw values without them

## See Also

- [Props to Twig Variables](props-to-twig.md)
- [Children & Slots](children-slots.md)
- Reference: [SDC component.yml](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml)
