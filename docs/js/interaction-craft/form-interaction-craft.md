---
description: "Validation timing, auto-resize textarea, input masking, autosave, inline editing, and multi-step form state — form UX patterns"
tldr: "Validate on blur for the first time. After the first error, switch to live validation."
---

# Form Interaction Craft

## When to Use

> Any form that goes beyond basic HTML submit — real-time validation, rich input formatting, autosave, inline editing, multi-step flows. These patterns add responsiveness and professionalism, but the wrong validation timing is more damaging than no JS at all.

## Decision: Validation Timing

| Timing | Trigger | Use When |
|---|---|---|
| On blur (after field exit) | `focusout` event | Default for most fields — user had a chance to complete input |
| On submit only | `submit` event | Short forms (2-3 fields), destructive actions, low-stakes data |
| After first blur, then live | `focusout` → switch to `input` | Best UX: don't interrupt typing, fix errors in real-time after first attempt |
| Live from first keystroke | `input` event | Password strength indicator only — never for format validation |
| On keystroke with debounce | `input` + debounce(300ms) | Username availability check, async validation |

**The Smashing Magazine rule (2022):** Never show errors before the user has had a chance to type. Validate on `blur` for the first time. After the first error, switch to live validation so errors disappear as the user corrects them.

```javascript
function smartValidation(input, validate) {
  let hasBlurred = false;
  input.addEventListener('blur', () => {
    hasBlurred = true;
    showError(input, validate(input.value));
  });
  input.addEventListener('input', () => {
    if (hasBlurred) showError(input, validate(input.value)); // Live only after first blur
  });
}
```

## Pattern: Auto-Resize Textarea

```javascript
function autoResize(textarea) {
  function resize() {
    textarea.style.height = 'auto';         // Reset to shrink if text removed
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
  textarea.addEventListener('input', resize);
  resize(); // Initialize
}
```

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

## Pattern: Autosave with Debounce

```javascript
function autosave(form, saveFn) {
  let status = form.querySelector('[data-autosave-status]');
  const debouncedSave = debounce(async () => {
    status.textContent = 'Saving...';
    try {
      await saveFn(new FormData(form));
      status.textContent = 'Saved';
      setTimeout(() => { status.textContent = ''; }, 3000);
    } catch {
      status.textContent = 'Save failed — check your connection';
    }
  }, 1000);

  form.addEventListener('input', debouncedSave);
  // Save before unload as safety net
  window.addEventListener('beforeunload', () => saveFn(new FormData(form)));
}
```

## Pattern: Click-to-Edit (Inline Editing)

```javascript
function inlineEdit(displayEl, editEl, saveFn) {
  displayEl.addEventListener('dblclick', () => {
    displayEl.hidden = true;
    editEl.hidden = false;
    editEl.value = displayEl.textContent;
    editEl.focus();
    editEl.select();
  });

  async function commit() {
    const value = editEl.value.trim();
    if (value && value !== displayEl.textContent) {
      await saveFn(value);
      displayEl.textContent = value;
    }
    displayEl.hidden = false;
    editEl.hidden = true;
  }

  editEl.addEventListener('blur', commit);
  editEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); commit(); }
    if (e.key === 'Escape') { displayEl.hidden = false; editEl.hidden = true; }
  });
}
```

## Multi-Step Form State

| Approach | Use When |
|---|---|
| Single page, hide/show sections | < 5 steps, all data needed together at submit |
| Separate URL per step | > 5 steps, users may need to bookmark or share a step |
| Wizard with back/next | Complex forms where later steps depend on earlier answers |

State management rule: never lose data when navigating backward. Store state in `sessionStorage` or URL params, not just JS variables (page refresh would clear it).

## Error Message Craft

| Rule | Example |
|---|---|
| Specific, not generic | "Email must include @" not "Invalid email" |
| Actionable | "Password must be 8+ characters" not "Password too short" |
| Positive framing | "Enter a valid date like 01/31/2025" not "Wrong date format" |
| Inline under field | Never at top of form only — user must scroll to find it |
| Screen reader announcement | Use `aria-live="polite"` region for dynamically injected errors |

## Common Mistakes

- **Validating on every keystroke** — error flashes immediately before user finishes typing; destroys UX
- **No client-side validation** — every error requires a round trip; poor UX
- **Preventing paste in masked inputs** — users cannot paste formatted phone numbers from contacts
- **Autosave without status feedback** — user doesn't know data is saved; exits without confidence
- **`onclick` for inline edit trigger** — mouse-only; add `keydown Enter` for keyboard users
- **Multi-step form with no back navigation** — WCAG 3.3.4 violation; always allow review and correction

## See Also

- [Keyboard Navigation Craft](./keyboard-navigation-craft.md) — keyboard handling within form widgets
- [Debounce and Throttle](./debounce-and-throttle.md) — debounce for search inputs and async validation
- [Optimistic UI](./optimistic-ui.md) — autosave pending state patterns
- Reference: [Smashing Magazine: Inline Validation UX](https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/)
