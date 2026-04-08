---
description: Create custom Tool plugins for the Edit Mode toolbar — PHP 8 attribute syntax, ToolInterface methods, icon system, and built-in tools
drupal_version: "11.x"
---

# Tool Plugins

## When to Use

> Use custom Tool plugins when you need custom toolbar actions beyond built-in tools — e.g., a color picker, annotation tool, or content validation tool.

## Decision

**Built-in tools by weight order:**

| Tool | ID | Hotkey | Weight | Module |
|------|----|--------|--------|--------|
| Pointer | `pointer` | `p` | 0 | navigation_plus |
| Place Block | `place_block` | `b` | 20 | lb_plus |
| Change | `edit_plus` | `c` | 40 | edit_plus |
| Move | `move` | `m` | 60 | lb_plus |
| Layout | `layout_tool` | `l` | 80 | lb_plus |
| Trash | `trash` | `t` | 100 | lb_plus |
| Duplicate | `duplicate` | `d` | 120 | lb_plus |
| Configure | `configure` | `o` | 140 | lb_plus |
| Section Library | `section_library` | `s` | 160 | lb_plus_section_library |

## Pattern

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
      'mouse_icon' => "url('/path/to/cursor.svg') 3 3, auto",
    ];
  }

  public function buildLeftSideBar(): array {
    return ['#theme' => 'my_annotation_sidebar'];
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

**All LB+ tools use `LbPlusToolTrait` for `applies()`** — returns true if entity's view display has Layout Builder enabled.

## Common Mistakes

- **Wrong**: Using weight values 0–160 → **Right**: Built-in tools occupy those weights; use 170+ for custom tools
- **Wrong**: Omitting `addAttachments()` → **Right**: Tools without JS libraries won't function interactively

## See Also

- [Mode Plugins](mode-plugins.md)
- [Sidebar System](sidebar-system.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `navigation_plus/src/Plugin/Tool/`, `lb_plus/src/Plugin/Tool/`
