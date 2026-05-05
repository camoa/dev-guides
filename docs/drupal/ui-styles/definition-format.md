---
description: Author *.ui_styles.yml plugin files in a theme or module — schema, category grouping, icons, and short vs long option form.
tldr: Place {name}.ui_styles.yml at the theme/module root; prefix plugin IDs with the theme/module name to avoid collisions. Each style declares options as class => label (short) or class => {label, icon, description} (long). Use category to group related styles.
drupal_version: "11.x"
---

# Style Definition Format

## When to Use

> Use this guide when authoring `*.ui_styles.yml` in a theme or module to declare reusable style options.

## Decision: Short Form vs Long Form for Options

| Option needs... | Use |
|---|---|
| Label only | Short form — `class-name: "Label"` |
| Description, icon, or per-option preview helpers | Long form — `class-name: { label: ..., icon: ... }` |

## Pattern

**File location**: `{module|theme}/{name}.ui_styles.yml`

```yaml
plugin_id:                          # machine name, unique across all active modules+themes
  enabled: true                     # optional, default true
  label: "Human-readable label"     # required
  description: "Helper text"        # optional
  category: "Typography"            # optional grouping; default "Other"
  icon: "mdi-format-color-text"     # optional — forces toolbar widget when all options have icons
  weight: -80                       # optional sort within category; default 0
  empty_option: "- None -"          # optional label for select widget empty state

  options:
    text-primary: "Primary"         # short form: class => label
    text-secondary:                 # long form: class => option object
      label: "Secondary"
      description: "Used for supporting copy"
      icon: "mdi-format-color-text"
      previewed_with:               # extra classes used only in the library preview
        - p-2
        - bg-neutral

  previewed_with:                   # style-level preview helpers; merged with option-level
    - border
    - p-2
  previewed_as: "inside"            # inside | aside | hidden — library preview layout

  links:
    - "https://example.com/docs/text-utilities"
```

### Category Grouping

Styles with the same `category` render under one fieldset in form widgets and one section in the Library page. Common categories: `"Typography"`, `"Colors"`, `"Spacing"`, `"Borders"`, `"Effects"`, `"Layout"`.

## Common Mistakes

- **Declaring two non-orthogonal options in the same style** (e.g. `border-top` and `border-bottom`) → They become mutually exclusive in the UI. Use separate styles or a "border position" composite style
- **Using a generic plugin ID** like `border` → Will collide with other modules. Prefix with theme/module name (e.g. `mytheme_border`)
- **Skipping `previewed_with`** for utility classes that need structural siblings (e.g. a text color shown on white) → Library preview looks broken

## See Also

- [Source Plugins (Form Widgets)](source-plugins.md)
- [Theme Authoring](theme-authoring.md)
- [Overriding & Disabling](overriding.md)
