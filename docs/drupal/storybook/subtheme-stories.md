---
description: Writing, overriding, and compositing Storybook stories in Drupal sub-themes
drupal_version: "11.x"
---

# Writing Stories for Sub-Themes

## When to Use

> Write sub-theme stories when your sub-theme adds new components not in the base theme, documents sub-theme-specific variants or prop combinations, or overrides how a base theme component is previewed. If you're using a base theme component as-is (no `replaces`, no new props), the base theme's stories already document it — no duplication needed.

## Decision

| Scenario | Approach |
|---|---|
| New component in sub-theme (`my_theme:cta`) | Create `.story.yml` in `components/cta/` |
| Override base theme component (`replaces: 'ui_suite_daisyui:card'`) | Create story using base component ID — it renders your override |
| Additional story for a base theme component | Use `component:` field in story to target the base component |
| Testing a specific prop combination not covered in base stories | Create new story file in sub-theme `components/{name}/` |

## Pattern

### Directory Structure for New Sub-Theme Components

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

### New Sub-Theme Component Story

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
library_wrapper:
  type: html_tag
  tag: div
  attributes:
    class: "p-8"
```

### Base Theme Component Override Story

When your sub-theme uses `replaces: 'ui_suite_daisyui:card'`, the override component is still referenced as `ui_suite_daisyui:card`. Use the base theme component ID — it renders your override automatically:

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

| File | Component | Pattern |
|---|---|---|
| `cta.default.story.yml` | New `cta` component | Full props + slots, with `library_wrapper` for padding |
| `cta.centered_primary.story.yml` | New `cta` component | Same component, `centered: true`, `variant: primary` |
| `card.border_border.story.yml` | Base `card` override | Uses sub-theme card (via `replaces`) with border variant |
| `section.grid-50x50.story.yml` | New `section` component | Composite story using grid layout |

## Common Mistakes

- **Wrong**: Creating stories for every CSS modifier variant → **Right**: Focus on stories that demonstrate distinct component behaviors or prop combinations, not every visual permutation
- **Wrong**: Duplicating base theme story content → **Right**: Use the `story:` shorthand — adds maintenance burden with no preview benefit
- **Wrong**: Placing stories outside the `components/` directory → **Right**: The `StoryPluginManager` only discovers stories inside `components/` alongside their component
- **Wrong**: Writing a story for a base theme override using the sub-theme prefix `my_theme:card` when you have a `replaces` → **Right**: Use the base theme component ID `ui_suite_daisyui:card` so the override renders correctly
- **Wrong**: No `library_wrapper` for full-width components → **Right**: Navbar, drawer, and similar components look broken without a container constraint in the pattern library

## See Also

- [UI Patterns 2 .story.yml Format](story-yml-format.md)
- [Tool Landscape & Decision](storybook-landscape.md)
- Reference: `drupal-ui-suite-daisyui.md` — Section 9 Sub-theming (Starterkit) for component override patterns
- Reference: `drupal-ui-patterns.md` — Pattern Library and Story discovery
