---
description: Complete YAML structure for icon pack definitions
drupal_version: "11.x"
---

# Icon Pack Definition

## When to Use

> Use when you're creating a new icon pack in a theme or module and need the complete YAML structure with all required and optional properties.

## Decision

| Property | Required | Use when... |
|---|---|---|
| `enabled` | No (defaults true) | Conditionally enabling packs |
| `label` | Yes | Display name in admin UI |
| `description` | No | Explaining pack purpose to site builders |
| `extractor` | Yes | Always - defines how icons are loaded |
| `config` | Yes | Configuring extractor sources |
| `template` | Yes | Always - defines rendered markup |
| `settings` | No | Icons need user customization |
| `library` | No | Pack requires CSS/JS |
| `license` | No | Third-party icon sets with licensing |

## Pattern

Minimal icon pack:

```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json

minimal_pack:
  label: "Minimal Icons"
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg
  template: >-
    <svg aria-hidden="true" focusable="false">{{ content }}</svg>
```

Full-featured pack with settings:

```yaml
full_pack:
  enabled: true
  label: "Full Icon Set"
  description: "Complete icon pack with all options"
  license:
    name: "MIT"
    url: "https://opensource.org/licenses/MIT"
    gpl-compatible: true
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg
      - icons/special/{icon_id}-icon.svg
  settings:
    size:
      title: "Size"
      type: "integer"
      default: 24
      minimum: 8
      maximum: 128
    color:
      title: "Color"
      type: "string"
      format: "color"
      default: "currentColor"
  library: "my_theme/icons"
  template: >-
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         fill="{{ color|default('currentColor') }}"
         class="icon icon-{{ icon_id|clean_class }}"
         aria-hidden="true"
         focusable="false">
      {{ content }}
    </svg>
```

Reference: `/core/assets/schemas/v1/metadata.schema.json` for complete schema.

## Common Mistakes

- **Wrong**: Missing required properties → **Right**: Include `label`, `extractor`, `config`, `template` minimum
- **Wrong**: Invalid YAML syntax → **Right**: Use `$schema` property and YAML linter
- **Wrong**: Template without accessibility → **Right**: Include `aria-hidden="true"` for decorative icons
- **Wrong**: Settings without defaults → **Right**: Always provide sensible default values
- **Wrong**: GPL-incompatible licenses → **Right**: Set `gpl-compatible: false` for non-compatible licenses

## See Also

- [Icon Pack Architecture](icon-pack-architecture.md)
- [Choosing Extractors](choosing-extractors.md)
- Reference: [Icon API YAML reference](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
