---
description: Choose between HTML Drag API, Pointer Events, and libraries for drag-and-drop — with keyboard accessibility required by WCAG 2.5.7
tldr: "Use the HTML Drag API for simple desktop-only drag. Use Pointer Events for touch + cross-device support."
---

# Drag and Drop Craft

## When to Use

> Use the HTML Drag API for simple desktop-only drag. Use Pointer Events for touch + cross-device support. Always build a keyboard alternative — WCAG 2.5.7 requires it.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Desktop-only drag (file upload, simple DnD) | HTML Drag API (`draggable`, `dragstart`, `drop`) | Simplest — built into browser, no library |
| Mobile drag support | Pointer Events API (`pointerdown`, `pointermove`, `pointerup`) | Touch events don't fire DnD events; Pointer Events are unified |
| Production sortable list | Pointer Events manually OR SortableJS | Pointer Events give full control; SortableJS adds accessibility + animations |
| Complex cross-container DnD (kanban) | SortableJS or similar library | Manual Pointer Events for kanban is 500+ lines and fragile |
| Keyboard accessibility (WCAG 2.5.7 required) | Separate keyboard mode alongside mouse/touch | No existing API provides both — always build a keyboard path |

**HTML Drag API limitations:**
- Does not fire on mobile (iOS/Android) — touch does not trigger `dragstart`
- Drop targets require `dragover.preventDefault()` to accept drops
- `dataTransfer` API is inconsistent across browsers

## Pattern

```javascript
// Native HTML Drag API (desktop only)
let dragSource = null;

container.addEventListener('dragstart', (e) => {
  dragSource = e.target.closest('[draggable]');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragSource.dataset.id);
  dragSource.classList.add('is-dragging');
});
container.addEventListener('dragover', (e) => {
  e.preventDefault(); // Required to allow drop
  e.target.closest('[data-drop-zone]')?.classList.add('is-drag-over');
});
container.addEventListener('dragleave', (e) => {
  e.target.closest('[data-drop-zone]')?.classList.remove('is-drag-over');
});
container.addEventListener('drop', (e) => {
  e.preventDefault();
  const target = e.target.closest('[data-drop-zone]');
  if (target && dragSource) target.appendChild(dragSource);
});
container.addEventListener('dragend', () => {
  dragSource?.classList.remove('is-dragging');
  document.querySelectorAll('.is-drag-over').forEach(el => el.classList.remove('is-drag-over'));
  dragSource = null;
});

// Keyboard sort (WCAG 2.5.7 — Space to pick up, Arrow to reorder, Space to drop)
function enableKeyboardSort(list) {
  let grabbed = null;
  list.addEventListener('keydown', (e) => {
    const item = e.target.closest('[role="option"]');
    if (!item) return;
    if (e.key === ' ') {
      e.preventDefault();
      if (!grabbed) { grabbed = item; item.setAttribute('aria-grabbed', 'true'); }
      else { grabbed.removeAttribute('aria-grabbed'); grabbed = null; }
    }
    if (grabbed && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
      e.preventDefault();
      const sibling = e.key === 'ArrowDown' ? grabbed.nextElementSibling : grabbed.previousElementSibling;
      if (sibling) { list.insertBefore(grabbed, e.key === 'ArrowDown' ? sibling.nextSibling : sibling); grabbed.focus(); }
    }
  });
}
```

## Common Mistakes

- **Wrong**: Assuming `dragstart` fires on mobile → **Right**: Use Pointer Events for touch; HTML Drag API does not trigger on iOS/Android
- **Wrong**: Forgetting `e.preventDefault()` in `dragover` → **Right**: Drop never fires without it
- **Wrong**: No keyboard alternative → **Right**: WCAG 2.5.7 requires a non-drag path for all drag operations
- **Wrong**: Calling `getBoundingClientRect()` on every `pointermove` → **Right**: Cache positions before drag starts; recalculate only on layout change
- **Wrong**: Removing `draggable` for keyboard users → **Right**: Build a separate keyboard mode alongside mouse mode

## See Also

- [Keyboard Navigation Craft](./keyboard-navigation-craft.md) — roving tabindex in drag-reorderable lists
- [Performance and Event Handling](./performance-and-event-handling.md) — rAF throttling for pointermove
- Reference: [MDN: HTML Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API)
- Reference: [W3C: WCAG 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)
- Reference: [GitHub Blog: Accessible Sortable List Challenges](https://github.blog/engineering/user-experience/exploring-the-challenges-in-creating-an-accessible-sortable-list-drag-and-drop/)
