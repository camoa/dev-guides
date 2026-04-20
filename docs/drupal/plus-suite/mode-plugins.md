---
description: Create custom Mode plugins for Plus Suite — PHP 8 attribute syntax, ModeInterface methods, and built-in modes
tldr: "Use custom Mode plugins when you need editing modes beyond Edit Mode — e.g., a Preview mode, Help mode, or workflow-specific mode."
drupal_version: "11.x"
---

# Mode Plugins

## When to Use

> Use custom Mode plugins when you need editing modes beyond Edit Mode — e.g., a Preview mode, Help mode, or workflow-specific mode.

## Decision

| Built-in Mode | ID | Purpose |
|---------------|-----|---------|
| Edit | `edit` | Main editing mode with tool system |
| Edit Front Page | `edit_front_page` | Links to canonical URL when on `/` |

## Pattern

```php
namespace Drupal\my_module\Plugin\Mode;

use Drupal\navigation_plus\Attribute\Mode;
use Drupal\navigation_plus\ModePluginBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Mode(
  id: 'preview',
  label: new TranslatableMarkup('Preview Mode'),
  weight: 200,
)]
class Preview extends ModePluginBase {

  public function applies(): bool {
    return $this->entity instanceof NodeInterface
      && $this->entity->hasField('layout_builder__layout');
  }

  public function buildToolbar(array &$variables): array {
    return ['#markup' => '<div class="preview-toolbar">Preview</div>'];
  }

  public function buildBars(array &$page_top, ModeInterface $mode): void {
    // No sidebars for preview mode.
  }

  public function buildModeButton(): array {
    return [
      '#type' => 'link',
      '#title' => $this->t('Preview'),
      '#url' => Url::fromRoute('<current>'),
    ];
  }

  public function getIconPath(): string {
    return $this->extensionList->getPath('my_module') . '/assets/preview.svg';
  }

  public function addAttachments(array &$attachments): void {
    $attachments['#attached']['library'][] = 'my_module/preview_mode';
  }

  public function getSummary(): string {
    return 'Preview content before publishing.';
  }
}
```

**Attribute properties:**

| Property | Type | Purpose |
|----------|------|---------|
| `id` | string | Unique plugin ID |
| `label` | TranslatableMarkup | Human-readable name |
| `weight` | int | Display order (lower = earlier) |

**Discovery:** `ModePluginManager` discovers from `Plugin/Mode` namespace.

## Common Mistakes

- **Wrong**: Returning `TRUE` always from `applies()` → **Right**: Scope to specific entity types; modes appearing on every entity pollute the toolbar
- **Wrong**: Creating modes that conflict with the tool system → **Right**: Modes change the entire toolbar context; design them as complete alternatives

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Tool Plugins](tool-plugins.md)
- Reference: `navigation_plus/src/Plugin/Mode/Edit.php`
