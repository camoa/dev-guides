---
description: Implement autocomplete on text fields with custom route, controller, and minimum character threshold
tldr: "Use `#autocomplete_route_name` for dynamic suggestions as users type. Use core's `system.entity_autocomplete` for existing entity types."
drupal_version: "11.x"
---

# Autocomplete Implementation

## When to Use

You need textfield suggestions that load dynamically as users type (entity reference, tag input, search suggestions).

## Steps

1. **Add autocomplete route**

   ```yaml
   # my_module.routing.yml
   my_module.autocomplete:
     path: '/my-module/autocomplete'
     defaults:
       _controller: '\Drupal\my_module\Controller\AutocompleteController::autocomplete'
     requirements:
       _permission: 'access content'
   ```

2. **Create autocomplete controller**

   ```php
   // src/Controller/AutocompleteController.php
   namespace Drupal\my_module\Controller;

   use Drupal\Core\Controller\ControllerBase;
   use Symfony\Component\HttpFoundation\JsonResponse;
   use Symfony\Component\HttpFoundation\Request;

   class AutocompleteController extends ControllerBase {
     public function autocomplete(Request $request) {
       $results = [];
       $input = $request->query->get('q');

       if ($input && strlen($input) >= 2) {
         $query = $this->entityTypeManager()
           ->getStorage('node')
           ->getQuery()
           ->condition('type', 'article')
           ->condition('title', $input, 'CONTAINS')
           ->range(0, 10)
           ->sort('title');

         $nids = $query->execute();
         $nodes = Node::loadMultiple($nids);

         foreach ($nodes as $node) {
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

3. **Add autocomplete to form element**

   ```php
   $form['autocomplete_field'] = [
     '#type' => 'textfield',
     '#title' => t('Search Content'),
     '#autocomplete_route_name' => 'my_module.autocomplete',
     '#autocomplete_route_parameters' => ['param' => 'value'],  // Optional
   ];
   ```

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Data source | Existing entity type | Use core autocomplete routes (system.entity_autocomplete) |
| Data source | Custom data | Create custom controller with JsonResponse |
| Input validation | Minimum characters needed | Check `strlen($input) >= N` before querying |
| Results display | Need extra info in label | Use 'label' for display, 'value' for form value |

## Common Mistakes

- Querying database on every keystroke → Add minimum character check (usually 2-3 characters)
- Not limiting results → Massive JSON responses; always use `range(0, 10)` or similar
- Returning non-JSON response → Autocomplete breaks; always use JsonResponse
- Not sanitizing query input → SQL injection risk; use entity query or proper escaping
- Missing access control on route → Security vulnerability; always define `_permission`

## See Also

- ← Previous: [File Upload Patterns](file-upload-patterns.md) | Next: [Access Control Patterns](access-control-patterns.md)
- Reference: `core/modules/system/src/Controller/EntityAutocompleteController.php`
