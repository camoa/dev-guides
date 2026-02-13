---
description: Organism SDC components with Layout Builder integration — navigation organisms, hero sections, Layout Builder blocks
drupal_version: "11.x"
---

# Organisms SDC + Layout Builder

## When to Use

> Use this when building complex sections like navbars, heroes, or card grids, and when integrating organisms with Layout Builder.

## Decision

| Organism Type | Integration Method | Example |
|---------------|-------------------|---------|
| **Header/Footer** | Template override | Page template includes organism |
| **Hero Section** | Layout Builder block | Block plugin renders SDC |
| **Card Grid** | Views + template | Views template includes card molecules |
| **Feature Section** | Layout Builder block | Block plugin with configurable SDC |

## Pattern

**Navigation Organism (Navbar):**

**File: `components/site-navbar/site-navbar.component.yml`**

```yaml
name: Site Navbar
status: stable
description: Site navigation organism
props:
  type: object
  properties:
    navbar_theme:
      type: string
      default: 'dark'
      enum: ['light', 'dark']
    placement:
      type: string
      default: 'sticky-top'
slots:
  branding:
    title: Branding
    description: Logo and site name
  navigation:
    title: Navigation
    description: Main navigation menu
  actions:
    title: Actions
    description: User menu, search, etc.
```

**File: `components/site-navbar/site-navbar.twig`**

```twig
{% embed 'radix:navbar' with {
  navbar_theme: navbar_theme,
  placement: placement,
  navbar_expand: 'lg',
} %}
  {% block branding %}
    {{ slots.branding }}
  {% endblock %}

  {% block navigation %}
    {{ slots.navigation }}
  {% endblock %}

  <div class="navbar-actions">
    {{ slots.actions }}
  </div>
{% endembed %}
```

**Template Integration (`templates/layout/page.html.twig`):**

```twig
{% include 'THEME_NAME:site-navbar' with {
  navbar_theme: 'dark',
  slots: {
    branding: navbar_branding,
    navigation: navbar_left,
    actions: navbar_right,
  }
} %}
```

**Hero Section Organism:**

**File: `components/hero-section/hero-section.component.yml`**

```yaml
name: Hero Section
status: stable
description: Hero section with heading, text, and CTA buttons
props:
  type: object
  properties:
    heading:
      type: string
      title: Heading
    heading_tag:
      type: string
      default: 'h1'
      enum: ['h1', 'h2']
    subheading:
      type: string
      title: Subheading
    background_image:
      type: string
      title: Background Image URL
    overlay_opacity:
      type: string
      default: '0.5'
      title: Overlay Opacity
slots:
  cta_buttons:
    title: CTA Buttons
    description: Call-to-action buttons
```

**File: `components/hero-section/hero-section.twig`**

```twig
{%
  set hero_classes = [
    'hero-section',
    'position-relative',
    'text-white',
    'py-5',
  ]
%}

<section {{ attributes.addClass(hero_classes) }} {% if background_image %}style="background-image: url('{{ background_image }}');"{% endif %}>
  <div class="hero-section__overlay" style="opacity: {{ overlay_opacity }};"></div>

  <div class="container position-relative">
    <div class="row justify-content-center text-center">
      <div class="col-lg-8">
        {% if heading %}
          <{{ heading_tag }} class="hero-section__heading display-3 mb-3">
            {{ heading }}
          </{{ heading_tag }}>
        {% endif %}

        {% if subheading %}
          <p class="hero-section__subheading lead mb-4">{{ subheading }}</p>
        {% endif %}

        {% if slots.cta_buttons %}
          <div class="hero-section__actions">
            {{ slots.cta_buttons }}
          </div>
        {% endif %}
      </div>
    </div>
  </div>
</section>
```

**Layout Builder Integration (Block Plugin):**

**File: `src/Plugin/Block/HeroSectionBlock.php`**

```php
<?php

namespace Drupal\THEME_NAME\Plugin\Block;

use Drupal\Core\Block\BlockBase;

/**
 * Provides a 'Hero Section' block.
 *
 * @Block(
 *   id = "hero_section_block",
 *   admin_label = @Translation("Hero Section"),
 *   category = @Translation("Custom")
 * )
 */
class HeroSectionBlock extends BlockBase {

  public function build() {
    return [
      '#type' => 'component',
      '#component' => 'THEME_NAME:hero-section',
      '#props' => [
        'heading' => $this->configuration['heading'] ?? '',
        'subheading' => $this->configuration['subheading'] ?? '',
        'background_image' => $this->configuration['background_image'] ?? '',
      ],
      '#slots' => [
        'cta_buttons' => [
          // Render buttons here
        ],
      ],
    ];
  }
}
```

**Configuration Steps:**

1. Enable Layout Builder for content type
2. Add block to layout region
3. Configure block settings (heading, image, etc.)
4. SDC organism renders with configured props

## Common Mistakes

- **Wrong**: Not using Radix navbar base → **Right**: Extend existing Radix navbar component
- **Wrong**: Hardcoding menu structure → **Right**: Use Drupal menu system
- **Wrong**: Missing responsive behavior → **Right**: Use Bootstrap navbar collapse
- **Wrong**: Not integrating with regions → **Right**: Map Drupal regions to navbar slots
- **Wrong**: Not using Bootstrap grid → **Right**: Use `.container`, `.row`, `.col-*` classes
- **Wrong**: Hardcoding spacing → **Right**: Use Bootstrap spacing utilities
- **Wrong**: Missing responsive behavior → **Right**: Test on mobile
- **Wrong**: Not using `#type => 'component'` → **Right**: Drupal's SDC render element
- **Wrong**: Hardcoding props in block → **Right**: Make configurable via block form
- **Wrong**: Missing cache tags → **Right**: Add proper cache metadata

## See Also

- [Molecules SDC Components](molecules-sdc-components.md)
- [Templates Drupal Theme Layer](templates-drupal-theme-layer.md)
- [Layout Builder Best Practices](layout-builder-best-practices.md)
- [Radix Component Reuse Strategy](radix-component-reuse-strategy.md)
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder
