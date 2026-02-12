---
description: AJAX forms — core system, element properties, callbacks, commands
drupal_version: "11.x"
---

# AJAX Form Architecture

### Core AJAX System

**System Components:**
| Component | File | Purpose |
|-----------|------|---------|
| Response Builder | `/web/core/lib/Drupal/Core/Form/FormAjaxResponseBuilder.php` | Builds AJAX responses |
| Event Subscriber | `/web/core/lib/Drupal/Core/Form/EventSubscriber/FormAjaxSubscriber.php` | Handles AJAX events |
| Command Library | `/web/core/lib/Drupal/Core/Ajax/` | AJAX commands |

**Reference Examples:**
- Simple AJAX: `/web/core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestSimpleForm.php`
- Shows: Select, checkbox, grouped elements with AJAX callbacks

### Element AJAX Property

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
```
change - Select, checkbox, radio (default)
click - Buttons, links
keyup - Textfields (use with debouncing)
blur - On field exit
custom - Custom JavaScript event
```

### AJAX Callback Patterns

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

**Static Callbacks for Anonymous Users:**
```
Issue: Non-static methods fail with anonymous users + Symfony
Solution: Make callback methods static
Reference: Drupal at your Fingertips - AJAX section
```

### Core AJAX Commands

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

**Command Files:**
- Location: `/web/core/lib/Drupal/Core/Ajax/`
- Study: Individual command classes for usage patterns

**Common Mistakes:**
- Forgetting wrapper ID in #ajax (nothing to replace)
- Wrapper ID doesn't exist in form (AJAX fails silently)
- Not returning render array or AjaxResponse (AJAX error)
- Using non-unique wrapper IDs (replaces wrong element)

**See Also:**
- AJAX Security (next section)
- AJAX Commands Reference (dedicated section)
- JavaScript API Guide
- Official: [AJAX Forms](https://www.drupal.org/docs/develop/drupal-apis/javascript-api/ajax-forms)
