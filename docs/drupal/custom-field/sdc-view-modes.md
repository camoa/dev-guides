---
description: "The custom_field_sdc sub-module renders a whole entity view mode through a Single Directory Component -- config shape, prop/slot resolution, fail-safes, and when to pick it over UI Patterns, Canvas, or the field formatter."
tldr: "custom_field_sdc replaces a whole view mode's render output with a component: props are static/token values typed on Manage display, slots pull a whole formatted field render array -- any failure falls back silently to normal field output except a failed validateComponent(), which logs."
drupal_version: "11.x"
---

# SDC View-Mode Rendering (`custom_field_sdc`)

## When to Use

You want an entity's **whole view mode** to render as a single directory component -- `node.article.teaser` comes out as your `card` component's markup instead of a field list -- configured entirely on Manage display, with no preprocess, no template override, and no code.

Despite living under `custom_field`, this sub-module has **nothing to do with custom fields**. It depends on `custom_field` only to borrow two things from it: the `#[PropWidget]` plugin system and `SdcTrait`'s component validator. It works on any entity type, any bundle, any view mode, on a display with no custom field on it at all.

## Pattern

Enable `custom_field_sdc`. On **Structure -> ... -> Manage display**, a details element titled *"Custom Field - Single directory component options"* appears on the form:

1. Tick **Render using a component**.
2. Pick a **Component** from the select -- grouped by the component's `group`, and listing only components that pass validation (see *Which Components Are Offered* below).
3. Fill in the component's **Props** -- each prop gets a form widget chosen by a `#[PropWidget]` plugin. Values are entered by hand, and may contain tokens.
4. Map the component's **Slots** -- each slot is a select listing the fields *already enabled on this view display*.

Save. Every entity rendered in that view mode now renders as the component.

## How It Actually Works

One hook does the whole job: `#[Hook('entity_view_alter')]` on `src/Hook/EntityHooks.php`. It runs after Drupal has built the normal field-by-field render array, then **discards that array and substitutes its own**:

```php
$original_build = $build;
$output = [
  '#entity_type' => $entity_type,
  '#' . $entity_type => $entity,          // e.g. '#node' => $node
  '#view_mode' => $original_build['#view_mode'] ?? 'default',
  'component' => [
    '#type' => 'component',
    '#component' => $component_id,
    '#slots' => [],
    '#props' => $props,
  ],
];
// ...slots and cache metadata...
$build = $output;
```

Note the shape: the component is a **child** named `component`, under a wrapper carrying the entity context keys. Anything else the original build held -- `#theme`, `#pre_render`, other modules' additions, every field -- is gone.

**Props are static values, made dynamic by tokens.** This is the point most easily missed. A prop's stored value is whatever the site builder typed on the display form; it is *not* read from the entity's fields. Each `#[PropWidget]` plugin resolves it through `getPropValue($value, $context)`, where `$context` carries `entity_type`, `entity` and a `BubbleableMetadata`. Those three exist for exactly one purpose: `PropWidgetTokenTrait::resolveTokens()` runs the value through the token service with the entity as token data, collecting cache metadata as it goes. So `[node:title]` in a prop field works -- but **only if the contrib `token` module is installed**; without it the trait returns the raw string untouched, tokens and all. A value with no `[` in it skips token processing entirely.

**Slots take a whole field render array, formatter output intact.** A slot's value is `$original_build[$field_name]` -- lifted verbatim out of the build that was about to be thrown away. Formatter settings, field template, cache metadata: all preserved. The consequence is a hard constraint: **a slot can only be filled from a field that is already enabled on this view display.** The form enforces it -- the field select is populated from `array_keys($display->getComponents())`. Move a field to Disabled and its slot silently empties.

Slot config also stores a `source` key, but in 5.0.2 the form hard-codes it (`'#type' => 'value'`, `'#value' => 'field'`) and the hook only acts on `source === 'field'`. It is a seam for future sources, not a choice you have today.

## Config Shape

Everything lives in the view display's third-party settings under a single `settings` key. Schema: `config/schema/custom_field_sdc.schema.yml`, keyed on `core.entity_view_display.*.*.*.third_party.custom_field_sdc`.

```yaml
# core.entity_view_display.node.article.default.yml
third_party_settings:
  custom_field_sdc:
    settings:
      enabled: true
      component: 'my_theme:card'
      props:
        heading:
          widget: string            # a #[PropWidget] plugin ID
          value: '[node:title]'
        ctaHref:
          widget: string
          value: 'https://example.org'
      slots:
        card_body:
          source: field
          field: body
```

Each prop entry is a `custom_field.dynamic_property`: a `widget` (constrained by `PluginExists` against `plugin.manager.custom_field_component_prop_widget`) plus a `value` whose schema type is derived from the widget ID -- `custom_field.prop_value.[%parent.widget]`. So a `boolean` widget stores a boolean, an `image` widget stores a mapping, an `array_object` widget stores a nested list of the same `{widget, value}` pairs, one per sub-prop.

The `variant` key in the schema is **inert in 5.0.2**. Nothing in `custom_field` reads it -- not `EntityHooks`, not `FormHooks`, not `SingleDirectoryComponentFormatter` (which also declares it as a default setting and never uses it). Core would honour a `variant` in the component context (`ComponentsTwigExtension` emits `data-component-variant` from it), but no code path puts it there. Do not build a design that depends on it.

## The Prop Widgets

Thirteen `#[PropWidget]` plugins ship in the main module, under `src/Plugin/Components/PropWidget/`: `string`, `integer`, `number`, `boolean`, `uri`, `image`, `object`, `attributes`, `array_string`, `array_integer`, `array_number`, `array_image`, `array_object`.

`PropWidgetManager::getPropWidget()` picks one from the prop's JSON Schema: `type` first, then special cases -- `Drupal\Core\Template\Attribute` -> `attributes`; `type: string` with `format: uri` or `uri-reference` -> `uri`; `type: array` resolved through `items.type`; an object whose `id` is `json-schema-definitions://canvas.module/image` -> the image widgets. A prop UI Patterns marked `ui-patterns://attributes` is skipped deliberately.

**A prop with no matching widget is silently skipped** -- both in the form (no input appears) and in the hook (`continue`). It is not an error; the component simply renders without that prop.

## Which Components Are Offered

`FormHooks` runs every discovered component through `SdcTrait::validateComponent()`, which returns `TRUE` or an array of human-readable reasons. A component is rejected when it has no `props`, no `props.properties`, or any prop that is malformed: missing `type`; `type: array` with no `items` or no `items.type`; object items with no `properties`; or a prop referencing Canvas's image definition while Canvas is not installed ("The Canvas module is a dependency for this prop").

Rejected components are not hidden -- they are listed in an **Invalid components** details element with their reasons, which is the fastest way to debug a component that will not appear in the select. Components whose metadata sets `noUi: true` (a Drupal 11.3+ property) are skipped entirely and never listed.

## Fail-Safes

Every failure path leaves the entity's **normal render output** in place rather than producing a broken page or a WSOD. Six early returns in `EntityHooks::entityViewAlter()`, three of them genuine fail-safes:

| Condition | Behaviour |
|---|---|
| `sdc_display` has claimed this display | Return -- see *Coexistence* below |
| Not enabled, or no component selected | Return |
| **Component ID no longer resolves** (`ComponentNotFoundException`) | Return, silently. Renaming or deleting a component reverts the display to normal field output |
| **Component fails `validateComponent()`** | Logged to the `custom_field_sdc` channel -- *"The component %component_id failed validation and could not be rendered"* -- then return. This is the one failure that leaves a trace; check the log when a display quietly stops using its component |
| **A required prop resolves to `NULL` or `''`** | Return. A token that cleared to nothing on one node makes that node fall back to field output while its siblings still render as the component -- inconsistent-looking output with no error anywhere |

Optional props that resolve empty are dropped from `#props` rather than passed as `''`, so the component's own Twig `default()` values apply.

## Cacheability

Handled, and worth understanding because the original build is discarded:

```php
$original_metadata = BubbleableMetadata::createFromRenderArray($original_build);
$original_metadata->merge($bubbleable_metadata)->applyTo($output);
```

Cache tags, contexts and max-age are lifted off the build that was thrown away, merged with whatever accumulated while resolving props (token replacements bubble their own metadata into the `BubbleableMetadata` passed in the context), and applied to the new output. Field-level cacheability survives even for fields that did not end up in a slot.

## Coexistence with `sdc_display`

The `sdc_display` contrib module alters the same hook for the same purpose. `custom_field_sdc` yields rather than fights: the very first thing `entityViewAlter()` does is read `$display->getThirdPartySetting('sdc_display', 'enabled')` and return if it is set. The form mirrors this -- when `sdc_display` is installed, a warning ("The *sdc_display* module is controlling this display") and `#states` hide the whole settings container while the `sdc_display` checkbox is ticked.

## Decision: `custom_field_sdc` vs UI Patterns vs Canvas vs the field formatter

All four render Drupal content through an SDC. They differ in **what supplies the prop values** and **who does the configuring**.

| You want... | Use | Because |
|---|---|---|
| One view mode of one bundle rendered as a component, props typed in by hand or via tokens | **`custom_field_sdc`** (this guide) | Cheapest possible setup -- one details element on Manage display, one hook, no extra module. Props are static/token values, not field-driven |
| Props bound to **fields**, per field, with sources you can swap (field value, entity property, another component) | **UI Patterns 2** (`ui_patterns_layouts` for whole displays, `ui_patterns_field_formatters` per field, `ui_patterns_blocks`, `ui_patterns_views`) | Its Source plugin system is the whole point: any prop can be fed from any registered source, and it is typed through PropTypes. `custom_field_sdc` has no equivalent -- a prop is a typed-in value |
| Editors composing pages from components, visually, per node | **Canvas** | It is a page builder. `custom_field_sdc` is a display setting a site builder configures once for a bundle; editors never see it |
| A **single compound field** rendered as a component, its sub-fields mapped to props and slots | The **`custom_field_sdc` field formatter** (`SingleDirectoryComponentFormatter`, see [Field-Level Formatters](field-level-formatters.md)) | Different tool, same plugin ID. It lives in the main module, needs no sub-module, and *is* field-driven -- sub-field -> prop. Richer too: per-slot format types, formatter settings and wrappers |
| Every view mode across many bundles driven by components, as a site-wide strategy | **`sdc_display`** or UI Patterns | `custom_field_sdc` is per-display config with no bulk story; it defers to `sdc_display` by design |

Combining is fine: a display can use `custom_field_sdc` for the view mode while a field inside a slot uses the `custom_field_sdc` *formatter* for its own component.

## What the Test Proves

`tests/src/Functional/ComponentViewModeRenderTest.php` is the clearest statement of intended usage -- it configures the display in `setUp()` exactly as the UI would store it, then asserts against the rendered page.

`testMyBanner()` sets `node.article.default` to core's `sdc_test:my-banner`, gives it four `string` props and maps the `banner_body` slot to the `body` field, then asserts the node page renders `[data-component-id="sdc_test:my-banner"] h3` with the prop text and `.component--my-banner--body` with the body value. Note what this proves: the *component's* markup replaced the node's, and the body slot carries **formatted field output**, not a raw value.

`testCardList()` is the more interesting one. It maps the `title` slot to the `title` **base field** -- proof that slots are not limited to configurable fields -- and drives a nested `array_object` prop, where each item is itself a map of `{widget, value}` pairs including a nested `array_string`. That is the shape to copy when a component takes a list of cards.

Neither test sets `variant`, and neither exercises the `sdc_display` deference path (that module is not a test dependency).

## Common Mistakes

- **Expecting props to read from the entity's fields** -- they do not. A prop's value is what the site builder typed. Use tokens (`[node:field_subtitle]`) for anything dynamic, or reach for UI Patterns if you want real field binding
- **Using tokens without the `token` module** -- `resolveTokens()` returns the raw string, so `[node:title]` renders literally. Core has no general token-replacement UI dependency here; install `drupal/token`
- **Mapping a slot to a field that is Disabled on the display** -- the slot resolves to `''`. The field must be in the enabled list, because the slot is lifted out of the original build by name
- **Configuring this on a Layout Builder-enabled display** -- `FormHooks` returns early for any display implementing `LayoutBuilderEnabledInterface` with Layout Builder on, so the settings never appear. Use Layout Builder's own component tooling there
- **Assuming a required prop failure is loud** -- it is not. The entity falls back to normal field output with nothing logged. Only the `validateComponent()` failure writes to the log
- **Setting `variant` in exported config and expecting a variant** -- inert in 5.0.2; nothing reads it
- **Looking for the formatter in this sub-module** -- `SingleDirectoryComponentFormatter` is in the main module. The sub-module ships no plugin classes at all -- six files: `.info.yml`, `.services.yml`, the config schema, two `#[Hook]` classes, and the functional test

## See Also

- [Sub-Modules](sub-modules.md)
- [Field-Level Formatters](field-level-formatters.md) -- the `SingleDirectoryComponentFormatter` this is constantly confused with
- [Custom Plugin Development](custom-plugins.md) -- writing your own `#[PropWidget]`
- [Token Support](token-support.md) -- the token layer prop values depend on
- [UI Patterns](../ui-patterns/index.md) -- the source-driven alternative
- Reference: `/modules/contrib/custom_field/modules/custom_field_sdc/`
