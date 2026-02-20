---
description: Pattern Library — browsable component preview with stories
drupal_version: "10.3+ / 11"
---

## Pattern Library

**Sub-module:** `ui_patterns_library`
**Dependencies:** `ui_patterns`

### What It Does

Provides a browsable component library at `/admin/appearance/ui/components` where developers and designers can preview components with their stories (documented example states).

### Library Pages

| Page | URL | Content |
|---|---|---|
| Overview | `/admin/appearance/ui/components` | All components grouped by category |
| Provider | `/admin/appearance/ui/components/{provider}` | Components from a specific module/theme |
| Single | `/admin/appearance/ui/components/{provider}/{machineName}` | Component detail with metadata, props/slots tables, stories |

### Stories

Stories are YAML files that define example renderings of a component. They are discovered by the `StoryPluginManager`:

**File naming:** `{component-name}.{story-id}.stories.yml`
**Location:** Same directory as the component (inside `components/`)

```yaml
# components/card/card.featured.story.yml
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

Stories can also reference components from other providers using the `component` key:

```yaml
# In a sub-theme, adding stories to a base theme component
component: "base_theme:card"
name: "Custom Story"
props:
  title: "Sub-theme version"
```

### Story Display Behavior

- Stories with a `variant` prop display once with that variant
- Stories without a `variant` prop display once per defined variant
- Library wrappers allow custom HTML around story output

### Customizing Library Pages

Library pages use Drupal's `hook_theme` system. Seven templates can be overridden:
- `ui_patterns_overview_page`
- `ui_patterns_single_page`
- `ui_patterns_component_metadata`
- `ui_patterns_overview_quicklinks`
- `ui_patterns_component_table`
- `ui_patterns_stories_full`
- `ui_patterns_stories_compact`

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using stories for runtime configuration | Stories are documentation artifacts, not configuration. They exist only in the library preview. Runtime behavior is controlled by source plugins. |
| Wrapping single renderables in unnecessary arrays in stories | Keep story structures flat. A single renderable does not need array wrapping. |
| Confusing the library with Storybook | The UI Patterns library is a Drupal-native tool. Storybook is an external JavaScript tool. They serve different purposes and can coexist. |

### See Also

- [Defining Components](#defining-components)
- [Variants](#variants)