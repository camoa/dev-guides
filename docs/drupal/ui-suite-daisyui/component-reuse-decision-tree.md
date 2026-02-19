---
description: When to reuse base components, override with replaces key, or create new components
---

# Component Reuse Decision Tree

## When to Use

When deciding whether to use a base theme component as-is, override it in your sub-theme, or create a new component from scratch.

## Decision

| If you need... | Then... | Why |
|---|---|---|
| Standard DaisyUI component with no visual changes | Use `ui_suite_daisyui:button` directly | No code needed, maintained upstream |
| Same component with different props/defaults | Use UI Styles to apply classes | Non-destructive, configurable per-instance |
| Changed HTML structure but same DaisyUI class system | Create sub-theme SDC with `replaces: 'ui_suite_daisyui:card'` | Inherits props/slots schema, overrides Twig only |
| New component not in DaisyUI | Create new SDC in sub-theme `components/` dir | Own namespace: `my_theme:feature_card` |
| Modified schema (new props, different types) | Create new component, don't use `replaces` | Different schema = different component |
| Component A wraps component B | Use `replaces` for A, embed B via slot | Slot composition, not inheritance |

## Pattern (replaces key)

The starterkit's card override demonstrates the `replaces` pattern:

```yaml
# my_theme/components/card/card.component.yml
name: Card
description: "Cards are used to group and display content."
group: "Data display"
replaces: 'ui_suite_daisyui:card'
# Full schema (variants, slots, props) defined here
variants:
  default:
    title: Default
  side:
    title: Side
  responsive:
    title: Responsive
slots:
  image:
    title: Image
  title:
    title: Title
  text:
    title: Text
  actions:
    title: Actions
props:
  type: object
  properties:
    heading_level:
      title: "Heading level"
      type: integer
      enum: [2, 3, 4, 5, 6]
    # ... additional props like url, actions_position
```

The sub-theme's `card.twig` can completely rewrite the HTML while keeping the same component interface. Optional `card.pcss.css` adds custom styles compiled by Vite.

## Namespace Resolution

- `ui_suite_daisyui:card` = base theme component
- `my_theme:card` with `replaces: 'ui_suite_daisyui:card'` = override (my_theme's Twig is used, referenced everywhere as `ui_suite_daisyui:card`)
- `my_theme:feature_card` = entirely new component (own namespace)
- When another component or template references `ui_suite_daisyui:card`, Drupal resolves to `my_theme:card` if it has `replaces`

## Common Mistakes

- **Using `replaces` when you want a NEW component** -- If your component has a different schema (new props, different slots), don't use `replaces`. When the base theme updates its schema, your override may break. WHY: `replaces` implies interface compatibility.
- **Creating sub-theme component without `replaces` and expecting it to substitute everywhere** -- A `my_theme:card` without `replaces` is a separate component. Templates and Layout Builder configs referencing `ui_suite_daisyui:card` will still use the base theme's version. WHY: Drupal only performs substitution when `replaces` is declared.
- **Duplicating the full component.yml when only overriding Twig** -- If you use `replaces` and only need to change the template, you still must provide the full schema in your component.yml (props, slots, variants). Partial schemas cause missing props. WHY: UI Patterns reads the replacement component's YAML as the authoritative schema.
- **Using `replaces` for components with `@source` CSS** -- If the base component has component-scoped CSS that your override also needs, ensure your sub-theme either inherits it or provides its own. WHY: `replaces` substitutes the component wholesale, including its CSS attachment.

## See Also

- Section 9 Sub-theming | Section 11 Layout Builder Integration
- `drupal-ui-patterns.md` -- Component schema and discovery
