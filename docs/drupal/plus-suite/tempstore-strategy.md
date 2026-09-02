---
description: "Tempstore+ strategy pattern — EntityTempstoreStrategy vs LayoutTempstoreStrategy, workspace keys, custom strategies, and param converter integration"
tldr: "Use Tempstore+ to manage unsaved changes across entities and Layout Builder sections. It solves different key generation, collection naming, and workspace awareness needs via the Strategy pattern."
drupal_version: "11.x"
---

# Tempstore Strategy Pattern

## When to Use

> When you need to understand how Plus Suite manages unsaved changes across entities and Layout Builder sections, or when adding custom tempstore strategies.

## Problem Solved

Core Layout Builder and entity forms both need temporary storage, but with different key generation, collection naming, and workspace awareness. Tempstore+ solves this with the Strategy pattern.

## Architecture

```
StrategySelector
  ├── EntityTempstoreStrategy (for entities)
  └── LayoutTempstoreStrategy (for section storage)
```

The `StrategySelector` iterates strategies by priority and returns the first one that `supports($subject)`.

## Strategy Interface

```php
interface TempstoreStrategyInterface {
  public function supports($subject): bool;
  public function get($subject);      // Retrieve from tempstore
  public function set($subject): void; // Store in tempstore
  public function has($subject): bool; // Check existence
  public function delete($subject): void; // Remove
  public function getKey($subject): string;
  public function getCollection($subject): string;
}
```

## EntityTempstoreStrategy

- **Supports**: Any `EntityInterface`
- **Collection**: `entity_tempstore.entity_storage`
- **Key format**: `{entity_type}.{id}.{language}` (+ workspace suffix)
- **Storage**: `['entity' => EntityInterface]`
- Uses `WorkspaceKeyTrait` for workspace-aware keys

## LayoutTempstoreStrategy

- **Supports**: `SectionStorageInterface`, layout-compatible entities, `NestedSectionStorageInterface`
- **Collection**: `layout_builder.section_storage.{storage_type}`
- **Key format**: From `TempStoreIdentifierInterface::getTempstoreKey()` (+ workspace suffix)
- **Storage**: `['section_storage' => SectionStorageInterface]`
- Static cache prevents duplicate loads
- Wraps/unwraps `NestedAwareSectionStorage` transparently

**Important**: Does NOT auto-bubble nested changes. Consumer must call `bubbleChangesToRoot()` explicitly.

## Workspace Key Generation

```php
// WorkspaceKeyTrait
protected function workspaceKeySuffix(): string {
  if ($this->workspaceManager && $workspace = $this->workspaceManager->getActiveWorkspace()) {
    return '.workspace:' . $workspace->id();
  }
  return '.live';
}
```

## Param Converter Integration

`EntityConverter` decorates core's entity param converter:
1. Checks `TempstoreActivationCheckerInterface::isActive()`
2. If active, loads entity from tempstore
3. Compares with original (recursive array diff)
4. If different, returns tempstore version
5. Calls `onEntitySwapped()` to track swapped entities

## Adding a Custom Strategy

```php
// my_module.services.yml
services:
  my_module.custom_strategy:
    class: Drupal\my_module\Strategy\CustomTempstoreStrategy
    tags:
      - { name: tempstore_strategy, priority: 50 }
```

```php
class CustomTempstoreStrategy implements TempstoreStrategyInterface {
  public function supports($subject): bool {
    return $subject instanceof MyCustomInterface;
  }
  // ... implement remaining methods
}
```

## Decision

| Subject | Strategy | When |
|---|---|---|
| Node/entity being edited inline | EntityTempstoreStrategy | Edit+ inline editing |
| Layout Builder sections | LayoutTempstoreStrategy | LB+ layout editing |
| Entity in LB context | LayoutTempstoreStrategy | Converts entity to section storage |
| Custom data needing temp storage | Custom strategy | Register tagged service |

## Common Mistakes

- **Do not** bypass Tempstore+ by using core's tempstore directly — you'll lose workspace awareness.
- **Do not** forget to call `bubbleChangesToRoot()` when modifying nested layout blocks programmatically.

## See Also

- [Inline Editing](inline-editing.md)
- [Nested Layouts](nested-layouts.md)
- [Workspaces Integration](workspaces-integration.md)
- Reference: `tempstore_plus/src/StrategySelector.php`
