---
description: Add help text to base fields using core.base_field_override config — not hook_form_alter().
drupal_version: "11.x"
tldr: To add help text or descriptions to base fields (e.g., node title), use `core.base_field_override.node.{bundle}.{field}.yml` config — not `hook_form_alter()`.
---

# Field Descriptions via Base Field Overrides

**What:** To add help text or descriptions to base fields (e.g., node title), use `core.base_field_override.node.{bundle}.{field}.yml` config — not `hook_form_alter()`.

**Rationale:** Config is exportable, doesn't require custom module code, and survives module changes. `hook_form_alter()` requires a custom module, runs on every form build (a small but real cost), needs careful conditional checks to avoid affecting other forms, and adds a maintenance surface. Base field overrides are core's built-in mechanism for exactly this use case.

**When it applies:** Adding help text, default values, label changes, or required-flag changes to base fields (title, status, promoted, etc.) on a per-bundle basis.

**Example:**

```yaml
# Right — config-only override
# config/sync/core.base_field_override.node.article.title.yml
langcode: en
status: true
field_name: title
entity_type: node
bundle: article
label: Headline
description: 'The article headline as it appears in listings and at the top of the article page.'
required: true
default_value: []
default_value_callback: ''
settings: {  }
```

```php
// Wrong — custom module + form_alter
function mymodule_form_node_article_form_alter(&$form, FormStateInterface $form_state) {
  $form['title']['widget'][0]['value']['#description'] =
    t('The article headline as it appears in listings and at the top of the article page.');
}
```
