---
description: Development standards for maintainable Drupal AJAX — dependency injection, render arrays, error handling, and Drupal.behaviors
tldr: "Apply these standards to all AJAX code. They prevent the most common sources of bugs, broken tests, and maintenance pain."
drupal_version: "11.x"
---

# Best Practices: Development Standards

## When to Use

You're writing AJAX code that needs to be maintainable, testable, and follow Drupal coding standards.

## Development Standards

**Development Standards:**

1. **Use Dependency Injection**

   ```php
   // BAD: Static calls
   $nodes = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple($nids);

   // GOOD: Dependency injection
   class MyForm extends FormBase {
     protected $entityTypeManager;

     public function __construct(EntityTypeManagerInterface $entity_type_manager) {
       $this->entityTypeManager = $entity_type_manager;
     }

     public static function create(ContainerInterface $container) {
       return new static(
         $container->get('entity_type.manager')
       );
     }
   }
   ```

2. **Return Render Arrays**

   ```php
   // BAD: HTML strings
   return '<div>Content</div>';

   // GOOD: Render arrays
   return [
     '#markup' => $this->t('Content'),
     '#prefix' => '<div id="wrapper">',
     '#suffix' => '</div>',
   ];
   ```

3. **Proper Error Handling**

   ```php
   public function ajaxCallback(array &$form, FormStateInterface $form_state) {
     try {
       $data = $this->loadData();
       return $form['target'];
     }
     catch (\Exception $e) {
       $this->logger('my_module')->error('AJAX error: @message', [
         '@message' => $e->getMessage(),
       ]);

       $response = new AjaxResponse();
       $response->addCommand(new MessageCommand(
         $this->t('An error occurred. Please try again.'),
         NULL,
         ['type' => 'error']
       ));
       return $response;
     }
   }
   ```

4. **Use Form State Storage**

   ```php
   // Store data between rebuilds
   $form_state->set('step', 2);
   $form_state->set('user_data', $values);

   // Retrieve stored data
   $step = $form_state->get('step');
   ```

5. **Follow Drupal Behaviors Pattern**

   ```javascript
   // Proper Drupal.behaviors implementation
   (function ($, Drupal) {
     Drupal.behaviors.myModuleAjax = {
       attach: function (context, settings) {
         // Use .once() to prevent duplicate initialization
         $('.ajax-link', context).once('my-module-ajax').on('click', function(e) {
           e.preventDefault();
           // AJAX logic
         });
       },
       detach: function (context, settings, trigger) {
         // Cleanup when element removed
         if (trigger === 'unload') {
           $('.ajax-link', context).off('click');
         }
       }
     };
   })(jQuery, Drupal);
   ```

## Anti-Patterns to Avoid

**Anti-Patterns to Avoid:**

| Anti-Pattern | Why Wrong | Correct Approach |
|---|---|---|
| `\Drupal::` in forms/controllers | Breaks testability, bypasses DI | Inject services via constructor |
| HTML strings in responses | Bypasses theming, security risk | Return render arrays |
| No error handling | Silent failures confuse users | Wrap in try/catch, log errors |
| Skipping `#validated => TRUE` | Validation errors on rebuild | Add to dependent fields |
| Using `$(document).ready()` | Runs once, not on AJAX updates | Use Drupal.behaviors |
| Missing `.once()` in behaviors | Duplicate event handlers | Always use `.once()` |

## See Also

- ← Previous: [Best Practices: Performance](best-practices-performance.md) | Next: [Best Practices: Accessibility](best-practices-accessibility.md)
- Reference: [Drupal coding standards](https://www.drupal.org/docs/develop/standards/coding-standards)
