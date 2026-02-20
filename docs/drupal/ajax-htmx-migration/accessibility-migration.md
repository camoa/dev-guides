---
description: Migrate AJAX accessibility features — ARIA live regions, screen reader announcements, and focus management for HTMX swaps
drupal_version: "11.x"
---

# Accessibility Migration

## When to Use

> Use this when migrating `AnnounceCommand`, `FocusFirstCommand`, and screen reader patterns from AJAX to HTMX. HTMX handles messages automatically but custom announcements need trigger headers.

## Decision

| AJAX feature | HTMX equivalent | How |
|---|---|---|
| `AnnounceCommand` | `triggerHeader` + `Drupal.announce()` | Fire event, call announce in JS listener |
| `FocusFirstCommand` | `htmx:afterSwap` event + `.focus()` | Listen for swap, set focus manually |
| `MessageCommand` | Auto-included | `HtmxRenderer` includes status messages |
| `SettingsCommand` | Auto-merged | `htmx-assets.js` merges settings |
| Screen reader regions | `aria-live` + `aria-atomic` on container | Declare in render array attributes |

## Pattern

**AJAX — explicit commands:**
```php
$response->addCommand(new AnnounceCommand('Content loaded', 'polite'));
$response->addCommand(new FocusFirstCommand('#content-wrapper'));
$response->addCommand(new MessageCommand('Saved!', NULL, ['type' => 'status'], TRUE));
```

**HTMX — ARIA live regions + trigger header:**
```php
use Drupal\Core\Htmx\Htmx;

// ARIA live region on the container
$form['results'] = [
  '#type' => 'container',
  '#attributes' => [
    'id' => 'search-results',
    'aria-live' => 'polite',
    'aria-atomic' => 'true',
  ],
];

// Screen reader announcement via trigger header
(new Htmx())
  ->triggerHeader(['announce' => ['message' => 'Content loaded', 'priority' => 'polite']])
  ->applyTo($build);
```

```javascript
// Listen and call Drupal.announce()
(function (Drupal, htmx) {
  htmx.on('announce', function(event) {
    Drupal.announce(event.detail.message, event.detail.priority);
  });
})(Drupal, htmx);
```

## Common Mistakes

- **Not using ARIA live regions** → HTMX swaps do not automatically announce. Add `aria-live="polite"` to containers that update
- **Forgetting `aria-atomic`** → Use `aria-atomic="true"` so screen readers announce the full content, not just the change
- **Manual focus management** → HTMX has no built-in focus commands. Use `htmx:afterSwap` event to call `.focus()` on elements
- **Assuming messages announce automatically** → Status messages appear visually but do not announce. Use `triggerHeader` + `Drupal.announce()` for important updates
- **Not testing with a screen reader** → Always test HTMX updates with NVDA, JAWS, or VoiceOver to verify announcements work

## See Also

- Previous: [Drupal Behavior Migration](drupal-behavior-migration.md)
- Next: [When NOT to Migrate](when-not-to-migrate.md)
- Reference: [ARIA live regions (MDN)](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions)
- Source: `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`
