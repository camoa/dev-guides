---
description: Custom Layout plugins for Plus Suite — YAML vs PHP class, icon_map, configurable layouts with Configure tool, and nested layout design
drupal_version: "11.x"
---

# Custom Layout Plugins

## When to Use

> Create custom layout plugins when core's basic one/two/three column layouts don't match your design system's grid. YAML covers most cases; use PHP class only when per-section configuration is needed.

## Decision

| Use YAML When | Use PHP Class When |
|---------------|-------------------|
| Static layouts with fixed regions | Configurable options (height, overlay, color) |
| Simple column arrangements | Dynamic region count |
| No per-instance customization needed | Settings form in Configure tool |
| Quick iteration during design | Complex rendering logic |

## Pattern

**YAML-defined layout (simplest):**

```yaml
# my_theme.layouts.yml
my_theme_hero_layout:
  label: 'Hero Layout'
  category: 'My Theme'
  template: layouts/hero-layout
  icon_map:
    - [media]
    - [content]
    - [cta]
  regions:
    media:
      label: Media
    content:
      label: Content
    cta:
      label: Call to Action
```

**Template:**
```twig
{# templates/layouts/hero-layout.html.twig #}
{% if content %}
<div{{ attributes.addClass('layout', 'layout--hero') }}>
  <div class="layout__region layout__region--media">{{ content.media }}</div>
  <div class="layout__region layout__region--content">{{ content.content }}</div>
  <div class="layout__region layout__region--cta">{{ content.cta }}</div>
</div>
{% endif %}
```

**PHP class layout (configurable):**

```php
#[Layout(
  id: 'my_theme_configurable_hero',
  label: new TranslatableMarkup('Configurable Hero'),
  template: 'layouts/configurable-hero',
  regions: [
    'media' => ['label' => new TranslatableMarkup('Media')],
    'content' => ['label' => new TranslatableMarkup('Content')],
  ],
)]
class ConfigurableHero extends LayoutDefault {

  public function defaultConfiguration(): array {
    return parent::defaultConfiguration() + ['height' => 'medium'];
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form = parent::buildConfigurationForm($form, $form_state);
    $form['height'] = [
      '#type' => 'select',
      '#title' => $this->t('Section Height'),
      '#options' => ['small' => 'Small', 'medium' => 'Medium', 'large' => 'Large'],
      '#default_value' => $this->configuration['height'],
    ];
    return $form;
  }

  public function build(array $regions): array {
    $build = parent::build($regions);
    $build['#attributes']['class'][] = 'hero--height-' . $this->configuration['height'];
    return $build;
  }
}
```

**LB+ Configure tool** (hotkey `o`) automatically opens `buildConfigurationForm()` for configurable layouts — no extra integration needed.

**Default section for content type:**
```yaml
third_party_settings:
  lb_plus:
    default_section:
      layout_plugin: my_theme_hero_layout
```

**`icon_map` examples:**
```yaml
# Equal three-column
icon_map:
  - [left, center, right]

# 25/50/25 split
icon_map:
  - [left, center, center, right]
```

## Common Mistakes

- **Wrong**: Creating more than 10 layout variations → **Right**: 5–8 layouts covers most design systems; more creates decision paralysis
- **Wrong**: Forgetting `icon_map` → **Right**: Without it, the Layout tool shows a generic preview making layouts indistinguishable
- **Wrong**: Creating layouts with 5+ regions → **Right**: More than 4 regions becomes unusable in Edit Mode; use nested layouts for complex structures

## See Also

- [Nested Layouts](nested-layouts.md)
- [Custom Design System Integration](custom-design-system.md)
- Reference: `web/core/modules/layout_discovery/src/Plugin/Layout/LayoutDefault.php`
