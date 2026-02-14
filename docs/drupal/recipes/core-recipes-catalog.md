---
description: Drupal core ships with 28 recipes as reusable building blocks and pattern examples
drupal_version: "11.x"
---

# Core Recipes Catalog

## When to Use

> Browse core recipes when you need reusable building blocks or want to learn recipe patterns from tested examples.

## Decision

| Recipe Type | Examples | Use For |
|-------------|----------|---------|
| Site Recipes | standard | Comprehensive site setup, composition examples |
| Content Type Recipes | article_content_type, page_content_type | Field creation, display configuration patterns |
| Media Type Recipes | image_media_type, video_media_type | Media bundle creation patterns |
| Role Recipes | administrator_role, content_editor_role | Permission grant patterns |
| Text Format Recipes | basic_html_format_editor, full_html_format | Text format + editor configuration |
| Feature Recipes | user_picture, article_comment, editorial_workflow | Entity field attachment, workflow patterns |
| System Config Recipes | core_recommended_performance, core_recommended_admin_theme | Simple config update patterns |

## Pattern

Site Recipes:

**standard** - Comprehensive site setup with content types, roles, and configuration. Composes 15+ recipes. Use as example of complex composition.

Content Type Recipes:

**article_content_type** - Article content type with image field, tags, comments. Demonstrates field creation and display configuration via config actions.

**page_content_type** - Basic page content type. Minimal example showing content type setup.

Media Type Recipes:

**image_media_type** - Image media type with file field. Shows media bundle creation pattern.

**video_media_type** (local_video_media_type, remote_video_media_type) - Local and remote video media types. Demonstrates oEmbed vs file field patterns.

Role Recipes:

**administrator_role** - Administrator role with minimal config. Shows `strict: false` pattern for roles that should exist but exact config doesn't matter.

**content_editor_role** - Content editor role with node permissions. Demonstrates `grantPermissionsForEachNodeType` pattern.

Text Format Recipes:

**basic_html_format_editor** - Basic HTML format with CKEditor 5. Shows text format + editor configuration. Grants `use text format` permission.

Feature Recipes:

**editorial_workflow** - Content moderation workflow. Shows workflow states and transitions configuration.

**article_tags** - Tags taxonomy on articles. Shows vocabulary creation and entity reference field. Depends on tags_taxonomy and article_content_type.

System Configuration Recipes:

**core_recommended_performance** - Performance settings (CSS/JS aggregation, caching). Shows simpleConfigUpdate for system config.

**core_recommended_front_end_theme** - Sets Olivero as default theme. Theme configuration with block placement.

## Common Mistakes

- **Wrong**: Copying core recipes verbatim → **Right**: Core recipes are examples; adapt to your needs
- **Wrong**: Not understanding recipe dependencies → **Right**: Many core recipes compose others; check `recipes:` key
- **Wrong**: Assuming core recipes are immutable → **Right**: Core recipes evolve; version-specific differences exist
- **Wrong**: Using standard recipe on existing sites → **Right**: Standard is for clean installs; `strict: true` fails on existing config
- **Wrong**: Not reading recipe config actions → **Right**: Core recipes demonstrate best practices; study their config actions patterns

## See Also

- [Recipe Tooling](recipe-tooling.md)
- [Best Practices & Patterns](best-practices-patterns.md)
- Reference: `core/recipes/` directory in Drupal core
