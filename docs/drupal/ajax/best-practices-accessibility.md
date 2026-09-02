---
description: Accessibility requirements for every Drupal AJAX implementation — WCAG 2.1 Level AA checklist and patterns
tldr: "Every AJAX implementation must meet WCAG 2.1 Level AA. This is not optional — it's a legal and ethical requirement."
drupal_version: "11.x"
---

# Best Practices: Accessibility

## When to Use

Every AJAX implementation must meet WCAG 2.1 Level AA standards.

## Accessibility Requirements

**Accessibility Requirements:**

1. **Screen Reader Announcements**
   - Announce all content updates using AnnounceCommand or MessageCommand
   - Use 'polite' priority for non-critical updates
   - Use 'assertive' only for errors requiring immediate attention
   - Provide meaningful context ("Search results updated with 5 items" not "Updated")

2. **Keyboard Navigation**
   - Add `'keypress' => TRUE` to all AJAX buttons
   - Manage focus after updates with FocusFirstCommand
   - Ensure all triggers are keyboard-accessible (no click-only elements)
   - Test with Tab, Enter, Space, Esc keys

3. **Focus Management**
   - Return focus to logical element after update
   - Don't move focus unexpectedly (confuses users)
   - Use FocusFirstCommand for new content regions
   - Close dialogs with Esc key (built-in to dialog system)

4. **Loading Indicators**
   - Provide progress messages read by screen readers
   - Show visual loading states (spinners, progress bars)
   - Disable triggering element during processing (prevent double-submit)
   - Clear loading state after completion

5. **ARIA Attributes**
   - Use `aria-live="polite"` for dynamic regions
   - Use `aria-atomic="true"` to read entire updated region
   - Add `aria-busy="true"` during loading
   - Mark expanded/collapsed states with `aria-expanded`

## Accessibility Testing Checklist

**Accessibility Testing Checklist:**

- [ ] Unplug mouse, navigate entire workflow with keyboard only
- [ ] Test with NVDA (Windows), JAWS (Windows), or VoiceOver (Mac)
- [ ] Verify all AJAX triggers are keyboard-accessible
- [ ] Confirm screen reader announces all content changes
- [ ] Check focus doesn't get lost after updates
- [ ] Verify loading indicators are announced
- [ ] Test with browser zoom at 200%
- [ ] Run automated tests with axe DevTools or WAVE

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

## See Also

- ← Previous: [Best Practices: Development Standards](best-practices-development.md)
- [WCAG Compliance Patterns](wcag-compliance-patterns.md)
- [Screen Reader Support](screen-reader-support.md)
- Reference: [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/), [Drupal Accessibility](https://www.drupal.org/about/features/accessibility)
