---
description: Prefer config-only solutions over custom PHP — when custom code is unavoidable, keep it in theme preprocess hooks, not controllers or services.
drupal_version: "11.x"
tldr: Prefer config-only solutions (fields, view displays, LB Styles, metatag config) over custom PHP. When custom code is unavoidable, keep it in theme preprocess hooks — not controllers or custom services.
---

# Config Over Code

**What:** Prefer config-only solutions (fields, view displays, LB Styles, metatag config) over custom PHP. When custom code is unavoidable, keep it in theme preprocess hooks — not controllers or custom services.

**Rationale:** Config is exportable, deployable through standard `drush config:import`, surfaced in the admin UI for site-builder review, and version-controlled in `config/sync`. Custom modules and services require code review, ongoing maintenance, security patching, and add upgrade risk. Theme preprocess hooks sit at the rendering edge and are the lowest-risk place for behavioral customization.

**When it applies:** Every "we need to customize X" decision. Ask: is there a field, formatter, view, view mode, LB style, or metatag setting that does this? If yes, use it. If no, can a preprocess hook do it? Only if both fail, write a module/service.

**Example:**

```
Need: Hide a field on the card view but show it on full
  Wrong: Custom theme function, hook_node_view_alter, or custom field formatter module
  Right: core.entity_view_display.node.article.card.yml — set field to hidden region

Need: Add a CSS class to specific blocks
  Wrong: Custom block plugin or theme function
  Right: Layout Builder Styles config (LB Styles module)

Need: Modify the title rendered for a specific node bundle
  Wrong: Custom controller or service
  Right: hook_preprocess_node__article in {theme}.theme

Need: Generate a complex computed value not expressible in config
  Acceptable: Custom service, but only after the config-only path is verified impossible
```
