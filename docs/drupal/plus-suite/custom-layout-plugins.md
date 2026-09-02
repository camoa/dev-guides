---
description: Custom Layout plugins for Plus Suite — YAML vs PHP class, icon_map, configurable layouts with Configure tool, and nested layout design
tldr: "Create custom layout plugins when core's basic one/two/three column layouts don't match your design system's grid. YAML covers most cases; use PHP class only when per-section configuration is needed."
drupal_version: "11.x"
---

# Custom Layout Plugins

## When to Use

> When you need section layouts that match your design system's grid (e.g., custom column ratios, asymmetric layouts, full-bleed sections) rather than core's basic one/two/three column layouts.

## How Layout Plugins Work in Plus Suite

Plus Suite uses standard Drupal Layout plugins (same as core Layout Builder). The Layout tool presents all available layouts when changing a section. Custom layout plugins appear automatically.

## Creating a Custom Layout Plugin

### Option 1: YAML-defined layout (simplest)

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

my_theme_sidebar_right:
  label: 'Content + Sidebar'
  category: 'My Theme'
  template: layouts/sidebar-right
  icon_map:
    - [content, content, sidebar]
  regions:
    content:
      label: Content
    sidebar:
      label: Sidebar

my_theme_three_unequal:
  label: 'Wide Center (25/50/25)'
  category: 'My Theme'
  template: layouts/three-unequal
  icon_map:
    - [left, center, center, right]
  regions:
    left:
      label: Left
    center:
      label: Center
    right:
      label: Right

my_theme_full_bleed:
  label: 'Full Bleed'
  category: 'My Theme'
  template: layouts/full-bleed
  icon_map:
    - [content]
  regions:
    content:
      label: Content
```

**Template files:**

```twig
{# templates/layouts/hero-layout.html.twig #}
{%
  set classes = [
    'layout',
    'layout--hero',
  ]
%}
{% if content %}
<div{{ attributes.addClass(classes) }}>
  <div class="layout__region layout__region--media">
    {{ content.media }}
  </div>
  <div class="layout__region layout__region--content">
    {{ content.content }}
  </div>
  <div class="layout__region layout__region--cta">
    {{ content.cta }}
  </div>
</div>
{% endif %}
```

### Option 2: PHP class layout (configurable)

```php
namespace Drupal\my_theme\Plugin\Layout;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Layout\Attribute\Layout;
use Drupal\Core\Layout\LayoutDefault;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Layout(
  id: 'my_theme_configurable_hero',
  label: new TranslatableMarkup('Configurable Hero'),
  category: new TranslatableMarkup('My Theme'),
  template: 'layouts/configurable-hero',
  regions: [
    'media' => ['label' => new TranslatableMarkup('Media')],
    'content' => ['label' => new TranslatableMarkup('Content')],
    'cta' => ['label' => new TranslatableMarkup('CTA')],
  ],
)]
class ConfigurableHero extends LayoutDefault {

  public function defaultConfiguration(): array {
    return parent::defaultConfiguration() + [
      'height' => 'medium',
      'overlay' => 'none',
    ];
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form = parent::buildConfigurationForm($form, $form_state);

    $form['height'] = [
      '#type' => 'select',
      '#title' => $this->t('Section Height'),
      '#options' => [
        'small' => $this->t('Small (300px)'),
        'medium' => $this->t('Medium (500px)'),
        'large' => $this->t('Large (80vh)'),
        'full' => $this->t('Full Screen (100vh)'),
      ],
      '#default_value' => $this->configuration['height'],
    ];

    $form['overlay'] = [
      '#type' => 'select',
      '#title' => $this->t('Content Overlay'),
      '#options' => [
        'none' => $this->t('None'),
        'light' => $this->t('Light overlay'),
        'dark' => $this->t('Dark overlay'),
        'gradient' => $this->t('Gradient'),
      ],
      '#default_value' => $this->configuration['overlay'],
    ];

    return $form;
  }

  public function submitConfigurationForm(array &$form, FormStateInterface $form_state): void {
    parent::submitConfigurationForm($form, $form_state);
    $this->configuration['height'] = $form_state->getValue('height');
    $this->configuration['overlay'] = $form_state->getValue('overlay');
  }

  public function build(array $regions): array {
    $build = parent::build($regions);
    $build['#attributes']['class'][] = 'hero--height-' . $this->configuration['height'];
    $build['#attributes']['class'][] = 'hero--overlay-' . $this->configuration['overlay'];
    return $build;
  }
}
```

## LB+ Configure Tool Integration

When a section uses a configurable layout plugin (PHP class with `buildConfigurationForm()`), the Configure tool (`o` hotkey) opens the layout's configuration form in a dialog. No extra integration needed — LB+ handles this automatically.

## Default Section Configuration

You can set your custom layout as the default for new sections:

```yaml
# Via entity_view_display third-party settings
third_party_settings:
  lb_plus:
    default_section:
      layout_plugin: my_theme_hero_layout
      config: {}
```

Or configure via **Structure → Content Types → Manage Display → LB+ Default Section**.

## Layout Icons (icon_map)

The `icon_map` in YAML layouts defines the visual preview shown in the Layout tool's chooser:

```yaml
# Equal three-column
icon_map:
  - [left, center, right]

# Two rows: full-width header + two columns
icon_map:
  - [header, header]
  - [left, right]

# 25/50/25 split
icon_map:
  - [left, center, center, right]
```

## Decision: YAML vs PHP Layout

| Use YAML When | Use PHP Class When |
|---|---|
| Static layouts with fixed regions | Configurable options (height, overlay, color) |
| Simple column arrangements | Dynamic region count |
| No per-instance customization needed | Settings form in Configure tool |
| Quick iteration during design | Complex rendering logic |

## Layouts for Nested Layout Blocks

Layout blocks use the same layout plugins. Design layouts specifically for nesting:

```yaml
# Designed for use inside layout blocks
my_theme_card_layout:
  label: 'Card Layout'
  category: 'My Theme - Nested'
  template: layouts/card-layout
  icon_map:
    - [image]
    - [body]
    - [footer]
  regions:
    image:
      label: Image
    body:
      label: Body
    footer:
      label: Footer
```

## Common Mistakes

- **Do not create too many layout variations** — 5-10 covers most design systems.
- **Do not put business logic in layout templates** — keep them structural.
- **Do not forget `icon_map`** — without it, the Layout tool shows a generic preview.
- **Do not create layouts with more than 4-5 regions** — it becomes unusable in Edit Mode.

## See Also

- [Nested Layouts](nested-layouts.md)
- [Custom Design System Integration](custom-design-system.md)
- Reference: `core/lib/Drupal/Core/Layout/LayoutDefault.php`
