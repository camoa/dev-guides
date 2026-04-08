---
description: Tempstore+ strategy pattern — EntityTempstoreStrategy vs LayoutTempstoreStrategy, workspace keys, custom strategies, and param converter integration
drupal_version: "11.x"
---

# Tempstore Strategy Pattern

## When to Use

> Use Tempstore+ when you need workspace-aware temporary storage for entities or layout sections. Do not bypass it with core tempstore directly.

## Decision

| Subject | Strategy | When |
|---------|----------|------|
| Node/entity being edited inline | `EntityTempstoreStrategy` | Edit+ inline editing |
| Layout Builder sections | `LayoutTempstoreStrategy` | LB+ layout editing |
| Entity in LB context | `LayoutTempstoreStrategy` | Converts entity to section storage |
| Custom data needing temp storage | Custom strategy | Register tagged service |

## Pattern

**`StrategySelector`** iterates strategies by priority, returns first that `supports($subject)`:

```
StrategySelector
  ├── EntityTempstoreStrategy (for entities)
  └── LayoutTempstoreStrategy (for section storage)
```

**Strategy interface:**

```php
interface TempstoreStrategyInterface {
  public function supports($subject): bool;
  public function get($subject);
  public function set($subject): void;
  public function has($subject): bool;
  public function delete($subject): void;
  public function getKey($subject): string;
  public function getCollection($subject): string;
}
```

**Workspace key suffix** (all strategies use `WorkspaceKeyTrait`):
```
// Active workspace "stage":
"node.42.en.workspace:stage"

// Without workspaces:
"node.42.en.live"
```

**Custom strategy:**

```php
# my_module.services.yml
services:
  my_module.custom_strategy:
    class: Drupal\my_module\Strategy\CustomTempstoreStrategy
    tags:
      - { name: tempstore_strategy, priority: 50 }
```

**Important:** `LayoutTempstoreStrategy` does NOT auto-bubble nested changes. Call `bubbleChangesToRoot()` explicitly when modifying nested layout blocks programmatically.

## Common Mistakes

- **Wrong**: Using core's tempstore directly → **Right**: Always use Tempstore+; core tempstore loses workspace awareness
- **Wrong**: Forgetting `bubbleChangesToRoot()` in programmatic code → **Right**: Nested changes don't persist without explicit bubbling

## See Also

- [Inline Editing](inline-editing.md)
- [Nested Layouts](nested-layouts.md)
- [Workspaces Integration](workspaces-integration.md)
- Reference: `tempstore_plus/src/Strategy/StrategySelector.php`
