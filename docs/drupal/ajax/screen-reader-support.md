---
description: Announce dynamic AJAX content changes to screen readers using AnnounceCommand, MessageCommand, and ARIA live regions
tldr: "Every AJAX content update must be announced to screen reader users. Silence after a dynamic update is a WCAG failure."
drupal_version: "11.x"
---

# Screen Reader Support

## When to Use

You need to ensure dynamic content updates are announced to screen reader users.

## Pattern

```php
use Drupal\Core\Ajax\AnnounceCommand;
use Drupal\Core\Ajax\MessageCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();

  // Method 1: AnnounceCommand (no visual indication)
  $response->addCommand(new AnnounceCommand(
    'Search results updated. 12 results found.',
    'polite'  // 'polite' or 'assertive'
  ));

  // Method 2: MessageCommand (visual + audio — announces by default)
  $response->addCommand(new MessageCommand(
    'Form saved successfully.',
    NULL,
    ['type' => 'status']
    // 4th param $clear_previous defaults to TRUE; announces via aria-live by default.
    // Pass ['announce' => ''] in options to suppress announcement.
  ));

  // Method 3: ARIA live region (in form build)
  $form['live_region'] = [
    '#type' => 'container',
    '#attributes' => [
      'id' => 'live-announcements',
      'aria-live' => 'polite',
      'aria-atomic' => 'true',
      'class' => ['visually-hidden'],  // Hidden visually, read by SR
    ],
  ];

  // Update live region content via AJAX
  $response->addCommand(new HtmlCommand(
    '#live-announcements',
    'Content loaded successfully.'
  ));

  return $response;
}
```

Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`

## Common Mistakes

- Using 'assertive' priority for non-critical updates → Interrupts current speech; use 'polite' for most cases
- Announcing technical details → Say "Form saved" not "AJAX callback executed successfully"
- Not providing context in announcements → "Updated" is vague; say "Search results updated with 5 items"
- Announcing too frequently → Overlapping announcements confuse users; debounce or combine messages
- Forgetting visual alternatives → Some users have both vision and hearing impairments; combine AnnounceCommand with visual indicators

## See Also

- ← Previous: [WCAG Compliance Patterns](wcag-compliance-patterns.md) | Next: [Debugging Techniques](debugging-techniques.md)
- Reference: [ARIA live regions specification](https://www.w3.org/TR/wai-aria-1.2/#live_region_roles)
