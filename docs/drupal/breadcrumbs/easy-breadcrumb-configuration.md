---
description: Complete reference for all Easy Breadcrumb configuration settings — title resolution, home segment, capitalization, custom paths, and SEO
tldr: "After installing Easy Breadcrumb, configure at `admin/config/user-interface/easy-breadcrumb`. All settings map to `easy_breadcrumb.settings.yml` which can be exported and version-controlled."
drupal_version: "11.x"
---

# Easy Breadcrumb Configuration

## When to Use

> After installing Easy Breadcrumb, configure at `admin/config/user-interface/easy-breadcrumb`. All settings map to `easy_breadcrumb.settings.yml` which can be exported and version-controlled.

## Decision

| Config key | Type | Purpose |
|---|---|---|
| `title_from_page_when_available` | bool | Use real page title via `TitleResolver` instead of URL slug — **enable this** |
| `include_title_segment` | bool | Add current page title as the final breadcrumb segment |
| `title_segment_as_link` | bool | Make the current page segment a link (requires `include_title_segment`) |
| `applies_admin_routes` | bool | Include admin routes in Easy Breadcrumb (default: `TRUE`) |
| `include_invalid_paths` | bool | Show non-routed path segments as plain text instead of dropping them |
| `remove_repeated_segments` | bool | Remove consecutive duplicate segments |
| `follow_redirects` | bool | Resolve redirect module redirects to their source paths |
| `include_home_segment` | bool | Add a "Home" link as the first segment |
| `home_segment_title` | string | Label for the home segment (e.g., `"Home"`) |
| `use_site_title` | bool | Use the site name from `system.site:name` as home segment title |
| `hide_single_home_item` | bool | Hide the breadcrumb entirely if it only contains the home segment |
| `use_menu_title_as_fallback` | bool | Use the menu link title when no `_title` exists on the route |
| `alternative_title_field` | string | Field machine name on entities (e.g., `field_breadcrumb_title`) for per-entity title override |
| `capitalizator_mode` | string | `none`, `ucwords` (Title Case), `ucfirst` (Sentence case), `ucall` (ALL CAPS), `ucforce` |
| `term_hierarchy` | bool | Add all taxonomy term parents in the breadcrumb for the current term |
| `language_path_prefix_as_segment` | bool | On multilingual sites, show the language prefix (`/en`) as a breadcrumb segment |
| `absolute_paths` | bool | Generate absolute URLs for all breadcrumb links |
| `add_structured_data_json_ld` | bool | Output `BreadcrumbList` JSON-LD in the `<head>` |
| `limit_segment_display` | bool | Enable segment count limiting |
| `segment_display_limit` | int | Maximum number of segments to show |
| `segment_display_minimum` | int | Minimum segments required before showing breadcrumb at all |
| `truncator_mode` | bool | Enable title truncation |
| `truncator_length` | int | Maximum character length per title |

## Pattern

**Custom paths format** (`custom_paths` textarea):
```
/news/archive :: News | /news :: Archive | /news/archive
regex!/products/(\w+)/(\d+) :: Products | /products :: $1 | /products/$1 :: Item $2
```

**Excluded paths** (`excluded_paths` textarea) — escape `/` as `\/`:
```
search
admin\/content
user\/login
```

**Replaced titles** (`replaced_titles` textarea):
```
ORIGINAL_TITLE::REPLACEMENT
```

## Common Mistakes

- **Wrong**: Configuring `replaced_titles` without enabling `title_from_page_when_available` → **Right**: Replacements only match resolved titles, not URL slugs
- **Wrong**: Setting `segment_display_minimum` to 2 and wondering why the Home-only breadcrumb disappears → **Right**: It is working as configured; adjust the minimum
- **Wrong**: Writing `admin/content` in `excluded_paths` without escaping the slash → **Right**: Use `admin\/content`

## See Also

- [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- [Structured Data (SEO)](structured-data-seo.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbConstants.php`
- Reference: `modules/contrib/easy_breadcrumb/src/Form/EasyBreadcrumbGeneralSettingsForm.php`
