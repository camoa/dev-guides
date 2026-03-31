---
description: Custom Search API plugins — processor development with PHP 8.1 attribute syntax, stage selection, and plugin namespace
drupal_version: "11.x"
---

# Custom Plugin Development

## When to Use

> Use this when you need a custom processor, backend, datasource, or other Search API plugin.

## Decision

| I Need To... | Create A... | Namespace |
|---|---|---|
| Transform field values at index time | Processor (preprocess_index) | `Plugin/search_api/processor/` |
| Add computed fields | Processor (add_properties) | `Plugin/search_api/processor/` |
| Filter items before indexing | Processor (alter_items) | `Plugin/search_api/processor/` |
| Modify search queries | Processor (preprocess_query) | `Plugin/search_api/processor/` |
| Modify search results | Processor (postprocess_query) | `Plugin/search_api/processor/` |
| Connect a new search engine | Backend | `Plugin/search_api/backend/` |
| Index non-entity data | Datasource | `Plugin/search_api/datasource/` |

## Pattern

```php
namespace Drupal\my_module\Plugin\search_api\processor;

use Drupal\search_api\Attribute\SearchApiProcessor;
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

}
```

## Common Mistakes

- **Wrong**: Wrong stage for the task → **Right**: Use `alter_items` to filter items, `preprocess_index` to transform values, `preprocess_query` to modify queries.
- **Wrong**: Missing stage declaration in attribute → **Right**: Processors must declare supported stages in the `#[SearchApiProcessor]` attribute.
- **Wrong**: Not overriding `supportsIndex()` → **Right**: Override to restrict your processor to specific index types if needed.

## See Also

- [Processor Architecture](processor-architecture.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/search_api/src/Processor/ProcessorPluginBase.php`
