---
description: Quick reference map of key Layout Builder classes, files, services, and common code patterns for programmatic use.
---

## 19. Code Reference Map

### When to Use

Quick reference for finding key classes and files when working with Layout Builder programmatically.

### Items

#### Core Classes

**Section Management:**
- `Drupal\layout_builder\Section` — Section value object (layout + components)
- `Drupal\layout_builder\SectionComponent` — Component within section (block placement)
- `Drupal\layout_builder\SectionStorageInterface` — Storage interface for sections
- `Drupal\layout_builder\Plugin\SectionStorage\DefaultsSectionStorage` — Default layout storage
- `Drupal\layout_builder\Plugin\SectionStorage\OverridesSectionStorage` — Per-entity override storage

**Entity Display:**
- `Drupal\layout_builder\Entity\LayoutBuilderEntityViewDisplay` — Extended view display entity
- `Drupal\layout_builder\Entity\LayoutEntityDisplayInterface` — Interface for LB displays

**Layout Plugins:**
- `Drupal\Core\Layout\LayoutInterface` — Layout plugin interface
- `Drupal\Core\Layout\LayoutDefault` — Base layout plugin class
- `Drupal\Core\Layout\LayoutDefinition` — Layout plugin definition
- `Drupal\Core\Layout\LayoutPluginManager` — Layout plugin discovery

**Block Plugins:**
- `Drupal\layout_builder\Plugin\Block\InlineBlock` — Non-reusable inline blocks
- `Drupal\layout_builder\Plugin\Block\FieldBlock` — Entity field blocks
- `Drupal\layout_builder\Plugin\Block\ExtraFieldBlock` — Extra field blocks

**Events:**
- `Drupal\layout_builder\Event\SectionComponentBuildRenderArrayEvent` — Component render event
- `Drupal\layout_builder\Event\PrepareLayoutEvent` — Pre-render layout event
- `Drupal\layout_builder\LayoutBuilderEvents` — Event constant definitions

**Services:**
- `inline_block.usage` (`Drupal\layout_builder\InlineBlockUsage`) — Track inline block usage
- `plugin.manager.layout_builder.section_storage` — Section storage plugin manager
- `plugin.manager.core.layout` — Layout plugin manager

#### Key Files

**Configuration Schema:**
- `/core/modules/layout_builder/config/schema/layout_builder.schema.yml` — Config structure definitions

**Layout Definitions:**
- `/core/modules/layout_builder/layout_builder.layouts.yml` — LB-specific layouts
- `/core/modules/layout_discovery/layout_discovery.layouts.yml` — Core general-purpose layouts

**Templates:**
- `/core/modules/layout_builder/templates/layout.html.twig` — Base layout template
- `/core/modules/layout_builder/templates/layout-builder-*.html.twig` — Admin UI templates
- `/core/themes/*/templates/layout/*.html.twig` — Theme-specific layout templates

**Forms:**
- `/core/modules/layout_builder/src/Form/DefaultsEntityForm.php` — Edit defaults form
- `/core/modules/layout_builder/src/Form/OverridesEntityForm.php` — Edit overrides form
- `/core/modules/layout_builder/src/Form/ConfigureSectionForm.php` — Section configuration
- `/core/modules/layout_builder/src/Form/AddBlockForm.php` — Add block form

**Routing:**
- `/core/modules/layout_builder/layout_builder.routing.yml` — LB routes
- `/core/modules/layout_builder/layout_builder.links.task.yml` — Local tasks

#### Common Patterns

**Load section storage:**
```php
$storage_manager = \Drupal::service('plugin.manager.layout_builder.section_storage');
$storage = $storage_manager->load('defaults', [
  'display' => EntityViewDisplay::load('node.article.default'),
]);
$sections = $storage->getSections();
```

**Create section:**
```php
use Drupal\layout_builder\Section;

$section = new Section('layout_twocol_section', ['label' => '']);
$display->appendSection($section);
$display->save();
```

**Create component:**
```php
use Drupal\layout_builder\SectionComponent;

$component = new SectionComponent(
  \Drupal::service('uuid')->generate(),
  'first',
  ['id' => 'system_branding_block', 'label_display' => '0']
);
$section->appendComponent($component);
```

**Get inline block usage:**
```php
$usage = \Drupal::service('inline_block.usage');
$orphans = $usage->getUnused(100);
```

**Access entity via context:**
```php
// In block plugin build()
$entity = $this->getContextValue('entity');
```

### Common Mistakes

- **Using wrong namespace** → Layout Builder classes in `Drupal\layout_builder`, core Layout API in `Drupal\Core\Layout`
- **Confusing Section and SectionComponent** → Section = container with layout. SectionComponent = block in section
- **Not using services** → Access plugin managers and usage tracking via dependency injection, not static calls
- **Wrong storage plugin** → Defaults use `DefaultsSectionStorage`, overrides use `OverridesSectionStorage`. Different loading
- **Forgetting to import classes** → Use statements required for Section, SectionComponent, etc.

### See Also

- Section 3: Config Schema (YAML structure)
- Section 6: Block Placement (creating components)
- Section 13: Events & Hooks (event classes)
- Reference: [Drupal API documentation](https://api.drupal.org/api/drupal/core!modules!layout_builder!layout_builder.module/group/layout_builder/11.x)
