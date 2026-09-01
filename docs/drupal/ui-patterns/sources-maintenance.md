---
description: UI Patterns 2.x — source references, versions, and maintenance notes
---

# Sources & Maintenance

## Module Info

- **Module:** `ui_patterns` 2.0.20
- **Drupal:** 11.4
- **Last Updated:** 2026-08-18

## Drupal Research Install

Path: `~/workspace/contrib/web/` (ui_patterns **2.0.15** installed there)

## Verification Note (2026-08-18)

Every plugin ID, `#[Source]` attribute, deriver ID shape, config-schema key and prop-type `convert_from` in this guide was re-derived from source at **2.0.19** (fetched from `git.drupalcode.org`), not from the 2.0.15 checkout in the research install. Where the two differ, this guide follows 2.0.19. Re-checked against **2.0.20** (2026-08-28) on 2026-09-01: its 19 issues rename no plugin ID, `#[Source]` attribute, prop type or `.component.yml` schema key, so every identifier below still holds. The one behavioural fix worth knowing is #3612960 — a prop legitimately named `id` no longer collides with the schema resolver's own `id` key. The differences that matter:

| Change | Landed in | Effect on this guide |
|---|---|---|
| `StringPropType::preprocess()` removed; escaping decided by value type in `normalize()` | 2.0.16–2.0.19 (issue #3611167) | Props System and Security sections rewritten — a plain string prop is now autoescaped by Twig, not marked safe |
| Attribute values escaped with `Html::escape()` instead of `strip_tags()` | 2.0.16–2.0.19 (issue #3558573) | Security section |
| `SourceTags` enum replaces bare tag strings | 2.0.16–2.0.19 (issue #3590492) | Source Plugins, Creating Custom Source Plugins |
| `no_ui` added to `#[Source]` (fourth positional parameter) | 2.0.16–2.0.19 (issue #3593760) | Source attribute properties table |
| `field_formatter` source schema moved from `ui_patterns_field_formatters` into the main module's `ui_patterns.sources.schema.yml` | 2.0.16–2.0.19 | Config Export Reference — key string is unchanged |
| `third_party_settings` added to `ui_patterns_slot_source` schema | 2.0.16–2.0.19 (issue #3540614) | Not yet documented |

Not covered by this guide and worth a future pass: the `ui_patterns_field` sub-module (a `SourceValueItem` field type that stores UI Patterns source configuration as field data), which saw heavy work across 2.0.16–2.0.19.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| UI Patterns 2 Official Docs | https://project.pages.drupalcode.org/ui_patterns/ | All sections | 2026-02-19 |
| Authoring a Component | https://project.pages.drupalcode.org/ui_patterns/2-authors/0-authoring-a-component/ | Defining Components, Props System | 2026-02-19 |
| Best Practices | https://project.pages.drupalcode.org/ui_patterns/2-authors/2-best-practices/ | Best Practices & Anti-Patterns | 2026-02-19 |
| Prop Type Plugins | https://project.pages.drupalcode.org/ui_patterns/3-devs/2-prop-type-plugins/ | Props System | 2026-02-19 |
| Source Plugins | https://project.pages.drupalcode.org/ui_patterns/3-devs/1-source-plugins/ | Source Plugins, Custom Source Plugins | 2026-02-19 |
| Component Form | https://project.pages.drupalcode.org/ui_patterns/1-users/0-component-form/ | Source Plugins, Architecture | 2026-02-19 |
| Stories and Library | https://project.pages.drupalcode.org/ui_patterns/2-authors/1-stories-and-library/ | Pattern Library | 2026-02-19 |
| UI Patterns FAQ | https://project.pages.drupalcode.org/ui_patterns/faq/ | Overview, SDC Integration | 2026-02-19 |
| Drupal.org Best Practices | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/ui-patterns/best-practices | Best Practices & Anti-Patterns | 2026-02-19 |
| Evolving Web Tutorial | https://evolvingweb.com/blog/speed-front-end-development-drupal-ui-patterns | Overview & Decision | 2026-02-19 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| ui_patterns | `modules/contrib/ui_patterns/` | All sections | 11.4 |
| ui_patterns (src) | `modules/contrib/ui_patterns/src/` | Architecture, Props System, Source Plugins, Custom Source Plugins | 11.4 |
| ui_patterns (schema) | `modules/contrib/ui_patterns/config/schema/ui_patterns.schema.yml` | Config Export Reference | 11.4 |
| ui_patterns (sources schema) | `modules/contrib/ui_patterns/config/schema/ui_patterns.sources.schema.yml` | Config Export Reference | 11.4 |
| ui_patterns_layouts | `modules/contrib/ui_patterns/modules/ui_patterns_layouts/` | Layout Builder Integration | 11.4 |
| ui_patterns_layouts (schema) | `modules/contrib/ui_patterns/modules/ui_patterns_layouts/config/schema/ui_patterns_layouts.schema.yml` | Config Export Reference, Layout Builder Integration | 11.4 |
| ui_patterns_views | `modules/contrib/ui_patterns/modules/ui_patterns_views/` | Views Integration | 11.4 |
| ui_patterns_views (schema) | `modules/contrib/ui_patterns/modules/ui_patterns_views/config/schema/ui_patterns_views.schema.yml` | Config Export Reference, Views Integration | 11.4 |
| ui_patterns_field_formatters | `modules/contrib/ui_patterns/modules/ui_patterns_field_formatters/` | Field Formatters | 11.4 |
| ui_patterns_field_formatters (schema) | `modules/contrib/ui_patterns/modules/ui_patterns_field_formatters/config/schema/ui_patterns_field_formatters.schema.yml` | Config Export Reference, Field Formatters | 11.4 |
| ui_patterns_blocks | `modules/contrib/ui_patterns/modules/ui_patterns_blocks/` | Blocks Integration | 11.4 |
| ui_patterns_blocks (schema) | `modules/contrib/ui_patterns/modules/ui_patterns_blocks/config/schema/ui_patterns_blocks.schema.yml` | Config Export Reference, Blocks Integration | 11.4 |
| ui_patterns_library | `modules/contrib/ui_patterns/modules/ui_patterns_library/` | Pattern Library | 11.4 |
| ui_suite_daisyui (components) | `themes/contrib/ui_suite_daisyui/components/` | Config Export Reference (example components) | 11.4 |
