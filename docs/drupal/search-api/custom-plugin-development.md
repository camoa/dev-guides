---
description: Custom Search API plugins — processor development with PHP 8.1 attribute syntax, stage selection, and plugin namespace
tldr: "Use this when you need a custom processor, backend, datasource, or other Search API plugin. Extend ProcessorPluginBase, which supplies default implementations for every ProcessorInterface method."
drupal_version: "11.x"
---

# Custom Plugin Development

## When to Use

> When you need a custom processor, backend, datasource, or other Search API plugin.

## Decision: Plugin Type Selection

| I Need To... | Create A... | Namespace |
|---|---|---|
| Transform field values at index time | Processor (preprocess_index) | `Plugin/search_api/processor/` |
| Add computed fields | Processor (add_properties) | `Plugin/search_api/processor/` |
| Filter items before indexing | Processor (alter_items) | `Plugin/search_api/processor/` |
| Modify search queries | Processor (preprocess_query) | `Plugin/search_api/processor/` |
| Modify search results | Processor (postprocess_query) | `Plugin/search_api/processor/` |
| Connect a new search engine | Backend | `Plugin/search_api/backend/` |
| Index non-entity data | Datasource | `Plugin/search_api/datasource/` |

## Pattern: Custom Processor

```php
namespace Drupal\my_module\Plugin\search_api\processor;

use Drupal\search_api\Attribute\SearchApiProcessor;
use Drupal\search_api\IndexInterface;
use Drupal\search_api\Processor\ProcessorPluginBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[SearchApiProcessor(
  id: 'my_custom_processor',
  label: new TranslatableMarkup('My Custom Processor'),
  description: new TranslatableMarkup('Does something custom.'),
  stages: [
    'preprocess_index' => 0,
    'preprocess_query' => 0,
  ],
)]
class MyCustomProcessor extends ProcessorPluginBase {

  public function preprocessIndexItems(array $items): void {
    foreach ($items as $item) {
      foreach ($item->getFields() as $field) {
        // Transform field values during indexing.
      }
    }
  }

  public function preprocessSearchQuery(QueryInterface $query): void {
    // Modify query before execution.
  }

}
```

## Common Mistakes

- **Wrong stage for the task** — Use `alter_items` to filter items, `preprocess_index` to transform values, `preprocess_query` to modify queries.
- **Missing stage declaration** — Processors must declare supported stages in the attribute/annotation.
- **Not checking `supportsIndex()`** — Override this to restrict your processor to specific index types.

## Pattern: Base Class Reference

`ProcessorPluginBase` (`search_api/src/Processor/ProcessorPluginBase.php`) supplies the default implementations for every `ProcessorInterface` method, so a custom processor only overrides the stages it declares.

## See Also

- [Processor Architecture](processor-architecture.md) — stage details
- [Events System](events-system.md) — lighter-weight alternative to processors
