---
description: Six field-level formatters for rendering custom field output -- stacked, inline, list, table, flipped table, and token template.
---

# Field-Level Formatters

## When to Use

You need to control how the entire custom field (all sub-fields together) is displayed on the view.

## CustomFormatter

Default stacked formatter -- renders sub-fields vertically with labels.

- **Plugin ID:** `custom_formatter`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| label_display | boolean | TRUE | Show sub-field labels |
| field_settings | array | [] | Per-sub-field formatter settings |

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

Renders sub-fields inline with separator.

- **Plugin ID:** `custom_inline_formatter`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| separator | string | ', ' | Separator between sub-fields |
| label_display | boolean | FALSE | Show labels inline |

```yaml
type: custom_inline_formatter
settings:
  separator: ' | '
  label_display: FALSE
```

**Gotchas:** No wrapping -- long content can overflow. Labels optional but inline with value.

## CustomListFormatter

Renders as HTML list (ul/ol).

- **Plugin ID:** `custom_list_formatter`

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

- **Plugin ID:** `custom_table_formatter`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| show_labels | boolean | TRUE | Show column headers |

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

- **Plugin ID:** `custom_flipped_table_formatter`
- **Settings:** Same as CustomTableFormatter

```html
<table>
  <tr><th>Street</th><td>123 Main St</td></tr>
  <tr><th>City</th><td>Anytown</td></tr>
</table>
```

**Gotchas:** Better for single-value fields. Multi-value creates wide tables.

## CustomTemplateFormatter

Token-based custom template.

- **Plugin ID:** `custom_template_formatter`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| template | string | '' | Token template string |

```yaml
settings:
  template: '<div class="address">[field:street], [field:city], [field:state] [field:zip]</div>'
```

**Gotchas:** Uses token system. Tokens available: `[field:column_name]` for each sub-field. HTML not sanitized -- XSS risk.

## Common Mistakes

- **Using table formatters for non-tabular data** -- Tables have accessibility implications; use only when data is truly tabular
- **Not sanitizing CustomTemplateFormatter output** -- Template allows raw HTML; sanitize user-entered content
- **Inline formatter with many fields** -- Long inline content breaks mobile layouts
- **Forgetting to configure per-sub-field formatters** -- Field-level formatter wraps sub-field formatters; both must be configured

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/Field/FieldFormatter/`
- Template: `/modules/contrib/custom_field/templates/custom-field.html.twig`
