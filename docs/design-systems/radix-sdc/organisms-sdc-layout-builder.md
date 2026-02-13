---
description: You've identified organisms using the Design System Recognition Guide
drupal_version: "11.x"
---

## 5. Organisms → SDC + Layout Builder

### When to Use This Section
- You've identified organisms using the Design System Recognition Guide
- You're building complex sections like navbars, heroes, card grids
- You need to integrate organisms with Layout Builder

### 5.1 Navigation Organisms

#### Pattern: Navbar Organism

**Radix provides:** `radix/components/navbar/` with Bootstrap navbar integration

**When to customize:**
- Brand-specific navigation structure
- Custom menu patterns
- Integration with Drupal menu system

**File: `components/site-navbar/site-navbar.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
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

  {# Custom actions slot #}
  <div class="navbar-actions">
    {{ slots.actions }}
  </div>
{% endembed %}
```

**File: `components/site-navbar/site-navbar.scss`**
```scss
@import '../../src/scss/init';

.navbar-actions {
  display: flex;
  align-items: center;
  gap: $spacer;

  @include media-breakpoint-down(lg) {
    flex-direction: column;
    width: 100%;
  }
}
```

**Template Integration: `templates/layout/page.html.twig`**
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

#### Common Mistakes
- **Not using Radix navbar base** — Extend existing Radix navbar component
- **Hardcoding menu structure** — Use Drupal menu system
- **Missing responsive behavior** — Use Bootstrap navbar collapse
- **Not integrating with regions** — Map Drupal regions to navbar slots

#### See Also
- [8.3 Overriding Radix Components](#83-overriding-radix-components)
- [6.1 Page Template Structure](#61-page-template-structure)

---

### 5.2 Hero and Feature Organisms

#### Pattern: Hero Section Organism

**File: `components/hero-section/hero-section.component.yml`**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/10.1.x/core/modules/sdc/src/metadata.schema.json
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

**File: `components/hero-section/hero-section.scss`**
```scss
@import '../../src/scss/init';

.hero-section {
  background-size: cover;
  background-position: center;
  min-height: 500px;
  display: flex;
  align-items: center;

  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: $dark;
  }

  &__heading {
    font-weight: $font-weight-bold;
  }

  &__actions {
    display: flex;
    gap: $spacer;
    justify-content: center;
    flex-wrap: wrap;
  }
}
```

#### Common Mistakes
- **Not using Bootstrap grid** — Use `.container`, `.row`, `.col-*` classes
- **Hardcoding spacing** — Use Bootstrap spacing utilities
- **Missing responsive behavior** — Test on mobile
- **Not using design tokens** — Reference SCSS variables

#### See Also
- [5.3 Layout Builder Integration](#53-layout-builder-integration)
- Bootstrap Mapping Guide: Section 6 (Organisms → Layout + Components)

---

### 5.3 Layout Builder Integration

#### Pattern: Organism as Layout Builder Block

**Step 1: Create Block Plugin** (in custom module or theme)

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

**Step 2: Configure Block in Layout Builder**

1. Enable Layout Builder for content type
2. Add block to layout region
3. Configure block settings (heading, image, etc.)
4. SDC organism renders with configured props

#### Decision Table: Layout Builder Integration

| Organism Type | Integration Method | Example |
|---------------|-------------------|---------|
| **Header/Footer** | Template override | Page template includes organism |
| **Hero Section** | Layout Builder block | Block plugin renders SDC |
| **Card Grid** | Views + template | Views template includes card molecules |
| **Feature Section** | Layout Builder block | Block plugin with configurable SDC |

#### Common Mistakes
- **Not using `#type => 'component'`** — Drupal's SDC render element
- **Hardcoding props** — Make configurable via block form
- **Not enabling Layout Builder** — Required for block placement
- **Missing cache tags** — Add proper cache metadata

#### See Also
- [6.2 Layout Builder Composition](#62-layout-builder-composition)
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder