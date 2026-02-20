---
description: Development standards for maintainable Drupal AJAX — dependency injection, render arrays, error handling, and Drupal.behaviors
drupal_version: "11.x"
---

# Best Practices: Development Standards

## When to Use

> Apply these standards to all AJAX code. They prevent the most common sources of bugs, broken tests, and maintenance pain.

## Decision

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| `\Drupal::` in forms/controllers | Breaks testability, bypasses DI | Inject services via constructor |
| HTML strings in responses | Bypasses theming, security risk | Return render arrays |
| No error handling | Silent failures confuse users | Wrap in try/catch, log errors |
| Skipping `#validated => TRUE` | Validation errors on rebuild | Add to dependent fields |
| Using `$(document).ready()` | Runs once, not on AJAX updates | Use Drupal.behaviors |
| Missing `.once()` in behaviors | Duplicate event handlers | Always use `.once()` |

## Pattern

```php
// 1. Dependency injection
class MyForm extends FormBase {
  public function __construct(
    private readonly EntityTypeManagerInterface $entityTypeManager
  ) {}

  public static function create(ContainerInterface $container) {
    return new static($container->get('entity_type.manager'));
  }
}

// 2. Return render arrays
return ['#markup' => $this->t('Content'), '#prefix' => '<div id="wrapper">', '#suffix' => '</div>'];

// 3. Error handling
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  try {
    $data = $this->loadData();
    return $form['target'];
  }
  catch (\Exception $e) {
    $this->logger('my_module')->error('AJAX error: @msg', ['@msg' => $e->getMessage()]);
    $response = new AjaxResponse();
    $response->addCommand(new MessageCommand($this->t('An error occurred.'), NULL, ['type' => 'error']));
    return $response;
  }
}
```

```javascript
// 4. Drupal.behaviors (not document.ready)
(function ($, Drupal) {
  Drupal.behaviors.myModuleAjax = {
    attach: function (context, settings) {
      // .once() prevents duplicate initialization on AJAX updates
      $('.ajax-link', context).once('my-module-ajax').on('click', function(e) {
        e.preventDefault();
        // AJAX logic
      });
    },
    detach: function (context, settings, trigger) {
      if (trigger === 'unload') {
        $('.ajax-link', context).off('click');
      }
    }
  };
})(jQuery, Drupal);
```

## Common Mistakes

- **Wrong**: `\Drupal::entityTypeManager()` in form class → **Right**: Inject EntityTypeManagerInterface in constructor
- **Wrong**: Returning `'<div>' . $content . '</div>'` → **Right**: Return render array with `#markup` and proper escaping
- **Wrong**: No try/catch in callbacks → **Right**: Unhandled exceptions produce cryptic 500 errors; always catch and return MessageCommand
- **Wrong**: `$(document).ready()` for AJAX-updated content → **Right**: Drupal.behaviors.attach runs after every AJAX update
- **Wrong**: No `.once()` in behaviors → **Right**: Each AJAX update calls attach again, duplicating event handlers

## See Also

- [Best Practices: Performance](best-practices-performance.md)
- [Best Practices: Accessibility](best-practices-accessibility.md)
- Reference: [Drupal coding standards](https://www.drupal.org/docs/develop/standards/coding-standards)
