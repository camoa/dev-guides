---
description: "Complete *.icons.yml schema — which keys are required, which are form-only, and why settings default: never reaches the template"
tldr: "You're creating a new icon pack and need the full YAML structure; only extractor and template are schema-required, and settings: default: values never reach the Twig template — repeat them with |default()."
drupal_version: "11.x"
---

# Icon Pack Definition

## When to Use

You're creating a new icon pack in a theme or module and need the complete YAML structure with all required and optional properties.

## Decision

| Property | Required | Use when... |
|---|---|---|
| `enabled` | No (defaults true) | Conditionally enabling packs |
| `label` | Recommended, not enforced | Display name in admin UI; falls back to the pack ID |
| `description` | No | Explaining pack purpose to site builders |
| `extractor` | Yes (schema) | Always - defines how icons are loaded |
| `config` | Yes (enforced by the extractor) | `config: sources` for `path`, `svg`, `svg_sprite`, `font` |
| `template` | Yes (schema) | Always - defines rendered markup |
| `settings` | No | Building an admin settings form for the pack |
| `library` | No | Pack requires CSS/JS |
| `license` | No | Third-party icon sets with licensing |
| `version`, `links`, `preview` | No | Metadata and admin previews |

`icon_pack.schema.json` lists only `extractor` and `template` under `required`. `label` is documented as "Recommended" in the `IconPackManager` docblock and `listIconPackOptions()` falls back to the pack ID. `config: sources` is not in the schema's `required` list at all — the extractors enforce it themselves and throw `IconPackConfigErrorException` from `checkRequiredConfigSources()` when it is missing.

## Pattern

Minimal icon pack. Note: **no `$schema:` key** — plugin YAML discovery makes every top-level key an icon-pack plugin ID, so a `$schema` entry breaks discovery for the whole site:

```yaml
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

Note that in the example above, `size: default: 24` and `color: default: "currentColor"` are **form** defaults only. Core never merges them into the template context — that is why the template repeats them with `|default(24)` and `|default('currentColor')`. Core states this explicitly: "`default:` (mixed) Form default value, will not be used as default value in the template, template must use `|default()` twig filter" (`IconPackManager.php:103-104`). Keep the two in sync by hand.

Reference: `/core/assets/schemas/v1/icon_pack.schema.json` for the complete schema (`metadata.schema.json` beside it is the SDC component schema — a different thing).

## Common Mistakes

- **Wrong**: Adding `$schema:` to `*.icons.yml` → **Right**: Fatal at discovery, and the URL usually cited points at the SDC schema anyway
- **Wrong**: Missing `extractor` or `template` → **Right**: `IconPackConfigErrorException` when json-schema validation is available; without it, `IconExtractorBase::createIcon()` throws "Missing `template` in your definition" at render time instead
- **Wrong**: Expecting `settings: default:` to reach the template → **Right**: It never does; always mirror it with `|default()` in the template
- **Wrong**: Template without accessibility → **Right**: Include `aria-hidden="true"` for decorative icons
- **Wrong**: GPL-incompatible licenses → **Right**: Set `gpl-compatible: false` for non-compatible licenses

## See Also

- [Icon Pack Architecture](icon-pack-architecture.md)
- [Choosing Extractors](choosing-extractors.md)
- Reference: [Icon API YAML reference](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
