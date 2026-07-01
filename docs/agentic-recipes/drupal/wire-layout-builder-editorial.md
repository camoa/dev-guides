---
# Routing block — an orchestrator reads to here and decides.
name: wire_layout_builder_editorial
capability: layout-builder-editorial-wiring
description: Use when a content type must be handed to content editors to compose pages in Layout Builder — enabling LB on the bundle, curating the block/layout/style palette, modeling repeating sections without Paragraphs, and hardening the editor UX so contextual editing works and page consistency holds.
# Metadata — read only after a match.
label: Wire Layout Builder for editorial use
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/layout-builder/enabling-lb
  - drupal/layout-builder/defaults-vs-overrides
  - drupal/layout-builder/inline-vs-reusable
  - drupal/layout-builder/field-extra-field-blocks
  - drupal/layout-builder/block-placement
  - drupal/layout-builder/sections-layouts
  - drupal/layout-builder/block-content-list-components
  - drupal/layout-builder/lb-restrictions
  - drupal/layout-builder/lb-styles-overview
  - drupal/layout-builder/lb-styles-groups
  - drupal/layout-builder/theming-lb
  - drupal/layout-builder/editor-form-display-hardening
drupal_compatibility: "^10.4 || ^11"
requires_modules:
  - layout_builder
  - block_content
optional_modules:
  - layout_builder_restrictions
  - layout_builder_styles
invokes_drupal_recipes: []
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Provision Layout Builder on a content type so content editors compose visually consistent pages from an approved palette — with contextual editing working end-to-end, repeating sections modeled without Paragraphs, no path for an editor to break page consistency, and the entire editorial capability living in **exported configuration**, not only in the database.

## Opinion

**Choose an editorial posture; never default to open.** `allow_custom` is not a bare on/off — combined with restrictions and styles it is a deliberate posture: *locked* (templated, `allow_custom: false`), *curated* (approved palette), or *open* (full freedom, rare). Pick one per bundle before enabling anything. Source: guide `drupal/layout-builder/defaults-vs-overrides`.

**Curate the palette; never hand editors raw Layout Builder.** A curated posture means an explicit allowlist of blocks and layouts, so editors compose from an approved set rather than the full plugin surface. Source: guide `drupal/layout-builder/lb-restrictions`.

**Editors get styles, not CSS.** Visual variation is expressed as Layout Builder Styles groups tied to design-token classes, so editors select approved options instead of writing markup. Source: guides `drupal/layout-builder/lb-styles-overview`, `drupal/layout-builder/lb-styles-groups`.

**Model repeating sections as block_content + taxonomy + Views — never Paragraphs.** Lists (testimonials, gallery, logos) are atomic `block_content` items grouped by a taxonomy reference and listed by a View of block_content. Source: guide `drupal/layout-builder/block-content-list-components`.

**Group by authoring intent, not by element.** Components that share authoring intent and section-level styling (heading + body + CTA) belong in **one** section, not three sibling sections. Source: guide `drupal/layout-builder/sections-layouts`.

**Every inline-block template must render its own attributes.** A block template used in Layout Builder that omits `{{ attributes }}` or `{{ title_suffix }}` silently breaks the contextual edit pencil and the Configure menu. Source: guide `drupal/layout-builder/theming-lb`.

**The capability ships in config, not the database.** Permissions, restrictions, styles, and the view display that carry the editorial capability must be in the exported configuration — a capability that works locally but was never exported does not survive deploy. Source: guides `drupal/layout-builder/enabling-lb`, `drupal/layout-builder/defaults-vs-overrides`.

### What this recipe refuses

- Paragraphs as the list-section modeling tool under Layout Builder.
- Any inline-block / block_content template used in LB that omits `{{ attributes }}` or `{{ title_suffix }}`.
- Granting an editor role Layout Builder access without a restriction allowlist (any non-*open* posture).
- Emitting three sibling sections for a component group that shares section-level styling.
- Leaving the editorial capability (perms, restrictions, styles) only in the database, unexported.

## Preconditions

- Drupal 10.4+ or 11.x; `layout_builder` and `block_content` enabled.
- For any *curated* or *locked* posture: `layout_builder_restrictions` and `layout_builder_styles` available (the palette and style groups depend on them). See `drupal/layout-builder/lb-restrictions`.
- The target content-type bundle exists, with its `Manage display` view mode available.
- The editor role to enable exists.
- Config export is in use (the capability must be exportable — see the state-awareness contract).

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
target:
  entity_type: string        # e.g. node
  bundle: string             # the content type
  view_mode: string          # default: "default"

editorial_posture: string    # "locked" | "curated" | "open"  (default: curated)
editor_role: string          # machine name of the role to enable

block_palette:               # allowlisted blocks (curated/locked); omit for open
  - string                   #   plugin id or category
layout_palette:              # allowlisted layouts (curated/locked)
  - string

style_palette:               # Layout Builder Styles to expose to editors
  - group: string            #   style group machine name
    styles: [string]

list_components:             # repeating sections modeled without Paragraphs
  - block_bundle: string     #   block_content bundle for the item
    group_field: string      #   taxonomy-term reference field used to filter
    view: string             #   View of block_content that lists the items
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate preconditions and resolve the posture.** Confirm modules and the target bundle. Map `editorial_posture` to its `allow_custom` value and restriction strategy: *locked* → `allow_custom: false`; *curated* → `allow_custom: true` + allowlist; *open* → `allow_custom: true`, no allowlist. See `drupal/layout-builder/enabling-lb`, `drupal/layout-builder/defaults-vs-overrides`.

2. **Enable Layout Builder on the bundle view display** with the resolved `allow_custom`. See `drupal/layout-builder/enabling-lb`.

3. **Model the list components.** For each entry in `list_components`, ensure its `block_content` bundle, its taxonomy-term grouping field, and the View of block_content that lists it — including per-category fixed-argument displays where a single placement must render one category. No Paragraphs. See `drupal/layout-builder/block-content-list-components` and `drupal/layout-builder/field-extra-field-blocks`.

4. **Curate the palette.** For non-*open* postures, apply the `layout_builder_restrictions` allowlist for `block_palette` and `layout_palette` on the view display. See `drupal/layout-builder/lb-restrictions`.

5. **Expose the style palette.** Wire the `style_palette` groups/styles as the Layout Builder Styles editors may apply. See `drupal/layout-builder/lb-styles-overview`, `drupal/layout-builder/lb-styles-groups`.

6. **Ensure render theming.** Where list components render as View rows, ensure the block_content render theme-hook trio is registered; ensure every inline-block template used in LB emits `{{ attributes }}` and `{{ title_suffix }}`. See `drupal/layout-builder/block-content-list-components`, `drupal/layout-builder/theming-lb`.

7. **Harden the editor form display.** Use the Media Library widget for media fields, hide legacy/raw fields, and add field descriptions on the bundle (and on any block_content bundle used inline). See `drupal/layout-builder/editor-form-display-hardening`.

8. **Grant the editor role its permissions.** For a scoped posture, prefer the per-bundle `configure editable <entity_type> <bundle> layout overrides` permission over `configure any layout`; always include `create and edit custom blocks` when inline blocks are in play. See `drupal/layout-builder/enabling-lb`.

9. **Export and confirm the capability is in config.** Export configuration and confirm the role permissions, restriction allowlist, style groups, and view-display settings are all present in the export — not only in the database.

10. **Rebuild caches and emit a summary** of what was created, skipped as a no-op, or surfaced as a conflict for operator review.

## Data flow

```
input: target (entity_type, bundle, view_mode)
       editorial_posture · editor_role
       block_palette · layout_palette · style_palette · list_components

reads project state:
       core.entity_view_display.<entity>.<bundle>.<view_mode>  (LB + restrictions + styles)
       user.role.<editor_role>                                 (permissions)
       block_content.type.* / field.* / views.view.*           (list components)
       layout_builder_styles.style.* / .group.*                (style palette)
       core.entity_form_display.*                              (editor form hardening)
       theme templates + hooks                                 (render theming)

applies opinion (guardrails):
       posture-first · curate-don't-open · styles-not-CSS ·
       block_content-not-Paragraphs · group-by-intent ·
       templates-emit-attributes · capability-in-config

references atomic detail (guides):
       drupal/layout-builder/{ enabling-lb, defaults-vs-overrides,
         inline-vs-reusable, field-extra-field-blocks, block-placement,
         sections-layouts, block-content-list-components, lb-restrictions,
         lb-styles-overview, lb-styles-groups, theming-lb,
         editor-form-display-hardening }

emits:
       core.entity_view_display ... layout_builder.enabled + allow_custom
         + third_party_settings.layout_builder_restrictions (allowlist)
       user.role.<editor_role>            (LB permission set)
       block_content.type.* / field.* / views.view.*  (list components)
       layout_builder_styles exposure     (style palette)
       core.entity_form_display.*         (hardened editor form)
       theme: block_content render trio + attribute-emitting inline templates
```

## State-awareness contract

The recipe reads existing state before writing. For every emitted config object: absent → create; present and matching the resolved spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review.

The capability must be present in **exported configuration**, not only the active (database) state. A permission, restriction, or style that exists in the running site but not in the export is treated as a conflict to resolve (export it), because it will not survive deploy — this is the difference between "works on my install" and a delivered capability.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

After the recipe runs, verify:

1. Layout Builder is enabled on the target bundle view display with the posture's `allow_custom` value.
2. For a *curated* or *locked* posture, the restriction allowlist is present in `third_party_settings.layout_builder_restrictions` on that view display and matches `block_palette` / `layout_palette`.
3. The editor role carries the resolved permission set — including `create and edit custom blocks` where inline blocks are used — and those permissions are present in **exported** config, not only the database.
4. The exposed Layout Builder Styles groups/styles match `style_palette`.
5. Each `list_components` entry has its `block_content` bundle, its taxonomy grouping field, and its listing View — and no Paragraphs type backs any of them.
6. The block_content render theme-hook trio is registered where list components render as View rows, and every inline-block template used in LB emits `{{ attributes }}` and `{{ title_suffix }}`.
7. A page of the target bundle, rendered as the editor role, shows the contextual edit pencil and the Layout Builder "Configure" menu (proving both the attribute-emitting templates and the granted permissions).
8. An editor attempt to place a block or layout outside the allowlist is denied (the restriction holds).

The recipe ships no verifier *script*, but every check above is **agent-runnable** — "ships no script" does not mean "not runnable". Checks 1–6 are `config-assert` (drush + config/template reads, no served site needed); check 6's template check may also run as a `self-fixture` (register a fixture inline block and assert its wrapper attributes). Checks 7 and 8 are `live-site` (render as the editor role and inspect the contextual-edit markup / attempt an out-of-allowlist placement). With **no served site**, checks 7–8 are correctly **fail-closed, not skipped**, per the consumer's verifier contract.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/layout-builder/enabling-lb` | Enabling LB on a bundle; the editor permission set |
| `drupal/layout-builder/defaults-vs-overrides` | The `allow_custom` editorial-posture spectrum |
| `drupal/layout-builder/inline-vs-reusable` | Inline vs reusable block_content decision |
| `drupal/layout-builder/field-extra-field-blocks` | Field / extra-field blocks in sections |
| `drupal/layout-builder/block-placement` | Placing and grouping components in a section |
| `drupal/layout-builder/sections-layouts` | Multi-component-per-section grouping rule |
| `drupal/layout-builder/block-content-list-components` | List sections without Paragraphs; fixed-arg Views workaround; block_content render trio |
| `drupal/layout-builder/lb-restrictions` | Restriction allowlist stored on the view display |
| `drupal/layout-builder/lb-styles-overview` | Layout Builder Styles as an editorial design system |
| `drupal/layout-builder/lb-styles-groups` | Style groups and their token classes |
| `drupal/layout-builder/theming-lb` | Inline-block templates must emit `{{ attributes }}` / `{{ title_suffix }}` |
| `drupal/layout-builder/editor-form-display-hardening` | Media Library widget, hiding legacy fields, field descriptions |
