---
description: Media access control and permissions — role-based permissions, type-specific grants, and programmatic access checking.
---

## 12. Media Access & Permissions

### When to Use

You need to control who can create, edit, delete, and view media.

### Decision

| Permission | Grants |
|---|---|
| `administer media` | Full media admin: create types, configure fields, view all media |
| `administer media types` | Create and edit media types, field configuration |
| `access media overview` | View `/admin/content/media` listing |
| `view media` | View published media entities (required for all users) |
| `view own unpublished media` | Authors see their own unpublished media |
| `create [type] media` | Upload new media of specific type |
| `edit own [type] media` | Edit own media of specific type |
| `edit any [type] media` | Edit all media of specific type |
| `delete own [type] media` | Delete own media of specific type |
| `delete any [type] media` | Delete all media of specific type |

### Pattern

**Role-based permissions** (in module.permissions.yml or via UI export):
```yaml
# Authenticated user permissions
authenticated:
  - 'view media'

# Content editor permissions
editor:
  - 'view media'
  - 'access media overview'
  - 'create image media'
  - 'edit own image media'
  - 'delete own image media'
  - 'create document media'
  - 'edit own document media'

# Media manager permissions
media_manager:
  - 'view media'
  - 'access media overview'
  - 'create image media'
  - 'edit any image media'
  - 'delete any image media'
  - 'create document media'
  - 'edit any document media'
  - 'delete any document media'
  - 'create remote_video media'
  - 'edit any remote_video media'

# Administrator permissions
administrator:
  - 'administer media'
  - 'administer media types'
```

**Programmatic access control**:
```php
// Check if user can view media entity
if ($media->access('view')) {
  // Render media
}

// Check if user can edit
if ($media->access('update')) {
  // Show edit form
}

// Check permission before showing upload widget
if (\Drupal::currentUser()->hasPermission('create image media')) {
  // Show upload button
}
```

### Common Mistakes

- Not granting `view media` to authenticated users → media doesn't display for logged-in users
- Granting `administer media` to content editors → too broad; use type-specific permissions
- Not using Media Library's built-in access checks → custom forms bypass security; use Media Library widget
- Exposing unpublished media in listings → check `status` field in views and queries
- Not considering file permissions separately → media permissions don't control direct file access; see [Media File System](media-file-system.md)

### See Also

- [Media File System](media-file-system.md) (file-level access)
- Reference: `/core/modules/media/media.permissions.yml`
- Reference: `/core/modules/media/src/MediaAccessControlHandler.php`
