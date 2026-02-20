## 6. Block Placement in Layouts

### When to Use

When adding blocks to Layout Builder sections programmatically, understanding component structure, or manipulating block configuration.

### Steps

1. **Create SectionComponent instance**
   ```php
   use Drupal\layout_builder\SectionComponent;

   $component = new SectionComponent(
     \Drupal::service('uuid')->generate(),  // UUID
     'first',                                // Region
     [
       'id' => 'system_branding_block',      // Block plugin ID
       'label_display' => '0',
       'context_mapping' => ['entity' => 'layout_builder.entity'],
     ]
   );
   ```

2. **Set weight (optional)**
   ```php
   $component->setWeight(10);  // Lower = earlier in region
   ```

3. **Add to section**
   ```php
   $section = $display->getSection(0);  // Or create new section
   $section->appendComponent($component);  // Add to end
   // OR
   $section->insertComponent(0, $component);  // Insert at position
   ```

4. **Save display or entity**
   ```php
   // For defaults
   $display->save();

   // For overrides
   $entity->save();
   ```

### Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing block plugin | Entity field data | Use `field_block:{entity_type}:{bundle}:{field_name}` derivative |
| Choosing block plugin | Custom content each placement | Use `inline_block:{block_content_type}` derivative |
| Choosing block plugin | Reusable content | Use `block_content:{uuid}` plugin for existing block content entity |
| Choosing block plugin | System/contrib block | Use base plugin ID (e.g., `system_branding_block`) |
| Setting context_mapping | Block needs entity | Map `entity: 'layout_builder.entity'` for field blocks, inline blocks |
| Choosing region | Multiple regions available | Check layout plugin definition for region names and default |
| Setting weight | Order matters | Lower weight renders first, negative weights allowed |

### Common Mistakes

- **Invalid block plugin ID** → Verify plugin exists with block manager. Typos cause white screen or missing blocks
- **Wrong derivative format** → Field blocks: `field_block:entity_type:bundle:field_name`. Inline blocks: `inline_block:block_content_type`
- **Missing context mapping** → Field blocks and inline blocks require entity context. Missing mapping = no entity data, block can't render
- **Forgetting to save** → Adding components to section doesn't persist until `$display->save()` or `$entity->save()`
- **Duplicate UUIDs** → Each component needs unique UUID. Duplicates cause unpredictable behavior
- **Region doesn't exist in layout** → Component with invalid region won't render. Verify region exists in layout plugin definition
- **Not handling return values** → Many SectionComponent methods return `$this` for chaining. Forgetting assignment after `setWeight()` etc. loses changes

### See Also

- Section 3: Config Schema (component configuration structure)
- Section 4: Sections & Layouts (section and region concepts)
- Section 7: Inline vs Reusable (block type decisions)
- Section 8: Field & Extra Field Blocks (entity field blocks)
- Reference: `/core/modules/layout_builder/src/SectionComponent.php`
