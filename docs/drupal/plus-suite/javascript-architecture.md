---
description: Plus Suite JavaScript architecture — key modules, AJAX commands, drupalSettings configuration, and extension patterns
drupal_version: "11.x"
---

# JavaScript Architecture

## When to Use

> Reference this when extending Plus Suite with custom JS, debugging client-side issues, or understanding AJAX command flow.

## Decision

| Component | Module | Purpose |
|-----------|--------|---------|
| Edit Mode App | navigation_plus | Core editing orchestration |
| Drop Zones | navigation_plus | Region and section drop zones |
| Hotkeys | navigation_plus | Keyboard shortcut handling |
| Sidebar Manager | navigation_plus | Sidebar panel management |
| Place Block | lb_plus | Drag blocks from sidebar |
| Move Block | lb_plus | Drag existing blocks |
| Nested Layout | lb_plus | Enter/exit nested editing |
| Inline Editor | edit_plus | CKEditor 5 text field inline editing |
| File Drag | navigation_plus | Desktop file drag-and-drop |

## Pattern

**Module system** — ES module patterns with Drupal behaviors:

```javascript
((Drupal) => {
  Drupal.behaviors.myToolPlugin = {
    attach(context, settings) {
      // Tool initialization
    },
  };
})(Drupal);
```

**AJAX commands:**

| Command | Module | Purpose |
|---------|--------|---------|
| `UpdateMarkup` | edit_plus | Replace rendered field after inline edit |
| `ShowFieldWithErrors` | edit_plus | Highlight validation errors |
| `ReplaceCommand` (modified) | core | Section replacement in nested contexts |

**`drupalSettings` from LB+:**

```javascript
drupalSettings['LB+'] = {
  sectionStorageType: 'overrides',
  sectionStorage: 'node.42.default.en',
  isLayoutBlock: false,
};
```

## Common Mistakes

- **Wrong**: Using jQuery for new Plus Suite JS → **Right**: Use vanilla JS with Drupal behaviors
- **Wrong**: Modifying `drupalSettings['LB+']` directly in JS → **Right**: Pass settings via PHP render arrays with `#attached`

## See Also

- [Sidebar System](sidebar-system.md)
- [Tool Plugins](tool-plugins.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `navigation_plus/js/`, `lb_plus/js/`, `edit_plus/js/`
