---
description: Programmatically extending Layout Builder Styles — event subscribers, template suggestions, role-based restrictions, and style entity manipulation.
---

## 11.4. Extending Layout Builder Styles

### When to Use

When you need to programmatically alter which styles are available, modify CSS classes before rendering, or integrate custom logic into the style selection process.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Alter styles before rendering | Event subscriber on `SECTION_COMPONENT_BUILD_RENDER_ARRAY` | Modify `$build['#attributes']['class']` array |
| Restrict styles by user role | Custom event subscriber checking permissions | Check `\Drupal::currentUser()->hasPermission()` before adding style |
| Add context-aware classes | Event subscriber checking node type or view mode | `$event->getComponent()->getEntity()` for context |
| Custom template suggestions | `hook_theme_suggestions_block_alter()` | Use `$variables['elements']['#layout_builder_style']` |
| Load styles programmatically | `\Drupal::entityTypeManager()->getStorage('layout_builder_style')->load($id)` | Access style config entities |

### Pattern

**Custom Event Subscriber (After LB Styles):**
```php
// modules/custom/my_module/src/EventSubscriber/CustomStyleSubscriber.php
namespace Drupal\my_module\EventSubscriber;

use Drupal\layout_builder\Event\SectionComponentBuildRenderArrayEvent;
use Drupal\layout_builder\LayoutBuilderEvents;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class CustomStyleSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    // Run AFTER layout_builder_styles (priority 50)
    $events[LayoutBuilderEvents::SECTION_COMPONENT_BUILD_RENDER_ARRAY] = [
      'onBuildRender',
      40,  // Lower priority = runs after LB Styles
    ];
    return $events;
  }

  public function onBuildRender(SectionComponentBuildRenderArrayEvent $event) {
    $build = $event->getBuild();

    // Access applied styles
    $selectedStyles = $event->getComponent()->get('layout_builder_styles_style');
    if (!$selectedStyles) {
      return;
    }

    // Add context-aware classes
    $node = \Drupal::routeMatch()->getParameter('node');
    if ($node && $node->bundle() === 'article') {
      $build['#attributes']['class'][] = 'article-component';
    }

    // Conditional class addition
    if (in_array('bg_primary', $selectedStyles)) {
      $build['#attributes']['class'][] = 'has-colored-background';
    }

    $event->setBuild($build);
  }
}
```

**Register Event Subscriber:**
```yaml
# modules/custom/my_module/my_module.services.yml
services:
  my_module.custom_style_subscriber:
    class: Drupal\my_module\EventSubscriber\CustomStyleSubscriber
    tags:
      - { name: event_subscriber }
```

**Load and Inspect Style Entities:**
```php
// Load a specific style
$style = \Drupal::entityTypeManager()
  ->getStorage('layout_builder_style')
  ->load('padding_large');

if ($style) {
  $classes = $style->getClasses();        // "p-5"
  $type = $style->getType();              // "component" or "section"
  $group = $style->getGroup();            // "spacing"
  $restrictions = $style->getBlockRestrictions();  // Array of block plugin IDs
}

// Load all styles of a type
$query = \Drupal::entityTypeManager()
  ->getStorage('layout_builder_style')
  ->getQuery()
  ->accessCheck(FALSE)
  ->condition('type', 'section')
  ->sort('weight', 'ASC');
$ids = $query->execute();
$section_styles = \Drupal::entityTypeManager()
  ->getStorage('layout_builder_style')
  ->loadMultiple($ids);
```

**Custom Template Suggestions Based on Styles:**
```php
// modules/custom/my_module/my_module.module
use Drupal\Core\Template\Attribute;

/**
 * Implements hook_theme_suggestions_block_alter().
 */
function my_module_theme_suggestions_block_alter(array &$suggestions, array $variables) {
  // LB Styles provides single-style template suggestions
  // Add custom logic for multiple styles
  $styles = $variables['elements']['#layout_builder_style'] ?? [];

  if (!empty($styles) && is_array($styles)) {
    // Add suggestion for combination of styles
    $style_combo = implode('_', $styles);
    $suggestions[] = 'block__lb_styles__' . $style_combo;

    // Add suggestion per individual style
    foreach ($styles as $style_id) {
      $suggestions[] = 'block__lb_style__' . $style_id;
    }
  }
}
```

**Programmatically Apply Styles to Layouts:**
```php
// Apply style to section programmatically
$section = $layout_builder_section->getComponent($uuid);
$layout_settings = $section->getLayoutSettings();
$layout_settings['layout_builder_styles_style'] = ['padding_large', 'bg_primary'];
$section->setLayoutSettings($layout_settings);

// Apply style to component programmatically
$component = $section->getComponent($component_uuid);
$component->set('layout_builder_styles_style', ['shadow', 'rounded']);
```

**Form Alter to Restrict Styles by Role:**
```php
// modules/custom/my_module/my_module.module

/**
 * Implements hook_form_alter().
 */
function my_module_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if ($form_id === 'layout_builder_add_block' || $form_id === 'layout_builder_update_block') {
    $current_user = \Drupal::currentUser();

    // Remove advanced styles for non-admin users
    if (!$current_user->hasPermission('administer layout builder styles')) {
      if (isset($form['layout_builder_style_effects'])) {
        foreach ($form['layout_builder_style_effects']['#options'] as $key => $label) {
          if (strpos($key, 'advanced_') === 0) {
            unset($form['layout_builder_style_effects']['#options'][$key]);
          }
        }
      }
    }
  }
}
```

Reference: `modules/contrib/layout_builder_styles/src/EventSubscriber/BlockComponentRenderArraySubscriber.php`

### Common Mistakes

- **Wrong event priority** → LB Styles uses priority 50. Use lower number (40) to run after, higher (60) to run before
- **Not checking if styles exist** → Always check `$selectedStyles` is not empty before processing
- **Modifying config entities directly** → Don't alter `LayoutBuilderStyle` entities at runtime. Alter render arrays instead
- **Not handling arrays** → `layout_builder_styles_style` can be string or array. Always convert to array for processing
- **Forgetting cache tags** → If loading style entities, add cache tags: `$build['#cache']['tags'][] = 'config:layout_builder_styles.style.' . $style_id;`
- **Breaking existing classes** → When altering `$build['#attributes']['class']`, append don't replace: `array_merge()` not assignment
- **Not testing without LB Styles** → Your code should gracefully degrade if module disabled

### See Also

- Section 13: Layout Builder Events & Hooks (other event subscribers)
- Section 11: Overview (architecture and rendering flow)
- Section 11.2: Style Definitions (config entity structure)
- Reference: `core/modules/layout_builder/src/Event/SectionComponentBuildRenderArrayEvent.php`
- Reference: `core/modules/layout_builder/src/LayoutBuilderEvents.php`
