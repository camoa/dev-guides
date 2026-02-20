---
description: Create custom AJAX commands with CommandInterface for complex DOM manipulation or third-party library integration
drupal_version: "11.x"
---

# Custom AJAX Commands

## When to Use

> Create custom AJAX commands when core commands don't meet your needs: custom animations, third-party library integration, or complex DOM manipulation requiring JavaScript logic.

## Pattern

**1. PHP command class:**

```php
// src/Ajax/CustomAnimateCommand.php
namespace Drupal\my_module\Ajax;

use Drupal\Core\Ajax\CommandInterface;

class CustomAnimateCommand implements CommandInterface {
  public function __construct(
    protected string $selector,
    protected int $duration = 300
  ) {}

  public function render() {
    return [
      'command' => 'customAnimate',    // Must match JS handler name
      'selector' => $this->selector,
      'duration' => $this->duration,
    ];
  }
}
```

**2. JavaScript handler:**

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

**3. Library and usage:**

```yaml
# my_module.libraries.yml
custom-ajax-commands:
  js:
    js/custom-ajax-commands.js: {}
  dependencies:
    - core/jquery
    - core/drupal.ajax
```

```php
$response = new AjaxResponse();
$response->addCommand(new CustomAnimateCommand('#my-element', 500));
$response->setAttachments(['library' => ['my_module/custom-ajax-commands']]);
return $response;
```

Reference: `core/lib/Drupal/Core/Ajax/CommandInterface.php`

## Common Mistakes

- **Wrong**: Not implementing CommandInterface → **Right**: Command won't be recognized; interface is required
- **Wrong**: Mismatch between `render()` command name and JavaScript → **Right**: Names must match exactly; command silently fails otherwise
- **Wrong**: Forgetting to attach library → **Right**: JavaScript handler not loaded; use `$response->setAttachments()` or `#attached`
- **Wrong**: Using underscores in command names → **Right**: Use camelCase in both PHP and JavaScript (`customAnimate` not `custom_animate`)
- **Wrong**: Missing `core/jquery` dependency → **Right**: Add to library dependencies to ensure jQuery loads first

## See Also

- [Feedback Commands](feedback-commands.md)
- [Custom Route Implementation](custom-route-implementation.md)
- Reference: `core/lib/Drupal/Core/Ajax/CommandInterface.php`
