---
description: "Choose between HTML Drag API, Pointer Events, and libraries for drag-and-drop — with keyboard accessibility required by WCAG 2.5.7"
tldr: "Use the HTML Drag API for simple desktop-only drag. Use Pointer Events for touch + cross-device support."
---

# Drag and Drop Craft

## When to Use

> File uploads, sortable lists, kanban boards, reorder UIs. The native HTML Drag and Drop API has significant limitations on mobile and accessibility — understanding when to reach past it is critical.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Desktop-only drag (file upload, simple DnD) | HTML Drag API (`draggable`, `dragstart`, `drop`) | Simplest — built into browser, no JS library |
| Mobile drag support | Pointer Events API (`pointerdown`, `pointermove`, `pointerup`) | Touch events don't fire DnD events; Pointer Events are unified |
| Production sortable list | Pointer Events manually OR SortableJS | Pointer Events give full control; SortableJS if you need accessibility+animations out of box |
| Complex cross-container DnD (kanban) | SortableJS or similar library | Manual Pointer Events for kanban is 500+ lines and fragile |
| Keyboard accessibility (required for WCAG 2.5.7) | Separate keyboard mode alongside mouse/touch | No existing API provides both — always build a keyboard path |

**HTML Drag API limitations:**
- Does not fire on mobile (iOS, Android) — touch does not trigger `dragstart`
- Custom drag ghost images are limited (Firefox differs from Chrome)
- Drop target feedback requires extra ceremony (`dragover.preventDefault()`)
- `dataTransfer` API is inconsistent across browsers

## Pattern: Native HTML Drag API (Desktop)

```javascript
let dragSource = null;

container.addEventListener('dragstart', (e) => {
  dragSource = e.target.closest('[draggable]');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragSource.dataset.id);
  dragSource.classList.add('is-dragging');
});

container.addEventListener('dragover', (e) => {
  e.preventDefault(); // Required to allow drop
  e.dataTransfer.dropEffect = 'move';
  const target = e.target.closest('[data-drop-zone]');
  target?.classList.add('is-drag-over');
});

container.addEventListener('dragleave', (e) => {
  e.target.closest('[data-drop-zone]')?.classList.remove('is-drag-over');
});

container.addEventListener('drop', (e) => {
  e.preventDefault();
  const id = e.dataTransfer.getData('text/plain');
  const target = e.target.closest('[data-drop-zone]');
  if (target && dragSource) target.appendChild(dragSource);
});

container.addEventListener('dragend', () => {
  dragSource?.classList.remove('is-dragging');
  document.querySelectorAll('.is-drag-over').forEach(el => el.classList.remove('is-drag-over'));
  dragSource = null;
});
```

## Pattern: Keyboard Equivalent (Required for WCAG 2.5.7)

WCAG 2.5.7 (Dragging Movements, Level AA) requires that all drag operations have a non-dragging alternative. The pattern below provides Space to pick up, Arrow keys to reorder, Space to drop.

```javascript
function enableKeyboardSort(list) {
  let grabbed = null;

  list.addEventListener('keydown', (e) => {
    const item = e.target.closest('[role="option"]');
    if (!item) return;

    if (e.key === ' ') {
      e.preventDefault();
      if (!grabbed) {
        grabbed = item;
        item.setAttribute('aria-grabbed', 'true');
        list.setAttribute('aria-label', 'Use Arrow keys to reorder. Press Space to drop.');
      } else {
        grabbed.removeAttribute('aria-grabbed');
        grabbed = null;
        list.setAttribute('aria-label', 'Reorderable list. Press Space to pick up an item.');
      }
    }

    if (grabbed && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
      e.preventDefault();
      const sibling = e.key === 'ArrowDown' ? grabbed.nextElementSibling : grabbed.previousElementSibling;
      if (sibling) {
        const ref = e.key === 'ArrowDown' ? sibling.nextSibling : sibling;
        list.insertBefore(grabbed, ref);
        grabbed.focus();
      }
    }
  });
}
```

## Visual Feedback Patterns

| Feedback Type | Implementation | Notes |
|---|---|---|
| Drag ghost | CSS `opacity: 0.5` on source + custom `setDragImage()` | Native ghost is often ugly; custom image = better control |
| Drop zone highlight | `is-drag-over` class on valid targets | Remove on `dragleave` AND `drop` to avoid stuck state |
| Insertion marker | Absolutely positioned `::after` line at drop position | Shows exactly where item will land |
| Invalid drop zone | `not-allowed` cursor via CSS `[data-drop-zone="inactive"]` | Give clear "can't drop here" signal |

## Performance During Drag

Layout reads during `dragover`/`pointermove` are expensive — avoid `getBoundingClientRect()` on every event. Cache element positions before drag starts in `dragstart`/`pointerdown`, update cache when layout changes. Use rAF throttle on `pointermove` to limit handler frequency.

## Common Mistakes

- **Assuming `dragstart` fires on mobile** — it does not on iOS/Android; Pointer Events are required for touch
- **Forgetting `e.preventDefault()` in `dragover`** — drop never fires without it
- **No keyboard alternative for drag operations** — WCAG 2.5.7 violation, fails accessibility audit
- **Calling `getBoundingClientRect()` on every `pointermove`** — triggers layout recalculation at 60fps; cache beforehand
- **Removing `draggable` attribute via JS for keyboard users** — wrong approach; build a separate keyboard mode alongside mouse mode

## See Also

- [Keyboard Navigation Craft](./keyboard-navigation-craft.md) — roving tabindex in drag-reorderable lists
- [Performance and Event Handling](./performance-and-event-handling.md) — rAF throttling for pointermove
- Reference: [MDN: HTML Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API)
- Reference: [W3C: WCAG 2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)
- Reference: [GitHub Blog: Accessible Sortable List Challenges](https://github.blog/engineering/user-experience/exploring-the-challenges-in-creating-an-accessible-sortable-list-drag-and-drop/)
