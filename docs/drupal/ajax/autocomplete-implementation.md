---
description: Implement autocomplete on text fields with custom route, controller, and minimum character threshold
drupal_version: "11.x"
---

# Autocomplete Implementation

## When to Use

> Use `#autocomplete_route_name` for dynamic suggestions as users type. Use core's `system.entity_autocomplete` for existing entity types. Create a custom controller only for non-entity data.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Data source | Existing entity type | Use `system.entity_autocomplete` route |
| Data source | Custom data | Create custom controller with JsonResponse |
| Input validation | Minimum characters needed | Check `strlen($input) >= N` before querying |
| Results display | Need extra info in label | Use 'label' for display, 'value' for form value |

## Pattern

**Route:**

```yaml
my_module.autocomplete:
  path: '/my-module/autocomplete'
  defaults:
    _controller: '\Drupal\my_module\Controller\AutocompleteController::autocomplete'
  requirements:
    _permission: 'access content'
```

**Controller:**

```php
class AutocompleteController extends ControllerBase {
  public function autocomplete(Request $request) {
    $results = [];
    $input = $request->query->get('q');

    if ($input && strlen($input) >= 2) {
      $nids = $this->entityTypeManager()->getStorage('node')->getQuery()
        ->condition('type', 'article')
        ->condition('title', $input, 'CONTAINS')
        ->range(0, 10)
        ->sort('title')
        ->execute();

      foreach (Node::loadMultiple($nids) as $node) {
        $results[] = [
          'value' => $node->getTitle(),
          'label' => $node->getTitle() . ' (' . $node->id() . ')',
        ];
      }
    }

    return new JsonResponse($results);
  }
}
```

**Form element:**

```php
$form['autocomplete_field'] = [
  '#type' => 'textfield',
  '#title' => t('Search Content'),
  '#autocomplete_route_name' => 'my_module.autocomplete',
];
```

Reference: `core/modules/system/src/Controller/EntityAutocompleteController.php`

## Common Mistakes

- **Wrong**: Querying on every keystroke → **Right**: Add minimum character check (usually 2–3 characters)
- **Wrong**: No result limits → **Right**: Massive JSON responses; always use `range(0, 10)` or similar
- **Wrong**: Returning non-JSON response → **Right**: Autocomplete breaks; always use JsonResponse
- **Wrong**: Not sanitizing query input → **Right**: SQL injection risk; use entity query or proper escaping
- **Wrong**: Missing access control on route → **Right**: Security vulnerability; always define `_permission`

## See Also

- [File Upload Patterns](file-upload-patterns.md)
- [Access Control Patterns](access-control-patterns.md)
- Reference: `core/modules/system/src/Controller/EntityAutocompleteController.php`
