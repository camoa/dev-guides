---
description: Defining permissions in modules, creating dynamic permissions with callbacks, and grouping them into roles.
---

# Permissions and Roles

## When to Use
Defining what actions users can perform and grouping those permissions into roles.

## Steps
1. **Define permissions in `MODULE.permissions.yml`**
   ```yaml
   administer widgets:
     title: 'Administer widgets'
     description: 'Create, edit, and delete widgets'
     restrict access: true  # Shows security warning

   view published widgets:
     title: 'View published widgets'
     description: 'View widgets marked as published'
   ```

2. **For dynamic permissions, use permission callbacks**
   ```yaml
   permission_callbacks:
     - Drupal\mymodule\WidgetPermissions::permissions
   ```
   ```php
   class WidgetPermissions {
     public function permissions() {
       $permissions = [];
       foreach (WidgetType::loadMultiple() as $type) {
         $permissions["edit {$type->id()} widgets"] = [
           'title' => $this->t('Edit @type widgets', ['@type' => $type->label()]),
         ];
       }
       return $permissions;
     }
   }
   ```

3. **Check permissions in code**
   ```php
   $account = \Drupal::currentUser();
   if ($account->hasPermission('administer widgets')) {
     // Allowed
   }
   ```

4. **Create roles programmatically (rare)**
   ```php
   $role = Role::create([
     'id' => 'widget_editor',
     'label' => 'Widget Editor',
   ]);
   $role->grantPermission('view published widgets');
   $role->grantPermission('edit own widgets');
   $role->save();
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Defining permission | Grants administrative power | Set `restrict access: true` for security warning |
| Choosing granularity | Action affects all entities of type | Single permission like "edit widgets" |
| Choosing granularity | Action depends on ownership or state | Multiple permissions: "edit own", "edit any" |
| Implementation | Permission is static | Use `*.permissions.yml` |
| Implementation | Permission depends on config entities | Use `permission_callbacks` |

## Common Mistakes
- Too many permissions -- Users can't understand them; aim for <10 per module
- Too few permissions -- Can't delegate safely; separate admin from editing
- Missing "view" permission -- Assuming authenticated users can view everything
- Not using "restrict access: true" -- Admin permissions lack security warnings
- Hardcoding permission strings -- Use constants: `MyModule::PERMISSION_ADMIN`

## See Also
- Reference: `/core/modules/user/src/PermissionHandler.php`
- [Route Access Checks](route-access-checks.md) for using permissions on routes
