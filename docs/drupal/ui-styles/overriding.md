---
description: "Override, disable, or extend UI Styles definitions declared by upstream modules or themes."
tldr: "Disable an upstream style by re-declaring its plugin ID with enabled: false in your theme's YAML. Add options by re-declaring with only the new options (arrays merge). For conditional/runtime overrides, implement hook_ui_styles_styles_alter(). Never edit upstream YAML directly."
drupal_version: "11.x"
---

# Overriding & Disabling

## When to Use

> Use this guide when adjusting a style declared by another module or theme — adding options, hiding it, or replacing it.

## Decision

| Goal | Approach |
|---|---|
| Hide a style entirely | `enabled: false` in your theme's YAML |
| Add a few options | Re-declare with just the new options (arrays merge) |
| Wholesale replacement | Disable + new plugin ID |
| Conditional adjustment (per-environment, per-role) | `hook_ui_styles_styles_alter()` |

## Pattern

**Disable** an upstream style:

```yaml
# mytheme.ui_styles.yml
upstream_module_text_color:
  enabled: false
```

**Add options** to an upstream style:

```yaml
upstream_module_text_color:
  options:
    text-brand: "Brand"      # added on top of upstream's options
```

**Programmatic alteration**:

```php
function mymodule_ui_styles_styles_alter(array &$definitions): void {
  if (isset($definitions['some_style'])) {
    unset($definitions['some_style']->getOptions()['banned-class']);
  }
}
```

## Common Mistakes

- **Forgetting weight matters when overriding** → If multiple sources define the same plugin ID, higher `weight` wins. Set explicit weights in conflict scenarios
- **Modifying upstream definitions in place** → Never edit the upstream module's YAML. Override from your theme or custom module

## See Also

- [Style Definition Format](definition-format.md)
- [Theme Authoring](theme-authoring.md)
- Reference: `hook_ui_styles_styles_alter` in `ui_styles.api.php`
