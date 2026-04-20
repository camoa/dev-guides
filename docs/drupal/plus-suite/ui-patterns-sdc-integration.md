---
description: UI Patterns and SDC integration with Plus Suite — what works, inline editing limitations, recommended architecture, and hybrid components
tldr: "Use UI Patterns layouts as structural section layouts and block_content for content blocks that need inline editing. Do not use UI Patterns blocks as your primary strategy if inline editing is a requirement."
drupal_version: "11.x"
---

# UI Patterns & SDC Integration

## When to Use

> Use UI Patterns layouts as structural section layouts and block_content for content blocks that need inline editing. Do not use UI Patterns blocks as your primary strategy if inline editing is a requirement.

## Decision

| Factor | UI Patterns Blocks | block_content Blocks |
|--------|--------------------|---------------------|
| Inline editing | No (props don't correlate) | Yes (full Edit+ support) |
| Sample content | Limited (component defaults only) | Full (field_sample_value) |
| Design system consistency | Excellent (SDC components) | Good (with themed templates) |
| Props configuration | Via source plugins (rich) | Via entity fields |

**Recommended split:**

| Use UI Patterns For | Use block_content For |
|---------------------|-----------------------|
| Section layouts (structural) | Content blocks (text, image, CTA) |
| Design system wrapper components | Blocks needing inline editing |
| Components with complex prop logic | Simple field-based content |
| Shared component library | Project-specific content types |

## Pattern

**Why this works:** LB+ is a drop-in UI replacement — `BlockManager::getFilteredDefinitions()` and `LayoutPluginManager` are unchanged, so UI Patterns plugins appear automatically in the sidebar and layout chooser.

**Feature compatibility:**

| Feature | Status |
|---------|--------|
| SDC as Layout Builder blocks | Works |
| SDC as section layouts | Works |
| Props configuration via Configure tool | Works |
| Promoted blocks for UI Patterns blocks | Works — use `ui_patterns:{provider}:{component}` as ID |
| Inline editing (Edit+) on props | Does NOT work — props bypass field rendering |
| Sample content for UI Patterns blocks | Limited — use `*.component.yml` defaults |

**Recommended architecture:**
```
UI Patterns Layout (SDC component as section layout)
  ├── Props: configured via Configure tool
  └── Slots (regions):
      ├── block_content:hero (standard block with inline editing)
      └── block_content:card (standard block with inline editing)
```

**Promoting UI Patterns blocks:**
```yaml
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'ui_patterns:my_theme:alert'
    block_config:
      icon:
        'ui_patterns:my_theme:alert': '/themes/custom/my_theme/assets/block-icons/alert.svg'
```

**Hybrid component** (block_content rendered through SDC — gets both Edit+ and design system):
```php
function my_theme_preprocess_block__inline_block__hero(&$variables) {
  $block = $variables['content']['#block_content'];
  $variables['content'] = [
    '#type' => 'component',
    '#component' => 'my_theme:hero',
    '#props' => ['heading' => $block->field_heading->value],
    '#slots' => ['media' => $block->field_media->view('default')],
  ];
}
```

## Common Mistakes

- **Wrong**: Expecting Edit+ to work on UI Patterns block props → **Right**: Props render through SDC, not field formatters; no correlation exists
- **Wrong**: Using UI Patterns blocks as primary strategy when editors need inline editing → **Right**: Use block_content for inline-editable content, UI Patterns for structural layouts
- **Wrong**: Deeply nesting UI Patterns layouts inside UI Patterns layouts → **Right**: Configuration becomes unwieldy beyond 2 levels

## See Also

- [Inline Editing](inline-editing.md)
- [Custom Block Types](custom-block-types.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
- Reference: [UI Patterns module](https://www.drupal.org/project/ui_patterns)
