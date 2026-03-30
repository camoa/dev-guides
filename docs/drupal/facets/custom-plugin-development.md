---
description: Facets custom plugin development — custom processors, widgets, URL processors, and facet sources with PHP 8 attribute syntax
drupal_version: "11.x"
---

# Custom Plugin Development

## When to Use

> Use this guide when you need a custom processor, widget, query type, or URL processor that doesn't exist in the built-in set.

## Decision

| I Need To... | Create A... | Namespace |
|---|---|---|
| Transform result values | Build processor | `Plugin/facets/processor/` |
| Filter results | Build processor | `Plugin/facets/processor/` |
| Sort results | Sort processor | `Plugin/facets/processor/` |
| Modify queries | Pre-query processor | `Plugin/facets/processor/` |
| Render facets differently | Widget | `Plugin/facets/widget/` |
| Handle URLs differently | URL processor | `Plugin/facets/url_processor/` |
| Connect to a new backend | Facet source | `Plugin/facets/facet_source/` |

## Pattern

**Custom processor:**

```php
namespace Drupal\my_module\Plugin\facets\processor;

use Drupal\facets\Annotation\FacetsProcessor;
use Drupal\facets\FacetInterface;
use Drupal\facets\Processor\BuildProcessorInterface;
use Drupal\facets\Processor\ProcessorPluginBase;

/**
 * @FacetsProcessor(
 *   id = "my_custom_processor",
 *   label = @Translation("My Custom Processor"),
 *   description = @Translation("Does something custom to facet results."),
 *   stages = {
 *     "build" = 45
 *   }
 * )
 */
class MyCustomProcessor extends ProcessorPluginBase implements BuildProcessorInterface {

  public function build(FacetInterface $facet, array $results): array {
    foreach ($results as $result) {
      $result->setDisplayValue(strtoupper($result->getDisplayValue()));
    }
    return $results;
  }

}
```

**Custom widget:**

```php
namespace Drupal\my_module\Plugin\facets\widget;

use Drupal\facets\Annotation\FacetsWidget;
use Drupal\facets\FacetInterface;
use Drupal\facets\Widget\WidgetPluginBase;

/**
 * @FacetsWidget(
 *   id = "my_custom_widget",
 *   label = @Translation("My Custom Widget"),
 *   description = @Translation("Renders facets in a custom way."),
 * )
 */
class MyCustomWidget extends WidgetPluginBase {

  public function build(FacetInterface $facet): array {
    $build = parent::build($facet);
    $build['#attached']['library'][] = 'my_module/my_widget';
    return $build;
  }

}
```

## Common Mistakes

- **Wrong**: Using core Drupal annotations instead of Facets-specific ones → **Right**: Use `@FacetsProcessor`, `@FacetsWidget`, etc. Not `@Plugin` or other core annotations.
- **Wrong**: Declaring a processor without specifying stages → **Right**: Processors must declare which stages they support in the annotation's `stages` key.
- **Wrong**: Implementing only `ProcessorInterface` for a build processor → **Right**: A build processor must implement `BuildProcessorInterface`, not just the base `ProcessorInterface`.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where custom processors fit
- [Widgets](widgets.md) — existing widgets to extend
- Reference: `web/modules/contrib/facets/src/Plugin/facets/processor/`, `src/Plugin/facets/widget/`
