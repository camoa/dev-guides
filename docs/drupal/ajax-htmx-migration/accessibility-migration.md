---
description: "Accessibility Migration — migrate screen reader announcements and focus management from AJAX to HTMX"
tldr: "Migrate AnnounceCommand/FocusFirstCommand accessibility patterns. HTMX has no built-in focus or announce commands — add aria-live/aria-atomic to containers and use a triggerHeader() + htmx.on('announce') to call Drupal.announce()."
drupal_version: "11.x"
---

# Accessibility Migration

## When to Use

> Migrate accessibility features like screen reader announcements and focus management from AJAX to HTMX. HTMX handles most accessibility automatically but custom announcements need trigger headers.

## Pattern

**AJAX Accessibility Features:**
```php
use Drupal\Core\Ajax\AnnounceCommand;
use Drupal\Core\Ajax\FocusFirstCommand;
use Drupal\Core\Ajax\MessageCommand;

$response = new AjaxResponse();

// Screen reader announcement
$response->addCommand(new AnnounceCommand('Content loaded', 'polite'));

// Focus management
$response->addCommand(new FocusFirstCommand('#content-wrapper'));

// Message with announcement
$response->addCommand(new MessageCommand('Saved!', NULL, ['type' => 'status'], TRUE));

return $response;
```

**HTMX Accessibility Features:**

Automatically handled by HTMX in Drupal:
1. **Status messages** — Included in `HtmxRenderer` response
2. **drupalSettings updates** — Merged via `htmx-assets.js`
3. **Behavior attachment** — Via `htmx:drupal:load` event

For additional accessibility:

```php
use Drupal\Core\Htmx\Htmx;

// ARIA live regions - add to container
$form['results'] = [
  '#type' => 'container',
  '#attributes' => [
    'id' => 'search-results',
    'aria-live' => 'polite',
    'aria-atomic' => 'true',
  ],
];

// Screen reader announcements via trigger header
(new Htmx())
  ->triggerHeader([
    'announce' => [
      'message' => 'Content loaded',
      'priority' => 'polite',
    ]
  ])
  ->applyTo($build);
```

```javascript
// JavaScript listener for announcements
(function (Drupal, htmx) {
  htmx.on('announce', function(event) {
    Drupal.announce(event.detail.message, event.detail.priority);
  });
})(Drupal, htmx);
```

Reference: `HtmxRenderer` at `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`

## Common Mistakes

- **Not using ARIA live regions** → HTMX swaps don't automatically announce. Add `aria-live="polite"` to containers that update
- **Forgetting `aria-atomic`** → Use `aria-atomic="true"` so screen readers announce the full content, not just changes
- **Manual focus management** → HTMX doesn't have built-in focus commands. Use `htmx:afterSwap` event to call `.focus()` on elements
- **Assuming messages announce** → Status messages appear visually but don't announce. Use trigger header with `Drupal.announce()` for important updates
- **Not testing with screen reader** → Always test HTMX updates with a screen reader (NVDA, JAWS, VoiceOver) to verify announcements work

## See Also

- Previous: [Drupal Behavior Migration](drupal-behavior-migration.md)
- Next: [When NOT to Migrate](when-not-to-migrate.md)
- Reference: [ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions)
