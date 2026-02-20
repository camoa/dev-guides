## 13. Layout Builder Events & Hooks

### When to Use

When you need to alter layout rendering, modify section/component behavior, or integrate custom logic during layout building.

### Items

#### SectionComponentBuildRenderArrayEvent

**Description:** Dispatched when a component builds its render array — primary hook point for altering block rendering in LB

**Event Name:** `LayoutBuilderEvents::SECTION_COMPONENT_BUILD_RENDER_ARRAY`

**Use Case:** Modify component render array, add cacheable metadata, alter block output

**Example:**
```php
namespace Drupal\mymodule\EventSubscriber;

use Drupal\layout_builder\Event\SectionComponentBuildRenderArrayEvent;
use Drupal\layout_builder\LayoutBuilderEvents;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class LayoutBuilderSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents() {
    return [
      LayoutBuilderEvents::SECTION_COMPONENT_BUILD_RENDER_ARRAY => 'onBuildRender',
    ];
  }

  public function onBuildRender(SectionComponentBuildRenderArrayEvent $event) {
    $build = $event->getBuild();

    // Modify render array
    if ($event->getComponent()->getPluginId() === 'system_branding_block') {
      $build['#prefix'] = '<div class="custom-wrapper">';
      $build['#suffix'] = '</div>';
    }

    $event->setBuild($build);

    // Add cache metadata
    $event->getCacheableMetadata()->addCacheTags(['custom_tag']);
  }
}
```

**Gotchas:**
- Fired for every component in every section on every layout render — keep logic fast
- Must use `setBuild()` to persist changes
- Caching metadata added via `getCacheableMetadata()`, not directly on build array

#### PrepareLayoutEvent

**Description:** Dispatched before layout builds, after section storage is determined

**Event Name:** `LayoutBuilderEvents::PREPARE_LAYOUT`

**Use Case:** Modify sections before rendering, add/remove components programmatically

**Example:**
```php
public function onPrepareLayout(PrepareLayoutEvent $event) {
  $section_storage = $event->getSectionStorage();

  // Add component to first section
  if ($section_storage->count() > 0) {
    $section = $section_storage->getSection(0);
    $component = new SectionComponent(
      \Drupal::service('uuid')->generate(),
      'content',
      ['id' => 'system_branding_block']
    );
    $section->appendComponent($component);
  }
}
```

**Gotchas:**
- Changes affect this render only, not saved
- For persistent changes, save section storage or entity after modifications

#### hook_layout_builder_view_context_alter()

**Description:** Alter contexts available to layout builder (entity, view_mode, etc.)

**Use Case:** Provide additional contexts to blocks in layouts

**Example:**
```php
function mymodule_layout_builder_view_context_alter(array &$contexts, \Drupal\Core\Plugin\Context\ContextInterface $layout_entity) {
  // Add custom context
  $contexts['mymodule_custom'] = new Context(
    new ContextDefinition('string'),
    'custom value'
  );
}
```

**Gotchas:**
- Contexts must implement ContextInterface
- Changes apply to all blocks in layout
- Be cautious with expensive context data — affects cache

#### hook_ENTITY_TYPE_view_alter()

**Description:** Standard entity view alter hook — works on entities rendered with LB

**Use Case:** Alter final entity render array after LB processes

**Example:**
```php
function mymodule_node_view_alter(array &$build, \Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display) {
  if (isset($build['_layout_builder'])) {
    // Entity uses Layout Builder
    $build['_layout_builder']['#prefix'] = '<div class="lb-wrapper">';
    $build['_layout_builder']['#suffix'] = '</div>';
  }
}
```

**Gotchas:**
- LB adds `_layout_builder` key to build array
- Runs after LB processing, so layout already rendered
- Standard entity view cache tags apply

#### hook_layout_alter()

**Description:** Alter layout plugin definitions

**Use Case:** Modify layout regions, labels, templates for existing layouts

**Example:**
```php
function mymodule_layout_alter(&$definitions) {
  if (isset($definitions['layout_onecol'])) {
    $definitions['layout_onecol']['label'] = 'Single Column';
    $definitions['layout_onecol']['category'] = 'Custom Category';
  }
}
```

**Gotchas:**
- Affects layout globally, not per-instance
- Changing regions breaks existing sections using that layout
- Clear cache after changes

#### hook_layout_builder_block_alter()

**Description:** Alter block plugin definitions in Layout Builder context

**Use Case:** Hide blocks from LB, modify block metadata

**Example:**
```php
function mymodule_layout_builder_block_alter(array &$definitions) {
  // Hide internal blocks from LB
  foreach ($definitions as $id => $definition) {
    if (strpos($id, 'field_block:node:article:field_internal') === 0) {
      unset($definitions[$id]);
    }
  }
}
```

**Gotchas:**
- Only affects LB context, not Block Layout
- Derivative blocks use base_id:derivative_id pattern

### Common Mistakes

- **Modifying events without returning** → Events use `setBuild()` or `setContexts()`. Forgetting to call setter = changes lost
- **Heavy processing in event subscribers** → Events fire on every page render. Keep logic fast, add caching
- **Not adding cache metadata** → Custom logic creates cache dependencies. Use `getCacheableMetadata()` to add tags/contexts
- **Assuming events fire during admin editing** → Events fire on view, not during layout editing in admin UI
- **Mutating section storage without saving** → Changes in events are runtime only. For persistent changes, save storage
- **Forgetting to register subscriber** → Event subscribers must be registered in `MODULE.services.yml` with tag `event_subscriber`

### See Also

- Section 6: Block Placement (component structure)
- Section 18: Security & Performance (caching considerations)
- Reference: `/core/modules/layout_builder/src/Event/SectionComponentBuildRenderArrayEvent.php`
- Reference: `/core/modules/layout_builder/src/Event/PrepareLayoutEvent.php`
