---
description: Validation timing, auto-resize textarea, input masking, autosave, inline editing, and multi-step form state — form UX patterns
tldr: "Validate on blur for the first time. After the first error, switch to live validation."
---

# Form Interaction Craft

## When to Use

> Validate on blur for the first time. After the first error, switch to live validation. Never validate on every keystroke for format errors — it destroys UX.

## Pattern: Input Masking (Phone Number)

```javascript
function phoneMask(input) {
  input.addEventListener('input', (e) => {
    const digits = e.target.value.replace(/\D/g, '').slice(0, 10);
    const parts = [digits.slice(0,3), digits.slice(3,6), digits.slice(6)].filter(Boolean);
    e.target.value = parts.length === 1 ? parts[0]
      : parts.length === 2 ? `(${parts[0]}) ${parts[1]}`
      : `(${parts[0]}) ${parts[1]}-${parts[2]}`;
  });
}
```

**Input masking rules:** Always strip and reformat — never prevent keystrokes. Supporting copy-paste with existing formatting (e.g. `(555) 123-4567` pasted in) is critical for UX; strip all non-digits and reformat. The UK Government Digital Service research found flexible separators improved form completion by 18%.

## Decision

| Timing | Trigger | Use When |
|---|---|---|
| On blur (after field exit) | `focusout` event | Default for most fields — user had a chance to complete input |
| On submit only | `submit` event | Short forms, destructive actions, low-stakes data |
| After first blur, then live | `focusout` → switch to `input` | Best UX: don't interrupt typing, fix errors in real-time after first attempt |
| Live from first keystroke | `input` event | Password strength indicator only — never for format validation |
| On keystroke with debounce | `input` + debounce(300ms) | Username availability check, async validation |

**Multi-step form state:**

| Approach | Use When |
|---|---|
| Single page, hide/show sections | < 5 steps, all data needed together at submit |
| Separate URL per step | > 5 steps, users may need to bookmark or share a step |
| Wizard with back/next | Complex forms where later steps depend on earlier answers |

## Pattern

```javascript
// Smart validation — validate on blur, then live after first error
function smartValidation(input, validate) {
  let hasBlurred = false;
  input.addEventListener('blur', () => { hasBlurred = true; showError(input, validate(input.value)); });
  input.addEventListener('input', () => { if (hasBlurred) showError(input, validate(input.value)); });
}

// Auto-resize textarea
function autoResize(textarea) {
  function resize() { textarea.style.height = 'auto'; textarea.style.height = `${textarea.scrollHeight}px`; }
  textarea.addEventListener('input', resize);
  resize();
}

// Autosave with debounce + status feedback
function autosave(form, saveFn) {
  const status = form.querySelector('[data-autosave-status]');
  const save = debounce(async () => {
    status.textContent = 'Saving...';
    try { await saveFn(new FormData(form)); status.textContent = 'Saved'; setTimeout(() => { status.textContent = ''; }, 3000); }
    catch { status.textContent = 'Save failed — check your connection'; }
  }, 1000);
  form.addEventListener('input', save);
  window.addEventListener('beforeunload', () => saveFn(new FormData(form))); // Safety net
}

// Click-to-edit inline
function inlineEdit(displayEl, editEl, saveFn) {
  displayEl.addEventListener('dblclick', () => {
    displayEl.hidden = true; editEl.hidden = false; editEl.value = displayEl.textContent; editEl.focus(); editEl.select();
  });
  async function commit() {
    const value = editEl.value.trim();
    if (value && value !== displayEl.textContent) { await saveFn(value); displayEl.textContent = value; }
    displayEl.hidden = false; editEl.hidden = true;
  }
  editEl.addEventListener('blur', commit);
  editEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); commit(); }
    if (e.key === 'Escape') { displayEl.hidden = false; editEl.hidden = true; }
  });
}
```

**Error message craft:**

| Rule | Example |
|---|---|
| Specific, not generic | "Email must include @" not "Invalid email" |
| Actionable | "Password must be 8+ characters" not "Password too short" |
| Inline under field | Never at top of form only |
| Screen reader announcement | `aria-live="polite"` region for dynamic errors |

## Common Mistakes

- **Wrong**: Validating on every keystroke → **Right**: Error flashes immediately before user finishes typing; use blur + debounce
- **Wrong**: Preventing paste in masked inputs → **Right**: Users cannot paste formatted phone numbers from contacts; strip and reformat instead
- **Wrong**: Autosave without status feedback → **Right**: User doesn't know data is saved; exits without confidence
- **Wrong**: `onclick` for inline edit trigger → **Right**: Add `keydown Enter` too — onclick is mouse-only
- **Wrong**: Multi-step form with no back navigation → **Right**: WCAG 3.3.4 violation; always allow review and correction
- **Wrong**: Multi-step state in JS variables only → **Right**: Use `sessionStorage` or URL params; page refresh clears JS state

## See Also

- [Keyboard Navigation Craft](./keyboard-navigation-craft.md) — keyboard handling within form widgets
- [Debounce and Throttle](./debounce-and-throttle.md) — debounce for search inputs and async validation
- [Optimistic UI](./optimistic-ui.md) — autosave pending state patterns
- Reference: [Smashing Magazine: Inline Validation UX](https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/)
