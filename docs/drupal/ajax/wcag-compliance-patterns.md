---
description: Make AJAX interactions accessible to keyboard users and screen readers — WCAG 2.1 Level AA patterns
tldr: "Apply these patterns to every AJAX implementation. Accessibility is not optional — WCAG 2.1 Level AA is the standard for Drupal sites."
drupal_version: "11.x"
---

# WCAG Compliance Patterns

## When to Use

You need to make AJAX interactions accessible to keyboard users, screen reader users, and users with disabilities (WCAG 2.1 Level AA compliance).

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Screen reader announcements | AnnounceCommand or MessageCommand | WCAG 4.1.3 - users know content changed |
| Focus management | FocusFirstCommand | WCAG 2.4.3 - keyboard users maintain context |
| Keyboard access | keypress: TRUE in #ajax | WCAG 2.1.1 - keyboard-only users can trigger AJAX |
| Live region updates | aria-live attributes | WCAG 1.3.1 - announces dynamic changes |
| Loading indicators | Accessible progress messages | WCAG 2.2.1 - users know operation in progress |

## Pattern

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\AnnounceCommand;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\FocusFirstCommand;
use Drupal\Core\Ajax\MessageCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();

  // 1. Update content
  $response->addCommand(new ReplaceCommand('#results', $updated_content));

  // 2. Announce change to screen readers
  $response->addCommand(new AnnounceCommand(
    'Results updated with 5 new items',
    'polite'  // Use 'assertive' only for errors
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
    'keypress' => TRUE,  // CRITICAL: enables ENTER/SPACE triggering
  ],
];

// Accessible loading indicator
$form['trigger']['#ajax']['progress'] = [
  'type' => 'throbber',
  'message' => t('Loading more results...'),  // Read by screen readers
];

// ARIA live region for dynamic content
$form['results'] = [
  '#type' => 'container',
  '#attributes' => [
    'id' => 'results',
    'aria-live' => 'polite',  // Announces content changes
    'aria-atomic' => 'true',  // Reads entire region on update
  ],
];
```

Reference: `core/lib/Drupal/Core/Ajax/AnnounceCommand.php`, `core/lib/Drupal/Core/Ajax/FocusFirstCommand.php`

## Common Mistakes

- Not announcing AJAX updates → WCAG 4.1.3 violation; screen reader users don't know content changed
- Missing `keypress: TRUE` on AJAX buttons → WCAG 2.1.1 violation; keyboard users can't trigger AJAX
- Not managing focus after updates → Users lose context; use FocusFirstCommand or InvokeCommand('focus')
- Using 'assertive' aria-live unnecessarily → Interrupts screen readers; reserve for errors
- Missing loading indicators → Users don't know operation in progress (WCAG 2.2.1)
- Not testing with screen readers → Use NVDA (Windows), JAWS (Windows), or VoiceOver (Mac) to verify

## See Also

- ← Previous: [Response Caching](response-caching.md) | Next: [Screen Reader Support](screen-reader-support.md)
- [Feedback Commands](feedback-commands.md)
- Reference: [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/), [Drupal Accessibility documentation](https://www.drupal.org/about/features/accessibility)
