---
description: Update UI immediately before server confirms — when to use optimistic state, rollback patterns, and pending state indicators
---

# Optimistic UI

## When to Use

> Use optimistic UI when the expected server response is success and failure is rare. Skip it for destructive, financial, or irreversible actions.

## Decision

| Scenario | Use Optimistic UI? | Why |
|---|---|---|
| Toggle like/bookmark/follow | Yes | Failure rate < 1%; rollback is non-destructive |
| Reorder list items | Yes | User sees intent immediately; rollback is a re-sort |
| Add comment/post | Yes with caution | Show optimistic state; replace with server-returned item after confirm |
| Delete a record | Maybe — with confirmation | Rollback after deletion confuses users; consider "undo" toast instead |
| Payment/financial transaction | No | Consequences of incorrect optimistic state are serious |
| Destructive irreversible action | No | Users must wait for server confirmation |
| File upload | No | Progress indication is more honest than optimistic completion |

**Pending state indicators:**

| Approach | When to Use | Avoid When |
|---|---|---|
| Subtle opacity (0.6) on pending items | Normal optimistic adds | High-frequency actions — constant dimming looks broken |
| Spinner inside button | Slow operations (> 1s) | Instant operations — spinner flash is worse than nothing |
| No indicator | Toggle states with < 100ms server response | Slow connections — users retry a completed action |

## Pattern

```javascript
// Optimistic toggle (like, bookmark, follow)
async function optimisticToggle(element, action) {
  const previous = element.dataset.state;
  const next = previous === 'liked' ? 'unliked' : 'liked';
  element.dataset.state = next;                         // Update UI immediately
  element.setAttribute('aria-pressed', next === 'liked');
  try {
    const result = await action(next);
    element.dataset.state = result.state;               // Replace with server canonical state
  } catch {
    element.dataset.state = previous;                   // Rollback
    element.setAttribute('aria-pressed', previous === 'liked');
    showErrorToast('Could not save — please try again');
  }
}

// Optimistic list item add
async function optimisticAdd(list, createFn, itemData) {
  const tempId = `temp-${Date.now()}`;
  const tempItem = renderItem({ ...itemData, id: tempId, pending: true });
  list.appendChild(tempItem);                          // Show immediately
  try {
    const saved = await createFn(itemData);
    list.replaceChild(renderItem(saved), tempItem);    // Replace temp with server response
  } catch {
    tempItem.remove();                                 // Rollback
    showErrorToast('Could not save — check your connection');
  }
}
```

## Common Mistakes

- **Wrong**: No rollback implementation → **Right**: Server failure silently corrupts UI state without rollback
- **Wrong**: Rollback without error message → **Right**: Always show a non-blocking toast explaining the failure
- **Wrong**: Blocking the UI while "confirming" → **Right**: Defeats the purpose; the whole point is non-blocking response
- **Wrong**: Optimistic state for destructive actions → **Right**: User thinks data is deleted; rollback is confusing
- **Wrong**: Using a temp ID and never replacing it → **Right**: Always reconcile with server-returned canonical ID
- **Wrong**: Replacing rollback with page reload → **Right**: Use rollback state + toast; reload is extreme

## See Also

- [Form Interaction Craft](./form-interaction-craft.md) — autosave with debounce + pending state
- Reference: [LogRocket: Optimistic UI in Frontend Architecture](https://javascript.plainenglish.io/optimistic-ui-in-frontend-architecture-do-it-right-avoid-pitfalls-7507d713c19c)
