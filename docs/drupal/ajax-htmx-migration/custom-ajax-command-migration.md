---
description: Migrate custom AJAX CommandInterface classes to HTMX trigger headers that fire custom JavaScript events
drupal_version: "11.x"
---

# Custom AJAX Command Migration

## When to Use

> Use this when migrating custom AJAX commands (`CommandInterface` classes) that perform specialized JavaScript operations. HTMX handles these via trigger headers.

## Pattern

**BEFORE — PHP Command class + JavaScript handler:**
```php
// CommandInterface class
class NotificationCommand implements CommandInterface {
  public function render() {
    return ['command' => 'showNotification', 'message' => $this->message, 'type' => 'success'];
  }
}

// Usage
$response = new AjaxResponse();
$response->addCommand(new NotificationCommand('Hello!'));
return $response;
```
```javascript
Drupal.AjaxCommands.prototype.showNotification = function(ajax, response) {
  $('body').append($('<div>').addClass('notification ' + response.type).text(response.message));
};
```

**AFTER — PHP trigger header + JavaScript event listener:**
```php
use Drupal\Core\Htmx\Htmx;

$build = ['#markup' => 'Content here'];

(new Htmx())
  ->triggerHeader([
    'showNotification' => ['message' => 'Hello!', 'type' => 'success'],
  ])
  ->applyTo($build);

return $build;
```
```javascript
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

## Common Mistakes

- **Creating `CommandInterface` classes** → Delete them. HTMX uses trigger headers, not command objects
- **Using `AjaxResponse::addCommand()`** → Use `Htmx::triggerHeader()` on render arrays instead
- **Not matching event names** → The PHP array key becomes the event name. `['myEvent' => $data]` triggers `htmx.on('myEvent', ...)`
- **Using jQuery in handler** → Modern HTMX code uses vanilla JavaScript. Drupal behaviors still work but update to `once()` API
- **Expecting command execution order** → HTMX triggers events after swap. For pre-swap actions, use the `htmx:beforeSwap` event

## See Also

- Previous: [JavaScript Event Migration](javascript-event-migration.md)
- Next: [Drupal Behavior Migration](drupal-behavior-migration.md)
- Reference: `Htmx::triggerHeader()` at `/core/lib/Drupal/Core/Htmx/Htmx.php`
- Reference: [HX-Trigger response header documentation](https://htmx.org/headers/hx-trigger/)
