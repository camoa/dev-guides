---
description: Install Plus Suite on a new or existing Drupal 11.3+ site — recipe vs manual installation, requirements, and post-install config
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
```

**Requirements:**

| Requirement | Version |
|-------------|---------|
| Drupal core | ^11.3 |
| PHP | 8.3+ |
| Core Navigation module | Enabled |
| Layout Builder | Enabled |
| Media Library | Enabled |

**Post-installation:**
1. Enable Layout Builder on your content type (Structure → Content Types → Manage Display)
2. Enable Edit Mode (Structure → Content Types → Edit → Navigation+ section)
3. Configure Promoted Blocks (Manage Display → LB+ settings)
4. Configure Field Sample Values (Manage Fields → per-field settings)

## Common Mistakes

- **Wrong**: Apply the recipe on an existing site with Layout Builder configured → **Right**: Install modules manually; recipe fails on conflicting `field.storage.node.layout_builder__layout`
- **Wrong**: Skip the DropzoneJS repository configuration → **Right**: Add the repository before requiring plus_suite; media drag-and-drop requires `enyo/dropzone`

## See Also

- [Architecture & Module Map](architecture-module-map.md)
- [Common Mistakes & Known Issues](common-mistakes-known-issues.md)
- Reference: [Recipe on existing sites issue #3517909](https://www.drupal.org/project/plus_suite/issues/3517909)
