---
description: Integrate JavaScript with Drupal's AJAX framework for dynamic content updates
drupal_version: "10.x/11.x"
---

# AJAX Integration

## When to Use

> Use when loading content dynamically without full page refresh, or when JavaScript needs to respond to Drupal AJAX events.

## Decision

Drupal provides comprehensive AJAX framework that automatically re-runs behaviors on updated content. Use Drupal.ajax for form submissions and commands; use fetch API for custom endpoints. Behaviors automatically work with AJAX - no special code needed if using context properly.

## Pattern

**Behavior AJAX compatibility** (automatic):

```javascript
Drupal.behaviors.ajaxAware = {
  attach(context, settings) {
    // Works on initial load AND after AJAX updates
    // No special AJAX handling needed if using context
    once('ajax-compatible', '.dynamic-content', context).forEach(function (element) {
      element.addEventListener('click', handleClick);
    });
  }
};
```

**Custom AJAX command** (server-side PHP):

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\InvokeCommand;

$response = new AjaxResponse();
$response->addCommand(new InvokeCommand('.selector', 'addClass', ['active']));
return $response;
```

**Custom AJAX command** (client-side JavaScript):

```javascript
Drupal.AjaxCommands.prototype.customCommand = function (ajax, response, status) {
  // Custom command implementation
  // Behaviors automatically re-run on updated content
  console.log('Custom command executed', response.data);
};
```

**Fetch API for custom endpoints** (modern alternative):

```javascript
fetch('/api/endpoint', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
  // Update DOM - behaviors will run on new content
  element.innerHTML = data.markup;
  Drupal.attachBehaviors(element); // Manually trigger if needed
});
```

## Common Mistakes

- **Wrong**: Not using context in behaviors → **Right**: Always query within context
  - **Why**: AJAX-loaded content doesn't initialize, mysterious bugs
- **Wrong**: Manually re-initializing after AJAX → **Right**: Let Drupal behaviors handle it
  - **Why**: Drupal does this automatically via behaviors
- **Wrong**: Custom AJAX without dependency → **Right**: Declare core/drupal.ajax dependency
  - **Why**: Missing dependency causes undefined errors
- **Wrong**: Forgetting detach() for AJAX-destroyed content → **Right**: Clean up in detach()
  - **Why**: Event listeners remain, memory leaks accumulate
- **Wrong**: Using $.ajax() instead of Drupal AJAX → **Right**: Use Drupal AJAX framework
  - **Why**: Misses automatic behavior re-execution, command system

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - AJAX-compatible initialization
- Reference: `/core/misc/ajax.js` - Core AJAX implementation
- Reference: [AJAX API Documentation](https://www.drupal.org/docs/develop/drupal-apis/ajax-api/core-ajax-callback-commands)
