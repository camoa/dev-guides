---
description: Creating custom render element plugins and form element plugins with proper plugin structure and pre-render callbacks.
---

# Custom Render Elements

## When to Use

When you have complex rendering logic that you reuse across multiple places -- voting widgets, custom table formatters, specialized containers, elements with default behaviors.

## Steps: Creating a Render Element Plugin

**1. Create the plugin class**

```php
namespace Drupal\mymodule\Plugin\Element;

use Drupal\Core\Render\Attribute\RenderElement;
use Drupal\Core\Render\Element\RenderElementBase;

/**
 * Provides an alert box render element.
 *
 * Properties:
 * - #alert_type: Alert type (success, warning, error, info). Default: 'info'.
 * - #message: Alert message text.
 * - #dismissible: Whether alert can be dismissed. Default: FALSE.
 *
 * Usage:
 * @code
 * $build['alert'] = [
 *   '#type' => 'alert_box',
 *   '#alert_type' => 'success',
 *   '#message' => $this->t('Operation completed successfully.'),
 *   '#dismissible' => TRUE,
 * ];
 * @endcode
 */
#[RenderElement('alert_box')]
class AlertBox extends RenderElementBase {

  /**
   * {@inheritdoc}
   */
  public function getInfo() {
    return [
      '#alert_type' => 'info',
      '#message' => '',
      '#dismissible' => FALSE,
      '#pre_render' => [
        [static::class, 'preRenderAlertBox'],
      ],
      '#theme_wrappers' => ['container'],
    ];
  }

  /**
   * Pre-render callback: Build the alert box markup.
   */
  public static function preRenderAlertBox($element) {
    $type = $element['#alert_type'];
    $dismissible_class = $element['#dismissible'] ? ' alert-dismissible' : '';

    $element['#attributes']['class'][] = 'alert';
    $element['#attributes']['class'][] = 'alert-' . $type . $dismissible_class;
    $element['#attributes']['role'] = 'alert';

    $element['message'] = [
      '#markup' => $element['#message'],
    ];

    if ($element['#dismissible']) {
      $element['close'] = [
        '#type' => 'html_tag',
        '#tag' => 'button',
        '#value' => 'x',
        '#attributes' => [
          'type' => 'button',
          'class' => ['close'],
          'data-dismiss' => 'alert',
          'aria-label' => t('Close'),
        ],
      ];
      $element['#attached']['library'][] = 'mymodule/alert-dismissible';
    }

    return $element;
  }

}
```

**2. Clear cache**

```bash
drush cr
```

**3. Use the element**

```php
$build['success_message'] = [
  '#type' => 'alert_box',
  '#alert_type' => 'success',
  '#message' => $this->t('Your changes have been saved.'),
  '#dismissible' => TRUE,
];
```

**Reference:** `core/lib/Drupal/Core/Render/Element/Link.php` -- real-world example

## Pattern: Form Element Plugin

For elements that work inside forms:

```php
namespace Drupal\mymodule\Plugin\Element;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Render\Attribute\FormElement;
use Drupal\Core\Render\Element\FormElementBase;

#[FormElement('color_picker')]
class ColorPicker extends FormElementBase {

  public function getInfo() {
    return [
      '#input' => TRUE,
      '#default_value' => '#000000',
      '#process' => [[static::class, 'processColorPicker']],
      '#element_validate' => [[static::class, 'validateColorPicker']],
      '#theme_wrappers' => ['form_element'],
    ];
  }

  public static function processColorPicker(&$element, FormStateInterface $form_state, &$complete_form) {
    $element['#attributes']['type'] = 'color';
    $element['#attributes']['class'][] = 'color-picker';
    $element['#attached']['library'][] = 'mymodule/color-picker';

    return $element;
  }

  public static function validateColorPicker(&$element, FormStateInterface $form_state, &$complete_form) {
    $value = $element['#value'];
    if (!preg_match('/^#[0-9A-Fa-f]{6}$/', $value)) {
      $form_state->setError($element, t('Invalid color format. Use #RRGGBB.'));
    }
  }

}
```

**Reference:** `core/lib/Drupal/Core/Render/Element/FormElementBase.php`

## Decision: Render Element vs Theme Hook

| Use Render Element Plugin When... | Use Theme Hook When... |
|---|---|
| Logic is complex and reusable | Presentation is primary concern |
| Default properties/behaviors needed | Simple variable -> template mapping |
| Element needs pre-render processing | No special processing needed |
| Want plugin alterability | Theme-level alterability sufficient |

## Common Mistakes

- **Not clearing cache after creating plugin** -- Plugin not discovered
- **Forgetting `#[RenderElement('element_type')]` attribute** -- Plugin not registered
- **Not extending `RenderElementBase` or `FormElementBase`** -- Missing required methods
- **Using underscores in element type name** -- Convention is hyphens or no separator
- **Not documenting properties in class docblock** -- Users don't know what's available
- **Overcomplicating simple theming needs** -- Theme hook might be simpler

## See Also

- [Core Render Elements](core-render-elements.md) for built-in examples
- Reference: [What Are Render Elements?](https://www.drupal.org/docs/drupal-apis/render-api/render-elements/what-are-render-elements)
- Reference: `core/lib/Drupal/Core/Render/ElementInfoManager.php` -- plugin manager
