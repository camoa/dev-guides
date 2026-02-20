---
description: Announce dynamic AJAX content changes to screen readers using AnnounceCommand, MessageCommand, and ARIA live regions
drupal_version: "11.x"
---

# Screen Reader Support

## When to Use

> Every AJAX content update must be announced to screen reader users. Silence after a dynamic update is a WCAG failure. Use 'polite' for non-critical updates and 'assertive' only for critical errors.

## Pattern

```php
use Drupal\Core\Ajax\AnnounceCommand;
use Drupal\Core\Ajax\MessageCommand;
use Drupal\Core\Ajax\HtmlCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();

  // Method 1: AnnounceCommand (no visual indication)
  $response->addCommand(new AnnounceCommand(
    'Search results updated. 12 results found.',
    'polite'
  ));

  // Method 2: MessageCommand with announce (visual + audio)
  $response->addCommand(new MessageCommand(
    'Form saved successfully.',
    NULL,
    ['type' => 'status'],
    TRUE  // Announce to screen readers
  ));

  // Method 3: Visually-hidden ARIA live region (in form build)
  // $form['live_region'] = [
  //   '#type' => 'container',
  //   '#attributes' => [
  //     'id' => 'live-announcements',
  //     'aria-live' => 'polite',
  //     'aria-atomic' => 'true',
  //     'class' => ['visually-hidden'],
  //   ],
  // ];
  $response->addCommand(new HtmlCommand('#live-announcements', 'Content loaded.'));

  return $response;
}
```

Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`

## Common Mistakes

- **Wrong**: Using 'assertive' for non-critical updates → **Right**: Interrupts current speech; use 'polite' for most cases
- **Wrong**: Announcing technical details → **Right**: Say "Form saved" not "AJAX callback executed successfully"
- **Wrong**: Vague announcement text → **Right**: "Updated" is not enough; say "Search results updated with 5 items"
- **Wrong**: Announcing too frequently → **Right**: Overlapping announcements confuse users; debounce or combine messages
- **Wrong**: No visual alternative → **Right**: Some users have both vision and hearing impairments; combine with visual indicators

## See Also

- [WCAG Compliance Patterns](wcag-compliance-patterns.md)
- [Debugging Techniques](debugging-techniques.md)
- Reference: [ARIA live regions specification](https://www.w3.org/TR/wai-aria-1.2/#live_region_roles)
