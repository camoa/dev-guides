---
description: "Trap focus in modals, implement roving tabindex for widget groups, restore focus after close — WCAG keyboard accessibility patterns"
tldr: "Use native HTML for single elements (buttons, links). Use roving tabindex for groups of related controls (tabs, toolbars, menus)."
---

# Keyboard Navigation Craft

## When to Use

> Any interactive component that goes beyond a native button, link, or form element. The W3C ARIA Authoring Practices Guide (APG) defines the patterns — this section covers the implementation craft.
>
> **The core mental model:** Tab moves between components. Arrow keys move within a component. Keep Tab stream short by grouping related controls into a single tab stop with internal arrow navigation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single interactive element (button, link) | Native HTML — no JS needed | Browser handles Tab, Enter, Space natively |
| Group of related controls (tabs, toolbar, menu) | Roving tabindex | One Tab stop, arrow keys inside |
| Modal/dialog that must isolate focus | Focus trap | Prevents Tab from escaping to background |
| Focus ring after element removed from DOM | Focus restoration to trigger | Screen readers need context of where they were |
| Skip navigation to main content | Skip link (first in DOM, shown on focus) | WCAG 2.4.1 requirement |
| Background content when overlay is open | `inert` attribute | Prevents interaction AND keyboard focus without JS |

## Pattern: Focus Trap

```javascript
function createFocusTrap(container) {
  const focusable = 'a[href], button:not([disabled]), input:not([disabled]), '
    + 'select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  function getFocusable() {
    return [...container.querySelectorAll(focusable)];
  }

  function trap(e) {
    if (e.key !== 'Tab') return;
    const items = getFocusable();
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus();
    }
  }

  return {
    activate() { container.addEventListener('keydown', trap); getFocusable()[0]?.focus(); },
    deactivate() { container.removeEventListener('keydown', trap); },
  };
}
```

## Pattern: Roving Tabindex

```javascript
function rovingTabindex(container, itemSelector) {
  const items = () => [...container.querySelectorAll(itemSelector)];

  function moveFocus(newItem) {
    items().forEach(el => el.setAttribute('tabindex', '-1'));
    newItem.setAttribute('tabindex', '0');
    newItem.focus();
  }

  container.addEventListener('keydown', (e) => {
    const current = document.activeElement;
    const all = items();
    const idx = all.indexOf(current);
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault(); moveFocus(all[(idx + 1) % all.length]);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault(); moveFocus(all[(idx - 1 + all.length) % all.length]);
    } else if (e.key === 'Home') {
      e.preventDefault(); moveFocus(all[0]);
    } else if (e.key === 'End') {
      e.preventDefault(); moveFocus(all[all.length - 1]);
    }
  });

  // Initialize — first item is tabbable, rest are -1
  items().forEach((el, i) => el.setAttribute('tabindex', i === 0 ? '0' : '-1'));
}
```

## Pattern: Focus Restoration

```javascript
class ModalManager {
  #trigger = null;
  #trap = null;

  open(modal, triggerEl) {
    this.#trigger = triggerEl ?? document.activeElement;
    document.body.setAttribute('inert', '');        // Lock background
    modal.removeAttribute('inert');
    modal.setAttribute('aria-modal', 'true');
    this.#trap = createFocusTrap(modal);
    this.#trap.activate();
    modal.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.close(modal);
    }, { once: true });
  }

  close(modal) {
    this.#trap?.deactivate();
    modal.setAttribute('inert', '');
    document.body.removeAttribute('inert');
    this.#trigger?.focus();           // Return focus to trigger element
    this.#trigger = null;
  }
}
```

## Tab Order vs Visual Order

Visual reordering via CSS `order`, `grid-template-areas`, or `flex-direction: row-reverse` does NOT change DOM order — Tab follows DOM order. If visual and DOM order diverge, keyboard users experience a confusing, non-linear Tab sequence. Fix: match DOM order to reading order, use CSS for visual reordering only when the relationship between elements is already visually clear.

## WCAG Keyboard Requirements

| Requirement | WCAG | Pattern |
|---|---|---|
| All interactive elements keyboard accessible | 2.1.1 | Native HTML first, then roving tabindex |
| No keyboard trap (except modals) | 2.1.2 | Always provide Escape to exit a focus trap |
| Focus order matches logical sequence | 2.4.3 | Keep DOM order = reading order |
| Focus always visible | 2.4.7 / 2.4.11 | Never `outline: none` without `:focus-visible` replacement |
| Skip to main content | 2.4.1 | First element in `<body>`, shown on `:focus` |

## Common Mistakes

- **Focus trap that lets Shift+Tab escape the first item** — always handle `shiftKey` in Tab trap
- **Closing modal without restoring focus** — screen reader users lose their place entirely
- **Using `tabindex="1"` or higher** — breaks natural tab flow; only use `0` and `-1`
- **Arrow key navigation without wrapping** — pressing Down on the last item does nothing; wrap to first
- **`inert` on entire `<body>` including the modal** — modal becomes inaccessible; apply `inert` selectively

## See Also

- [Form Interaction Craft](./form-interaction-craft.md) — keyboard handling inside form widgets
- [Accessibility and Motion](../../css/css-craft/accessibility-and-motion.md) — `:focus-visible` styling
- Reference: [W3C APG: Keyboard Interface Practices](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)
- Reference: [MDN: Keyboard-navigable JavaScript widgets](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Keyboard-navigable_JavaScript_widgets)
- Reference: [Adrian Roselli: Where to Put Focus When Opening a Modal](https://adrianroselli.com/2025/06/where-to-put-focus-when-opening-a-modal-dialog.html)
