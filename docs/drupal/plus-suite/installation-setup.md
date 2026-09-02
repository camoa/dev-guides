---
description: "Install Plus Suite on a new or existing Drupal 11.3+ site — recipe vs manual installation, requirements, and post-install config"
tldr: "Use the DDEV install script for new projects and evaluation. Use manual module installation for existing sites already using Layout Builder."
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> When setting up Plus Suite on a new or existing Drupal 11.3+ site.

## Pattern: Fresh Installation (Recommended)

Use the official DDEV install script:

```bash
curl -sL 'https://git.drupalcode.org/project/plus_suite/-/raw/1.1.x/install.sh' -o install.sh
bash install.sh
```

This script:
1. Creates a DDEV project with Drupal 11.3
2. Installs Drush
3. Adds the DropzoneJS repository for enyo/dropzone JS library
4. Requires `drupal/plus_suite` 1.1.21 (stable) with `--prefer-source`
5. Applies the recipe via `drush recipe ../recipes/plus_suite/`
6. Unpacks recipe dependencies to site's composer.json
7. Clears caches and launches with a one-time login

## Pattern: Existing Site Installation

**Known issue**: The recipe has [compatibility problems on existing sites](https://www.drupal.org/project/plus_suite/issues/3517909) when `field.storage.node.layout_builder__layout` already exists (any content type using Layout Builder).

Manual approach for existing sites:

```bash
# 1. Add DropzoneJS repository
composer config repositories.dropzone '{"type": "package", "package": {"name": "enyo/dropzone", "version": "6.0.0-beta.2", "dist": {"type": "zip", "url": "https://github.com/dropzone/dropzone/releases/download/v6.0.0-beta.2/dist.zip"}, "type": "drupal-library"}}'

# 2. Require the modules individually
composer require drupal/navigation_plus drupal/lb_plus drupal/edit_plus \
  drupal/tempstore_plus drupal/field_sample_value drupal/twig_events \
  drupal/section_library drupal/dropzonejs "enyo/dropzone:6.0.0-beta.2@beta"

# 3. Enable modules in order
drush en field_sample_value tempstore_plus twig_events navigation_plus edit_plus lb_plus \
  dropzonejs section_library lb_plus_section_library

# 4. Enable optional example blocks
drush en edit_plus_header_block edit_plus_cta_block edit_plus_teaser_block edit_plus_non_lb_node
```

## Requirements

| Requirement | Version |
|---|---|
| Drupal core | ^11.3 |
| PHP | 8.3+ |
| Core Navigation module | Enabled (replaces admin toolbar) |
| Layout Builder | Enabled |
| Media Library | Enabled |

## Post-Installation Configuration

After installing the modules, you must configure each content type to use Plus Suite. **The recipe does this automatically for the "Landing Page" type; for other content types, follow these steps:**

#### Step 1: Enable Layout Builder on Content Type

1. Go to **Structure → Content Types → [Your Type] → Manage Display** (`/admin/structure/types/manage/[type]/display`)
2. Check **"Use Layout builder"**
3. Check **"Allow each content item to have its layout customized"** (overrides per node)
4. Click **Save**
5. Click **"Manage layout"** to configure the default layout
6. Add a **One Column** section as default (recommended starting point)
7. Optionally remove all default sections for a blank starting page

#### Step 2: Enable Edit Mode on Content Type

1. Go to **Structure → Content Types → [Your Type] → Edit** (`/admin/structure/types/manage/[type]`)
2. Scroll to **"Navigation+"** section (under Additional Settings)
3. Set **Initial Mode** to "Edit" (activates Edit Mode when user first saves a node)
4. Enable **"Edit"** mode checkbox
5. Set **Default Tool** to "Place Block" (recommended)
6. Click **Save**

#### Step 3: Configure Promoted Blocks

1. Go to **Structure → Content Types → [Your Type] → Manage Display**
2. In the Layout Builder settings area, find **"Promoted Blocks"** configuration
3. Check the blocks you want in the quick-access sidebar (recommended: Basic, Image, Layout Block, and your custom block types)
4. Configure **custom SVG icons** per block for visual identification
5. Click **Save**

#### Step 4: Configure Field Sample Values

For each field on each block content type:
1. Go to **Structure → Block Types → [Block Type] → Manage Fields → [Field] → Edit**
2. Look for **"Set a sample value"** option
3. Select a generator (e.g., `random_text` for body fields, `entity_reference` for media)
4. Configure generator settings (paragraph count, text format, etc.)
5. Click **Save**

#### Step 5: Set Permissions

At `/admin/people/permissions`, grant to content editors:
- **"Use edit mode"** (Navigation+) — required for Edit Mode access
- **"access inline editing"** (Edit+) — required for the Change tool
- Standard Layout Builder permissions
- Standard media library permissions

#### Step 6: Configure UI Colors (Optional)

Navigate to **Manage → Configuration → Content → Plus Suite** (`/admin/config/content/plus-suite`) to set UI accent colors matching your theme.

#### Step 7: Set Up Nested Layouts (Optional)

If you need blocks-within-blocks (layout blocks), you must create the Layout Block type:

1. Go to **Structure → Block Types → Add block type** (`/admin/structure/block-content`)
2. Name it **"Layout Block"**
3. **Remove the body field** from this block type
4. Go to **Manage Display** for this block type
5. Check **"Use Layout builder"**
6. Check **"Allow each content item to have its layout customized"**
7. Click **Save** and configure a **default layout section** (One Column)
8. **Important:** A default layout MUST be configured or you will get "Undefined array key 'layout_plugin'" error
9. Go back to your content type's Manage Display and **promote the Layout Block**

## Decision

| Approach | Use When |
|---|---|
| Recipe (install.sh) | New projects, demos, evaluation |
| Manual module install | Existing sites, partial adoption, custom config |
| Individual modules | Only need some features (e.g., just Edit+ for inline editing) |

## Common Mistakes

- **Do not** try to apply the recipe on an existing site with Layout Builder already configured — it will fail on conflicting field storage config.
- **Do not** skip the DropzoneJS repository configuration — media drag-and-drop requires the enyo/dropzone JS library.
- **Do not** check only "Use Layout builder" without also checking "Allow each content item to have its layout customized" — both are needed for per-node layout customization.
- **Do not** leave the body field on the Layout Block type — it takes up space and serves no purpose inside a nested layout.

## See Also

- [Architecture & Module Map](architecture-module-map.md)
- [Nested Layouts](nested-layouts.md)
- [Common Mistakes & Known Issues](common-mistakes-known-issues.md)
- Reference: [Recipe on existing sites issue #3517909](https://www.drupal.org/project/plus_suite/issues/3517909)
