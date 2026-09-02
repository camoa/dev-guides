---
description: UI Patterns and SDC integration with Plus Suite — what works, inline editing limitations, recommended architecture, and hybrid components
tldr: "Use UI Patterns layouts as structural section layouts and block_content for content blocks that need inline editing. Do not use UI Patterns blocks as your primary strategy if inline editing is a requirement."
drupal_version: "11.x"
---

# UI Patterns & SDC Integration

## When to Use

> When you want to use Single Directory Components (SDC) as Layout Builder blocks and section layouts within Plus Suite, instead of or alongside traditional block_content types.

## How UI Patterns Works with Layout Builder

UI Patterns 2.x provides two sub-modules that expose SDC components to Layout Builder:

| Sub-module | What It Does | LB+ Integration |
|---|---|---|
| `ui_patterns_layouts` | Exposes SDC components (with slots) as Layout plugins | Works with LB+ Layout tool — components appear in layout chooser |
| `ui_patterns_blocks` | Exposes SDC components as Block plugins | Works with LB+ PlaceBlock tool — components appear in block sidebar |

## Why This Works with LB+

LB+ is a **drop-in UI replacement** for Layout Builder — it doesn't change the underlying plugin systems. Specifically:

1. **PlaceBlock tool** uses `BlockManager::getFilteredDefinitions('layout_builder')` to populate the sidebar — UI Patterns blocks (plugin ID: `ui_patterns:{provider}:{component}`) appear automatically in the "Other" tab.
2. **Layout tool** uses standard `LayoutPluginManager` to offer section layouts — UI Patterns layouts (layout ID: `ui_patterns:{provider}:{component}`) appear automatically in the layout chooser.
3. **Configure tool** opens the layout's `buildConfigurationForm()` — UI Patterns layouts expose their props as form elements through `ComponentFormBuilderTrait`.
4. **Section Library** can save and reuse sections that use UI Patterns layouts — the layout config (including props) is preserved.

## What Works

| Feature | Status | Notes |
|---|---|---|
| SDC as Layout Builder blocks | Works | Appears in PlaceBlock sidebar under "UI Patterns" category |
| SDC as section layouts | Works | Appears in Layout tool layout chooser |
| Props configuration | Works | Configure tool opens props form |
| Slot filling with blocks | Works | Place blocks into component slots via drag-and-drop |
| Variants | Works | Selectable in layout/block configuration |
| Entity field sources | Works | Context resolution via `ChainContextEntityResolver` |
| Promoted blocks | Works | Can promote UI Patterns blocks (use `ui_patterns:{provider}:{component}` as ID) |
| Nested layouts | Works | UI Patterns layouts can be used inside layout blocks |
| Section Library | Works | Sections with UI Patterns layouts save/restore correctly |
| Inline editing (Edit+) | Partial | Only works on fields exposed through standard field rendering, not on component props |

## Inline Editing Limitation

**Important**: Edit+ inline editing works by correlating rendered field output with entity form elements. UI Patterns components render props and slots through the SDC rendering pipeline, which is different from standard field rendering.

| Scenario | Edit+ Works? | Why |
|---|---|---|
| UI Patterns block with entity field sources | Props: No, Slots: Depends | Props render through SDC, not field formatters |
| UI Patterns block with manual text sources | No | No entity field to correlate with |
| Standard block_content in UI Patterns layout slot | Yes | Block fields render through standard pipeline |
| Entity fields in UI Patterns layout props | No | Props bypass field rendering |

**Workaround**: Use UI Patterns layouts for structural design (section layouts), but place standard block_content types (with Edit+ support) in the layout's slot regions. This gives you SDC-based layouts with full inline editing on the blocks inside.

## Recommended Architecture: SDC Layouts + Block Content

```
UI Patterns Layout (SDC component as section layout)
  ├── Props: configured via Configure tool (structural settings)
  └── Slots (regions):
      ├── block_content:hero (standard block with inline editing)
      ├── block_content:card (standard block with inline editing)
      └── block_content:testimonial (standard block with inline editing)
```

This gives you:

- **SDC-based section layouts** with design system props (spacing, background, grid type)
- **Full inline editing** on all block content within slots
- **Promoted blocks** in the PlaceBlock sidebar
- **Sample content generation** when blocks are placed

## Configuring UI Patterns Blocks as Promoted

```yaml
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'ui_patterns:my_theme:alert'
      - 'ui_patterns:my_theme:card'
      - 'ui_patterns:my_theme:hero'
    block_config:
      icon:
        'ui_patterns:my_theme:alert': '/themes/custom/my_theme/assets/block-icons/alert.svg'
        'ui_patterns:my_theme:card': '/themes/custom/my_theme/assets/block-icons/card.svg'
```

## Sample Content for UI Patterns Blocks

UI Patterns blocks don't use block_content entities, so `field_sample_value` generators don't apply. The block appears with empty props/slots. To improve UX:

1. Set prop defaults in the component's `*.component.yml`:

```yaml
props:
  type: object
  properties:
    heading:
      type: string
      title: Heading
      default: "Sample Heading"
    body:
      type: string
      title: Body
      default: "Lorem ipsum dolor sit amet"
```

2. Or use `hook_block_alter()` to set defaults programmatically.

## Decision: UI Patterns vs block_content for Plus Suite

| Factor | UI Patterns Blocks | block_content Blocks |
|---|---|---|
| Inline editing | No (props don't correlate) | Yes (full Edit+ support) |
| Sample content | Limited (component defaults only) | Full (field_sample_value) |
| Design system consistency | Excellent (SDC components) | Good (with themed templates) |
| Props configuration | Via source plugins (rich) | Via entity fields |
| Site builder UX | Form-based config | Inline + drag-and-drop |
| Developer experience | SDC + JSON Schema | Block type + fields |
| Reusability | Cross-project (SDC portable) | Per-project (config entities) |

## Recommended Approach

| Use UI Patterns For | Use block_content For |
|---|---|
| Section layouts (structural) | Content blocks (text, image, CTA) |
| Design system wrapper components | Blocks needing inline editing |
| Components with complex prop logic | Simple field-based content |
| Shared component library | Project-specific content types |

## Alternative: Hybrid Components

Create block_content types that render through SDC components via `hook_preprocess_block()`:

```php
function my_theme_preprocess_block__inline_block__hero(&$variables) {
  $block = $variables['content']['#block_content'];
  $variables['content'] = [
    '#type' => 'component',
    '#component' => 'my_theme:hero',
    '#props' => [
      'heading' => $block->field_heading->value,
      'variant' => $block->field_variant->value,
    ],
    '#slots' => [
      'media' => $block->field_media->view('default'),
    ],
  ];
}
```

This gives you block_content fields (Edit+ works) rendered through SDC components (design system consistency).

## Common Mistakes

- **Do not expect Edit+ inline editing on UI Patterns block props** — use block_content for inline editing needs.
- **Do not use UI Patterns blocks as the primary component strategy if inline editing is a key requirement.**
- **Do not nest UI Patterns layouts inside UI Patterns layouts deeply** — configuration becomes unwieldy.
- **Do combine UI Patterns layouts (structural) with block_content blocks (content)** for the best experience.

## See Also

- [Inline Editing](inline-editing.md)
- [Custom Block Types](custom-block-types.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
- Reference: [UI Patterns module](https://www.drupal.org/project/ui_patterns)
