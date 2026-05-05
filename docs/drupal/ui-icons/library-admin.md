---
description: Browse all registered icon packs in Drupal's admin Icon Library UI.
tldr: Enable ui_icons_library and visit /admin/appearance/ui-libraries/icons to see every registered pack with live icon previews, full IDs, settings, and a fuzzy search across all packs. Icon counts do not update until cache is cleared after adding icons.
drupal_version: "11.x"
---

# Icon Library Admin UI

## When to Use

> Browsing every available icon during theme development, debugging discovery, or showing a stakeholder which packs the site has.

## Pattern

Enable `ui_icons_library`. Visit `/admin/appearance/ui-libraries/icons`.

The page provides:
- List of every registered pack (label, version, license, source links)
- Per pack: grid of all icons with live previews
- Click any icon for detail: full ID (`pack_id:icon_id`), available settings, rendered template output
- Fuzzy search bar matching icon IDs across all packs

## Common Mistakes

- **Wrong**: expecting icon counts to update after adding icons without clearing cache → **Right**: run `drush cr`; YamlDiscovery caches the pack contents

## See Also

- [Pack Format](pack-format.md)
- [Authoring & Distribution](authoring.md)
- Reference: `modules/ui_icons_library/src/Controller/LibraryIndex.php`
