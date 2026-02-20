---
description: Blocks integration — exposing components as block plugins and embedding blocks in slots
drupal_version: "10.3+ / 11"
---

## Blocks Integration

**Sub-module:** `ui_patterns_blocks`
**Dependencies:** `block`, `ui_patterns`

### What It Does

Exposes every SDC component as a Drupal Block plugin. Each component becomes a derivative of the `ComponentBlock` base plugin, appearing in the block listing under the "UI Patterns" category.

### How It Works

`ComponentBlock` extends `BlockBase` and uses `ComponentFormBuilderTrait`. The deriver creates one block derivative per component:

```
Block: ui_patterns:my_theme:alert
  = Component: my_theme:alert
```

The block form provides the full component configuration form (props + slots):

```php
public function blockForm($form, FormStateInterface $form_state) {
    $form['ui_patterns'] = $this->buildComponentsForm(
        $form_state,
        $this->getComponentSourceContexts($form_state),
        $this->getDerivativeId()
    );
    return $form;
}
```

### Entity Context Resolution

When placed in Layout Builder, the block resolves entity context via `ChainContextEntityResolver`, making entity field sources available in the component form.

### Rendering

The `build()` method creates a standard component render array:

```php
public function build() {
    return [
        'content' => $this->buildComponentRenderable(
            $this->getDerivativeId(),
            $this->getComponentSourceContexts()
        ),
    ];
}
```

### Block Source Plugin

Conversely, UI Patterns core includes a `BlockSource` that allows embedding Drupal blocks **inside** component slots. This is separate from `ui_patterns_blocks` -- it is a source plugin, not a block plugin:

```php
#[Source(
  id: 'block',
  label: new TranslatableMarkup('Block'),
  prop_types: ['slot']
)]
class BlockSource extends DerivableContextSourceBase { ... }
```

The `BlockSource` filters out incompatible blocks (inline_block, system_main_block, page_title_block, layout_builder blocks, ui_patterns_blocks blocks) via `hook_plugin_filter_block__ui_patterns_alter()`.

### Config YAML

Block configuration is stored in `block.block.{block_id}.yml`. After `drush config:export`:

```yaml
# block.block.homepage_hero.yml
langcode: en
status: true
dependencies:
  module:
    - ui_patterns_blocks
  theme:
    - my_theme
id: homepage_hero
theme: my_theme
region: content
weight: 0
provider: null
plugin: 'ui_patterns:ui_suite_daisyui:hero'
settings:
  id: 'ui_patterns:ui_suite_daisyui:hero'
  label: 'Homepage Hero'
  label_display: '0'
  provider: ui_patterns_blocks
  ui_patterns:
    component_id: 'ui_suite_daisyui:hero'
    variant_id:
      source_id: select
      source:
        value: ''
    props:
      heading_level:
        source_id: select
        source:
          value: '1'
      centered:
        source_id: checkbox
        source:
          value: true
      overlay_image:
        source_id: url
        source:
          value: '/themes/my_theme/images/hero-bg.jpg'
    slots:
      title:
        sources:
          - source_id: textfield
            source:
              value: 'Welcome to Our Site'
            _weight: '0'
      text:
        sources:
          - source_id: wysiwyg
            source:
              value:
                value: '<p>Discover our latest content and resources.</p>'
                format: basic_html
            _weight: '0'
      button:
        sources:
          - source_id: component
            source:
              component:
                component_id: 'ui_suite_daisyui:button'
                variant_id:
                  source_id: select
                  source:
                    value: ''
                props:
                  url:
                    source_id: url
                    source:
                      value: '/explore'
                slots:
                  text:
                    sources:
                      - source_id: textfield
                        source:
                          value: 'Get Started'
                        _weight: '0'
            _weight: '0'
visibility: {}
```

Key observations:
- The `plugin` ID uses the format `ui_patterns:{provider}:{component}`.
- `settings.ui_patterns` follows the `ui_patterns_component` schema, matching `block.settings.ui_patterns:*:*`.
- Widget sources store values directly: `textfield` stores `value` as a string, `wysiwyg` stores `value` as a `text_format` mapping with `value` + `format`, `checkbox` stores `value` as a boolean.
- Nested components in slots use the `component` source, which recursively contains another full `ui_patterns_component` structure.
- The `_weight` property on slot sources controls rendering order.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Confusing `ui_patterns_blocks` with the `block` source plugin | `ui_patterns_blocks` makes components available *as* blocks. The `block` source plugin makes blocks available *inside* component slots. They are complementary, not the same thing. |
| Placing UI Patterns blocks inside UI Patterns layouts recursively without care | While nesting is supported, deep recursion of components-as-blocks within components-as-layouts can cause performance issues and confusing configuration. |

### See Also

- [Layout Builder Integration](#layout-builder-integration)
- [Slots System](#slots-system)
- Drupal Blocks Guide