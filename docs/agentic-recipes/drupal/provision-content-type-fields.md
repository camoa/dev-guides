---
# Routing block — an orchestrator reads to here and decides.
name: provision_content_type_fields
capability: content-type-field-provisioning
description: Use when a content type needs its fields defined — running an ordered per-field storage decision, sharing storages by concern, using custom compound fields only for genuinely polymorphic data, wiring entity display, and evolving compound schema safely on live data.
# Metadata — read only after a match.
label: Provision content type fields
recipe_schema_version: 1.0.0
version: 0.2.0
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
- DDEV runs the site; the verifier's commands go through `ddev`.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
target:
  entity_type: string          # e.g. node
  bundle: string               # the content type

fields:
  - name: string               # concern-named field machine name, with its field_ prefix
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

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/provision-content-type-fields/verify.php` run the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: storage-shapes
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/provision-content-type-fields/verify.php -- storages {target.entity_type} {target.bundle} {fields:json}
    pass: stdout empty
  - id: shared-storage-instanced
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/provision-content-type-fields/verify.php -- instances {target.entity_type} {target.bundle} {fields:json}
    pass: stdout empty
  - id: reference-settings-on-instance
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/provision-content-type-fields/verify.php -- references {target.entity_type} {target.bundle} {fields:json}
    pass: stdout empty
  - id: displays-wired
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/provision-content-type-fields/verify.php -- displays {target.entity_type} {target.bundle} {fields:json}
    pass: stdout empty
  - id: no-update-pending
    kind: config-assert
    run: ddev drush updatedb:status
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the proof is:

- `storage-shapes` checks each field's storage against its input flags: `type: custom` if and only if `polymorphic`; a classification is an `entity_reference` to `taxonomy_term`; a `reference_target` is an `entity_reference` to that entity type. It cannot tell which core type a plain field should be, because `shape` is free text. It also stands in for the over-engineering check: a `custom` storage on a field not marked polymorphic is a violation.
- One storage per concern is checked in the positive: each field's one storage is instanced on the target bundle and on every `shared_across_bundles` entry. No naming rule tells a bundle-named storage from a concern-named one.
- Cardinality is checked as at least the declared value, or unlimited. The input carries one cardinality per field, so "the maximum any bundle needs" has nothing else to compare against.
- `shared-storage-instanced` compares `required` on the target bundle only. The input gives one `required` per field, and the other bundles may carry their own.
- `reference-settings-on-instance` reads the raw config. A classification's instance must also list at least one vocabulary in `target_bundles`, and each must exist.
- `displays-wired` checks the `default` form and view displays of every bundle the field is on. The `display` hints are free text, so the widget and formatter chosen are not checked, nor is a UI Patterns source mapping.
- The zero-data-loss check of a sub-column added to a populated `custom` field is not run. It would test the `custom_field` module's own update service, not this recipe's output, and `custom_field:add-column` is interactive only. `no-update-pending` proves no update hook is pending on the site, so the hook that carries such a change ran. It is not scoped to this recipe: a pending update from any module fails it, and it passes on a run that evolved no compound field.
- `active-equals-export` proves the export is current after Sequence step 8. The state-awareness contract makes a second apply a no-op on that state.
- An absent or empty `fields` prints a violation in every script entry. Flags absent from a field take the Input contract defaults.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. Drush runs it with Drupal booted and passes the words after `--` in `$extra`.

```php .aida/provision-content-type-fields/verify.php
<?php

// Verifier checks for provision-content-type-fields.
// $extra: <check> <entity type> <bundle> <fields as JSON>
// Prints one line per violation, then throws so Drush exits non-zero.
[$check, $type, $bundle, $json] = array_pad($extra, 4, '');
$v = [];

if (!in_array($check, ['storages', 'instances', 'references', 'displays'], TRUE)) {
  throw new \InvalidArgumentException("unknown check '$check'");
}
$fields = json_decode($json === '' ? 'null' : $json, TRUE, 512, JSON_THROW_ON_ERROR);
if ($type === '' || $bundle === '') {
  $v[] = "$check: the entity type or bundle argument is missing";
}
elseif (!is_array($fields) || !$fields) {
  $v[] = "$check: fields is absent or empty";
}
else {
  foreach ($fields as $i => $field) {
    $name = $field['name'] ?? '';
    if ($name === '') {
      $v[] = "$check: fields[$i] has no name";
      continue;
    }
    $bundles = array_values(array_unique(array_merge([$bundle], $field['shared_across_bundles'] ?? [])));
    $storage = \Drupal::config("field.storage.$type.$name");

    if ($check === 'storages') {
      if ($storage->isNew()) {
        $v[] = "field.storage.$type.$name does not exist";
        continue;
      }
      $field_type = $storage->get('type');
      $target = $storage->get('settings.target_type');
      if (!empty($field['polymorphic'])) {
        if ($field_type !== 'custom') {
          $v[] = "field.storage.$type.$name is polymorphic but has type '$field_type', not 'custom'";
        }
      }
      elseif ($field_type === 'custom') {
        $v[] = "field.storage.$type.$name has type 'custom' but is not polymorphic";
      }
      elseif (!empty($field['classification'])) {
        if ($field_type !== 'entity_reference' || $target !== 'taxonomy_term') {
          $v[] = "field.storage.$type.$name is a classification but is not an entity_reference to taxonomy_term";
        }
      }
      elseif (($field['reference_target'] ?? '') !== '') {
        if ($field_type !== 'entity_reference' || $target !== $field['reference_target']) {
          $v[] = "field.storage.$type.$name is not an entity_reference to {$field['reference_target']}";
        }
      }
      $declared = (int) ($field['cardinality'] ?? 1);
      $actual = (int) $storage->get('cardinality');
      if ($declared === -1 ? $actual !== -1 : ($actual !== -1 && $actual < $declared)) {
        $v[] = "field.storage.$type.$name has cardinality $actual, below the declared $declared";
      }
    }
    elseif ($check === 'instances') {
      foreach ($bundles as $b) {
        $instance = \Drupal::config("field.field.$type.$b.$name");
        if ($instance->isNew()) {
          $v[] = "field.field.$type.$b.$name does not exist";
        }
        elseif ($b === $bundle && (bool) $instance->get('required') !== !empty($field['required'])) {
          $v[] = "field.field.$type.$b.$name has required " . var_export((bool) $instance->get('required'), TRUE) . ', not ' . var_export(!empty($field['required']), TRUE);
        }
      }
    }
    elseif ($check === 'references') {
      if ($storage->isNew() || $storage->get('type') !== 'entity_reference') {
        continue;
      }
      $storage_settings = $storage->get('settings') ?? [];
      if (array_key_exists('handler', $storage_settings) || array_key_exists('handler_settings', $storage_settings)) {
        $v[] = "field.storage.$type.$name carries handler settings, which belong on the instance";
      }
      if (empty($storage_settings['target_type'])) {
        $v[] = "field.storage.$type.$name has no target_type";
      }
      foreach ($bundles as $b) {
        $instance = \Drupal::config("field.field.$type.$b.$name");
        if ($instance->isNew()) {
          continue;
        }
        if (empty($instance->get('settings.handler'))) {
          $v[] = "field.field.$type.$b.$name has no handler";
        }
        if (!empty($field['classification'])) {
          $vocabularies = array_keys($instance->get('settings.handler_settings.target_bundles') ?? []);
          if (!$vocabularies) {
            $v[] = "field.field.$type.$b.$name is a classification with no vocabulary in target_bundles";
          }
          foreach ($vocabularies as $vid) {
            if (\Drupal::config("taxonomy.vocabulary.$vid")->isNew()) {
              $v[] = "field.field.$type.$b.$name targets vocabulary $vid, which does not exist";
            }
          }
        }
      }
    }
    else {
      foreach ($bundles as $b) {
        foreach (['form', 'view'] as $kind) {
          $display = \Drupal::config("core.entity_{$kind}_display.$type.$b.default");
          if ($display->isNew()) {
            $v[] = "core.entity_{$kind}_display.$type.$b.default does not exist";
          }
          elseif ($display->get("content.$name") === NULL || $display->get("hidden.$name") !== NULL) {
            $v[] = "core.entity_{$kind}_display.$type.$b.default does not show $name";
          }
        }
      }
    }
  }
}

if ($v) {
  echo implode(PHP_EOL, $v) . PHP_EOL;
  throw new \RuntimeException(count($v) . ' violation(s)');
}
```

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
