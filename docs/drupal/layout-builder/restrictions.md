---
description: Restricting which blocks can be added to layouts
drupal_version: "11.x"
---

# Layout Builder Restrictions

### When to Use

When you need to limit which blocks, layouts, or sections editors can add in Layout Builder to prevent overwhelming choices or enforce content governance.

### Steps

1. **Via Contrib Module (Recommended)**
   - Install [Layout Builder Restrictions](https://www.drupal.org/project/layout_builder_restrictions)
   - Navigate to view display Layout Builder settings
   - Configure allowed blocks per layout region
   - Configure allowed layouts per entity type/bundle

2. **Via hook_layout_builder_restrictions_allowed_blocks_alter()**
   ```php
   function mymodule_layout_builder_restrictions_allowed_blocks_alter(array &$blocks, array $context) {
     // Restrict to specific blocks
     $allowed = [
       'field_block:node:article:body',
       'system_branding_block',
       'inline_block:basic',
     ];

     $blocks = array_intersect_key($blocks, array_flip($allowed));
   }
   ```

3. **Via core alter hooks**
   ```php
   function mymodule_layout_builder_block_alter(array &$definitions) {
     // Remove blocks from Layout Builder entirely
     foreach ($definitions as $id => $definition) {
       if (strpos($id, 'field_block:node:article:field_internal') === 0) {
         unset($definitions[$id]);
       }
     }
   }
   ```

4. **Via permissions**
   - "Administer blocks" required to see all blocks
   - Without permission, users only see blocks they have access to

### Decision Points

| At this point... | If... | Then... |
|---|---|---|
| Too many blocks | Editors overwhelmed | Use Layout Builder Restrictions to whitelist allowed blocks per region |
| Security concern | Some blocks expose sensitive data | Remove blocks via alter hook or restrict with permissions |
| Layout governance | Want to enforce specific layouts | Restrict allowed layouts to approved set |
| Per-bundle control | Different bundles need different blocks | Configure restrictions per entity_view_display |
| Editorial training | Want to simplify UI | Hide advanced blocks, show only commonly-used ones |

### Common Mistakes

- **Not installing Layout Builder Restrictions** → Core provides no UI for restrictions. Attempting to configure without contrib module = writing custom code
- **Over-restricting** → Restricting too much frustrates editors. Balance governance with flexibility
- **Forgetting about permissions** → Block-level permissions apply in LB. User without "Administer blocks" sees fewer blocks than admin
- **Not testing as editor** → Restrictions configured as admin may hide blocks editors need. Test with editor role
- **Restricting after editors trained** → Changing available blocks after editors learn system causes confusion. Plan restrictions early
- **Assuming restrictions are security** → Restrictions are UI convenience, not security hardening. Don't rely on them to prevent access to sensitive data

### See Also

- Section 8: Field & Extra Field Blocks (controlling field block availability)
- Section 16: Best Practices (editorial governance)
- Reference: [Layout Builder Restrictions module](https://www.drupal.org/project/layout_builder_restrictions)
