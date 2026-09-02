---
description: "Create custom Tool plugins for the Edit Mode toolbar — PHP 8 attribute syntax, ToolInterface methods, icon system, and built-in tools"
tldr: "Use custom Tool plugins when you need custom tools for the Edit Mode toolbar — e.g., a color picker, annotation tool, or content validation tool."
drupal_version: "11.x"
---

# Tool Plugins

## When to Use

> When you need to create custom tools for the Edit Mode toolbar (e.g., a color picker, annotation tool, or content validation tool).

## Tool Plugin Architecture

Tools are discovered by `ToolPluginManager` from the `Plugin/Tool` namespace using PHP 8 attributes.

## Pattern: Attribute Definition

```php
use Drupal\navigation_plus\Attribute\Tool;

#[Tool(
  id: 'my_tool',
  label: new TranslatableMarkup('My Tool'),
  hot_key: 'x',
  weight: 200,
)]
class MyTool extends ToolPluginBase {
  // ...
}
```

| Property | Type | Purpose |
|---|---|---|
| `id` | string | Unique plugin ID |
| `label` | TranslatableMarkup | Human-readable name |
| `hot_key` | string\|null | Keyboard shortcut key |
| `weight` | int | Toolbar order (lower = further left) |

## Required Methods (ToolInterface)

```php
interface ToolInterface {
  // Icon configuration for the toolbar button.
  public function getIconsPath(): array;

  // Buttons visible regardless of active tool.
  public function buildGlobalTopBarButtons(array &$global_top_bar): array;

  // Buttons visible only when this tool is active.
  public function buildToolTopBarButtons(): array;

  // Content for the right sidebar.
  public function buildRightSideBar(): array;

  // Content for the left sidebar.
  public function buildLeftSideBar(): array;

  // Settings form elements for the settings sidebar.
  public function buildSettings(): array;

  // Optional sub-tool definitions.
  public function subTools(): array;

  // Attach CSS/JS libraries.
  public function addAttachments(array &$attachments): void;

  // Whether this tool applies to the current entity.
  public function applies(EntityInterface $entity): bool;
}
```

## Built-in Tools (by weight order)

| Tool | ID | Hotkey | Weight | Module | Purpose |
|---|---|---|---|---|---|
| Pointer | `pointer` | `p` | 0 | navigation_plus | Default preview/select tool |
| Place Block | `place_block` | `b` | 20 | lb_plus | Drag blocks from sidebar |
| Change | `edit_plus` | `c` | 40 | edit_plus | Inline field editing |
| Move | `move` | `m` | 60 | lb_plus | Drag existing blocks |
| Layout | `layout_tool` | `l` | 80 | lb_plus | Change section layouts |
| Trash | `trash` | `t` | 100 | lb_plus | Delete blocks/sections |
| Duplicate | `duplicate` | `d` | 120 | lb_plus | Clone blocks |
| Configure | `configure` | `o` | 140 | lb_plus | Section settings |
| Section Library | `section_library` | `s` | 160 | lb_plus_section_library | Save/reuse sections |

## Icon System

`getIconsPath()` returns an array with:

```php
return [
  'icon_id' => 'my-icon',        // SVG icon identifier
  'pack_id' => 'my_module',       // Icon pack (module name)
  'mouse_icon' => "url('/path/to/cursor.svg') 3 3, auto",  // CSS cursor
  'tool_indicator_icons' => [
    'section' => '<svg>...</svg>',  // Icon shown on section hover
    'block' => '<svg>...</svg>',    // Icon shown on block hover
  ],
];
```

## Tool Indicator Events

When rendering sections and blocks in Edit Mode, `lb_plus` dispatches events for tools to add indicator buttons:

- `SectionToolIndicatorEvent` — tools add section-level action buttons
- `BlockToolIndicatorEvent` — tools add block-level action buttons

## LbPlusToolTrait

All LB+ tools use `LbPlusToolTrait` for the `applies()` check:

```php
trait LbPlusToolTrait {
  protected function lbPlusToolApplies(EntityInterface $entity): bool {
    // Returns true if entity's view display has Layout Builder enabled.
  }
}
```

## Pattern: Creating a Custom Tool

```php
namespace Drupal\my_module\Plugin\Tool;

use Drupal\navigation_plus\Attribute\Tool;
use Drupal\navigation_plus\ToolPluginBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Tool(
  id: 'annotate',
  label: new TranslatableMarkup('Annotate'),
  hot_key: 'a',
  weight: 180,
)]
class Annotate extends ToolPluginBase {

  public function getIconsPath(): array {
    return [
      'icon_id' => 'annotate',
      'pack_id' => 'my_module',
    ];
  }

  public function buildLeftSideBar(): array {
    return [
      '#theme' => 'my_annotation_sidebar',
      '#annotations' => $this->getAnnotations(),
    ];
  }

  public function buildSettings(): array {
    return [
      'show_resolved' => [
        '#type' => 'checkbox',
        '#title' => $this->t('Show resolved annotations'),
      ],
    ];
  }

  public function applies(EntityInterface $entity): bool {
    return $entity->access('update');
  }

  public function addAttachments(array &$attachments): void {
    $attachments['#attached']['library'][] = 'my_module/annotate_tool';
  }
}
```

## Common Mistakes

- **Do not** use weight values that conflict with built-in tools (0-160 are taken).
- **Do not** forget `addAttachments()` — tools without JS libraries won't function.

## See Also

- [Mode Plugins](mode-plugins.md)
- [Sidebar System](sidebar-system.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `navigation_plus/src/Plugin/Tool/`, `lb_plus/src/Plugin/Tool/`
