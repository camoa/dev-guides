---
description: Decide when to apply ARIA roles, states, and properties — native HTML almost always suffices and ARIA should be the exception.
tldr: Use native HTML elements first (`<button>`, `<nav>`, `<ul>`); apply ARIA only when no native equivalent exists; when you set an ARIA role you MUST implement its full keyboard behavior or the result is worse than no ARIA at all.
---

# ARIA Usage

## When to Use

> Apply ARIA when native HTML semantics are insufficient — but native HTML is almost always sufficient, so ARIA should be the exception, not the default.

## Decision

| Situation | Correct approach | Wrong approach |
|---|---|---|
| Need a clickable button | `<button>` | `<div role="button">` |
| Need a navigation region | `<nav>` | `<div role="navigation">` |
| Need to mark a field required | `required` attribute | `aria-required="true"` on the same field |
| Need to announce list items | `<ul>` / `<ol>` | `<div role="list">` |
| Custom widget with no HTML equivalent | ARIA role + keyboard behavior in JS | ARIA role without implementing keyboard |
| Toolbar button currently unavailable | `aria-disabled="true"` | `disabled` attribute |
| Focusable element that should be unavailable but discoverable | `aria-disabled="true"` | `disabled` (removes from tab order entirely) |

**`disabled` vs `aria-disabled`:** `disabled` removes the element from the focus order entirely — `tabindex="0"` will not override this. Use `aria-disabled="true"` when the element should remain focusable so users can learn why it is disabled.

**The Safari list caveat:** Safari removes list semantics from `<ul>` / `<ol>` when `list-style: none`, `display: flex`, or `display: grid` is applied outside a `<nav>`. In that case `role="list"` is required to restore semantics — the one case where a redundant-looking ARIA role is correct.

## Pattern

```html
<!-- ARIA when genuinely needed: custom tab widget -->
<div role="tablist" aria-label="Report sections">
  <button role="tab" aria-selected="true" aria-controls="panel-summary" id="tab-summary">
    Summary
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-detail" id="tab-detail" tabindex="-1">
    Detail
  </button>
</div>
<div role="tabpanel" id="panel-summary" aria-labelledby="tab-summary">...</div>
```

When you set `role="tab"`, the element MUST behave like a tab: arrow key navigation, `aria-selected` state management, `tabindex="-1"` for non-selected tabs.

## Common Mistakes

- **Wrong**: `<div role="button">` instead of `<button>` → **Right**: `<button>` gets Enter/Space, focus, and pointer for free
- **Wrong**: `<input required aria-required="true">` → **Right**: `required` already implies `aria-required`; the duplicate is noise
- **Wrong**: Setting ARIA role without implementing the required keyboard pattern → **Right**: ARIA roles without matching keyboard behavior create a broken experience worse than no ARIA
- **Wrong**: Assuming `aria-hidden` makes an element invisible → **Right**: It only hides from AT; the element is still visible and focusable unless also removed with `display: none` or `inert`

## See Also

- [Keyboard and Focus](keyboard-and-focus.md) — required keyboard patterns for custom widgets
- Reference: https://www.w3.org/WAI/ARIA/apg/ (ARIA Authoring Practices Guide)
- Reference: https://www.w3.org/TR/wai-aria-1.2/
