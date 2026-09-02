---
description: Drupal core ships with 28 recipes as reusable building blocks and pattern examples
tldr: "Browse core recipes when you need reusable building blocks or want to learn recipe patterns from tested examples."
drupal_version: "11.x"
---

# Core Recipes Catalog

## When to Use

> Browse core recipes when you need reusable building blocks or want to learn recipe patterns from tested examples.

Drupal core ships with 28 recipes (as of 11.2). Browse these for patterns and reusable building blocks.

## Items: The 28 Core Recipes

### Site Recipes

**standard**
Comprehensive site setup with content types, roles, and configuration. Composes 15+ recipes. Use as example of complex composition.

### Content Type Recipes

**article_content_type**
Article content type with image field, tags, comments. Demonstrates field creation and display configuration via config actions.

**page_content_type**
Basic page content type. Minimal example showing content type setup.

### Media Type Recipes

**image_media_type**
Image media type with file field. Shows media bundle creation pattern.

**audio_media_type**
Audio media type with file field. Similar pattern to image.

**video_media_type** (local_video_media_type, remote_video_media_type)
Local and remote video media types. Demonstrates oEmbed vs file field patterns.

**document_media_type**
Document media type with file field. PDF/document handling example.

### Role Recipes

**administrator_role**
Administrator role with minimal config. Shows `strict: false` pattern for roles that should exist but exact config doesn't matter.

**content_editor_role**
Content editor role with node permissions. Demonstrates `grantPermissionsForEachNodeType` pattern.

### Text Format Recipes

**basic_html_format_editor**
Basic HTML format with CKEditor 5. Shows text format + editor configuration. Grants `use text format` permission.

**full_html_format_editor**
Full HTML format with CKEditor 5. Similar pattern with wider HTML allowlist.

**restricted_html_format**
Restricted HTML format (no editor). Minimal text format for all users.

### Feature Recipes

**user_picture**
User picture field and configuration. Demonstrates adding field to user entity.

**article_comment**
Commenting on articles. Shows comment type creation and field attachment. Depends on article_content_type.

**article_tags**
Tags taxonomy on articles. Shows vocabulary creation and entity reference field. Depends on tags_taxonomy and article_content_type.

**tags_taxonomy**
Tags vocabulary. Basic taxonomy vocabulary creation pattern.

**basic_shortcuts**
Shortcut menu with common links. Shows menu link creation via config actions.

**basic_block_type**
Basic custom block type. Demonstrates custom block bundle creation.

**content_search**
Search page for content. Configures search_page and related views.

**editorial_workflow**
Content moderation workflow. Shows workflow states and transitions configuration.

**standard_responsive_images**
Responsive image styles. Demonstrates image style and responsive image style creation.

### System Configuration Recipes

**core_recommended_admin_theme**
Sets Claro as admin theme. Simple theme configuration example.

**core_recommended_front_end_theme**
Sets Olivero as default theme. Theme configuration with block placement.

**core_recommended_performance**
Performance settings (CSS/JS aggregation, caching). Shows simpleConfigUpdate for system config.

**core_recommended_maintenance**
Maintenance mode configuration. Error logging and update settings.

### Base Recipes

**comment_base**
Comment module with base configuration. Foundation for article_comment and similar recipes.

**example**
Minimal example recipe for documentation purposes.

## Common Mistakes

- Copying core recipes verbatim → Core recipes are examples; adapt to your needs
- Not understanding recipe dependencies → Many core recipes compose others; check `recipes:` key
- Assuming core recipes are immutable → Core recipes evolve; version-specific differences exist
- Using standard recipe on existing sites → Standard is for clean installs; `strict: true` fails on existing config
- Not reading recipe config actions → Core recipes demonstrate best practices; study their config actions patterns

## See Also

- Previous: ← [Recipe Tooling](recipe-tooling.md)
- Next: [Best Practices & Patterns](best-practices-patterns.md) →
- Reference: `core/recipes/` directory in Drupal core
