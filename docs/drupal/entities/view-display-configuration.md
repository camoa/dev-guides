---
description: View display — formatter selection and field visibility in view modes
drupal_version: "11.x"
---

# View Display Configuration

## When to Use

When controlling how fields appear in entity view modes (full, teaser, RSS, etc.), including formatter selection, label display, and field visibility.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Full page view | 'default' mode | Complete entity display |
| List/preview | 'teaser' mode | Abbreviated display for listings |
| RSS/API | Custom view mode | Specialized output format |
| Different formatters | Formatter type per mode | Different rendering for different contexts |
| Hide fields | hidden key | Exclude from view mode without deleting field |

## Pattern

View display in `config/install/core.entity_view_display.node.article.default.yml`:

```yaml
langcode: en
status: true
dependencies:
  config:
    - field.field.node.article.body
    - field.field.node.article.field_image
    - field.field.node.article.field_tags
    - image.style.large
    - node.type.article
  module:
    - image
    - taxonomy
    - text
    - user
id: node.article.default
targetEntityType: node
bundle: article
mode: default
content:
  field_image:
    type: image
    label: hidden
    settings:
      image_link: ''
      image_style: large
      image_loading:
        attribute: lazy
    weight: -1
  body:
    type: text_default
    label: hidden
    settings: {}
    weight: 0
  field_tags:
    type: entity_reference_label
    label: above
    settings:
      link: true
    weight: 10
  links:
    weight: 100
    region: content
hidden:
  langcode: true
  search_api_excerpt: true
```

**Label display options**:
- `hidden`: No label displayed
- `above`: Label above field value
- `inline`: Label and value on same line
- `visually_hidden`: Hidden from screen but accessible

Reference: `/core/lib/Drupal/Core/Entity/EntityViewBuilder.php`

## Common Mistakes

- **Wrong**: Not setting image_loading attribute → **Right**: No lazy loading; poor LCP performance
- **Wrong**: Missing image_style on image fields → **Right**: Full-size images; slow page loads
- **Wrong**: Using 'above' labels on every field → **Right**: Visual clutter; hide labels when obvious from context
- **Wrong**: Not configuring link: true for entity references → **Right**: Missed internal linking opportunities
- **Wrong**: Forgetting module dependencies → **Right**: Formatters won't work; blank output

**Performance**:
- ALWAYS use image_style on image fields. Never display original images.
- Set image_loading: lazy on below-fold images for better LCP/FCP.
- Hide unused fields rather than formatting empty ones (empty formatters still process).

**Security**:
- Entity reference formatters with link: true check entity access automatically.
- Text formatters run through text format filters; never bypass format system.

**Development Standards**:
- Use semantic label display (hidden when redundant, above when needed for clarity)
- Consistent weight gaps (0, 10, 20) allow insertion without renumbering
- Always set region: content explicitly

## See Also

- [Form Display Configuration](form-display-configuration.md)
- [View Mode Development](view-mode-development.md)
- Reference: [Entity display modes](https://www.drupal.org/docs/drupal-apis/entity-api/display-modes-view-modes-and-form-modes)
