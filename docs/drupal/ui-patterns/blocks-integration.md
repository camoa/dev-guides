---
description: Blocks Integration — components as block plugins, BlockSource for embedding blocks in slots
drupal_version: "11.x"
---

# Blocks Integration

**Sub-module:** `ui_patterns_blocks`
**Dependencies:** `block`, `ui_patterns`

## When to Use

> Use `ui_patterns_blocks` when you want SDC components available as placeable blocks in the block layout UI or Layout Builder. Use the `block` source plugin (separate) when you want to embed Drupal blocks inside component slots.

## Decision

| Feature | Sub-module / Plugin | Direction |
|---------|-------------------|-----------|
| Components available as blocks | `ui_patterns_blocks` sub-module | Component → Block |
| Blocks embeddable in component slots | `block` source plugin (core UI Patterns) | Block → Slot |

## Pattern

### How `ui_patterns_blocks` works

Each SDC component becomes a derivative block plugin:

```
Block: ui_patterns:my_theme:alert
  = Component: my_theme:alert
```

The block form provides the full component configuration form (props + slots). When placed in Layout Builder, entity context is resolved via `ChainContextEntityResolver`.

### Block render output

```php
public function build() {
    return [
        'content' => $this->buildComponentRenderable(
            $this->getDerivativeId(),
            $this->getComponentSourceContexts()
        ),
    ];
}
```

### `BlockSource` filter — excluded from component slots

The `block` source plugin excludes these from slots:
- `inline_block` (prevents config-to-content dependencies)
- `system_main_block`, `page_title_block` (Layout Builder convention)
- `layout_builder` and `ui_patterns_blocks` provider blocks (prevents recursion)

## Common Mistakes

- **Wrong**: Confusing `ui_patterns_blocks` with the `block` source plugin → **Right**: `ui_patterns_blocks` makes components available *as* blocks; the `block` source makes blocks available *inside* slots
- **Wrong**: Deep recursive nesting of components-as-blocks within components-as-layouts → **Right**: Nesting is supported but deep recursion causes performance issues and confusing configuration

## See Also

- [Layout Builder Integration](layout-builder-integration.md)
- [Slots System](slots-system.md)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_blocks/`
