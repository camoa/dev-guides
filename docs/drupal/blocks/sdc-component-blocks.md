---
description: Use Single Directory Components (SDC) as blocks — Component Block module and UI Patterns auto-registration
tldr: "Use when exposing Twig SDC components as placeable blocks. Component Block module handles zero-PHP cases."
drupal_version: "11.x"
---

# SDC Component Blocks

## When to Use

> Using Single Directory Components (SDC) as blocks, making Twig components available in the block system.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Component as block without PHP | Component Block contrib module | Zero PHP code, pure Twig components |
| Component with server-side data processing | Custom block plugin rendering component | Full PHP control, inject services |
| Component exposed in Layout Builder | Component Block with Layout Builder | Site builders can add components via UI |
| Component with complex configuration | Block plugin + component render element | More control over configuration form |

## Pattern

**Component Block module approach:**

1. Install module: `composer require drupal/component_block`
2. Create SDC component in `{module}/components/my_component/`
3. Component automatically appears as block plugin
4. Block configuration maps to component props

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

**Reference:** https://www.drupal.org/project/component_block, `core/lib/Drupal/Core/Render/Element/Component.php`

## UI Patterns Auto-Block Registration

When the `ui_patterns_blocks` sub-module is enabled, every SDC component is automatically registered as a block plugin — no custom PHP needed.

**How it works:**
- UI Patterns scans all SDC `component.yml` files at cache rebuild
- Each component becomes a block plugin with ID pattern: `ui_patterns:namespace:component_name`
  - Example: `ui_patterns:ui_suite_daisyui:hero`, `ui_patterns:my_theme:card`
- Props become block configuration form fields (auto-generated from JSON Schema)
- Slots become block regions that accept other blocks
- Config schema follows pattern: `block.settings.ui_patterns:*:*:`

**When to use UI Patterns blocks vs custom block plugins:**

| If you need... | Use... | Why |
|---|---|---|
| Component as block with props exposed to editors | UI Patterns block | Zero PHP, admin form auto-generated from schema |
| Server-side data processing before rendering | Custom block plugin rendering `#type: component` | Full PHP control, service injection |
| Complex configuration beyond component schema | Custom block plugin + component render element | Custom form elements, validation logic |

**Pattern: Placing a UI Patterns block in config**

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

## Common Mistakes

- Not validating component props in block config → Invalid props cause component render errors
- Mixing component logic with block logic → Keep components pure; put business logic in block plugin
- Hardcoding component props when they should be configurable → Use `blockForm()` to expose props
- Not handling missing components gracefully → Check component exists before rendering
- Forgetting component library must be enabled → SDC components require the component's module enabled
- Installing `ui_patterns_blocks` without complete `component.yml` schemas → Missing prop titles/descriptions produce poor auto-generated forms

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- → SDC Development Guide (for component creation)
- → `drupal-ui-patterns.md` — full UI Patterns documentation
- Reference: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
