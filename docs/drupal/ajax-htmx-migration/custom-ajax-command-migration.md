---
description: "Custom AJAX Command Migration — migrate custom CommandInterface classes to HTMX trigger headers"
tldr: "Migrate custom AJAX commands that perform specialized JS operations. Delete the CommandInterface class — use Htmx::triggerHeader() instead, where the PHP array key becomes the JS event name that htmx.on() listens for."
drupal_version: "11.x"
---

# Custom AJAX Command Migration

## When to Use

> Migrate custom AJAX commands that perform specialized JavaScript operations. HTMX handles these via trigger headers that fire custom events.

## Pattern

**BEFORE: Custom AJAX Command**
```php
// PHP Command class
namespace Drupal\my_module\Ajax;

use Drupal\Core\Ajax\CommandInterface;

class NotificationCommand implements CommandInterface {
  protected $message;

  public function __construct($message) {
    $this->message = $message;
  }

  public function render() {
    return [
      'command' => 'showNotification',
      'message' => $this->message,
      'type' => 'success',
    ];
  }
}

// JavaScript handler
(function ($, Drupal) {
  Drupal.AjaxCommands.prototype.showNotification = function(ajax, response) {
    var notification = $('<div>')
      .addClass('notification ' + response.type)
      .text(response.message);
    $('body').append(notification);
  };
})(jQuery, Drupal);

// Usage in controller
$response = new AjaxResponse();
$response->addCommand(new NotificationCommand('Hello!'));
return $response;
```

**AFTER: HTMX Trigger Header**
```php
// PHP - use trigger header to fire custom event
use Drupal\Core\Htmx\Htmx;

$build = [
  '#markup' => 'Content here',
];

(new Htmx())
  ->triggerHeader([
    'showNotification' => [
      'message' => 'Hello!',
      'type' => 'success',
    ]
  ])
  ->applyTo($build);

return $build;
```

```javascript
// JavaScript - listen for the custom event
(function (Drupal, htmx) {
  htmx.on('showNotification', function(event) {
    var data = event.detail;
    var notification = document.createElement('div');
    notification.className = 'notification ' + data.type;
    notification.textContent = data.message;
    document.body.appendChild(notification);
  });
})(Drupal, htmx);
```

Reference: `Htmx::triggerHeader()` in `/core/lib/Drupal/Core/Htmx/Htmx.php`

## Common Mistakes

- **Creating CommandInterface classes** → Delete them. HTMX uses trigger headers, not command objects
- **Using `AjaxResponse::addCommand()`** → Use `Htmx::triggerHeader()` on render arrays instead
- **Not matching event names** → The PHP array key becomes the event name. `['myEvent' => $data]` triggers `htmx.on('myEvent', ...)`
- **Trying to use jQuery in handler** → Modern HTMX code should use vanilla JavaScript. Drupal behaviors still work but use `once()` API
- **Expecting command execution order** → HTMX triggers events after swap. If you need actions before swap, use `htmx:beforeSwap` event

## See Also

- Previous: [JavaScript Event Migration](javascript-event-migration.md)
- Next: [Drupal Behavior Migration](drupal-behavior-migration.md)
- Reference: HTMX HX-Trigger response header documentation
