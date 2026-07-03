---
# Routing block — an orchestrator reads to here and decides.
name: provision_content_type_fields
capability: content-type-field-provisioning
description: Use when a content type needs its fields defined — running an ordered per-field storage decision, sharing storages by concern, using custom compound fields only for genuinely polymorphic data, wiring entity display, and evolving compound schema safely on live data.
# Metadata — read only after a match.
label: Provision content type fields
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/entities/field-storage-decision
  - drupal/entities/field-type-selection
  - drupal/entities/field-storage-configuration
  - drupal/entities/field-instance-configuration
  - drupal/entities/entity-reference-patterns
  - drupal/entities/content-type-configuration
  - drupal/entities/form-display-configuration
  - drupal/entities/view-display-configuration
  - drupal/custom-field/overview
  - drupal/custom-field/schema-updates
  - drupal/ui-patterns/field-formatters
  - drupal/ui-patterns/source-plugins
drupal_compatibility: "^10.4 || ^11"
requires_modules:
  - field
optional_modules:
  - custom_field
  - ui_patterns
invokes_drupal_recipes: []
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Provision a content type's fields with the correct **storage architecture** — each field's storage shape chosen by an ordered decision, recurring concerns collapsed to one concern-named shared storage, compound fields used only for genuine polymorphism, entity display wired, and any evolution of a populated compound field done through the safe managed path — so the data model is queryable, reusable, and free of fragmentation or over-engineering.

## Opinion

**Decide storage shape before creating any field.** Run one ordered dispatch per field — polymorphic → compound; classification → vocabulary reference; shared concern → shared storage; entity-worthy collection → wrapper; independent entity → reference; else → plain field. Deciding ad hoc is what produces fragmentation and over-modeling. Source: guide `drupal/entities/field-storage-decision`.

**Share storage by concern, and name it by concern.** When a concern recurs across bundles of one entity type, emit ONE storage named for the concern (`field_eyebrow`), instanced across bundles — never `field_hero_eyebrow` + `field_card_eyebrow`. Source: guide `drupal/entities/field-storage-configuration`.

**A `custom` compound only for genuine polymorphism.** Reach for a compound (`type: custom`) when a value has ≥2 mutually-exclusive sub-shapes and no single core field expresses them. An optional single value is not polymorphic — it is a single-value field with `required: false`. Source: guide `drupal/custom-field/overview`.

**Classification is a vocabulary, not a string.** A controlled classification dimension is a taxonomy vocabulary referenced by an `entity_reference`, even when only one bundle uses it today — so terms, hierarchy, and term metadata stay governed. Source: guides `drupal/entities/field-type-selection`, `drupal/entities/entity-reference-patterns`.

**Storage is per entity-type; reconcile cardinality to the max.** Cardinality is a storage-level property with no per-bundle override, so a shared storage takes the maximum any bundle needs, and lower per-bundle limits are enforced at the widget. The same concern on two different entity types is legitimately two storages. Source: guide `drupal/entities/field-storage-configuration`.

**Reference settings live on the instance, not the storage.** `handler`, `handler_settings`, and `target_bundles` belong on the field instance; the storage carries only `target_type`. Source: guide `drupal/entities/field-instance-configuration`.

**Wire display declaratively.** Where UI Patterns 2 maps fields to component props/slots, use the declarative source mapping instead of Twig template overrides. Source: guides `drupal/ui-patterns/field-formatters`, `drupal/ui-patterns/source-plugins`.

**Evolve a populated compound field through the managed path.** Adding or removing a sub-column on a `custom` field that already holds content goes through the module's update service (a `hook_update_N()` calling `custom_field.update_manager`, or the `cf-add-column` command) — never hand-rolled `ALTER TABLE`, never delete-and-recreate. Source: guide `drupal/custom-field/schema-updates`.

### What this recipe refuses

- N bundle-named storages for one semantic concern.
- A `custom` compound for an optional single value (over-engineering), or N parallel "fill one" fields for data that is actually one polymorphic value.
- `handler`/`handler_settings` on a field storage (they fail schema validation there).
- Altering a populated `custom` field with hand-rolled SQL `ALTER TABLE` or delete-and-recreate when the module's managed update service exists.
- Suggesting `drush entity:updates` / `entup` — it does not exist in Drupal 10/11 and never managed field-storage column schema.

## Preconditions

- Drupal 10.4+ or 11.x; the `field` module (core).
- `custom_field` enabled if any field in the model is polymorphic (needs a `custom` compound).
- `ui_patterns` enabled if the display uses declarative field→component mapping.
- The target content-type bundle exists, or is created as step 1 (see `drupal/entities/content-type-configuration`).
- A field/content model is supplied via the input contract.
- Config export is in use, so the provisioned model is deployable.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
target:
  entity_type: string          # e.g. node
  bundle: string               # the content type

fields:
  - name: string               # concern-named machine name (snake_case)
    concern: string            # semantic role — used to detect sharing
    shape: string              # human description of the data shape
    polymorphic: boolean       # ≥2 mutually-exclusive sub-shapes? (default false)
    classification: boolean    # a controlled vocabulary? (default false)
    shared_across_bundles:     # other bundles carrying the same concern
      - string
    cardinality: integer       # values allowed; -1 = unlimited (default 1)
    required: boolean          # instance-level (default false)
    reference_target: string   # entity type, when the field is a reference

display:                       # optional hints; wiring is deterministic from the model
  form: string                 # widget preferences
  view: string                 # formatter / UI Patterns source-mapping preferences
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate preconditions and load the model.** Confirm modules and the target bundle; if the bundle does not exist, create it. See `drupal/entities/content-type-configuration`.

2. **Run the storage-decision dispatch per field.** For each field, evaluate the ordered decision and record the verdict (compound / vocabulary reference / shared storage / wrapper / reference / plain field). See `drupal/entities/field-storage-decision`.

3. **Collapse shared concerns.** Group fields by `concern`; where one concern recurs across bundles, resolve to a single concern-named storage instanced per bundle, and reconcile cardinality to the maximum any bundle needs. See `drupal/entities/field-storage-configuration`.

4. **Create storages and instances config-first**, per the verdicts — reference `handler`/`handler_settings` on the instance, `target_type` on the storage. For classifications, ensure the vocabulary exists and reference it. See `drupal/entities/field-instance-configuration`, `drupal/entities/entity-reference-patterns`.

5. **Create compound fields only where the verdict was polymorphic** (`type: custom`), with the sub-field columns the shape needs — never for optional-single or "fill one" cases. See `drupal/custom-field/overview`.

6. **Wire entity display.** Configure the form-display widgets and view-display formatters for the created fields; where UI Patterns 2 is used, declare the field→component source mapping instead of Twig overrides. See `drupal/entities/form-display-configuration`, `drupal/entities/view-display-configuration`, `drupal/ui-patterns/field-formatters`, `drupal/ui-patterns/source-plugins`.

7. **If evolving an existing populated compound field**, make the sub-column change through the managed update service (`hook_update_N()` calling `custom_field.update_manager`, or `cf-add-column`) — never hand-rolled SQL, never delete-and-recreate. See `drupal/custom-field/schema-updates`.

8. **Export configuration, rebuild caches, and emit a summary** of what was created, skipped as a no-op, or surfaced as a conflict for operator review.

## Data flow

```
input: target (entity_type, bundle)
       fields[]  (concern, shape, polymorphic, classification,
                  shared_across_bundles, cardinality, required, reference_target)
       display   (optional widget/formatter hints)

reads project state:
       field.storage.<entity_type>.* / field.field.<entity_type>.<bundle>.*
       existing bundles + taxonomy vocabularies
       core.entity_form_display.* / core.entity_view_display.*
       existing `custom` field column definitions (for evolution)

applies opinion (guardrails):
       decide-shape-first · share-by-concern · compound-only-if-polymorphic ·
       classification-is-a-vocabulary · cardinality-on-storage ·
       reference-settings-on-instance · managed-compound-evolution

references atomic detail (guides):
       drupal/entities/{ field-storage-decision, field-type-selection,
         field-storage-configuration, field-instance-configuration,
         entity-reference-patterns, content-type-configuration,
         form-display-configuration, view-display-configuration }
       drupal/custom-field/{ overview, schema-updates }
       drupal/ui-patterns/{ field-formatters, source-plugins }

emits:
       field.storage.<entity_type>.<name>        (concern-named; cardinality = max)
       field.field.<entity_type>.<bundle>.<name>  (handler_settings here, not storage)
       taxonomy.vocabulary.*                       (for classifications, if absent)
       core.entity_form_display.* / core.entity_view_display.*
       (compound evolution, when applicable, via custom_field.update_manager)
```

## State-awareness contract

The recipe reads existing state before writing. For every emitted config object: absent → create; present and matching the resolved spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review.

Storage-level changes carry cross-bundle blast radius: adding a bundle instance to an existing shared storage is a create; reducing a shared storage's cardinality is a conflict (it affects every bundle already using it) and is never applied silently. Evolving a **populated** `custom` field always goes through the managed update service — a destructive delete-and-recreate is never chosen for a field that holds data.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

After the recipe runs, verify:

1. Each field's storage shape matches its decision verdict — polymorphic → a `type: custom` compound; classification → an `entity_reference` to a taxonomy vocabulary; independent entity → `entity_reference`; else a plain field.
2. Each recurring concern is exactly ONE concern-named storage instanced across its bundles — not N bundle-named storages — and its cardinality equals the maximum any bundle needs.
3. Every `entity_reference` field keeps `handler`/`handler_settings` on the instance and only `target_type` on the storage.
4. No `custom` compound exists where a single non-required core field would suffice (no over-engineering).
5. A sub-column added to a seeded `custom` field via the managed update service leaves existing rows intact (zero data loss).
6. Every created field has a form-display widget and a view-display formatter wired.

The recipe ships no verifier *script*, but every check is **agent-runnable**. Checks 1–4 and 6 are `config-assert` (drush + config reads, no served site needed). Check 5 is `self-fixture` — it seeds a `custom` field with rows, runs `custom_field.update_manager` to add a column, and asserts the rows survive, cleaning up the fixture afterward (it does not assume an operator fixture). No check requires a served site, so none is fail-closed on its absence.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/entities/field-storage-decision` | The ordered per-field storage dispatch |
| `drupal/entities/field-type-selection` | Data-shape → field-type mapping |
| `drupal/entities/field-storage-configuration` | Shared-storage-by-concern, cardinality reconciliation |
| `drupal/entities/field-instance-configuration` | Reference settings on the instance, not storage |
| `drupal/entities/entity-reference-patterns` | Vocabulary and entity references |
| `drupal/entities/content-type-configuration` | Creating the bundle |
| `drupal/entities/form-display-configuration` | Form widgets |
| `drupal/entities/view-display-configuration` | View formatters |
| `drupal/custom-field/overview` | The polymorphic trigger and its over-engineering guard |
| `drupal/custom-field/schema-updates` | Managed compound-schema evolution on live data |
| `drupal/ui-patterns/field-formatters` | Declarative field→component formatter mapping |
| `drupal/ui-patterns/source-plugins` | UI Patterns source IDs for field data |
