---
description: Pattern Library — browsable component library, stories YAML format, template overrides
drupal_version: "11.x"
---

# Pattern Library

**Sub-module:** `ui_patterns_library`
**Dependencies:** `ui_patterns`

## When to Use

> Enable `ui_patterns_library` when developers and designers need to browse, preview, and document components with example states (stories).

## Decision

| Need | Approach |
|------|---------|
| Browse all components | `/admin/appearance/ui/components` |
| Preview components with example states | Add `.{story-id}.stories.yml` files |
| Override library page templates | Implement `hook_theme` overrides for `ui_patterns_*` templates |

## Pattern

### Story file format

**File naming:** `{component-name}.{story-id}.stories.yml`
**Location:** Same directory as the component, inside `components/`

```yaml
# components/card/card.featured.stories.yml
name: "Featured Card"
description: "A card with all slots filled and highlighted variant"
props:
  title: "Featured Article"
  image_url: "https://example.com/image.jpg"
  variant: "highlighted"
slots:
  content:
    - type: component
      component: "my_theme:rich-text"
      props:
        text: "<p>Featured content goes here.</p>"
  footer:
    - "#markup": "<span>Read more</span>"
```

### Story display behavior

- Stories with a `variant` prop display once with that variant
- Stories without a `variant` prop display once per defined variant

### Seven overridable templates

- `ui_patterns_overview_page`
- `ui_patterns_single_page`
- `ui_patterns_component_metadata`
- `ui_patterns_overview_quicklinks`
- `ui_patterns_component_table`
- `ui_patterns_stories_full`
- `ui_patterns_stories_compact`

## Common Mistakes

- **Wrong**: Using stories for runtime configuration → **Right**: Stories are documentation artifacts; runtime behavior is controlled by source plugins
- **Wrong**: Wrapping single renderables in unnecessary arrays in stories → **Right**: Keep story structures flat
- **Wrong**: Treating the UI Patterns library as a Storybook replacement → **Right**: They serve different purposes (Drupal-native vs external JS tool) and can coexist

## See Also

- [Defining Components](defining-components.md)
- [Variants](variants.md)
- Reference: [Stories and Library](https://project.pages.drupalcode.org/ui_patterns/2-authors/1-stories-and-library/)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_library/`
