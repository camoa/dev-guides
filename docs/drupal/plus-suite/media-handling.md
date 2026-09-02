---
description: "Media handling in Plus Suite — desktop drag-and-drop with DropzoneJS, media replacement, file association settings, and related events"
tldr: "Use desktop drag-and-drop or media replacement to handle media in Plus Suite. Both depend on the DropzoneJS module and enyo/dropzone JS library."
drupal_version: "11.x"
---

# Media Handling

## When to Use

> When you need to understand how Plus Suite handles media drag-and-drop from desktop onto the page, or media replacement on existing blocks.

## Three Media Workflows

1. **Desktop drag-and-drop (new)**: Drag file from desktop onto page
2. **Media replacement**: Drag file onto existing media block to replace it
3. **Media library**: Use standard media library widget via Change tool

## Desktop Drag-and-Drop (DropzoneJS)

Requires `dropzonejs` module and `enyo/dropzone` JS library.

**Flow**:
1. File dragged from desktop triggers `file-drag` behavior
2. Drop zones appear on valid regions
3. File uploaded via DropzoneJS
4. `MediaDropzoneJs::newMedia()` controller fires
5. User settings checked for file extension → block type association
6. If no association, `MediaBlockFileAssociationForm` opens (modal)
7. Media entity created, block placed with media reference

## Media Replacement

**Flow**:
1. File dragged onto existing media block
2. `MediaDropzoneJs::replaceMedia()` controller fires
3. `LayoutBuilderReplaceMedia` event dispatched
4. New media entity created
5. Block's media reference field updated
6. Layout rebuilt via the `UpdateElement` AJAX command

## File Association Settings

Per-user setting mapping file extensions to block types. Stored in `user.navigation_plus_settings`:

```php
// Example: .jpg → Image block type
$user->navigation_plus_settings[0]['file_associations'] = [
  'jpg' => 'image',
  'png' => 'image',
  'mp4' => 'video',
];
```

Configurable via the Settings sidebar → Media File Association section.

## Events for Media

| Event | When | Purpose |
|---|---|---|
| `LayoutBuilderNewMedia` | New file dropped on page | Create media entity and block |
| `LayoutBuilderReplaceMedia` | File dropped on existing block | Replace media reference |
| `EditableFieldAttributes` | Change tool on media field | Add replace attributes |

## Common Mistakes

- **Do not** forget the DropzoneJS repository in composer.json — the JS library isn't available via packagist directly.
- **Do not** skip the file association configuration — without it, every drop triggers a modal asking for block type.

## See Also

- [Installation & Setup](installation-setup.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `navigation_plus/src/Controller/MediaUpload.php`
