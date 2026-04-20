---
description: Copy to clipboard with visual feedback, Share API for native mobile share, paste sanitization — Clipboard API patterns
tldr: "Use `navigator.clipboard.writeText()` as the primary path on HTTPS. Use `navigator.share()` for mobile share sheets."
---

# Clipboard and Copy Patterns

## When to Use

> Use `navigator.clipboard.writeText()` as the primary path on HTTPS. Use `navigator.share()` for mobile share sheets. Always provide visual confirmation — without it, users retry the copy.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Write text to clipboard | `navigator.clipboard.writeText()` | Modern async API; works on HTTPS |
| Read text from clipboard | `navigator.clipboard.readText()` | Requires explicit user permission grant |
| Copy rich content (HTML) | `navigator.clipboard.write()` with `ClipboardItem` | Writes typed data, not just text |
| Share URL/title natively | `navigator.share()` | Opens OS-level share sheet on mobile |
| Legacy fallback (HTTP or old browser) | `document.execCommand('copy')` (deprecated) | Last resort only |

**Security requirements:**
- `navigator.clipboard` requires HTTPS (or localhost)
- `writeText()` requires a transient user gesture (must be called from an event handler)
- `readText()` additionally requires the `clipboard-read` permission

**Visual feedback quality:**

| Approach | Professional | Why |
|---|---|---|
| Icon swaps (clipboard → checkmark) after copy | Yes | Clear confirmation without text change |
| "Copied!" text for 2 seconds then reverts | Yes | Explicit; disappears without user action |
| No feedback at all | No | Users retry the copy because they're unsure |
| Permanent "Copied!" state | No | Breaks on second copy attempt |
| Alert dialog on copy | No | Blocks workflow for a non-destructive action |

## Pattern

```javascript
// Copy with visual feedback
async function copyToClipboard(text, button) {
  const originalLabel = button.textContent;
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = 'Copied!';
    button.setAttribute('aria-label', 'Copied to clipboard');
    setTimeout(() => { button.textContent = originalLabel; button.setAttribute('aria-label', 'Copy to clipboard'); }, 2000);
  } catch {
    button.textContent = 'Failed';
    setTimeout(() => { button.textContent = originalLabel; }, 2000);
  }
}

// Feature detection with execCommand fallback
async function safeCopy(text) {
  if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(text);
  const ta = Object.assign(document.createElement('textarea'), { value: text, style: 'position:fixed;opacity:0' });
  document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
}

// Native share with clipboard fallback
async function shareContent({ title, text, url }) {
  if (navigator.share) await navigator.share({ title, text, url });
  else await copyToClipboard(url, document.querySelector('#share-btn'));
}

// Paste sanitization (strip HTML from plain-text inputs)
element.addEventListener('paste', (e) => {
  e.preventDefault();
  const text = e.clipboardData.getData('text/plain'); // Plain text only — no XSS
  document.execCommand('insertText', false, text);
});
```

## Common Mistakes

- **Wrong**: Calling `clipboard.writeText()` outside a user gesture → **Right**: Must be called from a click/keydown handler; fails silently otherwise
- **Wrong**: Not checking `navigator.clipboard` exists → **Right**: Feature-detect before calling; crashes on HTTP pages
- **Wrong**: `execCommand` as primary path → **Right**: Use Clipboard API first; execCommand is deprecated and may be removed
- **Wrong**: No visual feedback after copy → **Right**: Users don't know it worked and press copy again
- **Wrong**: Pasting raw `text/html` clipboard data into content editable → **Right**: Always use `text/plain` or sanitize HTML with DOMPurify

## See Also

- [Form Interaction Craft](./form-interaction-craft.md) — paste handling in form inputs
- Reference: [MDN: Navigator.clipboard](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/clipboard)
- Reference: [SitePoint: Clipboard API](https://www.sitepoint.com/clipboard-api/)
