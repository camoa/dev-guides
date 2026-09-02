---
description: Plus Suite JavaScript architecture — key modules, AJAX commands, drupalSettings configuration, and extension patterns
tldr: "Reference this when extending Plus Suite with custom JS, debugging client-side issues, or understanding AJAX command flow."
drupal_version: "11.x"
---

# JavaScript Architecture

## When to Use

> When you need to understand Plus Suite's JavaScript modules, extend them, or debug client-side issues.

## Pattern: Module System

Plus Suite uses ES module patterns with Drupal behaviors:

```javascript
// Example: tool-plugin.js (module type in libraries.yml)
((Drupal) => {
  Drupal.behaviors.myToolPlugin = {
    attach(context, settings) {
      // Tool initialization
    },
  };
})(Drupal);
```

## Key JavaScript Components

| Component | Module | File | Purpose |
|---|---|---|---|
| Edit Mode App | navigation_plus | `edit-mode-app.bundle.js` | Core editing orchestration |
| Drop Zones | navigation_plus | `dropzones/` | Region and section drop zones |
| Context Menu | navigation_plus | `context-menu/` | Right-click actions |
| Tool Indicators | navigation_plus | `tool-indicators/` | Hover action buttons |
| Hotkeys | navigation_plus | `hotkeys.js` | Keyboard shortcut handling |
| Sidebar Manager | navigation_plus | `sidebar/sidebar-manager.js` | Sidebar panel management |
| Place Block | lb_plus | `draggable-new-blocks.js` | Drag blocks from sidebar |
| Move Block | lb_plus | `draggable-existing-blocks.js` | Drag existing blocks |
| Nested Layout | lb_plus | `edit-layout-block.js` | Enter/exit nested editing |
| Content Preview | lb_plus | `block-preview.js` | Toggle block content preview |
| Layout Outlines | lb_plus | `layout-outlines.js` | Toggle layout grid outlines |
| Duplicate Block | lb_plus | `duplicate-tool-plugin.js` | Block cloning |
| Inline Editor | edit_plus | CKEditor 5 integration | Text field inline editing |
| File Drag | navigation_plus | `file-drag.js` | Desktop file drag-and-drop |

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Need core client-side editing orchestration | Edit Mode App (`edit-mode-app.bundle.js`, navigation_plus) | It is the module that drives editing behavior |
| Need to replace a rendered element after a change | Dispatch `UpdateElement` | It calls `updateElement()`, wired through `EditPlusFormTrait::updatePage()` |

## Pattern: AJAX Commands

| Command | Module | JS Method | Purpose |
|---|---|---|---|
| `UpdateElement` | navigation_plus | `updateElement()` | Replace a rendered element, used by edit_plus via `EditPlusFormTrait::updatePage()` |
| `ShowFieldWithErrors` | edit_plus | `ShowFieldWithErrors()` | Highlight validation errors |
| Core `ReplaceCommand` | core | Modified by NestedLayoutResponseSubscriber | Section replacement |
| Core `CloseDialogCommand` | core | Modified for nested contexts | Dialog handling |

## Pattern: drupalSettings

LB+ passes configuration via `drupalSettings`:

```javascript
drupalSettings['LB+'] = {
  sectionStorageType: 'overrides',
  sectionStorage: 'node.42.default.en',
  isLayoutBlock: false,
};
```

## Common Mistakes

- **Do not use jQuery for new Plus Suite JS** — use vanilla JS with Drupal behaviors.
- **Do not modify `drupalSettings['LB+']` directly** — use PHP render arrays with `#attached`.

## See Also

- [Sidebar System](sidebar-system.md)
- [Tool Plugins](tool-plugins.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `navigation_plus/js/`, `lb_plus/js/`, `edit_plus/js/`
