---
description: Authoring *.ui_skins.css_variables.yml to expose CSS custom properties as theme-settings form fields.
tldr: Declare CSS variable plugins in `{theme}.ui_skins.css_variables.yml` at the theme root. Each plugin maps a machine name to a CSS variable, a form widget type, a label, and a map of CSS scope → default value. Plugin ID becomes the CSS variable name with `--` prefix.
drupal_version: "11.x"
---

# CSS Variable Definition

## When to Use

> Use this when authoring `*.ui_skins.css_variables.yml` to expose CSS custom properties as theme-settings form fields that site builders can edit.

## Decision

| Need | Approach |
|---|---|
| One global default | Single `:root` entry in `default_values` |
| Different default inside a theme variant | Add a scope keyed on the variant's class (e.g. `.theme-dark`) |
| Per-component variable | Scope to the component's class (e.g. `.card`) |

## Pattern

**File location**: `{module|theme}/{module|theme_name}.ui_skins.css_variables.yml`

```yaml
plugin_id:                          # machine name; becomes the CSS variable name (with -- prefix)
  enabled: true                     # optional, default true
  type: ui_skins_alpha_color        # optional widget type; default "textfield"
  label: "Brand primary"            # required, translatable
  description: "Primary brand color used for CTAs and links"  # optional, translatable
  label_context: "ui_skins"         # optional translation context
  description_context: "ui_skins"   # optional
  category: "Colors"                # optional grouping; default "Other"
  category_context: "ui_skins"      # optional
  weight: -50                       # optional sort within category; default 0

  default_values:                   # required; map of CSS scope => value
    ":root": "#0066ccff"
    ".theme-dark": "#3399ffff"
```

**CSS variable naming**: the plugin ID maps to the CSS variable name. `brand_primary` becomes `--brand-primary`.

## Common Mistakes

- **Using a label without `category`** → Falls into "Other" — fine for one or two variables, painful with twenty
- **Setting a hex value without alpha when using `ui_skins_alpha_color`** → Widget expects an 8-character hex (`RRGGBBAA`). Provide alpha or use `textfield` type
- **Confusing variable scope with theme dependencies** → Scope is a CSS selector for the *value*; theme dependencies activate other themes

## See Also

- [Variable Types & Widgets](ui-skins-variable-types.md)
- [Variable Scopes](ui-skins-variable-scopes.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- Reference: `src/CssVariable/CssVariablePluginManager.php`, `src/Definition/CssVariableDefinition.php`
