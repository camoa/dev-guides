---
description: "Copy to clipboard with visual feedback, Share API for native mobile share, paste sanitization — Clipboard API patterns"
tldr: "Use `navigator.clipboard.writeText()` as the primary path on HTTPS. Use `navigator.share()` for mobile share sheets."
---

# Clipboard and Copy Patterns

## When to Use

> Copy-to-clipboard buttons, code snippet sharing, referral links, one-time codes. The Clipboard API reached Baseline status in March 2025 and is supported across all modern browsers. Always provide visual confirmation — without it, users don't know the copy succeeded.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Write text to clipboard | `navigator.clipboard.writeText()` | Modern async API; works on HTTPS |
| Read text from clipboard | `navigator.clipboard.readText()` | Requires explicit user permission grant |
| Copy rich content (HTML) | `navigator.clipboard.write()` with `ClipboardItem` | Writes typed data, not just text |
| Share URL/title natively | `navigator.share()` | Opens OS-level share sheet on mobile |
| Legacy fallback (HTTP or old browser) | `document.execCommand('copy')` (deprecated) | Last resort only — execCommand is deprecated and may be removed |

**Security requirements:**
- `navigator.clipboard` requires HTTPS (or localhost)
- `writeText()` requires transient user activation (must be called from a user gesture)
- `readText()` requires the `clipboard-read` permission in addition to user activation

## Pattern: Copy with Visual Feedback

```javascript
async function copyToClipboard(text, button) {
  const originalLabel = button.textContent;
  const originalIcon = button.querySelector('[data-icon]')?.getAttribute('data-icon');

  try {
    await navigator.clipboard.writeText(text);
    // Success feedback
    button.textContent = 'Copied!';
    if (originalIcon) button.querySelector('[data-icon]').setAttribute('data-icon', 'check');
    button.setAttribute('aria-label', 'Copied to clipboard');
    setTimeout(() => {
      button.textContent = originalLabel;
      if (originalIcon) button.querySelector('[data-icon]').setAttribute('data-icon', originalIcon);
      button.setAttribute('aria-label', 'Copy to clipboard');
    }, 2000);
  } catch {
    button.textContent = 'Failed';
    setTimeout(() => { button.textContent = originalLabel; }, 2000);
  }
}
```

## Pattern: Feature Detection and Fallback

```javascript
async function safeCopy(text) {
  if (navigator.clipboard?.writeText) {
    // Modern path — HTTPS required
    return navigator.clipboard.writeText(text);
  }
  // Deprecated fallback — execCommand (may fail in some browsers)
  const ta = Object.assign(document.createElement('textarea'), {
    value: text, style: 'position:fixed;opacity:0'
  });
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');   // Deprecated — only use as last resort
  ta.remove();
}
```

## Pattern: Share API (Mobile Native Share)

```javascript
async function shareContent({ title, text, url }) {
  if (navigator.share) {
    // Native OS share sheet — mobile first
    await navigator.share({ title, text, url });
  } else {
    // Desktop fallback — copy URL
    await copyToClipboard(url, document.querySelector('#share-btn'));
  }
}
```

## Visual Feedback Quality Table

| Approach | Professional | Why |
|---|---|---|
| Icon swaps (clipboard → checkmark) after copy | Yes | Clear visual confirmation without text change |
| "Copied!" text for 2 seconds then reverts | Yes | Explicit, disappears without user action |
| Toast notification on copy | Yes for bulk copy actions | Don't use toast for individual copy buttons — too heavy |
| No feedback at all | No | Users retry the copy because they're unsure it worked |
| Permanent state change (stays "Copied!") | No | Breaks on second copy attempt |
| Alert dialog on copy | No | Blocks workflow for a non-destructive action |

## Paste Handling and Sanitization

Never trust clipboard content. When pasting:
- Strip HTML from plain-text inputs: `clipboardData.getData('text/plain')` instead of `text/html`
- Sanitize HTML before inserting into rich text editors: use DOMPurify or equivalent
- Limit paste size for performance — large pastes can freeze the browser

```javascript
element.addEventListener('paste', (e) => {
  e.preventDefault();
  const text = e.clipboardData.getData('text/plain'); // Plain text only
  document.execCommand('insertText', false, text);    // Insert at cursor
});
```

## Common Mistakes

- **Calling `clipboard.writeText()` from a non-user-gesture context** — fails silently (promise rejects)
- **Not checking `navigator.clipboard` exists before calling** — crashes on HTTP pages
- **Using the deprecated `execCommand` as the primary path** — it may be removed; use Clipboard API first
- **No visual feedback after copy** — users don't know it worked and press copy again
- **Feedback that never reverts** — confusing on repeated copies
- **Pasting raw HTML from `text/html` into a content editable** — XSS vector if content comes from untrusted sources

## See Also

- [Form Interaction Craft](./form-interaction-craft.md) — paste handling in form inputs
- Reference: [MDN: Navigator.clipboard](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/clipboard)
- Reference: [SitePoint: Clipboard API](https://www.sitepoint.com/clipboard-api/)
