---
description: Configure granular permissions for taxonomy term operations
drupal_version: "11.x"
---

# Taxonomy Permissions & Access

## When to Use

> Use per-vocabulary permissions for granular term CRUD control. Grant `administer taxonomy` only to trusted site administrators.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Users need vocabulary-specific control | Per-vocabulary permissions | Granular: `create terms in VOCAB_ID`, `edit terms in VOCAB_ID`, etc. |
| Site admins manage all taxonomy | `administer taxonomy` | Full control over all vocabularies and terms |
| Terms should be public | Ensure users have `access content` | Terms require published status + `access content` permission |
| Terms are unpublished | Only `administer taxonomy` users | Unpublished terms only visible to admins |
| Revision access needed | Grant both edit + revert permissions | Reverting requires BOTH `revert term revisions in VOCAB` AND `edit terms in VOCAB` |

## Pattern

**Per-vocabulary permissions:**
- `create terms in VOCAB_ID` — Create new terms
- `edit terms in VOCAB_ID` — Edit existing terms
- `delete terms in VOCAB_ID` — Delete terms
- `view term revisions in VOCAB_ID` — View revision history
- `revert term revisions in VOCAB_ID` — Revert to previous revision (requires edit too)
- `delete term revisions in VOCAB_ID` — Delete specific revisions (requires delete too)

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

if ($term->access('view')) {
  // User can view term
}
if ($term->access('update')) {
  // User can edit term
}
```

## Common Mistakes

- **Wrong**: Granting `administer taxonomy` to content editors → **Right**: Use per-vocabulary permissions instead
- **Wrong**: Forgetting `access content` for term viewing → **Right**: Terms require published status AND `access content` permission
- **Wrong**: Not combining edit + revert for revision access → **Right**: Grant both permissions or users see "access denied"
- **Wrong**: Assuming terms have view permissions like nodes → **Right**: Terms use simpler access: published + `access content` for all, OR `administer taxonomy` for admins
- **Wrong**: Overlooking vocabulary access in entity reference → **Right**: If user can't view terms, they won't appear in autocomplete/select widgets

## See Also

- [Taxonomy Views Integration](taxonomy-views.md)
- [Term Storage & Querying](term-storage-querying.md)
- Reference: `/core/modules/taxonomy/src/TermAccessControlHandler.php` (lines 20-72)
- Reference: `/core/modules/taxonomy/src/TaxonomyPermissions.php` (lines 64-82)
- Reference: [Drupal.org Permissions by Term module](https://www.drupal.org/project/permissions_by_term)
