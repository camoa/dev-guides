---
description: Implement modal overlays with the native <dialog> element and showModal() so the browser handles focus trapping, inert, and Escape automatically.
tldr: Use `<dialog>.showModal()` for modals — the browser makes background content inert and handles Escape; never add a custom JS focus trap to a native modal; use `inert` on background content when `<dialog>` is not viable, but the overlay must be a sibling not a descendant of the inerted element.
---

# Native Dialog

## When to Use

> Use the native `<dialog>` element with `.showModal()` for modal overlays — the browser handles inert, focus cycling, and z-ordering so you do not have to implement error-prone focus traps.

## Decision

| Need | Pattern | Avoid |
|---|---|---|
| Modal dialog (blocks background) | `<dialog>.showModal()` | Custom div + JS focus trap |
| Non-modal panel / sidebar | `<dialog>.show()` | `<dialog>.showModal()` (would trap focus unintentionally) |
| Custom overlay where `<dialog>` is not viable | `inert` attribute on background content | Manual `aria-hidden` tree-walk |
| Close on Escape | Native — browser handles it for `.showModal()` | Re-implementing Escape listener for native modals |
| Focus trap inside modal | None needed — `.showModal()` makes background inert | Manual focus trap |

**`showModal()` vs `show()`:** `.showModal()` opens the dialog in the top layer, makes all outside content inert, and handles Escape to close. `.show()` opens non-modally — focus is not trapped, background remains accessible.

**`inert` DOM structure:** The custom overlay must NOT be a descendant of the `inert` element.

```html
<!-- WRONG: overlay inside inerted container -->
<div id="app" inert>
  <div class="overlay">...</div>  <!-- unreachable -->
</div>

<!-- CORRECT: overlay outside inerted content -->
<div id="page-content" inert>...</div>
<div class="overlay">...</div>
```

## Pattern

```html
<button id="open-btn">Open settings</button>

<dialog id="settings-dialog" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Account Settings</h2>
  <p>Update your details here.</p>
  <button onclick="this.closest('dialog').close()">Close</button>
</dialog>

<script>
  document.getElementById('open-btn').addEventListener('click', () => {
    document.getElementById('settings-dialog').showModal();
  });
</script>
```

Name the dialog by pointing `aria-labelledby` at the visible heading — do not use `aria-label` unless no visible heading exists.

## Common Mistakes

- **Wrong**: Adding a JS focus trap to a native modal dialog → **Right**: `.showModal()` already handles this; custom traps create double focus management and bugs
- **Wrong**: Using `.show()` when modal behavior is expected → **Right**: Background content remains interactive; AT users can navigate out of the dialog
- **Wrong**: Removing the native Escape-to-close behavior → **Right**: `.showModal()` handles Escape; do not `preventDefault()` on Escape unless you have a close-confirmation workflow
- **Wrong**: `inert` on the element containing the overlay → **Right**: The overlay becomes unreachable; restructure DOM so the overlay is a sibling

## See Also

- [Keyboard and Focus](keyboard-and-focus.md) — focus restoration after dialog close
- [Live Regions](live-regions.md) — coordinating announcements with inert toggling
- Reference: https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal
- Reference: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inert
