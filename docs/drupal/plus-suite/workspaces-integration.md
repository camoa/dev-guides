---
description: Plus Suite Workspaces integration — workspace-aware tempstore keys, isolation per workspace, and known compatibility
drupal_version: "11.x"
---

# Workspaces Integration

## When to Use

> Use Plus Suite with Drupal Workspaces when you need staged content publishing. Tempstore+ handles workspace isolation automatically via key suffixes.

## Decision

| Scenario | Works? | Notes |
|----------|--------|-------|
| Edit content in workspace | Yes | Tempstore keys include workspace ID |
| Layout changes in workspace | Yes | Layout tempstore also workspace-aware |
| Inline editing in workspace | Yes | Entity tempstore workspace-aware |
| Nested layouts in workspace | Yes | All strategies use WorkspaceKeyTrait |
| Publishing workspace | Yes | Tempstore cleared on publish |

## Pattern

Tempstore+ uses `WorkspaceKeyTrait` to append workspace context to all tempstore keys:

```php
// With active workspace "stage":
"node.42.en.workspace:stage"

// Without workspaces (live):
"node.42.en.live"
```

This ensures:
- Edits in workspace A don't affect workspace B
- Tempstore data is isolated per workspace
- Switching workspaces loads the correct tempstore state

**Service provider weight:** `TempstorePlusServiceProvider` sets weight to 1 (after workspaces module) to ensure workspace manager is available when strategies are constructed.

## Common Mistakes

- **Wrong**: Assuming tempstore data persists across workspace switches → **Right**: Each workspace has its own tempstore namespace; switching workspaces shows that workspace's state

## See Also

- [Tempstore Strategy Pattern](tempstore-strategy.md)
- Reference: `tempstore_plus/src/Strategy/WorkspaceKeyTrait.php`
