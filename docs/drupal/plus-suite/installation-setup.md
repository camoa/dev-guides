---
description: Install Plus Suite on a new or existing Drupal 11.3+ site — recipe vs manual installation, requirements, and post-install config
tldr: "Use the DDEV install script for new projects and evaluation. Use manual module installation for existing sites already using Layout Builder."
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> Use the DDEV install script for new projects and evaluation. Use manual module installation for existing sites already using Layout Builder.

## Decision

| Approach | Use When |
|----------|----------|
| Recipe (`install.sh`) | New projects, demos, evaluation |
| Manual module install | Existing sites, partial adoption, custom config |
| Individual modules | Only need some features (e.g., just Edit+ for inline editing) |

## Pattern

**Fresh installation (recommended):**

```bash
curl -sL 'https://git.drupalcode.org/project/plus_suite/-/raw/1.1.x/install.sh' -o install.sh
bash install.sh
```

The script: creates a DDEV project with Drupal 11.3, installs Drush, adds the DropzoneJS repository, requires `drupal/plus_suite` 1.1.21 (stable) with `--prefer-source`, applies the recipe, unpacks dependencies, clears caches, and launches with a one-time login.

**Existing site installation:**

```bash
# 1. Add DropzoneJS repository
composer config repositories.dropzone '{"type": "package", "package": {"name": "enyo/dropzone", "version": "6.0.0-beta.2", "dist": {"type": "zip", "url": "https://github.com/dropzone/dropzone/releases/download/v6.0.0-beta.2/dist.zip"}, "type": "drupal-library"}}'

# 2. Require modules
composer require drupal/navigation_plus drupal/lb_plus drupal/edit_plus \
  drupal/tempstore_plus drupal/field_sample_value drupal/twig_events \
  drupal/section_library drupal/dropzonejs "enyo/dropzone:6.0.0-beta.2@beta"

# 3. Enable in order
drush en field_sample_value tempstore_plus twig_events navigation_plus edit_plus lb_plus \
  dropzonejs section_library lb_plus_section_library

# 4. Optional example blocks
drush en edit_plus_header_block edit_plus_cta_block edit_plus_teaser_block edit_plus_non_lb_node
```

**Requirements:**

| Requirement | Version |
|-------------|---------|
| Drupal core | ^11.3 |
| PHP | 8.3+ |
| Core Navigation module | Enabled (replaces admin toolbar) |
| Layout Builder | Enabled |
| Media Library | Enabled |

**Post-installation — configure each content type:**

#### Step 1: Enable Layout Builder on Content Type

1. Go to **Structure → Content Types → [Your Type] → Manage Display**
2. Check **"Use Layout builder"**
3. Check **"Allow each content item to have its layout customized"**
4. Click **Save**
5. Click **"Manage layout"** and add a **One Column** section as default

#### Step 2: Enable Edit Mode on Content Type

1. Go to **Structure → Content Types → [Your Type] → Edit**
2. Scroll to **"Navigation+"** section (under Additional Settings)
3. Set **Initial Mode** to "Edit"
4. Enable **"Edit"** mode checkbox
5. Set **Default Tool** to "Place Block"
6. Click **Save**

#### Step 3: Configure Promoted Blocks

1. Go to **Structure → Content Types → [Your Type] → Manage Display**
2. In Layout Builder settings, find **"Promoted Blocks"**
3. Check desired blocks (recommended: Basic, Image, Layout Block, custom types)
4. Configure **custom SVG icons** per block

#### Step 4: Configure Field Sample Values

For each field on each block content type:
1. Go to **Structure → Block Types → [Block Type] → Manage Fields → [Field] → Edit**
2. Find **"Set a sample value"** — select a generator (`random_text`, `entity_reference`, etc.)

#### Step 5: Set Permissions

At `/admin/people/permissions`, grant to content editors:
- **"Use edit mode"** (Navigation+)
- **"access inline editing"** (Edit+)
- Standard Layout Builder and media library permissions

#### Step 6: Configure UI Colors (Optional)

Navigate to **Manage → Configuration → Content → Plus Suite** (`/admin/config/content/plus-suite`) to set accent colors.

#### Step 7: Set Up Nested Layouts (Optional)

If you need layout blocks (blocks-within-blocks):

1. Go to **Structure → Block Types → Add block type**
2. Name it **"Layout Block"**, machine name: `layout_block`
3. **Remove the body field**
4. Go to the block type's **Manage Display**
5. Check **"Use Layout builder"** and **"Allow each content item to have its layout customized"**
6. Click **Save** and configure a **default One Column layout**
7. **Critical**: A default layout MUST be configured or you will get "Undefined array key 'layout_plugin'" error
8. Go to your content type's Manage Display and **promote the Layout Block** in LB+ promoted blocks

## Common Mistakes

- **Wrong**: Apply the recipe on an existing site with Layout Builder configured → **Right**: Install modules manually; recipe fails on conflicting `field.storage.node.layout_builder__layout`
- **Wrong**: Skip the DropzoneJS repository configuration → **Right**: Add the repository before requiring plus_suite; media drag-and-drop requires `enyo/dropzone`
- **Wrong**: Check only "Use Layout builder" without "Allow each content item..." → **Right**: Check BOTH options for per-node layout customization
- **Wrong**: Leave body field on Layout Block type → **Right**: Remove it; body field serves no purpose inside nested layouts

## See Also

- [Architecture & Module Map](architecture-module-map.md)
- [Nested Layouts](nested-layouts.md)
- [Common Mistakes & Known Issues](common-mistakes-known-issues.md)
- Reference: [Recipe on existing sites issue #3517909](https://www.drupal.org/project/plus_suite/issues/3517909)
