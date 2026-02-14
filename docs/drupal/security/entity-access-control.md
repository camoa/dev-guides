---
description: Controlling entity CRUD operations through custom access handlers with proper cache metadata and entity query access checks.
---

# Entity Access Control

## When to Use
Controlling access to entity operations (view, update, delete, create) through entity access handlers.

## Steps
1. **Check access before operations**
   ```php
   // Always check before entity operations
   $node = Node::load($nid);
   if (!$node->access('update')) {
     throw new AccessDeniedHttpException();
   }
   $node->setTitle('New Title')->save();
   ```

2. **Define custom entity access handler**
   ```php
   // In entity type annotation
   handlers = {
     "access" = "Drupal\mymodule\WidgetAccessControlHandler",
   }
   ```

3. **Implement access handler**
   ```php
   namespace Drupal\mymodule;
   use Drupal\Core\Entity\EntityAccessControlHandler;
   use Drupal\Core\Entity\EntityInterface;
   use Drupal\Core\Session\AccountInterface;

   class WidgetAccessControlHandler extends EntityAccessControlHandler {
     protected function checkAccess(EntityInterface $entity, $operation, AccountInterface $account) {
       switch ($operation) {
         case 'view':
           // Published widgets are viewable by all
           if ($entity->isPublished()) {
             return AccessResult::allowed()
               ->addCacheableDependency($entity);
           }
           // Unpublished: only owner or admin
           return AccessResult::allowedIf(
             $account->id() == $entity->getOwnerId()
             || $account->hasPermission('administer widgets')
           )->cachePerPermissions()->cachePerUser()->addCacheableDependency($entity);

         case 'update':
           // Owner can edit own, admin can edit all
           return AccessResult::allowedIf(
             $account->id() == $entity->getOwnerId()
           )->orIf(
             AccessResult::allowedIfHasPermission($account, 'administer widgets')
           )->cachePerUser()->cachePerPermissions();

         case 'delete':
           // Only admin can delete
           return AccessResult::allowedIfHasPermission($account, 'administer widgets');

         default:
           return AccessResult::neutral();
       }
     }

     protected function checkCreateAccess(AccountInterface $account, array $context, $entity_bundle = NULL) {
       return AccessResult::allowedIfHasPermission($account, 'create widgets');
     }
   }
   ```

4. **Use access in queries**
   ```php
   // Entity query with access check
   $query = \Drupal::entityQuery('node')
     ->accessCheck(TRUE)  // REQUIRED in D10+
     ->condition('type', 'article')
     ->execute();
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Choosing handler | Standard content entity | Extend `EntityAccessControlHandler` |
| Choosing handler | Config entity | Usually no access handler (admin-only) |
| checkAccess logic | Operation is view | Check published status, ownership |
| checkAccess logic | Operation is update/delete | Check ownership + permissions |
| Query building | Querying entities | ALWAYS use `->accessCheck(TRUE)` |

## Common Mistakes
- Using `->accessCheck(FALSE)` without justification -- Exposes all entities, security hole
- Not calling `$entity->access()` before operations -- Access checks bypassed
- Direct database queries -- Completely bypass entity access system
- Forgetting cache metadata -- Access result not invalidated when entity changes
- Not implementing checkCreateAccess -- Create always denied

## See Also
- Reference: `/core/lib/Drupal/Core/Entity/EntityAccessControlHandler.php`
- [Content Access (Node Grants)](content-access-node-grants.md) for node-specific grants
- Reference: https://www.drupal.org/docs/8/api/entity-api/access-checking-for-content-entities
