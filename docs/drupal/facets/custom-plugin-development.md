---
description: "Building custom Facets processors, widgets, and URL processors when the built-in plugin set doesn't cover a case"
tldr: "Use this guide when you need a custom processor, widget, query type, or URL processor that doesn't exist in the built-in set. Use the Facets-specific annotations and interfaces, not core equivalents."
drupal_version: "11.x"
---

# Custom Plugin Development

## When to Use

> When you need a custom processor, widget, query type, or URL processor that doesn't exist in the built-in set.

## Decision: Plugin Type Selection

| I Need To... | Create A... | Namespace |
|---|---|---|
| Transform result values | Build processor | `Plugin/facets/processor/` |
| Filter results | Build processor | `Plugin/facets/processor/` |
| Sort results | Sort processor | `Plugin/facets/processor/` |
| Modify queries | Pre-query processor | `Plugin/facets/processor/` |
| Render facets differently | Widget | `Plugin/facets/widget/` |
| Handle URLs differently | URL processor | `Plugin/facets/url_processor/` |
| Connect to a new backend | Facet source | `Plugin/facets/facet_source/` |

**As of 3.0.4**, URL processor plugins may declare themselves with either the `@FacetsUrlProcessor` annotation or the `#[Drupal\facets\Attribute\FacetsUrlProcessor]` attribute — `UrlProcessorPluginManager` accepts both. It is the only Facets plugin type with an attribute class; processors, widgets, query types, facet sources and hierarchies remain annotation-only.

## Pattern: Custom Processor

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
      // Modify each result.
      $result->setDisplayValue(strtoupper($result->getDisplayValue()));
    }
    return $results;
  }

}
```

## Pattern: Custom Widget

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
    // Customize the render array.
    $build['#attached']['library'][] = 'my_module/my_widget';
    return $build;
  }

}
```

## Common Mistakes

- **Wrong annotation** — Use `@FacetsProcessor`, `@FacetsWidget`, etc. Not core annotations.
- **Missing stage declaration** — Processors must declare which stages they support in the annotation.
- **Not implementing the right interface** — A build processor must implement `BuildProcessorInterface`, not just `ProcessorInterface`.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where custom processors fit
- [Widgets](widgets.md) — existing widgets to extend
- Reference: `src/Plugin/facets/`
