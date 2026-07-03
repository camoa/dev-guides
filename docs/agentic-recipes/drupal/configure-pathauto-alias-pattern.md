---
# Routing block — an orchestrator reads to here and decides.
name: configure_pathauto_alias_pattern
capability: pathauto-alias-pattern-configuration
description: Use when a single bundle or vocabulary just needs a clean URL-alias pattern via Pathauto — composing the token pattern, scoping it to the bundle with a selection-criteria condition, and generating aliases. Not for a full SEO build; see the SEO foundation recipe for the metatag/schema/sitemap layers.
# Metadata — read only after a match.
label: Configure Pathauto alias pattern
recipe_schema_version: 1.0.0
version: 0.1.0
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

6. **Rebuild caches and emit a summary** — the pattern created/no-op/conflict, and how many aliases were generated.

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

After the recipe runs, verify:

1. `pathauto.pattern.{id}` exists with the expected `type`, `pattern`, and `weight`.
2. Its `selection_criteria` carries an `entity_bundle` condition listing the target bundle(s) **with** `context_mapping` set.
3. A sample entity of the target bundle resolves to an alias matching the pattern (e.g. an Article titled "Hello World" gets `/articles/hello-world`).
4. Running Pathauto's bulk-generate in update mode raises no ContextException.
5. A second apply produces no config changes (idempotent).

The recipe ships no verifier *script*, but every check is **agent-runnable**. Checks 1–2 and 5 are `config-assert` (drush + config reads). Checks 3–4 are `live-site` — they require a served site with at least one entity of the bundle to confirm the alias actually resolves; on a config-only environment they are reported as fail-closed (not silently skipped), per the runnability contract.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/seo-geo/pathauto-patterns` | Token pattern syntax, per-bundle scoping, bulk generation, transliteration, and the `context_mapping` trap |

### Related recipes

- `drupal_seo_foundation` — the full SEO build (metatag, JSON-LD, sitemap, robots, canonical); owns pathauto as one layer. Use it instead of this recipe when the need is a whole SEO foundation, not a single alias pattern.
