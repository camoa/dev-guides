---
description: "Configure granular permissions for taxonomy term operations"
tldr: "Use per-vocabulary permissions for granular term CRUD control. Grant `administer taxonomy` only to trusted site administrators."
drupal_version: "11.x"
---

# Taxonomy Permissions & Access

## When to Use

> Use this guide when configuring granular permissions for taxonomy term operations.

Drupal provides per-vocabulary permissions for term CRUD operations.

## Steps

1. **Understand base permissions** — Taxonomy module provides global permissions:
   - `administer taxonomy` — Full control over all vocabularies and terms
   - `access taxonomy overview` — View taxonomy overview pages

2. **Use per-vocabulary permissions** — Dynamically generated for each vocabulary:
   - `create terms in VOCAB_ID` — Create new terms in vocabulary
   - `edit terms in VOCAB_ID` — Edit existing terms
   - `delete terms in VOCAB_ID` — Delete terms
   - `view term revisions in VOCAB_ID` — View term revision history
   - `revert term revisions in VOCAB_ID` — Revert to previous revision (requires edit permission too)
   - `delete term revisions in VOCAB_ID` — Delete specific revisions (requires delete permission too)

3. **Configure via UI** — Navigate to `/admin/people/permissions`, search for vocabulary name

4. **Configure via code** — Check permissions in access control:
   ```php
   $account = \Drupal::currentUser();
   $vid = 'tags';

   if ($account->hasPermission('administer taxonomy')) {
     // Full access
   }
   elseif ($account->hasPermission("create terms in $vid")) {
     // Can create in specific vocabulary
   }
   ```

## Pattern

**Permission check in controller:**
```php
use Drupal\Core\Access\AccessResult;

public function checkAccess($vid) {
  $account = \Drupal::currentUser();

  return AccessResult::allowedIfHasPermissions(
    $account,
    ["create terms in $vid", 'administer taxonomy'],
    'OR'
  );
}
```

**Term access check (automatic):**
```php
$term = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->load($tid);

// Access checked automatically
if ($term->access('view')) {
  // User can view term
}
if ($term->access('update')) {
  // User can edit term
}
```

Reference: `/core/modules/taxonomy/src/TermAccessControlHandler.php` (lines 20-72)

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Permission granularity | Users need vocabulary-specific control | Use per-vocabulary permissions |
| Permission granularity | Site admins manage all taxonomy | Grant `administer taxonomy` |
| View access | Terms should be public | Ensure users have `access content` permission |
| View access | Terms are unpublished | Only users with `administer taxonomy` see unpublished terms |

## Common Mistakes

- Granting `administer taxonomy` to content editors → Too permissive; allows vocabulary deletion and structure changes. Use per-vocabulary permissions instead
- Forgetting `access content` for term viewing → Terms require both published status AND user has `access content`. Unpublished terms only visible to admins
- Not combining edit + revert for revision access → Reverting revisions requires BOTH `revert term revisions in VOCAB` AND `edit terms in VOCAB`. Grant both or users see "access denied"
- Assuming terms have view permissions like nodes → Terms use simpler access: published + `access content` for all users, OR `administer taxonomy` for admins. No per-term permissions without contrib
- Overlooking vocabulary access in entity reference → If user can't view terms, they won't appear in autocomplete or select widgets. Ensure field users have appropriate permissions

## See Also

- ← Previous: [Taxonomy Views Integration](taxonomy-views.md) | Next: [Term Storage & Querying](term-storage-querying.md) →
- Reference: `/core/modules/taxonomy/src/TaxonomyPermissions.php` (lines 64-82)
- Reference: [Drupal.org Permissions by Term module](https://www.drupal.org/project/permissions_by_term)
