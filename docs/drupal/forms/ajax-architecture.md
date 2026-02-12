---
description: AJAX forms — core system, element properties, callbacks, commands
drupal_version: "11.x"
---

# AJAX Form Architecture

## When to Use

> Use AJAX when options must change based on server data. Use #states for simple show/hide logic.

## Decision

| Need | Solution | Why |
|------|----------|-----|
| Dependent dropdowns | AJAX | Options from server |
| Show/hide fields | #states | Client-side, faster |
| Load entities/data | AJAX | Server-side data |
| Multiple element updates | AjaxResponse + Commands | Granular control |
| Single element update | Return render array | Simpler |

## Core AJAX System

**System Components:**
| Component | File | Purpose |
|-----------|------|---------|
| Response Builder | `/web/core/lib/Drupal/Core/Form/FormAjaxResponseBuilder.php` | Builds AJAX responses |
| Event Subscriber | `/web/core/lib/Drupal/Core/Form/EventSubscriber/FormAjaxSubscriber.php` | Handles AJAX events |
| Command Library | `/web/core/lib/Drupal/Core/Ajax/` | AJAX commands |

Reference: `/web/core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestSimpleForm.php`

## Element AJAX Property

**Configuration Array:**
```php
'#ajax' => [
  'callback' => '::ajaxCallback',           // Required
  'wrapper' => 'element-wrapper-id',        // Target container ID
  'event' => 'change',                      // Trigger event (default varies)
  'method' => 'replace',                    // Command method
  'effect' => 'fade',                       // Visual effect
  'progress' => [                           // Loading indicator
    'type' => 'throbber',                   // or 'fullscreen'
    'message' => $this->t('Loading...'),
  ],
],
```

**Common Events:**
- change - Select, checkbox, radio (default)
- click - Buttons, links
- keyup - Textfields (use with debouncing)
- blur - On field exit
- custom - Custom JavaScript event

## AJAX Callback Patterns

**Pattern 1: Return Element (Simple):**
```php
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  return $form['container']; // Replaces #ajax wrapper
}
```

**Pattern 2: Return AjaxResponse (Advanced):**
```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\MessageCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#wrapper', $form['element']));
  $response->addCommand(new MessageCommand('Updated'));
  return $response;
}
```

## Core AJAX Commands

**Common Commands:**
| Command | Purpose | Parameters |
|---------|---------|------------|
| ReplaceCommand | Replace element | selector, content |
| AppendCommand | Add after | selector, content |
| PrependCommand | Add before | selector, content |
| RemoveCommand | Delete element | selector |
| MessageCommand | Show status | message, type (status/warning/error) |
| RedirectCommand | Navigate | url |
| InvokeCommand | Call JS method | selector, method, arguments |
| OpenModalDialogCommand | Open modal | title, content, options |

Location: `/web/core/lib/Drupal/Core/Ajax/`

## Common Mistakes

- **Wrong**: Forgetting wrapper ID in #ajax → **Right**: Add wrapper ID to target element
- **Wrong**: Wrapper ID doesn't exist in form → **Right**: Ensure ID exists
- **Wrong**: Not returning render array or AjaxResponse → **Right**: Return proper type
- **Wrong**: Using non-unique wrapper IDs → **Right**: Use unique IDs

## See Also

- [AJAX Security](ajax-security.md)
- [Form States System](form-states-system.md)
- Documentation: [AJAX Forms](https://www.drupal.org/docs/develop/drupal-apis/javascript-api/ajax-forms)
- Reference: `/web/core/lib/Drupal/Core/Ajax/`
