---
description: "Update UI immediately before server confirms — when to use optimistic state, rollback patterns, and pending state indicators"
tldr: "Use optimistic UI when the expected server response is success and failure is rare. Skip it for destructive, financial, or irreversible actions."
---

# Optimistic UI

## When to Use

> Any action where the expected server response is success and failure is rare — liking a post, toggling a setting, reordering items, adding a tag. The UI updates instantly; the server confirms in the background. When the server fails, the UI rolls back with a non-blocking error.
>
> Optimistic UI is about perceived performance. Users feel the app is fast because the feedback is immediate, not because the network is faster.

## Decision

| Scenario | Use Optimistic UI? | Why |
|---|---|---|
| Toggle like/bookmark/follow | Yes | Failure rate < 1%; rollback is non-destructive |
| Reorder list items | Yes | User sees intent immediately; rollback is a re-sort |
| Add comment/post | Yes with caution | Show optimistic state, replace with server-returned item after confirm |
| Delete a record | Maybe — with confirmation | Rollback is confusing after deletion; consider "undo" toast instead |
| Payment/financial transaction | No | Consequences of incorrect optimistic state are serious |
| Destructive irreversible action | No | Users must wait for confirmation before UI reflects it |
| File upload | No | Progress indication is more honest than optimistic completion |

## Pattern: Optimistic Toggle

```javascript
async function optimisticToggle(element, action) {
  const previous = element.dataset.state;          // Store rollback value
  const next = previous === 'liked' ? 'unliked' : 'liked';

  // 1. Update UI immediately
  element.dataset.state = next;
  element.setAttribute('aria-pressed', next === 'liked');

  try {
    // 2. Sync with server async
    const result = await action(next);
    // 3. Replace optimistic state with server's canonical response
    element.dataset.state = result.state;
  } catch {
    // 4. Rollback on failure
    element.dataset.state = previous;
    element.setAttribute('aria-pressed', previous === 'liked');
    showErrorToast('Could not save — please try again');
  }
}
```

## Pattern: Optimistic List Item Add

```javascript
async function optimisticAdd(list, createFn, itemData) {
  const tempId = `temp-${Date.now()}`;     // Temporary ID for DOM reference
  const tempItem = renderItem({ ...itemData, id: tempId, pending: true });
  list.appendChild(tempItem);               // Show immediately

  try {
    const saved = await createFn(itemData);
    const realItem = renderItem(saved);
    list.replaceChild(realItem, tempItem);  // Replace temp with server response
  } catch {
    tempItem.remove();                      // Rollback — remove temp item
    showErrorToast('Could not save — check your connection');
  }
}
```

## Pending State Indicators

| Approach | When to Use | Avoid When |
|---|---|---|
| Subtle opacity reduction (0.6) on pending items | Normal optimistic adds | High-frequency actions — constant dimming looks broken |
| Spinner inside button, button stays enabled | Slow operations (>1s) | Instant operations — spinner flash is worse than nothing |
| No indicator (full confidence) | Toggle states with <100ms server response | Slow connections — users retry a completed action |
| "Saving..." label near affected area | Autosave patterns | Inline editing — label steals visual attention |

## Rollback UX

Good rollback is invisible: the state snaps back, and a non-blocking toast explains what happened. Never use a blocking modal for rollback — the user has already moved on.

The toast should:
- Be dismissible immediately (not wait 5 seconds to disappear)
- Offer a retry action if the action had user intent
- Not interrupt what the user is currently doing

## Common Mistakes

- **No rollback implementation** — server failure silently corrupts UI state
- **Rollback without error message** — user has no idea the action failed
- **Blocking the UI while "confirming" optimistically** — defeats the purpose; the whole point is non-blocking
- **Optimistic state for destructive actions** — user thinks data is deleted; rollback is confusing
- **Replacing rollback with page reload** — extreme; use rollback state + toast
- **Using a temporary ID and never replacing it** — server returns the real ID; always reconcile

## See Also

- [Form Interaction Craft](./form-interaction-craft.md) — autosave with debounce + pending state
- [Skeleton and Loading States](../../css/css-craft/skeleton-and-loading-states.md) — loading UI for the non-optimistic path
- Reference: [JavaScript in Plain English: Optimistic UI in Frontend Architecture](https://javascript.plainenglish.io/optimistic-ui-in-frontend-architecture-do-it-right-avoid-pitfalls-7507d713c19c)
