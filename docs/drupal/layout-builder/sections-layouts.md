---
description: How sections work as containers with layout plugins, regions, and section storage types for defaults and overrides.
---

## 4. Sections & Layouts

### When to Use

When you need to understand how sections work, what layout plugins provide, and how regions structure content within a section.

### Items

#### Section (value object)

**Description:** A section is a container that uses a layout plugin to define regions and holds components (blocks) placed in those regions

**Key Methods:**
| Method | Returns | Purpose |
|--------|---------|---------|
| `getLayoutId()` | string | Layout plugin ID |
| `getLayout()` | LayoutInterface | Instantiated layout plugin |
| `getComponents()` | SectionComponent[] | All components in section |
| `getComponentsByRegion($region)` | SectionComponent[] | Components in specific region, sorted by weight |
| `appendComponent($component)` | $this | Add component to end of region |
| `toRenderArray()` | array | Render section with all components |

**Example:**
```php
use Drupal\layout_builder\Section;
use Drupal\layout_builder\SectionComponent;

$section = new Section('layout_twocol_section', ['label' => 'Two columns']);
$component = new SectionComponent(\Drupal::service('uuid')->generate(), 'first', [
  'id' => 'system_branding_block',
  'label_display' => '0',
]);
$section->appendComponent($component);
$build = $section->toRenderArray($contexts);
```

**Gotchas:**
- Section object is a value object — no entity, just data structure
- Stored as serialized array in config or entity field
- Third-party settings on sections enable module extensions (e.g., layout_builder_styles)

#### Layout Plugin

**Description:** Defines regions available in a section and how they render

**Properties:**
| Property | Type | Description |
|----------|------|-------------|
| label | string | Human-readable layout name |
| category | string | Grouping in layout selection UI |
| regions | mapping | Region machine names and labels |
| default_region | string | Region for new components when none specified |
| template | string | Twig template name |
| library | string | Asset library to attach |

**Example:**
```yaml
# my_theme.layouts.yml
my_custom_layout:
  label: 'Custom Layout'
  category: 'Custom'
  template: layout--custom
  library: my_theme/custom_layout
  default_region: main
  icon_map:
    - [sidebar, main]
  regions:
    sidebar:
      label: Sidebar
    main:
      label: Main Content
```

**Gotchas:**
- Layout plugins are discovered from `*.layouts.yml` files in modules/themes
- Template receives regions as variables, each region contains component render arrays
- `icon_map` defines visual representation in admin UI (grid pattern)
- Layout plugin can define configuration form for per-section settings

#### Region

**Description:** Named area within a layout where components can be placed

**Characteristics:**
- Defined by layout plugin's `regions` mapping
- Machine name used in component configuration
- Label shown in admin UI
- Default region receives components when region not specified

**Example:**
```php
// Get components for a region
$section = $display->getSection(0);
$components = $section->getComponentsByRegion('first');

// Add component to region
$component->setRegion('second');
$section->appendComponent($component);
```

**Gotchas:**
- Components reference region by machine name — renaming region breaks existing components
- Invalid region names cause components to not render (no error, just missing)
- Empty regions still render in template (themers can hide with CSS)

#### Section Storage

**Description:** Manages where sections are stored — defaults (in view display config) vs overrides (in entity field)

**Types:**
| Storage | Class | Where Stored | Use Case |
|---------|-------|--------------|----------|
| Defaults | DefaultsSectionStorage | entity_view_display third_party_settings | Default layout for all entities |
| Overrides | OverridesSectionStorage | Entity field (layout_section type) | Per-entity custom layouts |

**Example:**
```php
// Access section storage
$storage_manager = \Drupal::service('plugin.manager.layout_builder.section_storage');
$storage = $storage_manager->findByContext($contexts, $cacheability);
$sections = $storage->getSections();
```

**Gotchas:**
- Overrides storage only exists when `allow_custom: true` on view display
- Changing defaults doesn't update entities with overrides
- Section storage plugins can be extended by contrib (e.g., per-user layouts)

### Common Mistakes

- **Hardcoding layout IDs** → Use layout plugin manager to validate layouts exist. Layout IDs change if module/theme providing them is removed
- **Not checking region existence** → Verify region exists in layout before placing component. Invalid regions fail silently
- **Assuming section order** → Sections stored as array, order matters. Use `getSections()` not direct array access on programmatic manipulation
- **Forgetting contexts** → `toRenderArray($contexts)` needs entity context for field blocks to render correctly
- **Mutating sections without saving** → Section changes in defaults require `$display->save()`. Override sections require entity save

### See Also

- Section 5: Core Layout Plugins (available layouts)
- Section 6: Block Placement (components in regions)
- Section 9: Defaults vs Overrides (section storage types)
- Reference: `/core/modules/layout_builder/src/Section.php`
- Reference: `/core/lib/Drupal/Core/Layout/LayoutInterface.php`
