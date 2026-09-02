---
description: Plus Suite Workspaces integration — workspace-aware tempstore keys, isolation per workspace, and known compatibility
tldr: "Use Plus Suite with Drupal Workspaces when you need staged content publishing. Tempstore+ handles workspace isolation automatically via key suffixes."
drupal_version: "11.x"
---

# Workspaces Integration

## When to Use

> When using Plus Suite with Drupal's Workspaces module for staged content publishing.

## Pattern: How Tempstore+ Enables Workspace Support

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

## Service Provider Weight

`TempstorePlusServiceProvider` sets weight to 1 (after workspaces module) to ensure workspace manager is available when strategies are constructed.

## Decision: Workspaces with Plus Suite

| Scenario | Works? | Notes |
|---|---|---|
| Edit content in workspace | Yes | Tempstore keys include workspace ID |
| Layout changes in workspace | Yes | Layout tempstore also workspace-aware |
| Inline editing in workspace | Yes | Entity tempstore workspace-aware |
| Nested layouts in workspace | Yes | All strategies use WorkspaceKeyTrait |
| Publishing workspace | Works with core workflow | Tempstore cleared on publish |

## Common Mistakes

- **Do not assume tempstore data persists across workspace switches** — each workspace has its own tempstore namespace.

## See Also

- [Tempstore Strategy Pattern](tempstore-strategy.md)
- Reference: `tempstore_plus/src/WorkspaceKeyTrait.php`
