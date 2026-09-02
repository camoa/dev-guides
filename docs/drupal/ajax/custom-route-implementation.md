---
description: Build custom AJAX endpoints outside Form API with nojs/ajax route parameters and graceful degradation
tldr: "Use custom AJAX routes when you need AJAX endpoints outside Form API: autocomplete, search, content loading, or API-style endpoints. Always implement the `nojs` fallback for JavaScript-disabled environments."
drupal_version: "11.x"
---

# Custom Route Implementation

## When to Use

You need AJAX endpoints outside Form API (autocomplete, search, content loading, API-style endpoints).

## Steps

1. **Define route**

   ```yaml
   # my_module.routing.yml
   my_module.ajax_content:
     path: '/my-module/ajax/content/{type}/{ajax}'
     defaults:
       _controller: '\Drupal\my_module\Controller\AjaxController::getContent'
       ajax: 'nojs'
     requirements:
       _permission: 'access content'
       type: '[a-z]+'
       ajax: 'nojs|ajax'
   ```

2. **Create controller**

   ```php
   // src/Controller/AjaxController.php
   namespace Drupal\my_module\Controller;

   use Drupal\Core\Ajax\AjaxResponse;
   use Drupal\Core\Ajax\ReplaceCommand;
   use Drupal\Core\Controller\ControllerBase;

   class AjaxController extends ControllerBase {
     public function getContent($type, $ajax = 'nojs') {
       $content = $this->buildContent($type);

       if ($ajax === 'ajax') {
         $response = new AjaxResponse();
         $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
         return $response;
       }

       // Non-AJAX fallback
       return [
         '#theme' => 'my_template',
         '#content' => $content,
       ];
     }

     private function buildContent($type) {
       return [
         '#markup' => $this->t('Content for @type', ['@type' => $type]),
       ];
     }
   }
   ```

3. **Create frontend JavaScript** (only when you need custom behavior on the response — see the `use-ajax` shortcut below for the common case)

   ```javascript
   // js/ajax-link.js
   (function ($, Drupal) {
     Drupal.behaviors.myModuleAjaxLink = {
       attach: function (context, settings) {
         $('.ajax-load-link', context).once('ajax-load').on('click', function(e) {
           e.preventDefault();
           const url = $(this).attr('href').replace('/nojs/', '/ajax/');

           $.ajax({
             url: url,
             success: function(response) {
               // Commands execute automatically
             }
           });
         });
       }
     };
   })(jQuery, Drupal);
   ```

4. **Use link in render array**

   ```php
   $build['link'] = [
     '#type' => 'link',
     '#title' => t('Load Content'),
     '#url' => Url::fromRoute('my_module.ajax_content', [
       'type' => 'example',
       'ajax' => 'nojs',
     ]),
     '#attributes' => ['class' => ['ajax-load-link']],
     '#attached' => ['library' => ['my_module/ajax-link']],
   ];
   ```

## Shortcut: Skip the Custom JavaScript with `use-ajax`

**Shortcut — skip the custom JavaScript with `use-ajax`:** for a plain link that just needs the `nojs`→`ajax` swap and an AjaxResponse handled, core already does this. Add class `use-ajax` to the link and attach `core/drupal.ajax` instead of a custom library:

```php
$build['link'] = [
  '#type' => 'link',
  '#title' => t('Load Content'),
  '#url' => Url::fromRoute('my_module.ajax_content', ['type' => 'example', 'ajax' => 'nojs']),
  '#attributes' => ['class' => ['use-ajax']],
  '#attached' => ['library' => ['core/drupal.ajax']],
];
```

`Drupal.behaviors.AJAX` (`core/misc/ajax.js`) binds every `.use-ajax` element, does the `/nojs/` → `/ajax/` replacement itself, and calls `Drupal.ajax()` — no custom JS file needed. Reach for step 3's manual approach only when the click needs logic beyond firing the AJAX request (e.g. custom dialog options via `data-dialog-type`).

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Route definition | Needs graceful degradation | Use `{ajax}` parameter with 'nojs' default |
| Access control | Complex permissions | Use `_custom_access` callback instead of `_permission` |
| Response type | Multiple commands needed | Use AjaxResponse with multiple addCommand() calls |
| Response type | Single element update | Return render array directly from callback |

## Common Mistakes

- Not providing non-AJAX fallback → Breaks for users without JavaScript; always handle `nojs` path
- Using wrong route parameter pattern → `{ajax}` requirement must be `nojs|ajax` exactly
- Forgetting to replace `/nojs/` with `/ajax/` in custom JavaScript → AJAX never triggers; or skip the custom JS and add the `use-ajax` class, which core handles automatically
- Not using ControllerBase → Missing helper methods like `t()`, `entityTypeManager()`, etc.
- Missing access control → Security vulnerability; always define `_permission` or `_custom_access`

## See Also

- ← Previous: [Custom AJAX Commands](custom-ajax-commands.md) | Next: [File Upload Patterns](file-upload-patterns.md)
- [Access Control Patterns](access-control-patterns.md)
- Reference: `core/modules/system/tests/modules/ajax_test/ajax_test.routing.yml`
