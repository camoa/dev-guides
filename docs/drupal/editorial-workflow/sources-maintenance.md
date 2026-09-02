---
description: "Source references and maintenance manifest for the editorial workflow guides — web sources, code sources, and version history"
---

# Sources & Maintenance
## Sources & Maintenance Manifest

### Research Install
Path: contrib/web

### Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| User roles and permissions | https://www.drupal.org/docs/user_guide/en/user-roles.html | editorial-role-permission-model.md | 2026-07-03 |
| Content Moderation | https://www.drupal.org/docs/administering-a-drupal-site/managing-content/content-moderation | content-moderation-state-machine.md, content-moderation-existing-content-migration.md | 2026-07-03 |

### Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| Content Moderation | core/modules/content_moderation/ | content-moderation-state-machine.md, content-moderation-existing-content-migration.md | 11.4.5 |
| Workflows | core/modules/workflows/ | content-moderation-state-machine.md | 11.4.5 |
| Editorial Workflow (core recipe) | core/recipes/editorial_workflow/config/workflows.workflow.editorial.yml | content-moderation-state-machine.md | 11.4.5 |
| Demo: Umami (author/editor roles) | core/profiles/demo_umami/config/install/user.role.author.yml, user.role.editor.yml | editorial-role-permission-model.md | 11.4.5 |
| Config Action: per-bundle permissions | core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/PermissionsPerBundle.php | editorial-role-permission-model.md | 11.4.5 |
| Config Action: add moderation | core/modules/content_moderation/src/Plugin/ConfigAction/AddModeration.php | content-moderation-state-machine.md | 11.4.5 |
| Content Editor Role (core recipe, shipped by Drupal CMS) | drupal-cms/web/core/recipes/content_editor_role/config/user.role.content_editor.yml | editorial-role-permission-model.md | Drupal CMS 2.0.0 / core 11.3.2 |
| Content Basics (basic_editorial workflow) | drupal-cms/recipes/drupal_cms_content_type_base/config/workflows.workflow.basic_editorial.yml | content-moderation-state-machine.md | Drupal CMS 2.0.0 / core 11.3.2 |

The last two rows come from a second install outside the primary Research Install path, kept as full paths because they are not under it.

### Version History
| Date | Change |
|------|--------|
| 2026-07-03 | Manifest reconstructed from the guide's own citations and the installed source. |
