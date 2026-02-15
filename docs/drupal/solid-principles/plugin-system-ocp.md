---
description: Use Drupal plugins to extend functionality without modifying existing code
drupal_version: "11.x"
---

# Plugin System - Open for Extension (OCP)

## When to Use

Plugins are Drupal's primary OCP mechanism -- extend functionality without modifying existing code. Use plugins for blocks, field formatters/widgets, views plugins, etc.

## Decision

| To extend... | Use plugin type... | Define in... |
|---|---|---|
| Block system | Block plugin | `src/Plugin/Block/MyBlock.php` |
| Field display | Field formatter plugin | `src/Plugin/Field/FieldFormatter/` |
| Field input | Field widget plugin | `src/Plugin/Field/FieldWidget/` |
| Views data | Views plugin | `src/Plugin/views/` |
| Custom system | Custom plugin type | Define plugin manager |

## Pattern

**GOOD: Extending via plugin (OCP)**

```php
// New block plugin - extends block system without modifying core
namespace Drupal\mymodule\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Block\Attribute\Block;

#[Block(
  id: "my_custom_block",
  admin_label: new TranslatableMarkup("My Custom Block"),
)]
class MyCustomBlock extends BlockBase {
  public function build() {
    return ['#markup' => 'Extended without modifying core'];
  }
}
```

**BAD: Modifying core (violates OCP)**

```php
// NEVER: Editing /core/modules/block/src/BlockBase.php
// Adding your custom logic to core files
```

Plugin discovery is automatic -- plugin manager scans `src/Plugin/{PluginType}/` namespace. No modifications needed to existing code.

Reference:

- `/core/lib/Drupal/Core/Block/BlockBase.php` -- base class open for extension
- `/core/lib/Drupal/Core/Plugin/PluginBase.php` -- plugin foundation

## Common Mistakes

- Modifying core/contrib plugin classes directly -- create new plugin extending base. **WHY:** Core updates overwrite your changes; breaks upgrades; loses customizations
- Using hooks to modify plugin behavior when custom plugin would work -- create plugin. **WHY:** Hooks run on every request; plugins load only when used (performance)
- Not using plugin derivatives for similar plugins -- use plugin derivatives. **WHY:** 50 separate block plugins when you could use 1 derivative = code duplication
- Hardcoding plugin IDs instead of plugin manager -- use plugin manager service. **WHY:** Can't extend with new plugins; tight coupling to specific implementations

## See Also

- [Hooks & Events](hooks-events-ocp.md) for alter-based extension
- [Injection Interfaces](injection-interfaces-isp.md) for plugin injection patterns
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Plugin System Architecture](https://drupalize.me/tutorial/what-are-plugins)
