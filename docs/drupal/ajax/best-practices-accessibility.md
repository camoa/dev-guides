---
description: Accessibility requirements for every Drupal AJAX implementation — WCAG 2.1 Level AA checklist and patterns
drupal_version: "11.x"
---

# Best Practices: Accessibility

## When to Use

> Every AJAX implementation must meet WCAG 2.1 Level AA. This is not optional — it's a legal and ethical requirement. Use this guide as a pre-deployment checklist.

## Decision

| Requirement | Implementation | WCAG Criterion |
|-------------|----------------|----------------|
| Announce all content updates | AnnounceCommand or MessageCommand | 4.1.3 |
| Keyboard access to AJAX triggers | `'keypress' => TRUE` in `#ajax` | 2.1.1 |
| Manage focus after updates | FocusFirstCommand | 2.4.3 |
| Loading state announcements | Progress message in `#ajax` | 2.2.1 |
| Dynamic region markup | `aria-live`, `aria-atomic` | 1.3.1 |

## Pattern

```php
// Screen reader announcements
$response->addCommand(new AnnounceCommand('Results updated with 5 items', 'polite'));

// Keyboard trigger
$form['trigger']['#ajax']['keypress'] = TRUE;

// Focus management
$response->addCommand(new FocusFirstCommand('#new-content-region'));

// ARIA attributes on dynamic regions
$form['results'] = [
  '#type' => 'container',
  '#attributes' => [
    'id' => 'results',
    'aria-live' => 'polite',
    'aria-atomic' => 'true',
    'aria-busy' => 'false',  // Set to 'true' during loading via InvokeCommand
  ],
];

// Loading indicator with accessible message
$form['trigger']['#ajax']['progress'] = [
  'type' => 'throbber',
  'message' => t('Loading, please wait...'),
];
```

**Accessibility testing checklist:**

- [ ] Unplug mouse — navigate entire workflow with keyboard only
- [ ] Test with NVDA (Windows), JAWS (Windows), or VoiceOver (Mac)
- [ ] Verify all AJAX triggers are keyboard-accessible
- [ ] Confirm screen reader announces all content changes
- [ ] Check focus doesn't get lost after updates
- [ ] Verify loading indicators are announced
- [ ] Test with browser zoom at 200%
- [ ] Run automated checks with axe DevTools or WAVE

## Common Mistakes

- **Wrong**: No screen reader announcement after AJAX update → **Right**: WCAG 4.1.3 violation; always announce with AnnounceCommand
- **Wrong**: AJAX buttons only respond to click → **Right**: WCAG 2.1.1 violation; add `'keypress' => TRUE`
- **Wrong**: Focus left on stale element after update → **Right**: WCAG 2.4.3; use FocusFirstCommand to restore context
- **Wrong**: 'assertive' for non-critical updates → **Right**: Interrupts screen readers; 'polite' for most updates
- **Wrong**: Skipping manual testing with screen readers → **Right**: Automated tools miss most ARIA issues; test with real assistive technology

## See Also

- [WCAG Compliance Patterns](wcag-compliance-patterns.md)
- [Screen Reader Support](screen-reader-support.md)
- Reference: [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/), [Drupal Accessibility](https://www.drupal.org/about/features/accessibility)
