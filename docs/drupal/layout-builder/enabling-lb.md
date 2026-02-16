---
description: How to enable Layout Builder on content types, custom entities, and view modes via UI, config, or code.
---

## 2. Enabling Layout Builder

### When to Use

When you want to enable Layout Builder on a content type, custom entity type, or specific view mode.

### Steps

1. **Via UI**
   - Navigate to Structure → Content types → [Content type] → Manage display
   - Enable "Use Layout Builder" checkbox
   - Optionally enable "Allow each content item to have its layout customized"
   - Save

2. **Via Configuration**
   - Edit `core.entity_view_display.{entity_type}.{bundle}.{view_mode}.yml`
   - Add third_party_settings for layout_builder
   - Export or include in recipe

3. **Programmatically**
   ```php
   use Drupal\layout_builder\Entity\LayoutBuilderEntityViewDisplay;

   $display = LayoutBuilderEntityViewDisplay::load('node.article.default');
   $display->enableLayoutBuilder()
     ->setOverridable(FALSE)  // or TRUE for per-entity overrides
     ->save();
   ```

4. **Verify permissions**
   - "Configure any layout" — administer default layouts
   - "Configure editable {entity_type} {bundle} layout overrides" — per-entity layouts

5. **Result**: LB enabled, section field added (if overrides), fields converted to blocks in default section

### Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Enabling LB | Fresh install or new content type | Enable defaults only first, test workflow before enabling overrides |
| Enabling LB | Existing content with field display config | Fields automatically become field blocks in first section, verify display settings preserved |
| Allowing overrides | Need per-entity layouts | Enable "allow_custom", grants per-entity customization but prevents updating from defaults |
| Allowing overrides | All entities should match default | Leave "allow_custom" disabled, easier maintenance and updates |

### Common Mistakes

- **Enabling overrides immediately** → Start with defaults. Overrides create maintenance burden. Once entity is overridden, default updates don't apply
- **Not checking permissions** → Different permissions for defaults vs overrides. Configure permissions or editors can't use LB
- **Forgetting to save** → UI requires explicit save. Config export requires explicit drush cex. Changes aren't automatic
- **Not testing field conversion** → When enabling LB on existing display, fields become blocks. Verify formatters and labels preserved

### See Also

- Section 3: Config Schema (YAML structure)
- Section 9: Defaults vs Overrides (choosing between them)
- Reference: `/core/modules/layout_builder/src/Entity/LayoutBuilderEntityViewDisplay.php` (enableLayoutBuilder method)
