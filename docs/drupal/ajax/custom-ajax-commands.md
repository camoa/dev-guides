---
description: Create custom AJAX commands with CommandInterface for complex DOM manipulation or third-party library integration
tldr: "Create custom AJAX commands when core commands don't meet your needs: custom animations, third-party library integration, or complex DOM manipulation requiring JavaScript logic."
drupal_version: "11.x"
---

# Custom AJAX Commands

## When to Use

Core AJAX commands don't meet your needs (custom animations, third-party library integration, complex DOM manipulation).

## Steps

1. **Create command class**

   ```php
   // src/Ajax/CustomAnimateCommand.php
   namespace Drupal\my_module\Ajax;

   use Drupal\Core\Ajax\CommandInterface;

   class CustomAnimateCommand implements CommandInterface {
     protected $selector;
     protected $duration;

     public function __construct($selector, $duration = 300) {
       $this->selector = $selector;
       $this->duration = $duration;
     }

     public function render() {
       return [
         'command' => 'customAnimate',
         'selector' => $this->selector,
         'duration' => $this->duration,
       ];
     }
   }
   ```

2. **Create JavaScript handler**

   ```javascript
   // js/custom-ajax-commands.js
   (function (Drupal) {
     Drupal.AjaxCommands.prototype.customAnimate = function (ajax, response, status) {
       const $element = jQuery(response.selector);
       $element.fadeOut(response.duration, function() {
         $element.fadeIn(response.duration);
       });
     };
   })(Drupal);
   ```

3. **Register library**

   ```yaml
   # my_module.libraries.yml
   custom-ajax-commands:
     js:
       js/custom-ajax-commands.js: {}
     dependencies:
       - core/jquery
       - core/drupal.ajax
   ```

4. **Use custom command**

   ```php
   use Drupal\my_module\Ajax\CustomAnimateCommand;

   public function ajaxCallback(array &$form, FormStateInterface $form_state) {
     $response = new AjaxResponse();
     $response->addCommand(new CustomAnimateCommand('#my-element', 500));
     $response->setAttachments(['library' => ['my_module/custom-ajax-commands']]);
     return $response;
   }
   ```

## Common Mistakes

- Not implementing CommandInterface → Command won't be recognized; always implement interface
- Mismatch between command name in `render()` and JavaScript → Command silently fails; names must match exactly
- Forgetting to attach library → JavaScript handler not loaded; use `$response->setAttachments()` or `#attached`
- Not handling jQuery dependency → Breaks if jQuery not loaded; add `core/jquery` to library dependencies
- Using underscores in command names → Use camelCase in both PHP and JavaScript (customAnimate, not custom_animate)

## See Also

- ← Previous: [Feedback Commands](feedback-commands.md) | Next: [Custom Route Implementation](custom-route-implementation.md)
- Reference: `core/lib/Drupal/Core/Ajax/CommandInterface.php`
