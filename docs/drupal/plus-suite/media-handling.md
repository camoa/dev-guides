---
description: Media handling in Plus Suite — desktop drag-and-drop with DropzoneJS, media replacement, file association settings, and related events
drupal_version: "11.x"
---

# Media Handling

## When to Use

> Use desktop drag-and-drop for fast media placement. Configure file associations per user to skip the association modal. Use the Change tool for media library selection.

## Decision

| Workflow | Method | When |
|----------|--------|------|
| New media from desktop | Desktop drag-and-drop (DropzoneJS) | Dragging files from file browser |
| Replace existing media | File drag onto existing block | Updating hero images, banners |
| Select from media library | Change tool (Edit+) | Selecting existing media entities |

## Pattern

**Desktop drag-and-drop flow:**
1. File dragged from desktop triggers `file-drag` behavior
2. Drop zones appear on valid regions
3. File uploaded via DropzoneJS
4. `MediaDropzoneJs::newMedia()` controller fires
5. User settings checked for file extension → block type association
6. If no association, `MediaBlockFileAssociationForm` opens (modal)
7. Media entity created, block placed with media reference

**File association settings** (per-user, eliminates modal):
```php
$user->navigation_plus_settings[0]['file_associations'] = [
  'jpg' => 'image',
  'png' => 'image',
  'mp4' => 'video',
];
```
Configure via Settings sidebar → Media File Association section.

**Media events:**

| Event | When |
|-------|------|
| `LayoutBuilderNewMedia` | New file dropped on page |
| `LayoutBuilderReplaceMedia` | File dropped on existing block |
| `EditableFieldAttributes` | Change tool on media field |

## Common Mistakes

- **Wrong**: Forgetting the DropzoneJS repository in composer.json → **Right**: The JS library isn't available via packagist; add repository before requiring plus_suite
- **Wrong**: Skipping file association configuration → **Right**: Without associations, every drag triggers a modal asking for block type; configure common extensions

## See Also

- [Installation & Setup](installation-setup.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `lb_plus/src/Controller/MediaDropzoneJs.php`
