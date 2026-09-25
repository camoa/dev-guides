---
# Routing block — an orchestrator reads to here and decides.
name: configure_pathauto_alias_pattern
capability: pathauto-alias-pattern-configuration
description: Use when a single bundle or vocabulary just needs a clean URL-alias pattern via Pathauto — composing the token pattern, scoping it to the bundle with a selection-criteria condition, and generating aliases. Not for a full SEO build; see the SEO foundation recipe for the metatag/schema/sitemap layers.
# Metadata — read only after a match.
label: Configure Pathauto alias pattern
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/seo-geo/pathauto-patterns
drupal_compatibility: "^10.4 || ^11"
requires_modules:
  - pathauto
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Provision a Pathauto URL-alias pattern (`pathauto.pattern.{id}`) for one bundle or vocabulary — a correct token pattern, scoped to the target with a selection-criteria bundle condition carrying the right `context_mapping`, then aliases generated for existing content — so the target gets clean, deterministic URLs. This is the **narrow** capability: just the alias pattern, not a full SEO foundation.

## Opinion

**This recipe is scoped to aliases only.** If the task is a whole SEO build (metatags, JSON-LD, sitemap, robots, canonical), route to the `drupal_seo_foundation` recipe, which owns pathauto as one layer of many behind a broader input contract. Reach here when the need is genuinely "just give this bundle a clean URL pattern." Source: guide `drupal/seo-geo/pathauto-patterns`.

**Scope the pattern with a selection-criteria condition, not a bare pattern.** A `pathauto.pattern.{id}` targets an entity type via `type` (e.g. `canonical_entities:node`) and is restricted to specific bundles by an `entity_bundle` condition under `selection_criteria`. That condition MUST carry `context_mapping` (`node: node`) — omitting it raises a ContextException at generation time. Source: guide `drupal/seo-geo/pathauto-patterns`.

**Build the token pattern from stable tokens.** Prefer stable, human-meaningful tokens (`[node:title]`, `[term:name]`, a section prefix) over volatile ones; let Pathauto's transliteration and separator settings normalize the result rather than encoding those choices into the pattern. Source: guide `drupal/seo-geo/pathauto-patterns`.

**Pattern weight resolves precedence.** When multiple patterns can match one entity, the lower `weight` wins; set weight deliberately when a bundle-specific pattern must override a catch-all. Source: guide `drupal/seo-geo/pathauto-patterns`.

### What this recipe refuses

- A pattern with a bundle condition missing `context_mapping` (ContextException on generate).
- Re-implementing the SEO foundation's metatag/schema/sitemap layers — out of scope; defer to `drupal_seo_foundation`.
- Silently overwriting an existing differing pattern for the same target.

## Preconditions

- Drupal 10.4+ or 11.x; the `pathauto` module (with `path`/`token`).
- The target bundle or vocabulary exists.
- Config export is in use, so the pattern is deployable.
- DDEV runs the site; the verifier's commands go through `ddev`.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
pattern:
  id: string                   # machine name for the pattern
  label: string
  entity_type: string          # node | taxonomy_term | user | media …
  bundles:                     # bundles/vocabularies the pattern applies to
    - string
  pattern: string              # token pattern, e.g. '/articles/[node:title]'
  weight: integer              # precedence; lower wins (default 0)

generate_existing: boolean     # generate aliases for existing content (default true)
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate the target and tokens.** Confirm the entity type and bundle(s) exist and the tokens in `pattern` are available for that entity type. See `drupal/seo-geo/pathauto-patterns`.

2. **Read existing patterns for the target** — determine absent / present-and-matching / present-and-differing before writing (see the state-awareness contract).

3. **Compose the pattern config** — `pathauto.pattern.{id}` with `type: canonical_entities:{entity_type}`, the `pattern` string, and `weight`.

4. **Scope it with a selection-criteria bundle condition** — an `entity_bundle:{entity_type}` condition listing `bundles`, with `context_mapping` set (e.g. `node: node`). Omitting `context_mapping` is the ContextException trap. See `drupal/seo-geo/pathauto-patterns`.

5. **Import config and generate aliases** — apply the config, then generate aliases for existing content of the target when `generate_existing` is true (Pathauto's bulk-generate for the target entity type).

6. **Export configuration, rebuild caches, and emit a summary** — the pattern created/no-op/conflict, and how many aliases were generated.

## Data flow

```
input: pattern (id, label, entity_type, bundles[], pattern, weight)
       generate_existing

reads project state:
       pathauto.pattern.*        (existing patterns for the target)
       pathauto.settings         (separator, transliterate, max_length …)
       existing bundles/vocabularies + available tokens

applies opinion (guardrails):
       aliases-only-scope · condition-with-context_mapping ·
       stable-tokens · weight-resolves-precedence

references atomic detail (guides):
       drupal/seo-geo/pathauto-patterns

emits:
       pathauto.pattern.<id>     (type, pattern, weight,
                                  selection_criteria: entity_bundle + context_mapping)
       url_alias entries         (generated for existing content)
```

## State-awareness contract

The recipe reads existing state before writing. For the pattern config: absent → create; present and matching the resolved spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review.

Alias generation respects Pathauto's `update_action` setting (leave existing aliases vs regenerate) — the recipe does not force-overwrite hand-crafted aliases unless the caller opts in. Generating aliases for existing content is safe to repeat; a second run over unchanged content and settings produces no new aliases.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/configure-pathauto-alias-pattern/verify.php` run the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: pattern-config
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/configure-pathauto-alias-pattern/verify.php -- pattern {pattern.id} {pattern.entity_type} {pattern.pattern} {pattern.weight:json}
    pass: stdout empty
  - id: bundle-condition
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/configure-pathauto-alias-pattern/verify.php -- condition {pattern.id} {pattern.entity_type} {pattern.bundles}
    pass: stdout empty
  - id: fixture-gets-this-pattern
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/configure-pathauto-alias-pattern/verify.php -- fixture {pattern.id} {pattern.entity_type} {pattern.bundles}
    pass: stdout empty
  - id: existing-content-aliased
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/configure-pathauto-alias-pattern/verify.php -- existing {pattern.id} {pattern.entity_type} {pattern.bundles} {generate_existing:json}
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the proof is:

- `bundle-condition`, `fixture-gets-this-pattern` and `existing-content-aliased` run once per bundle in `pattern.bundles`. An empty list reads unknown, not pass.
- `pattern-config` reads an absent `weight` as 0, its default.
- `fixture-gets-this-pattern` saves one entity of the bundle and checks two things: Pathauto picks this pattern for it, and an alias was written. Then it deletes the entity, which deletes the alias. It checks no exact alias string, because the transliteration and separator settings shape it.
- `bundle-condition` checks nothing for an entity type with no bundle key, such as `user`. Core derives an `entity_bundle` condition only for entity types that have one, so such a pattern has no condition to hold.
- A bundle condition without `context_mapping` makes Pathauto log a ContextException and skip the pattern, and bulk generation still exits 0. `bundle-condition` names the missing mapping, and the fixture gets no alias from this pattern.
- The fixture sets the label and bundle and nothing else. A bundle that cannot save that way, such as a media type that needs a source file, fails the entry rather than passing it.
- `existing-content-aliased` reads content, not config, and names up to 20 entities of the bundle with no alias. It skips an entity whose automatic-alias box is off, because bulk generation skips it too. An absent `generate_existing` counts as true, its default. When it is false, the entry checks nothing.
- `existing-content-aliased` looks for aliases under the entity type's canonical prefix, such as `/taxonomy/term/`. Pathauto aliases forum vocabulary terms under its `/forum/` prefix instead, so the entry reports aliased forum terms as missing and fails closed. Pathauto's own bulk update for terms has the same limit. A pattern with more `selection_criteria` than the bundle, such as a language, makes the entry report entities the pattern never applies to, and it fails closed too.
- `active-equals-export` proves the export is current after Sequence step 6. The state-awareness contract makes a second apply a no-op on that state.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. Drush runs it with Drupal booted and passes the words after `--` in `$extra`.

```php .aida/configure-pathauto-alias-pattern/verify.php
<?php

// Verifier checks for configure-pathauto-alias-pattern.
// $extra: <check> <pattern id> <entity type> <check arguments...>
//   existing takes <bundle> <generate_existing JSON>.
// Prints one line per violation, then throws so Drush exits non-zero.
[$check, $id, $type] = array_pad($extra, 3, '');
$arg = $extra[3] ?? '';
$v = [];

if (!in_array($check, ['pattern', 'condition', 'fixture', 'existing'], TRUE)) {
  throw new \InvalidArgumentException("unknown check '$check'");
}
if ($id === '' || $type === '' || $arg === '') {
  $v[] = "$check: the pattern id, entity type or " . ($check === 'pattern' ? 'pattern' : 'bundle') . ' argument is missing';
}
elseif (\Drupal::config("pathauto.pattern.$id")->isNew()) {
  $v[] = "pathauto.pattern.$id does not exist";
}
elseif ($check === 'pattern') {
  $config = \Drupal::config("pathauto.pattern.$id");
  $weight = json_decode($extra[4] ?? 'null', TRUE, 512, JSON_THROW_ON_ERROR) ?? 0;
  if ($config->get('type') !== "canonical_entities:$type") {
    $v[] = "pathauto.pattern.$id has type '" . $config->get('type') . "', not 'canonical_entities:$type'";
  }
  if ($config->get('pattern') !== $arg) {
    $v[] = "pathauto.pattern.$id has pattern '" . $config->get('pattern') . "', not '$arg'";
  }
  if ((int) $config->get('weight') !== (int) $weight) {
    $v[] = "pathauto.pattern.$id has weight " . (int) $config->get('weight') . ", not $weight";
  }
}
elseif ($check === 'existing') {
  if (json_decode($extra[4] ?? 'null', TRUE, 512, JSON_THROW_ON_ERROR) ?? TRUE) {
    $definition = \Drupal::entityTypeManager()->getDefinition($type);
    $prefix = \Drupal::service('plugin.manager.alias_type')->createInstance("canonical_entities:$type")->getSourcePrefix();
    // Bulk generation's create action starts after id 0 and skips an entity whose stored state is SKIP.
    $query = \Drupal::entityTypeManager()->getStorage($type)->getQuery()->accessCheck(FALSE)
      ->condition($definition->getKey('id'), 0, '>');
    if ($definition->getKey('bundle')) {
      $query->condition($definition->getKey('bundle'), $arg);
    }
    $alias_storage = \Drupal::entityTypeManager()->getStorage('path_alias');
    $missing = [];
    foreach (array_chunk(array_values($query->execute()), 500) as $chunk) {
      $skipped = array_keys(array_filter(
        \Drupal::keyValue("pathauto_state.$type")->getMultiple($chunk),
        fn ($state) => (int) $state === \Drupal\pathauto\PathautoState::SKIP,
      ));
      $paths = [];
      foreach (array_diff($chunk, $skipped) as $entity_id) {
        $paths[$entity_id] = $prefix . $entity_id;
      }
      $aliased = [];
      if ($paths) {
        $alias_ids = $alias_storage->getQuery()->accessCheck(FALSE)->condition('path', array_values($paths), 'IN')->execute();
        foreach ($alias_storage->loadMultiple($alias_ids) as $alias) {
          $aliased[] = $alias->getPath();
        }
      }
      $missing = array_merge($missing, array_keys(array_diff($paths, $aliased)));
    }
    if ($missing) {
      $v[] = count($missing) . " $type of bundle $arg have no alias, including " . implode(',', array_slice($missing, 0, 20));
    }
  }
}
elseif ($check === 'condition' && !\Drupal::entityTypeManager()->getDefinition($type)->getKey('bundle')) {
  // Core derives entity_bundle:* only for entity types with a bundle key.
}
elseif ($check === 'condition') {
  $listed = FALSE;
  foreach (\Drupal::config("pathauto.pattern.$id")->get('selection_criteria') ?? [] as $condition) {
    if (($condition['id'] ?? '') === "entity_bundle:$type" && in_array($arg, $condition['bundles'] ?? [], TRUE)) {
      $listed = TRUE;
      if (empty($condition['context_mapping'])) {
        $v[] = "pathauto.pattern.$id: the entity_bundle:$type condition listing $arg has no context_mapping";
      }
    }
  }
  if (!$listed) {
    $v[] = "pathauto.pattern.$id has no entity_bundle:$type condition listing $arg";
  }
}
else {
  $definition = \Drupal::entityTypeManager()->getDefinition($type);
  // User declares no label entity key; its label field is name.
  $label_key = $definition->getKey('label') ?: ($type === 'user' ? 'name' : '');
  $values = $label_key === '' ? [] : [$label_key => 'aida verify fixture'];
  if ($definition->getKey('bundle')) {
    $values[$definition->getKey('bundle')] = $arg;
  }
  $entity = \Drupal::entityTypeManager()->getStorage($type)->create($values);
  try {
    $entity->save();
    $picked = \Drupal::service('pathauto.generator')->getPatternByEntity($entity);
    if ($picked?->id() !== $id) {
      $v[] = "a new $type of bundle $arg gets pattern '" . ($picked?->id() ?? 'none') . "', not '$id'";
    }
    $path = '/' . $entity->toUrl()->getInternalPath();
    if (!\Drupal::entityTypeManager()->getStorage('path_alias')->loadByProperties(['path' => $path])) {
      $v[] = "a new $type of bundle $arg got no alias for $path";
    }
  }
  finally {
    if (!$entity->isNew()) {
      $entity->delete();
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
| `drupal/seo-geo/pathauto-patterns` | Token pattern syntax, per-bundle scoping, bulk generation, transliteration, and the `context_mapping` trap |

### Related recipes

- `drupal_seo_foundation` — the full SEO build (metatag, JSON-LD, sitemap, robots, canonical); owns pathauto as one layer. Use it instead of this recipe when the need is a whole SEO foundation, not a single alias pattern.
