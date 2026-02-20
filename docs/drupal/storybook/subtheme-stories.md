---
description: Writing, overriding, and compositing Storybook stories in Drupal sub-themes
drupal_version: "11.x"
---

# Writing Stories for Sub-Themes

## When to Use

> Write sub-theme stories when your sub-theme adds new components or needs specific variant documentation not covered by the base theme. Skip stories when using a base theme component as-is — the base theme's stories already document it.

Write sub-theme stories when:
- Your sub-theme adds new components not in the base theme
- You want to document sub-theme-specific variants or prop combinations
- You want to override how a base theme component is previewed (different images, text, layout context)

## Decision

| Scenario | Approach |
|---|---|
| New component in sub-theme (`my_theme:cta`) | Create `.story.yml` in `components/cta/` |
| Override base theme component (`replaces: 'ui_suite_daisyui:card'`) | Create story referencing base component ID — it renders the override |
| Additional story for a base theme component | Use `component:` field to target the base component |
| Testing a specific prop combination not in base stories | Create new story file in sub-theme `components/{name}/` |
| Using a base theme component with no changes | No story needed — base theme stories apply |

## Pattern

### New Sub-Theme Component

Place stories alongside the component:

```
my_theme/
  components/
    cta/
      cta.component.yml
      cta.twig
      cta.pcss.css
      cta.default.story.yml
      cta.centered_primary.story.yml
```

```yaml
# components/cta/cta.default.story.yml
name: "CTA default"
props:
  heading_level: 2
  centered: false
slots:
  title: "Build something remarkable"
  text: "Start with a solid foundation."
  buttons:
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: primary
        size: lg
      slots:
        label: "Get started"
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: ghost
        size: lg
      slots:
        label: "Learn more"
library_wrapper: '<div class="p-8">{{ _story }}</div>'
```

### Override of a Base Theme Component

When your sub-theme uses `replaces: 'ui_suite_daisyui:card'`, target the base theme component ID — it will render your override:

```yaml
# components/card/card.border_border.story.yml (in sub-theme)
name: "Card with border (sub-theme)"
component: "ui_suite_daisyui:card"   # targets base ID — renders sub-theme override
props:
  border: border
  heading_level: 3
slots:
  image:
    theme: image
    uri: "https://picsum.photos/400/200"
    alt: "Sample"
    width: 400
    height: 200
  title: "Sub-theme Card Variant"
  text: "This story tests the sub-theme card override with border."
  actions:
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: primary
      slots:
        label: "Read more"
```

### Composition with `story:` Shorthand

Combine existing stories into a section-level story without repeating content:

```yaml
# components/section/section.grid-50x50.story.yml
name: "Section 50x50 grid"
slots:
  items:
    - story: "my_theme:cta.default"
    - story: "ui_suite_daisyui:card.default"
```

### Starterkit Pattern Reference

The ui_suite_daisyui starterkit ships these example sub-theme stories:

| File | Component | Pattern |
|---|---|---|
| `cta.default.story.yml` | New `cta` component | Full props + slots, with `library_wrapper` for padding |
| `cta.centered_primary.story.yml` | New `cta` component | Same component, `centered: true`, `variant: primary` |
| `card.border_border.story.yml` | Base `card` override | Uses sub-theme card (via `replaces`) with border variant |
| `section.grid-50x50.story.yml` | New `section` component | Composite story using grid layout |

## Common Mistakes

- **Wrong**: Creating stories for every CSS modifier variant → **Right**: Focus on stories that demonstrate distinct component behaviors or prop combinations, not every visual permutation.
- **Wrong**: Duplicating base theme story content instead of using the `story:` shorthand → **Right**: `story:` shorthand avoids maintenance burden with no preview benefit.
- **Wrong**: Placing stories outside the `components/` directory → **Right**: `StoryPluginManager` only discovers stories inside `components/` alongside their component.
- **Wrong**: Writing a story for a base theme override using the sub-theme provider prefix (`my_theme:card`) when you have a `replaces` → **Right**: Use the base theme component ID (`ui_suite_daisyui:card`) so the override renders correctly.
- **Wrong**: No `library_wrapper` for full-width components → **Right**: Navbars, drawers, and similar components look broken without a container constraint in the pattern library.

## See Also

- [UI Patterns 2 .story.yml Format](story-yml-format.md)
- Reference: `drupal-ui-suite-daisyui.md` — Section 9 Sub-theming (Starterkit) for component override patterns
- Reference: `drupal-ui-patterns.md` — Pattern Library and Story discovery
