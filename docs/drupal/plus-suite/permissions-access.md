---
description: Plus Suite permissions matrix — Edit Mode access, inline editing, LB+ admin, and minimum permissions per role
tldr: "Apply this permission matrix when setting up roles for content editors and site builders."
drupal_version: "11.x"
---

# Permissions & Access

## When to Use

> Apply this permission matrix when setting up roles for content editors and site builders.

## Decision

| Role | Permissions |
|------|------------|
| Anonymous | None |
| Authenticated | None (or `use toolbar plus edit mode` for public editing) |
| Content Editor | Edit mode + inline editing + content permissions |
| Site Builder | All editor permissions + promote blocks + configure LB+ |
| Administrator | All permissions |

## Pattern

**Permission matrix:**

| Permission | Module | Purpose | Typical Role |
|------------|--------|---------|--------------|
| `use toolbar plus edit mode` | navigation_plus | Access Edit Mode toggle | Content editor |
| `configure toolbar plus modes` | navigation_plus | Enable/disable modes per bundle | Site admin |
| `administer Navigation + configuration` | navigation_plus | Global Plus Suite settings | Site admin |
| `access inline editing` | edit_plus | Use the Change tool | Content editor |
| `administer layout builder + configuration` | lb_plus | LB+ settings (promoted blocks) | Site admin |
| `promote layout builder + blocks` | lb_plus | Configure promoted blocks | Site builder |
| Standard Layout Builder permissions | core | Create and administer LB | Content editor |
| Standard media permissions | core | Upload and manage media | Content editor |

**Minimum permissions for content editors:**
```
- use toolbar plus edit mode
- access inline editing
- create and edit own content (per type)
- administer node display (if managing layouts)
- use media library
```

## Common Mistakes

- **Wrong**: Granting `administer Navigation + configuration` to content editors → **Right**: This allows changing global UI colors and settings; reserve for site admin
- **Wrong**: Granting `use toolbar plus edit mode` without `access inline editing` → **Right**: Users can enter Edit Mode but can't change anything; grant both together

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Inline Editing](inline-editing.md)
