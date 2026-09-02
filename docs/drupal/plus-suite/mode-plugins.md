---
description: "Create custom Mode plugins for Plus Suite — PHP 8 attribute syntax, ModeInterface methods, and built-in modes"
tldr: "Use custom Mode plugins when you need editing modes beyond the built-in Edit Mode — e.g., a Preview mode, Help mode, or workflow-specific mode."
drupal_version: "11.x"
---

# Mode Plugins

## When to Use

> When you need to create custom editing modes beyond the built-in Edit Mode (e.g., a Preview mode, Help mode, or workflow-specific mode).

## Mode Plugin Architecture

Modes are discovered by `ModePluginManager` from the `Plugin/Mode` namespace using PHP 8 attributes.

## Pattern: Attribute Definition

```php
use Drupal\navigation_plus\Attribute\Mode;

#[Mode(
  id: 'my_mode',
  label: new TranslatableMarkup('My Custom Mode'),
  weight: 200,
)]
class MyMode extends ModePluginBase implements PluginFormInterface {
  // ...
}
```

| Property | Type | Purpose |
|---|---|---|
| `id` | string | Unique plugin ID |
| `label` | TranslatableMarkup | Human-readable name |
| `weight` | int | Display order (lower = earlier) |

## Required Methods (ModeInterface)

```php
interface ModeInterface {
  // Whether this mode applies to the current entity/context.
  public function applies(): bool;

  // Build the toolbar render array for this mode.
  public function buildToolbar(array &$variables): array;

  // Build top bar and sidebars for this mode.
  public function buildBars(array &$page_top, ModeInterface $mode): void;

  // Render array for the mode toggle button in the Navigation sidebar.
  public function buildModeButton(): array;

  // Absolute path to SVG icon file for mode button.
  public function getIconPath(): string;

  // Add CSS/JS library attachments.
  public function addAttachments(array &$attachments): void;

  // Configuration summary string.
  public function getSummary(): string|TranslatableMarkup;
}
```

## Built-in Modes

| Mode | ID | Weight | Purpose |
|---|---|---|---|
| Edit | `edit` | 100 | Main editing mode with tool system |
| Edit Front Page | `edit_front_page` | 100 | Links to canonical URL when on `/` |

## Edit Mode Internal Flow

The `Edit` mode plugin (`navigation_plus/src/Plugin/Mode/Edit.php`):
1. `buildToolbar()` — renders tool buttons sorted by weight
2. `buildTopBar()` — renders Save, Refresh, Discard buttons
3. `buildSideBars()` — renders left/right sidebars from active tools
4. `getToolPlugins()` — loads all tool plugins that apply to current entity
5. `getActiveTool()` — reads `activeTool` cookie (defaults to `pointer`)

## Pattern: Creating a Custom Mode

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
    // Only on nodes with Layout Builder.
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

## Common Mistakes

- **Do not** create modes that conflict with existing tool system — modes change the entire toolbar context.
- **Do not** forget to implement `applies()` — returning `TRUE` always means the mode appears on every entity.

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Tool Plugins](tool-plugins.md)
- Reference: `navigation_plus/src/Plugin/Mode/Edit.php`
