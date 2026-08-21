---
description: "Browse every registered icon pack in the admin Icon Library at /admin/appearance/ui/icons."
tldr: "Enable ui_icons_library and visit /admin/appearance/ui/icons to browse packs and preview icons with a fuzzy search bar. Requires access ui icons library; clear cache after adding icons since YamlDiscovery caches pack contents."
drupal_version: "11.x"
---

# Icon Library Admin UI

## When to Use

> Browsing every available icon during theme development, debugging discovery, or showing a stakeholder which packs the site has.

## Pattern

Enable `ui_icons_library`. Visit **`/admin/appearance/ui/icons`**; a single pack is at `/admin/appearance/ui/icons/{pack_id}`. Both need the `access ui icons library` permission.

The page lists every registered pack (label, version, license, source links), and per pack shows a grid of all icons with live previews. Click any icon for detail: full ID, available settings, the rendered template output.

A search bar fuzzy-matches icon IDs across all packs.

## Common Mistakes

- **Wrong**: expecting icon counts to update without clearing cache → **Right**: run `drush cr` after adding icons; YamlDiscovery caches the pack contents

## See Also

- [Icon Pack Format](pack-format.md)
- [Authoring & Distribution](authoring.md)
- Reference: `modules/ui_icons_library/src/Controller/LibraryIndex.php`
