---
description: End-to-end component creation in Plus Suite — complete 9-step walkthrough creating a Testimonial block with all features integrated
tldr: "Follow this walkthrough when creating any new Plus Suite component from scratch. Use the checklist at the end to verify completeness."
drupal_version: "11.x"
---

# End-to-End Component Creation

## When to Use

> When you need a complete walkthrough of creating a new page-building component from scratch, integrating all Plus Suite features.

## Example: Creating a "Testimonial" Component

This walkthrough creates a complete Testimonial block that works with all Plus Suite features.

## Step 1: Create Block Content Type

**Admin UI**: Structure → Block Types → Add custom block type

| Field | Machine Name | Type | Settings |
|---|---|---|---|
| Quote | `field_quote` | Text (formatted, long) | Required, full_html |
| Author | `field_author` | Text (plain) | Required |
| Author Title | `field_author_title` | Text (plain) | Optional |
| Author Photo | `field_author_photo` | Entity reference (media) | Image bundle |
| Rating | `field_rating` | List (integer) | 1-5 stars |

## Step 2: Create View Display

**Manage Display** for block_content:testimonial:

- Use "Default" view mode
- Configure field formatters and label visibility
- Enable Layout Builder if the testimonial needs internal layout flexibility

## Step 3: Configure Sample Values

Per field on **Manage Fields → [Field] → Edit**:

| Field | Generator | Config |
|---|---|---|
| Quote | `random_text` | count: 1, format: full_html |
| Author | `default` | Core generates name |
| Author Title | Custom `branded_headline` | Generates job titles |
| Author Photo | `entity_reference` | Selects random image media |
| Rating | `default` | Random 1-5 |

## Step 4: Create Event Subscriber Module

```yaml
# my_theme_plus.info.yml
name: 'My Theme Plus Suite Integration'
type: module
description: 'Design system integration for Plus Suite.'
core_version_requirement: ^11.3
dependencies:
  - lb_plus:lb_plus
  - edit_plus:edit_plus
  - field_sample_value:field_sample_value
```

```yaml
# my_theme_plus.services.yml
services:
  my_theme_plus.testimonial_properties:
    class: Drupal\my_theme_plus\EventSubscriber\TestimonialProperties
    tags:
      - { name: event_subscriber }
```

```php
// src/EventSubscriber/TestimonialProperties.php
namespace Drupal\my_theme_plus\EventSubscriber;

use Drupal\edit_plus\Event\BlockPropertiesEvent;
use Drupal\lb_plus\Event\PlaceBlockEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class TestimonialProperties implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PlaceBlockEvent::class => 'onPlaceBlock',
      BlockPropertiesEvent::class => 'onBlockProperties',
    ];
  }

  public function onPlaceBlock(PlaceBlockEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block || $block->bundle() !== 'testimonial') {
      return;
    }
    // Set default rating to 5 stars.
    $block->set('field_rating', 5);
  }

  public function onBlockProperties(BlockPropertiesEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block || $block->bundle() !== 'testimonial') {
      return;
    }

    $config = $event->getInlineBlockConfiguration();

    $event->addBlockProperty([
      '#type' => 'select',
      '#title' => t('Style'),
      '#options' => [
        'card' => t('Card'),
        'quote' => t('Large Quote'),
        'minimal' => t('Minimal'),
      ],
      '#default_value' => $config['testimonial_style'] ?? 'card',
      '#attributes' => ['data-auto-submit' => 'true'],
    ]);

    $event->addBlockProperty([
      '#type' => 'checkbox',
      '#title' => t('Show star rating'),
      '#default_value' => $config['show_rating'] ?? TRUE,
      '#attributes' => ['data-auto-submit' => 'true'],
    ]);
  }
}
```

## Step 5: Create Promoted Block Icon

Create `my_theme/assets/block-icons/testimonial.svg` (40x40px):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" fill="none">
  <rect width="40" height="40" rx="4" fill="#f0f0f0"/>
  <path d="M10 14l4-6h4l-3 6h3v8h-8v-8zm12 0l4-6h4l-3 6h3v8h-8v-8z" fill="#666"/>
</svg>
```

## Step 6: Configure Promoted Blocks

Via admin UI or config export:

```yaml
# On the entity_view_display for your content type
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'inline_block:testimonial'
    block_config:
      icon:
        'inline_block:testimonial': '/themes/custom/my_theme/assets/block-icons/testimonial.svg'
```

## Step 7: Configure Edit+ Field Settings

Per field, set third-party settings:

| Field | Edit+ Disable | Edit+ Handle |
|---|---|---|
| Quote | false | form_item (uses inline_textarea/CKEditor) |
| Author | false | form_item |
| Author Title | false | form_item |
| Author Photo | false | wrapper |
| Rating | false | form_item |

## Step 8: Create Block Template

```twig
{# block--inline-block--testimonial.html.twig #}
{% set style = configuration.testimonial_style|default('card') %}
{% set show_rating = configuration.show_rating|default(true) %}

<div{{ attributes.addClass('testimonial', 'testimonial--' ~ style) }}>
  {% if content.field_author_photo|render %}
    <div class="testimonial__photo">
      {{ content.field_author_photo }}
    </div>
  {% endif %}

  <blockquote class="testimonial__quote">
    {{ content.field_quote }}
  </blockquote>

  <div class="testimonial__attribution">
    <cite class="testimonial__author">{{ content.field_author }}</cite>
    {% if content.field_author_title|render %}
      <span class="testimonial__title">{{ content.field_author_title }}</span>
    {% endif %}
  </div>

  {% if show_rating and content.field_rating|render %}
    <div class="testimonial__rating">
      {{ content.field_rating }}
    </div>
  {% endif %}
</div>
```

## Step 9: Add Theme CSS

```scss
// _testimonial.scss
.testimonial {
  padding: var(--spacing-lg);
  border-radius: var(--border-radius);

  &--card {
    background: var(--color-surface);
    box-shadow: var(--shadow-sm);
  }

  &--quote {
    text-align: center;
    font-size: var(--font-size-xl);
  }

  &--minimal {
    border-left: 3px solid var(--color-primary);
    padding-left: var(--spacing-md);
  }
}
```

## Component Checklist

When creating any new Plus Suite component, ensure:

- [ ] Block content type created with appropriate fields
- [ ] Sample value generators configured for all fields
- [ ] Block promoted with custom SVG icon
- [ ] Event subscriber for PlaceBlockEvent (defaults) and BlockPropertiesEvent (design options)
- [ ] Edit+ handle types configured per field
- [ ] Block template created with design variant support
- [ ] CSS styles cover all design variants
- [ ] Block appears in correct category in "Other" tab
- [ ] Inline editing works for all editable fields
- [ ] Sample content appears on first placement
- [ ] Design options (block properties) update preview immediately

## Decision: Which Features to Implement

| Feature | Required? | Effort |
|---|---|---|
| Block content type + fields | Yes | Low |
| Sample value generators | Yes (for good UX) | Low |
| Promoted block + icon | Recommended | Low |
| Block properties | Optional | Medium |
| Custom template | Recommended | Low |
| Custom sample value plugin | Optional (for branded content) | Medium |
| Layout plugin (for sections) | Optional | Medium |
| Custom tool plugin | Rare | High |

## Common Mistakes

- **Do not skip sample value generators** — empty blocks on placement defeat the purpose of Plus Suite.
- **Do not create block properties without `data-auto-submit`** — users expect instant preview.
- **Do not forget to test inline editing on every field before shipping.**
- **Do not use complex validation on fields that will be edited inline** — use simple constraints.

## See Also

- [Custom Block Types](custom-block-types.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Design System Integration](custom-design-system.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
