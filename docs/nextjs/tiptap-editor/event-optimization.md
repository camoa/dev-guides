---
description: You need to optimize expensive operations triggered by editor events (auto-save, API calls, analytics).
---

## 10.2 Debouncing & Throttling Editor Events

### When to Use
You need to optimize expensive operations triggered by editor events (auto-save, API calls, analytics).

### Pattern
```typescript
import { debounce } from 'lodash'

// Debounce: Wait for pause in events before executing
const saveToServer = debounce((content) => {
  fetch('/api/save', {
    method: 'POST',
    body: JSON.stringify(content),
  })
}, 1000) // Wait 1 second after last change

editor.on('update', ({ editor }) => {
  saveToServer(editor.getJSON())
})

// Throttle: Execute at most once per interval
import { throttle } from 'lodash'

const updateCharCount = throttle((count) => {
  document.querySelector('.char-count').textContent = count
}, 100) // Update at most every 100ms

editor.on('update', ({ editor }) => {
  updateCharCount(editor.storage.characterCount.characters())
})
```

### Decision
| Scenario | Use | Interval | Why |
|---|---|---|---|
| Auto-save to server | Debounce | 1000-2000ms | Wait for typing pause |
| Analytics tracking | Throttle | 5000ms | Avoid spam |
| Character count display | Throttle | 100ms | Smooth updates |
| Toolbar state updates | None | N/A | Must be immediate |
| Search/filter | Debounce | 300ms | Wait for typing pause |

### Common Mistakes
- Not debouncing auto-save → Server flooded with requests on every keystroke
- Using throttle for auto-save → Saves mid-edit; debounce is better
- Forgetting to cancel debounced functions on unmount → Memory leak; call `.cancel()`
- Setting debounce interval too high → Feels unresponsive; 500-1000ms is ideal
- Throttling selection updates → Toolbar state lags; use immediate updates

### See Also
- ← 10.1 Editor Events
- → 17.1 React Performance

