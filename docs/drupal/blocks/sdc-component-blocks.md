---
description: Use Single Directory Components (SDC) as blocks — Component Block module and UI Patterns auto-registration
drupal_version: "11.x"
---

# SDC Component Blocks

## When to Use

> Use when exposing Twig SDC components as placeable blocks. Component Block module handles zero-PHP cases. UI Patterns auto-registers all SDC components as blocks when `ui_patterns_blocks` sub-module is enabled.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Component as block without PHP | Component Block contrib module | Zero PHP code, pure Twig components |
| Component with server-side data processing | Custom block plugin rendering component | Full PHP control, inject services |
| Component exposed in Layout Builder | Component Block with Layout Builder | Site builders can add components via UI |
| Component with complex configuration | Block plugin + component render element | More control over configuration form |
| Component as block with props exposed to editors | UI Patterns block (`ui_patterns_blocks`) | Zero PHP, admin form auto-generated from schema |

## Pattern

**Using component in custom block plugin:**

```php
#[Block(
  id: "component_demo",
  admin_label: new TranslatableMarkup("Component Demo"),
)]
class ComponentDemoBlock extends BlockBase {

  public function build() {
    return [
      '#type' => 'component',
      '#component' => 'mymodule:my_component',
      '#props' => [
        'title' => $this->configuration['title'] ?? 'Default Title',
        'description' => 'Dynamic content from block',
      ],
      '#slots' => [
        'default' => ['#markup' => 'Slot content'],
      ],
    ];
  }

  public function defaultConfiguration() {
    return ['title' => 'Default Title'] + parent::defaultConfiguration();
  }

  public function blockForm($form, FormStateInterface $form_state) {
    $form['title'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Component Title'),
      '#default_value' => $this->configuration['title'],
    ];
    return $form;
  }

  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->configuration['title'] = $form_state->getValue('title');
  }
}
```

**Component structure (my_component/my_component.component.yml):**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/modules/sdc/src/metadata.schema.json
name: My Component
status: stable
props:
  type: object
  properties:
    title:
      type: string
      title: Title
    description:
      type: string
      title: Description
  required: [title]
slots:
  default:
    title: Content
```

**Component Block module approach:**
1. Install module: `composer require drupal/component_block`
2. Create SDC component in `{module}/components/my_component/`
3. Component automatically appears as block plugin
4. Block configuration maps to component props

**UI Patterns auto-block registration:**

When `ui_patterns_blocks` sub-module is enabled, every SDC component is automatically registered as a block plugin — no custom PHP needed.

- Plugin ID pattern: `ui_patterns:namespace:component_name`
  - Example: `ui_patterns:ui_suite_daisyui:hero`, `ui_patterns:my_theme:card`
- Props become block configuration form fields (auto-generated from JSON Schema)
- Slots become block regions that accept other blocks

**Placing a UI Patterns block in config:**
```yaml
# block.block.ui_patterns_hero.yml
plugin: 'ui_patterns:my_theme:hero'
settings:
  title: 'Welcome'
  variant: 'primary'
  label: 'Hero Block'
  label_display: '0'
  provider: ui_patterns
```

**Reference:** https://www.drupal.org/project/component_block, `core/lib/Drupal/Core/Render/Element/Component.php`

## Common Mistakes

- **Wrong**: Not validating component props in block config → **Right**: Invalid props cause component render errors
- **Wrong**: Mixing component logic with block logic → **Right**: Keep components pure; put business logic in block plugin
- **Wrong**: Hardcoding component props when they should be configurable → **Right**: Use `blockForm()` to expose props
- **Wrong**: Not handling missing components gracefully → **Right**: Check component exists before rendering
- **Wrong**: Forgetting component library must be enabled → **Right**: SDC components require the component's module enabled
- **Wrong**: Installing `ui_patterns_blocks` without complete `component.yml` schemas → **Right**: Missing prop titles/descriptions produce poor auto-generated forms

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- Reference: `drupal-ui-patterns.md` — full UI Patterns documentation
- Reference: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
