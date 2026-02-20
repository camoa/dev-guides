---
description: Make AJAX interactions accessible to keyboard users and screen readers — WCAG 2.1 Level AA patterns
drupal_version: "11.x"
---

# WCAG Compliance Patterns

## When to Use

> Apply these patterns to every AJAX implementation. Accessibility is not optional — WCAG 2.1 Level AA is the standard for Drupal sites.

## Decision

| If you need... | Use... | WCAG Criterion |
|----------------|--------|----------------|
| Screen reader announcements | AnnounceCommand or MessageCommand | 4.1.3 |
| Focus management after updates | FocusFirstCommand | 2.4.3 |
| Keyboard AJAX triggers | `keypress: TRUE` in `#ajax` | 2.1.1 |
| Live region updates | `aria-live` attributes | 1.3.1 |
| Loading indicators | Accessible progress messages | 2.2.1 |

## Pattern

```php
use Drupal\Core\Ajax\AnnounceCommand;
use Drupal\Core\Ajax\FocusFirstCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();

  // 1. Update content
  $response->addCommand(new ReplaceCommand('#results', $updated_content));

  // 2. Announce change to screen readers
  $response->addCommand(new AnnounceCommand(
    'Results updated with 5 new items',
    'polite'  // 'assertive' only for errors
  ));

  // 3. Manage focus for keyboard users
  $response->addCommand(new FocusFirstCommand('#results'));

  return $response;
}

// Keyboard-accessible AJAX trigger
$form['trigger'] = [
  '#type' => 'button',
  '#value' => t('Load More'),
  '#ajax' => [
    'callback' => '::loadMore',
    'wrapper' => 'results',
    'keypress' => TRUE,  // Enables ENTER/SPACE triggering
    'progress' => [
      'type' => 'throbber',
      'message' => t('Loading more results...'),  // Read by screen readers
    ],
  ],
];

// ARIA live region for dynamic content
$form['results'] = [
  '#type' => 'container',
  '#attributes' => [
    'id' => 'results',
    'aria-live' => 'polite',
    'aria-atomic' => 'true',
  ],
];
```

Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`, `core/lib/Drupal/Core/Ajax/FocusFirstCommand.php`

## Common Mistakes

- **Wrong**: Not announcing AJAX updates → **Right**: WCAG 4.1.3 violation; screen reader users don't know content changed
- **Wrong**: Missing `keypress: TRUE` on AJAX buttons → **Right**: WCAG 2.1.1 violation; keyboard users can't trigger AJAX
- **Wrong**: Not managing focus after updates → **Right**: Use FocusFirstCommand or InvokeCommand('focus')
- **Wrong**: Using 'assertive' aria-live unnecessarily → **Right**: Reserve for errors; 'polite' for most content updates
- **Wrong**: Not testing with screen readers → **Right**: Test with NVDA (Windows), JAWS (Windows), or VoiceOver (Mac)

## See Also

- [Screen Reader Support](screen-reader-support.md)
- [Feedback Commands](feedback-commands.md)
- Reference: [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/), [Drupal Accessibility](https://www.drupal.org/about/features/accessibility)
