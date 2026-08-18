---
description: "Component YAML schema keys core actually reads, and why the YAML declares while the Twig decides"
tldr: "Core validates props against the schema but never strips undeclared ones and never applies YAML default: — the Twig's ?? / |default() is the only real default. There is no libraryDependencies key; use libraryOverrides: dependencies:. Read the .twig, not the YAML, to learn a component's real API."
drupal_version: "11.x"
---

# Component YAML Schema

## When to Use

> Use this when you're defining component metadata, specifying props and slots, configuring library dependencies, or reading someone else's `.component.yml` to find out how their component behaves.

## THE MECHANISM: the YAML declares, the Twig decides

**Read this before anything else in this guide. Every other SDC topic defers to it.**

Core reads the `.component.yml` in order to *validate* and to *describe*. It never uses it to *transform* the data on its way to the template. Three consequences follow, all verified against Drupal 11.3 core:

1. **Core validates props but never strips them.** `ComponentValidator::validateProps()` takes the Twig context **by value** and returns a `bool` (`ComponentValidator.php:172`), so it has no way to write anything back. Before validating it narrows the context to declared prop names — `$props_raw = array_intersect_key($context, array_flip($prop_names))` (`:189-190`) — so a prop you never declared is not merely allowed, it is never examined. It arrives in the Twig and works normally. And the call site is `assert($this->doValidateProps($context, $component_id));` (`ComponentsTwigExtension.php:106`), which a production `zend.assertions=-1` compiles out entirely. Validation is a development-time lint, not a runtime gate.

2. **Core never applies `default:` from the YAML.** The validator runs with `Constraint::CHECK_MODE_TYPE_CAST` only (`ComponentValidator.php:202`); `CHECK_MODE_APPLY_DEFAULTS` appears nowhere in core. A `default:` in the YAML is documentation for humans and a hint for consumers such as UI Patterns — **the value a prop actually has when the caller omits it is whatever the Twig sets with `??` or `|default()`, and nothing else.**

3. **Slot `required: true` is inert.** The per-slot schema (`metadata.schema.json` → `$defs/slotDefinition`) allows only `title`, `description` and `examples`, and `ComponentNodeVisitor::validateSlots()` (`:150-185`) walks the template's blocks and reports only slots that were *supplied but never declared*. Nothing in core reads a slot `required` key or reports a missing slot. Neither schema file sets `additionalProperties: false` at the level where you would write it, so the key is accepted in silence.

**Therefore:** to learn what a component's props are called, what they do, and what they default to, **read the `.twig`**. The `.component.yml` records what someone declared — which may be stale, incomplete, or aspirational. When the two disagree, the Twig is what ships. Write the YAML to match the Twig, never the other way round.

## Decision

**Minimum viable file:** an empty `.component.yml` is valid. The JSON Schema declares no `required` array, and `ComponentMetadata` defaults `name` to the title-cased machine name, `status` to `stable`, `description` to a placeholder and `group` to "All Components" (`ComponentMetadata.php:135-142`). Core's own kernel test asserts that a component with an empty metadata file is found.

**Keys core actually reads:**

| Key | Purpose | Notes |
|---|---|---|
| `$schema` | JSON Schema URL | Enables IDE validation; no runtime effect |
| `name` | Human-readable name | Defaults to title-cased machine name |
| `description` | Component purpose | — |
| `status` | `experimental \| stable \| deprecated \| obsolete` | Defaults to `stable`; also falls back to `stable` for any value outside the enum, though the definition validator flags it when assertions are on |
| `noUi` | Exclude the component from component-picker UIs | — |
| `group` | Admin category | Read by `ComponentPluginManager::processDefinitionCategory()` but **absent from both JSON Schema files** — valid, just undocumented upstream |
| `replaces` | Replacement directive | Also read by PHP but absent from the JSON Schemas. Usable from themes **and** modules — see [Replacing Templates with SDCs](replacing-templates-with-sdcs.md) |
| `props` | JSON Schema for typed data | — |
| `slots` | Content insertion points | — |
| `variants` | Named variant metadata | Drupal **11.2+** — see [Component Variants](component-variants.md) |
| `libraryOverrides` | The only library key | Carries `dependencies`, `css` and `js` |
| `thirdPartySettings` | Free-form storage for contrib | — |

**There is no `libraryDependencies` key.** It is not in `metadata.schema.json`, not in `metadata-full.schema.json`, and `ComponentPluginManager::libraryFromDefinition()` reads only `$definition['libraryOverrides']` (`:207-220`). Because neither schema sets `additionalProperties: false` at the top level, writing `libraryDependencies:` raises no error at any validation level — your `core/once` dependency is simply never attached and the component's JS breaks at runtime with nothing pointing back at the YAML. Use `libraryOverrides: dependencies:`.

**Slot names and prop names share one namespace.** `ComponentValidator::validateDefinition()` throws `InvalidComponentException` when the same key is declared as both (`ComponentValidator.php:55-67`).

## Pattern

**Recommended baseline** (none of these are enforced, all of them are worth writing):
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: 'Component Name'
status: stable
```

**Props** — Reference: `/core/modules/system/tests/modules/sdc_test/components/my-button/my-button.component.yml`
```yaml
props:
  type: object
  required:
    - text
  properties:
    text:
      type: string
      title: 'Button Text'
      minLength: 2
    variant:
      type: string
      title: 'Visual Variant'
      enum: [primary, secondary, danger]
      default: primary   # documentation only — see THE MECHANISM above
    disabled:
      type: boolean
      title: 'Disabled State'
      default: false     # documentation only — see THE MECHANISM above
```

The `default:` lines above do **not** make `variant` become `primary` when the caller omits it. The template has to say so:

```twig
{% set variant = variant|default('primary') %}
{% set disabled = disabled ?? false %}
```

Keep the two in sync, and treat a mismatch between them as a bug in the YAML.

**Slots** — Reference: `/core/themes/olivero/components/teaser/teaser.component.yml`
```yaml
slots:
  content:
    title: 'Main Content'
    description: 'Primary content area'
  header:
    title: 'Header Content'
    description: 'Optional header region'
```

`title`, `description` and `examples` are the only keys the slot schema allows. **Do not write `required: true` on a slot** — nothing reads it (see THE MECHANISM above), so it reads as a guarantee to the next developer that core will not honour. If a slot is genuinely mandatory, say so in `description:` and give the block a sensible fallback inside the template.

**Library Dependencies** — Reference: `/core/modules/system/tests/modules/sdc_test_replacements/components/my-button/my-button.component.yml`
```yaml
libraryOverrides:
  dependencies:
    - core/once
    - my_theme/utilities
  js:
    custom.js:
      attributes: { defer: true }
      preprocess: false
```

Two things to know about `libraryOverrides`:
- It is applied with `array_merge()` over the auto-generated library, so a `css` or `js` key **replaces** the auto-discovered entry for that bucket rather than adding to it.
- The moment `libraryOverrides` is non-empty, core appends `core/drupal` to the dependency list unconditionally (`ComponentPluginManager.php:217-221`), so you never need to list it yourself.

## Common Mistakes

- **Wrong**: Writing `libraryDependencies:` → **Right**: Use `libraryOverrides: dependencies:`. The wrong key raises no error anywhere; your dependency is simply never attached.
- **Wrong**: Not including `$schema` URL → **Right**: Without it, IDEs can't provide validation/autocomplete, and developers lose development-time error checking.
- **Wrong**: Using `type: array` for renderable content (e.g. `card_title_prefix`) → **Right**: Arrays of renderable content should be slots, not props. Props are for typed scalar/object data that validates against JSON Schema.
- **Wrong**: Trusting an unfamiliar component's `.component.yml` as the description of its API → **Right**: Nothing keeps the YAML honest at runtime. Undeclared props still work, declared defaults are never applied, and required slots are never enforced. Open the `.twig` before you write the call.

## See Also

- Reference: `/core/assets/schemas/v1/metadata.schema.json` — Official JSON Schema (component-authoring shape)
- Reference: `/core/assets/schemas/v1/metadata-full.schema.json` — The schema the definition is actually validated against, after core adds `id`, `path`, `provider`, `machineName`, `library`, `template`
- Reference: `/core/lib/Drupal/Core/Theme/Component/ComponentMetadata.php` — Every default core applies to a missing key
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Official Component YAML Reference](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml)
