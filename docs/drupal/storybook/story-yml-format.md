---
description: UI Patterns 2 .story.yml schema: slot value types, story shorthand, naming conventions, and sub-theme story patterns
drupal_version: "11.x"
---

# UI Patterns 2 `.story.yml` Format

## When to Use

> Write `.story.yml` files when adding components to a UI Suite DaisyUI sub-theme, documenting example states of any UI Patterns 2 SDC component, or previewing components in the Drupal pattern library. No Node.js, no Storybook.js required — only a running Drupal with `ui_patterns_library` enabled for viewing.

## Decision

| Need | Slot value type | Notes |
|---|---|---|
| Plain text content | Plain string | `title: "My text"` |
| Embed another component | `type: component` | Requires full provider prefix |
| Raw HTML element | `type: html_tag` | Use `tag`, `value`, `attributes` |
| Icon (requires ui_icons) | `type: icon` | Requires `pack` and `name` |
| Drupal image render array | `theme: image` | Colon-less shorthand |
| Multiple items in sequence | YAML list | Mix types freely |
| Reference another story | `story:` shorthand | `provider:component.story-id` |

## Pattern

### Full Schema

```yaml
# components/{name}/{name}.{variant}.story.yml
name: "Human-readable story name"
description: "Optional description."
component: "provider:component-name"   # optional — override which component this story targets
props:
  variant: "primary"
  heading_level: 2
slots:
  title: "Plain text slot value"
  message:
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: "primary"
      slots:
        label: "Click me"
    - type: html_tag
      tag: p
      value: "Additional text"
  image:
    theme: image
    uri: "https://example.com/img.jpg"
    alt: "Descriptive alt text"
    width: 400
    height: 300
library_wrapper:
  type: html_tag
  tag: div
  attributes:
    class: "max-w-sm"
```

### Naming Convention

```
{component-name}.{story-id}.story.yml
```

- `{story-id}` is kebab-case or underscore-separated
- Convention from ui_suite_daisyui source: underscores preferred over hyphens in story IDs

Examples: `alert.alert_success.story.yml`, `card.image_full.story.yml`, `tabs.size_xl.story.yml`

### `story:` Shorthand

Reference an existing story as a slot value — useful for compositing complex stories from simpler ones:

```yaml
slots:
  actions:
    story: "ui_suite_daisyui:button.default"  # provider:component.story-id
```

### Real-World Example — Alert

```yaml
# alert.alert_success.story.yml
name: "Alert success"
props:
  variant: success
  heading_level: 3
slots:
  title: "Operation complete"
  message: "Your changes have been saved successfully."
  buttons:
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: neutral
        size: sm
      slots:
        label: "Dismiss"
```

### Real-World Example — Card with Image, Badge, Action

```yaml
# card.with_badge.story.yml
name: "Card with badge"
props:
  heading_level: 2
  border: border
slots:
  image:
    theme: image
    uri: "https://picsum.photos/400/200"
    alt: "Card image"
    width: 400
    height: 200
  title:
    - "Article Title"
    - type: component
      component: "ui_suite_daisyui:badge"
      props:
        variant: primary
      slots:
        label: "New"
  text: "A short description of this card's content."
  actions:
    - type: component
      component: "ui_suite_daisyui:button"
      props:
        variant: primary
      slots:
        label: "Read more"
```

### Where Stories Appear

With `ui_patterns_library` enabled:
- `/admin/appearance/ui/components` — all components with story previews
- `/admin/appearance/ui/components/{provider}/{name}` — individual component detail

## Common Mistakes

- **Wrong**: Using `title: "text"` when the slot needs nested components → **Right**: Only plain strings work as direct values; nested components require the list format with `type:`
- **Wrong**: Full-width component story with no `library_wrapper` → **Right**: Add `library_wrapper` with `class: "w-full"` so the story renders in proper layout context
- **Wrong**: Story IDs with spaces or uppercase — `My Story` → **Right**: Use kebab-case or underscores only — `my_story`
- **Wrong**: Referencing components without provider prefix — `button` → **Right**: Always use `ui_suite_daisyui:button`
- **Wrong**: Using JavaScript expressions in YAML — this is pure YAML, no functions or dynamic data

## See Also

- [Tool Landscape & Decision](storybook-landscape.md)
- [Sub-Theme Stories](subtheme-stories.md)
- Reference: `drupal-ui-patterns.md` — full UI Patterns 2 documentation including props schema
- Reference: `drupal-ui-suite-daisyui.md` — component catalog with all props and slots
- Reference: https://project.pages.drupalcode.org/ui_patterns/2-authors/1-stories-and-library/
