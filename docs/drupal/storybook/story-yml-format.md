---
description: Complete UI Patterns 2 .story.yml schema reference — all slot value types, props, naming conventions, and verbatim examples from ui_suite_daisyui 5.0.x source
drupal_version: "11.x"
---

# UI Patterns 2 `.story.yml` Format

## When to Use

> Write `.story.yml` files when adding or documenting components for the UI Patterns 2 pattern library — any SDC theme with `ui_patterns_library` enabled. No Node.js or Storybook.js required. Use Storybook.js tools when you need interactive Controls.

Write `.story.yml` files when:
- Adding new components to a UI Suite DaisyUI sub-theme or any UI Patterns 2 SDC theme
- Documenting example states of any SDC component for the pattern library
- Previewing components at `/admin/appearance/ui/components`

## Decision

### Complete Top-Level Schema

Source: `ui_patterns/modules/ui_patterns_library/src/StoryPluginManager.php` — `$defaults` array is the authoritative key list.

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `name` | string | **Yes** | Human-readable display name shown in the pattern library UI |
| `description` | string | No | Subtitle shown below the story name on the component page |
| `component` | string | No | Override target component as `provider:component_id`. Omit when story is in the same folder as the component |
| `props` | object | No | Key-value pairs matching the component's JSON schema props |
| `slots` | object | No | Named slot content — keys match slot IDs in `component.yml`. Values are slot value definitions |
| `library_wrapper` | string | No | Inline Twig template string. Use `{{ _story }}` to place the rendered component. Must be a **string**, not a YAML object |

File naming regex enforced by `DirectoryWithMetadataDiscovery`:

```
/^([a-z0-9_-])+\.([a-z0-9_-])+\.story\.yml$/i
```

Pattern: `{component_id}.{story_id}.story.yml` — both segments are `[a-z0-9_-]+`.

Discovery scans `components/` directories recursively across all enabled modules and themes. The story ID derived from the filename becomes the plugin's `machineName`.

### Props

Props are direct scalar values (string, boolean, integer, object) matching the component's JSON schema definition. The `StoriesSyntaxConverter` does **not** process props — they are passed through as-is.

```yaml
props:
  variant: primary          # string enum
  heading_level: 2          # integer
  soft: true                # boolean
  attributes:
    class: ["bg-base-100", "w-96", "shadow-sm"]   # Attribute object
  icon:
    pack_id: hero_outline_24    # icon prop type (object, not a slot render array)
    icon_id: information-circle
    settings:
      stroke_width: 2
      stroke_color: stroke-info
```

**Key distinction**: `icon` as a **prop** is a structured object with `pack_id`/`icon_id`/`settings`. Different from `type: icon` as a **slot value**.

### Slot Value Types — Complete Reference

Slot values are Drupal render arrays. The `StoriesSyntaxConverter` strips the `#` prefix requirement — write keys without `#`.

**Detection rule** from source code: an array is recognized as a render array when it has exactly ONE of these keys: `markup`, `plain_text`, `theme`, `item_list`, `type` (or their `#`-prefixed versions). Zero or two+ triggers = NOT a render array.

| Type | Trigger key | Use when |
|---|---|---|
| Plain string | — | Simple text content |
| `html_tag` | `type: html_tag` | Wrap content in an HTML element |
| `component` | `type: component` | Embed another SDC component |
| Drupal image | `theme: image` | Render an image with alt/dimensions |
| Icon | `type: icon` | Render a UI Icons icon in a slot |
| Item list | `theme: item_list` | Drupal item list render array |
| YAML list | — (sequence) | Multiple renderables in one slot |
| Raw markup | `markup:` | Inject trusted HTML directly |
| Plain text | `plain_text:` | Escaped text directly |

### Naming Convention

```
{component_id}.{story_id}.story.yml
```

- Both segments: lowercase letters, digits, hyphens, underscores
- Convention from ui_suite_daisyui 5.0.x: underscores preferred (`alert_success`, `image_full`, `size_xl`)
- Story ID becomes the `machineName` — must be unique within a component scope
- File must be in a `components/` directory

## Pattern

### 1. Plain string slot

```yaml
slots:
  title: "Card Title"
  message: "12 unread messages. Tap to see."
```

### 2. `type: html_tag`

```yaml
slots:
  text:
    type: html_tag
    tag: p
    value: "A card component has a figure, a body, and actions parts"
```

`value` must be a plain string — cannot itself be a render array.

### 3. `type: component` — Embed another SDC component

```yaml
slots:
  actions:
    type: component
    component: "ui_suite_daisyui:button"
    slots:
      label: "Buy Now"
    props:
      variant: primary
```

`story:` sub-key loads an existing story's data as a base:

```yaml
slots:
  center:
    type: component
    component: ui_suite_daisyui:menu
    story: flat            # loads menu.flat story data as base
    props:
      variant: horizontal__md
```

### 4. `theme: image`

```yaml
slots:
  image:
    theme: image
    uri: "https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp"
    alt: Shoes
```

`uri` accepts absolute URLs or Drupal stream wrapper paths (`public://image.jpg`).

### 5. YAML list — Multiple items in one slot

```yaml
slots:
  buttons:
    - type: component
      component: "ui_suite_daisyui:button"
      slots:
        label: Deny
      props:
        size: sm
    - type: component
      component: "ui_suite_daisyui:button"
      slots:
        label: Accept
      props:
        variant: primary
        size: sm
```

### 6. `library_wrapper`

```yaml
name: Default
library_wrapper: '<div class="w-full bg-base-200 p-4">{{ _story }}</div>'
slots:
  label: daisyUI
```

Use when components need layout context: navbars (full width), drawers (height), cards (max-width constraint).

### Complete Working Examples

#### Alert with icon prop and string slot (verbatim from ui_suite_daisyui 5.0.x)

```yaml
# alert.alert_success.story.yml
name: Alert success
slots:
  message: "12 unread messages. Tap to see."
props:
  variant: success
  icon:
    pack_id: hero_outline_24
    icon_id: information-circle
    settings:
      stroke_width: 2
      stroke_color: stroke-success-content
```

#### Card with image, mixed title list, and component slots (verbatim from ui_suite_daisyui 5.0.x)

```yaml
# card.with_badge.story.yml
name: "With badge"
slots:
  image:
    theme: image
    uri: "https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp"
    alt: Shoes
  title:
    - "Card title"
    - type: component
      component: "ui_suite_daisyui:badge"
      slots:
        label: "NEW"
      props:
        variant: secondary
  text:
    type: html_tag
    tag: p
    value: "If a dog chews shoes whose shoes does he choose?"
  actions:
    - type: component
      component: "ui_suite_daisyui:badge"
      slots:
        label: "Fashion"
      props:
        outline: outline
    - type: component
      component: "ui_suite_daisyui:badge"
      slots:
        label: "Products"
      props:
        outline: outline
props:
  variant: compact
  heading_level: 2
  attributes:
    class: ["bg-base-100", "w-96", "shadow-sm"]
```

#### Navbar with `story:` shorthand (verbatim from ui_suite_daisyui 5.0.x)

```yaml
# navbar.default.story.yml
name: Default
slots:
  start:
    type: component
    component: ui_suite_daisyui:button
    slots:
      label: daisyUI
    props:
      variant: ghost
  center:
    type: component
    component: ui_suite_daisyui:menu
    story: flat              # loads menu.flat story's slots/props as base
    props:
      variant: horizontal__md
  end:
    type: component
    component: ui_suite_daisyui:button
    slots:
      label: Button
```

#### Drawer with nested components (verbatim from ui_suite_daisyui 5.0.x)

```yaml
# drawer.default.story.yml
name: Default
slots:
  content:
    type: component
    component: "ui_suite_daisyui:button"
    slots:
      label: Open drawer
    props:
      variant: primary
      drawer_id: my-drawer-1
      attributes:
        class: ["drawer-button"]
  sidebar:
    type: component
    component: "ui_suite_daisyui:menu"
    props:
      variant: vertical__md
      items:
        - title: "Sidebar Item 1"
          url: "#"
        - title: "Sidebar Item 2"
        - title: "Sidebar Item 3"
          url: "#"
      attributes:
        class: ["bg-base-200", "text-base-content", "min-h-full", "w-80", "p-4"]
props:
  variant: default
  drawer_id: my-drawer-1
```

### Where Stories Appear

With `ui_patterns_library` submodule enabled:
- `/admin/appearance/ui/components` — global overview, all providers
- `/admin/appearance/ui/components/{provider}` — per-provider overview
- `/admin/appearance/ui/components/{provider}/{component_id}` — single component page with all stories

If a story has a `variant` prop, it renders once. If no `variant` prop, it renders once per defined variant — this behavior is intentional but often surprising.

## Common Mistakes

- **Wrong**: Using `type:` and `theme:` together in the same YAML mapping → **Right**: The converter detects render arrays by exactly ONE trigger key. Two = broken output.
- **Wrong**: Writing `library_wrapper` as a YAML object → **Right**: Must be an inline Twig template string: `library_wrapper: '<div>{{ _story }}</div>'`
- **Wrong**: Confusing icon as a **prop** vs icon as a **slot render array** → **Right**: Prop uses `pack_id`/`icon_id`/`settings` at the prop level; slot render array uses `type: icon` with the same keys.
- **Wrong**: Putting a render array inside `html_tag`'s `value` → **Right**: `value` must be a plain string. Use a list of html_tag items instead.
- **Wrong**: Omitting `component:` when the story file is NOT in the same folder as the component → **Right**: Cross-provider stories require explicit `component: "provider:component_id"`.
- **Wrong**: Adding `#` prefixes manually alongside unprefixed keys → **Right**: The converter handles `#` prefixes. Mixing `#`-prefixed and unprefixed keys in the same array causes the converter to skip that array.
- **Wrong**: Naming story files with hyphens when the component uses underscores → **Right**: The story_id in the filename must match exactly when referencing via `story:` shorthand.

## See Also

- [Tool Landscape & Decision](storybook-landscape.md)
- [Sub-Theme Stories](subtheme-stories.md)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_library/src/StoriesSyntaxConverter.php` — canonical render key list and conversion logic
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_library/src/StoryPluginManager.php` — story schema defaults and discovery
- Reference: `modules/contrib/ui_patterns/docs/2-authors/1-stories-and-library.md` — official story format documentation
- Reference: `drupal-ui-patterns.md` — full UI Patterns 2 documentation including props schema
- Reference: `drupal-ui-suite-daisyui.md` — component catalog with all props and slots
