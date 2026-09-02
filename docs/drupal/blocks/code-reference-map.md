---
description: Quick reference of key classes, interfaces, and services in Drupal's block system
tldr: "Quick lookup of key classes, interfaces, and services in Drupal's block system when building or debugging block code."
drupal_version: "11.x"
---

# Code Reference Map

## When to Use

> Quick lookup of key classes, interfaces, and services in Drupal's block system.

## Decision

| Layer | Key Classes | Location |
|-------|-------------|----------|
| Block Plugin API | `BlockBase`, `BlockPluginInterface`, `Attribute\Block` | `core/lib/Drupal/Core/Block/` |
| Block Module | `Entity\Block`, `BlockViewBuilder`, `BlockRepository` | `core/modules/block/` |
| Block Content | `Entity\BlockContent`, `Plugin\Block\BlockContentBlock` | `core/modules/block_content/` |
| Layout Builder | `Plugin\Block\InlineBlock`, `FieldBlock`, `ExtraFieldBlock` | `core/modules/layout_builder/` |
| Conditions | `ConditionPluginBase`, `ConditionInterface` | `core/lib/Drupal/Core/Condition/` |

## Pattern

**Block Plugin API (core/lib/Drupal/Core/Block/):**
- `BlockBase` — Base class all block plugins extend
- `BlockPluginInterface` — Required interface for block plugins
- `BlockPluginTrait` — Shared implementation for BlockBase
- `BlockManager` — Plugin manager for discovering block plugins
- `BlockManagerInterface` — Interface for block manager
- `Attribute\Block` — PHP attribute for block plugin definition
- `TitleBlockPluginInterface` — Interface for blocks that set page title
- `MessagesBlockPluginInterface` — Interface for message blocks

**Block Module (core/modules/block/):**
- `Entity\Block` — Config entity for block placement
- `BlockInterface` — Interface for Block config entity
- `BlockAccessControlHandler` — Access control for Block entities
- `BlockViewBuilder` — Renders blocks with wrappers
- `BlockRepository` — Service for loading blocks by region/theme
- `BlockRepositoryInterface` — Interface for block repository
- `BlockForm` — Form for placing/configuring blocks
- `BlockListBuilder` — Admin UI for listing blocks
- `Plugin\ConfigAction\PlaceBlock` — Recipe action for placing blocks

**Block Content Module (core/modules/block_content/):**
- `Entity\BlockContent` — Content entity for fieldable blocks
- `Entity\BlockContentType` — Bundle entity for block types
- `BlockContentInterface` — Interface for BlockContent entity
- `BlockContentTypeInterface` — Interface for BlockContentType
- `Plugin\Block\BlockContentBlock` — Plugin wrapper for content blocks
- `BlockContentForm` — Form for editing content blocks
- `Access\BlockContentIsReusableAccessCheck` — Access check for reusable flag

**Layout Builder (core/modules/layout_builder/):**
- `Plugin\Block\InlineBlock` — Non-reusable inline blocks
- `Plugin\Block\FieldBlock` — Entity fields as blocks
- `Plugin\Block\ExtraFieldBlock` — Extra fields as blocks
- `Plugin\Derivative\InlineBlockDeriver` — Derivatives per block type

**Condition Plugins (core/lib/Drupal/Core/Condition/):**
- `ConditionPluginBase` — Base class for visibility conditions
- `ConditionInterface` — Interface for conditions
- `ConditionManager` — Plugin manager for conditions
- `ConditionPluginCollection` — Collection of condition plugins
- `Attribute\Condition` — PHP attribute for condition plugins

**Services:**
- `plugin.manager.block` — BlockManager service
- `block.repository` — BlockRepository service
- `entity_type.manager` — For loading Block/BlockContent entities
- `condition.manager` — ConditionManager service
- `config.factory` — For accessing block configuration

**Core Block Examples:**
- `system/src/Plugin/Block/SystemBrandingBlock` — Config, DI, cache tags
- `system/src/Plugin/Block/SystemMenuBlock` — Derivatives, cache contexts
- `user/src/Plugin/Block/UserLoginBlock` — Form rendering, access control
- `system/src/Plugin/Block/PageTitleBlock` — Simple block, no config
- `views/src/Plugin/Block/ViewsBlock` — Complex derivatives, Views integration

## Common Mistakes

- Importing wrong namespace → Block plugin uses `Core\Block`, not `block` module
- Confusing Block (entity) with BlockBase (plugin) → Different layers of system
- Looking for BlockContent in wrong namespace → It's `block_content` module, not `block`
- Not checking if class/service exists → Some features only in newer Drupal versions

## See Also

- [Block System Architecture](block-system-architecture.md)
- [Creating Block Plugins](creating-block-plugins.md)
- [Dependency Injection in Blocks](dependency-injection.md)
- Reference: https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Block/
