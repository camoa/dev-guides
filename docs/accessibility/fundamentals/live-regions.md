---
description: Announce dynamic DOM changes to screen readers using aria-live regions without creating constant noise.
tldr: Maintain two centralized live regions (one polite, one assertive) rather than scattering them per component; use `assertive` only for critical time-sensitive events; clear the region then set on the next animation frame to guarantee re-announcement of identical messages.
---

# Live Regions

## When to Use

> Use live regions when the DOM changes without a focus move and users need to know about it — but treat them as a scarce resource; overuse creates constant noise for screen-reader users.

## Decision: Urgency Table

| Urgency | Visual analogue | `aria-live` value | Example |
|---|---|---|---|
| **Critical** | Modal / alert | `assertive` (or `role="alert"`) | Session timeout, API failure, data loss |
| **Standard** | Toast / status banner | `polite` | Search results loaded, "Saved" confirmation |
| **Passive** | Silent counter | `off` | Live character count |

**Rule:** Use `assertive` only for critical, time-sensitive events. Nearly every other update should be `polite`.

## Pattern: Centralized Announcer

```html
<!-- Place once, near <body> open, before page content -->
<div id="announcer-polite" aria-live="polite" aria-atomic="true" class="visually-hidden"></div>
<div id="announcer-assertive" aria-live="assertive" aria-atomic="true" class="visually-hidden"></div>
```

```javascript
function announce(message, urgency = 'polite') {
  const el = document.getElementById(`announcer-${urgency}`);
  // Clear then set — guarantees re-announcement of identical messages
  el.textContent = '';
  requestAnimationFrame(() => { el.textContent = message; });
}
```

Many frameworks (Angular CDK, React aria-live, Drupal `Drupal.announce()`) ship an announcer abstraction — use it instead of building your own.

## Rules

- **Debounce high-frequency updates**: If a region can update many times per second (e.g., search result count while typing), debounce by 300–500ms
- **Delay near focus management**: Add 50–100ms delay before announcing so live-region updates do not overlap other speech
- **Avoid interstitial-state noise**: "Loading…" announcements almost always create more interruption than value — announce the result state, not the in-progress state
- **Coordinate with `inert`**: When a dialog opens and sections become `inert`, cancel pending announcements targeting those regions

## Common Mistakes

- **Wrong**: Multiple `aria-live` regions scattered per component → **Right**: Merge into two centralized regions; scattered regions produce unpredictable speech queue behavior
- **Wrong**: `role="alert"` on a container that updates every keystroke → **Right**: Assertive + frequent = unusable
- **Wrong**: Announcing "Loading..." then the result → **Right**: Often double-announces; skip the loading state or test thoroughly
- **Wrong**: Forgetting to clear the region before re-setting → **Right**: Identical text does not re-trigger; clear then set on next animation frame

## See Also

- [Forms Accessibility](forms-accessibility.md) — error live-region coordination
- [Native Dialog](native-dialog.md) — coordinating announcements with inert toggling
- Reference: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-live
