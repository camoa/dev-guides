---
description: "Seven field-level formatters for rendering custom field output -- stacked, inline, list, table, flipped table, token template, and SDC. Plugin IDs have no _formatter suffix except custom_formatter."
tldr: "You need to control how the entire custom field (all sub-fields together) is displayed on the view. Plugin IDs are short (custom_inline, not custom_inline_formatter) -- only custom_formatter carries the _formatter suffix."
drupal_version: "11.x"
---

# Field-Level Formatters

## When to Use

You need to control how the entire custom field (all sub-fields together) is displayed on the view.

**Plugin IDs are short** -- `custom_inline`, not `custom_inline_formatter`. Only `custom_formatter` carries the `_formatter` suffix. Copying a `type:` value with the wrong suffix into display config fails on import.

## CustomFormatter

Default stacked formatter -- renders sub-fields vertically with labels.

- **Plugin ID:** `custom_formatter`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| fields | array | [] | Per-sub-field formatter settings, inherited from `BaseFormatter` |

This formatter declares no settings of its own; whether a sub-field's label shows is a per-sub-field setting inside `fields`, not a field-level toggle.

**Template:** `custom-field.html.twig`

```twig
{# custom-field.html.twig #}
<div{{ attributes.addClass('custom-field') }}>
  {% for item in items %}
    <div class="custom-field__item">
      {{ item.content }}
    </div>
  {% endfor %}
</div>
```

**Gotchas:** Each sub-field uses its configured formatter. Nested render arrays.

## CustomInlineFormatter

Renders sub-fields inline with separators.

- **Plugin ID:** `custom_inline`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| show_labels | boolean | FALSE | Show sub-field labels inline |
| label_separator | string | `': '` | Between a label and its value |
| item_separator | string | `', '` | Between sub-fields |

```yaml
type: custom_inline
settings:
  show_labels: true
  label_separator: ': '
  item_separator: ' | '
```

**Gotchas:** No wrapping -- long content can overflow. There is no single `separator` setting; label and item separators are configured independently.

## CustomListFormatter

Renders as HTML list (ul/ol).

- **Plugin ID:** `custom_list`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| list_type | string | ul | ul/ol |

```html
<ul class="custom-field-list">
  <li>Street: 123 Main St</li>
  <li>City: Anytown</li>
  <li>State: CA</li>
</ul>
```

**Gotchas:** Each sub-field is a list item. Semantically inappropriate for non-list data.

## CustomTableFormatter

Renders as HTML table with columns per sub-field.

- **Plugin ID:** `custom_table`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| sort_by | string | `_delta` | Sub-field to sort rows by; `_delta` keeps entry order |
| sort_order | string | `asc` | `asc` / `desc` |
| hide_empty | boolean | -- | Skip empty values |
| hide_header | boolean | -- | Suppress the `<thead>` row |

```html
<table class="custom-field-table">
  <thead>
    <tr><th>Street</th><th>City</th><th>State</th></tr>
  </thead>
  <tbody>
    <tr><td>123 Main St</td><td>Anytown</td><td>CA</td></tr>
  </tbody>
</table>
```

**Gotchas:** Best for multi-value fields. Single-value creates table with one data row.

## FlippedTableFormatter

Renders as HTML table with rows per sub-field (transposed).

- **Plugin ID:** `flipped_table`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| hide_empty | boolean | -- | Skip empty values |

Not the same setting set as CustomTableFormatter -- there is no sorting and no header toggle here, because sub-field names *are* the row headers.

```html
<table>
  <tr><th>Street</th><td>123 Main St</td></tr>
  <tr><th>City</th><td>Anytown</td></tr>
</table>
```

**Gotchas:** Better for single-value fields. Multi-value creates wide tables.

## CustomTemplateFormatter

Token-based custom template.

- **Plugin ID:** `custom_template`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| template | string | '' | Token template string |
| tokens | string | `basic` | `basic` or `advanced`. `advanced` runs the template through the contrib Token module |
| advanced_tokens | array | -- | `recursion_limit` and `global_types`, applied only in `advanced` mode |

```yaml
type: custom_template
settings:
  tokens: basic
  template: '<div class="address">[field:street], [field:city], [field:state] [field:zip]</div>'
```

**Gotchas:** Tokens available: `[field:column_name]` for each sub-field. HTML not sanitized -- XSS risk. `tokens: advanced` requires the Token module and pulls in global token types, so watch `recursion_limit` on nested data.

## SingleDirectoryComponentFormatter

Renders the whole custom field through a Single Directory Component, mapping sub-fields onto component slots and props. Sub-fields of any type can feed a component. Positioned upstream as an alternative to the `sdc_display` contrib module.

- **Plugin ID:** `custom_field_sdc`
- **Class:** `src/Plugin/Field/FieldFormatter/SingleDirectoryComponentFormatter.php` -- **in the main module**, despite the plugin ID. The `custom_field_sdc` sub-module contains no formatter at all.
- **Label in the UI:** "SDC (Single directory component)"
- **Settings:** the component to render, plus a per-prop mapping resolved by the `#[PropWidget]` plugins (see Custom Plugin Development)

**Gotchas:** You do **not** need to enable `custom_field_sdc` to use this formatter -- it ships with the main module and appears in the field display dropdown as soon as `custom_field` is on. The sub-module does something different: it adds whole-**view-mode** component rendering (a "Custom Field - Single directory component options" details element on the entity view display form, plus a `hook_entity_view_alter()` that swaps the entity's build for the component). Enable it only if you want the whole view mode rendered as a component. Prop mapping is only as good as the component's `*.component.yml` schema; a prop with no matching sub-field type has no widget to map it.

## Common Mistakes

- **Copying a plugin ID with a `_formatter` suffix** -- Only `custom_formatter` has one. `custom_inline`, `custom_list`, `custom_table`, `flipped_table`, `custom_template` do not, and display config referencing the suffixed name fails to import
- **Using table formatters for non-tabular data** -- Tables have accessibility implications; use only when data is truly tabular
- **Not sanitizing CustomTemplateFormatter output** -- Template allows raw HTML; sanitize user-entered content
- **Inline formatter with many fields** -- Long inline content breaks mobile layouts
- **Forgetting to configure per-sub-field formatters** -- Field-level formatter wraps sub-field formatters; both must be configured

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/`
- Template: `/modules/contrib/custom_field/templates/custom-field.html.twig`
