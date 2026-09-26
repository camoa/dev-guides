---
# Routing block — an orchestrator reads to here and decides.
name: wire_layout_builder_editorial
capability: layout-builder-editorial-wiring
description: Use when a content type must be handed to content editors to compose pages in Layout Builder — enabling LB on the bundle, curating the block/layout/style palette, modeling repeating sections without Paragraphs, and hardening the editor UX so contextual editing works and page consistency holds.
# Metadata — read only after a match.
label: Wire Layout Builder for editorial use
recipe_schema_version: 1.0.0
version: 0.2.0
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
- When `list_components` is non-empty, a custom module exists, or is created, to hold `hook_block_content_view()`: core invokes entity view hooks for modules only. On Drupal 10 or 11.0 it also needs the `#[LegacyHook]` procedural function and the `services.yml` entry the guide shows. See `drupal/layout-builder/block-content-list-components`.
- Config export is in use (the capability must be exportable — see the state-awareness contract).
- DDEV runs the site; the verifier's commands go through `ddev`.

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

3. **Model the list components.** For each entry in `list_components`, ensure its `block_content` bundle, its taxonomy-term grouping field, and the View of block_content that lists it — including per-category fixed-argument displays where a single placement must render one category. Create a dedicated `block_content` view mode for the rows, such as `list_item`, and select it as the View's row view mode on its default display. No Paragraphs. See `drupal/layout-builder/block-content-list-components` and `drupal/layout-builder/field-extra-field-blocks`.

4. **Curate the palette.** For non-*open* postures, apply the `layout_builder_restrictions` allowlist for `block_palette` and `layout_palette` on the view display. See `drupal/layout-builder/lb-restrictions`.

5. **Expose the style palette.** Wire the `style_palette` groups/styles as the Layout Builder Styles editors may apply. See `drupal/layout-builder/lb-styles-overview`, `drupal/layout-builder/lb-styles-groups`.

6. **Ensure render theming.** Where list components render as View rows, ensure the block_content render theme-hook trio is registered: `hook_theme()` and the bundle suggestions alter in the theme, and `hook_block_content_view()` in a module, since core fires entity view hooks for modules only. Scope that hook to a dedicated `block_content` view mode, such as `list_item`: create the view mode and select it as the row view mode of each `list_components` View, so placed and inline blocks keep their output; ensure every inline-block template used in LB emits `{{ attributes }}` and `{{ title_suffix }}`. See `drupal/layout-builder/block-content-list-components`, `drupal/layout-builder/theming-lb`.

7. **Harden the editor form display.** Use the Media Library widget for media fields, hide legacy/raw fields, and add field descriptions on the bundle (and on any block_content bundle used inline). See `drupal/layout-builder/editor-form-display-hardening`.

8. **Grant the editor role its permissions.** For a scoped posture, prefer the per-bundle `configure editable <bundle> <entity_type> layout overrides` permission over `configure any layout`; always include `create and edit custom blocks` when inline blocks are in play. See `drupal/layout-builder/enabling-lb`.

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
       theme templates + hooks, module block_content_view hook (render theming)

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
       theme: block_content theme hook + suggestions + attribute-emitting inline templates
       core.entity_view_mode.block_content.<row view mode>  (View rows only)
       module: hook_block_content_view setting #theme in the row view mode
```

## State-awareness contract

The recipe reads existing state before writing. For every emitted config object: absent → create; present and matching the resolved spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review.

The capability must be present in **exported configuration**, not only the active (database) state. A permission, restriction, or style that exists in the running site but not in the export is treated as a conflict to resolve (export it), because it will not survive deploy — this is the difference between "works on my install" and a delivered capability.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/wire-layout-builder-editorial/verify.php` run the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: lb-enabled-with-posture
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- display {target.entity_type} {target.bundle} {target.view_mode:json} {editorial_posture:json}
    pass: stdout empty
  - id: restriction-allowlist
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- restrictions {target.entity_type} {target.bundle} {target.view_mode:json} {editorial_posture:json} {layout_palette:json}
    pass: stdout empty
  - id: allowlist-denies
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- offered {target.entity_type} {target.bundle} {target.view_mode:json} {editorial_posture:json} {block_palette:json}
    pass: stdout empty
  - id: editor-permissions
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- permissions {editor_role} {target.entity_type} {target.bundle} {editorial_posture:json} {block_palette:json}
    pass: stdout empty
  - id: editor-can-edit-layout
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- editor-access {editor_role} {target.entity_type} {target.bundle} {editorial_posture:json} {target.view_mode:json}
    pass: stdout empty
  - id: style-palette
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- styles {style_palette:json}
    pass: stdout empty
  - id: list-components
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- lists {list_components:json}
    pass: stdout empty
  - id: block-content-theme-hook
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- trio {list_components:json}
    pass: stdout empty
  - id: templates-emit-attributes
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/wire-layout-builder-editorial/verify.php -- templates
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the proof is:

- An absent `editorial_posture` reads as `curated`, and an absent `target.view_mode` as `default`, the Input contract defaults.
- `lb-enabled-with-posture` also checks the `layout_builder__layout` field storage and instance for a *curated* or *open* posture. Core adds that field when overrides are allowed.
- `restriction-allowlist` and `allowlist-denies` check nothing for an *open* posture. For the others, `restriction-allowlist` compares `allowed_layouts` with `layout_palette`. `allowlist-denies` asks core's block plugin manager which blocks the Layout Builder chooser offers on the default layout, with `layout_builder_restrictions` filtering them. It adds the inline blocks the module's restriction plugins allow in that region, as the module's inline block list does. Every offered block must match a `block_palette` entry by plugin id, base plugin id or untranslated category, and every entry must match an offered block. It builds Layout Builder's sample entity for the bundle and deletes it afterwards.
- `editor-permissions` requires, for a *curated* or *open* posture, one of `configure editable <bundle> <entity_type> layout overrides`, `configure all <bundle> <entity_type> layout overrides` or `configure any layout`, the three that core's overrides access check accepts. Core generates the per-bundle two only for a display that allows overrides, so a *locked* posture has none to hold. It requires `create and edit custom blocks` when the posture is *open* or `block_palette` names an `inline_block` plugin or the `Inline blocks` category.
- The contextual pencil and the "Configure" menu are drawn in the browser by the contextual module's JavaScript, so no command sees them. `editor-can-edit-layout` stands in for the permission half: it saves a user with `editor_role` and an entity of the bundle that user owns, then asks the overrides section storage for `view` access, the check the layout route runs. Access must be granted for *curated* and *open* and denied for *locked*. Both fixtures are deleted. The "editable" permission also needs the role's own update access to the entity, so a role without it fails the entry.
- `templates-emit-attributes` stands in for the template half. It renders a block through the default theme for each `block_content` bundle, once as an inline block and once as a reusable `block_content` block, as a user who may see contextual links. The block's content is the view builder's `full` build of an unsaved block of that bundle, so core's `#block_content` suggestions, such as `block__block_content__type__<bundle>`, pick the template. Nothing is saved. The block's attributes carry a probe attribute and core's contextual module adds its placeholder to `title_suffix`, so the markup shows whether the template that won prints each one. Rendering follows `include`, `extends` and `embed`, and aliases such as `{% set block_attributes = attributes %}`, which a text search of the template misses. A template that prints only on some condition the probe does not meet, such as a label, is not caught.
- `style-palette` checks each listed group and style exists, and each style belongs to its group. Layout Builder Styles are site-wide, so styles outside the palette are not flagged. An absent or empty `style_palette` checks nothing.
- `list-components` checks the `block_content` bundle, a taxonomy-term reference field on it, and a View whose base table is `block_content_field_data`, so no Paragraphs type backs the list. An absent or empty `list_components` checks nothing, and so does `block-content-theme-hook`.
- `block-content-theme-hook` checks two of the three hooks: a `block_content` theme hook is registered, and an unsaved `block_content` of each listed bundle builds with `#theme` set to `block_content`. It reads the row of the entry's `view` from its default display. The entry fails when that View does not exist, when that row's type is not `entity:block_content`, when its view mode is `default` or `full`, which placed and inline blocks also build in, or when `core.entity_view_mode.block_content.<mode>` does not exist. A View whose row is overridden on a non-default display (`defaults.row: false`) fails the entry, because the check reads the default display, which is where Sequence step 3 sets it. Otherwise it builds in that view mode. The second is not implied by the first: core's `BlockContentViewBuilder` removes the `#theme` its parent sets, so only the second hook puts it back. The bundle suggestions from the third hook are not checked.
- `active-equals-export` proves the permissions, restrictions, styles and display are in the export after Sequence step 9, not only in the database.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. Drush runs it with Drupal booted and passes the words after `--` in `$extra`.

```php .aida/wire-layout-builder-editorial/verify.php
<?php

// Verifier checks for wire-layout-builder-editorial.
// $extra: <check> <check arguments...>; JSON arguments are null when absent.
// Prints one line per violation, then throws so Drush exits non-zero.
$check = $extra[0] ?? '';
$arg = array_slice(array_pad($extra, 6, ''), 1);
$v = [];
$json = fn (string $s) => json_decode($s === '' ? 'null' : $s, TRUE, 512, JSON_THROW_ON_ERROR);
$etm = \Drupal::entityTypeManager();

switch ($check) {
  case 'display':
  case 'restrictions':
  case 'offered':
    [$type, $bundle] = $arg;
    $mode = $json($arg[2]) ?? 'default';
    $posture = $json($arg[3]) ?? 'curated';
    $name = "core.entity_view_display.$type.$bundle.$mode";
    $display = \Drupal::config($name);
    if ($type === '' || $bundle === '') {
      $v[] = "$check: the entity type or bundle argument is missing";
    }
    elseif (!in_array($posture, ['locked', 'curated', 'open'], TRUE)) {
      $v[] = "$check: editorial_posture '$posture' is not locked, curated or open";
    }
    elseif ($display->isNew()) {
      $v[] = "$name does not exist";
    }
    elseif ($check === 'display') {
      if ($display->get('third_party_settings.layout_builder.enabled') !== TRUE) {
        $v[] = "$name does not have Layout Builder enabled";
      }
      if ((bool) $display->get('third_party_settings.layout_builder.allow_custom') !== ($posture !== 'locked')) {
        $v[] = "$name has allow_custom " . var_export((bool) $display->get('third_party_settings.layout_builder.allow_custom'), TRUE) . " for a $posture posture";
      }
      if ($posture !== 'locked') {
        foreach (["field.storage.$type.layout_builder__layout", "field.field.$type.$bundle.layout_builder__layout"] as $field) {
          if (\Drupal::config($field)->isNew()) {
            $v[] = "$field does not exist, so the bundle has no layout override field";
          }
        }
      }
    }
    elseif ($posture === 'open') {
      // An open posture carries no allowlist.
    }
    elseif (!\Drupal::moduleHandler()->moduleExists('layout_builder_restrictions')) {
      $v[] = "layout_builder_restrictions is not enabled for a $posture posture";
    }
    elseif ($check === 'restrictions') {
      $palette = $json($arg[4]) ?? [];
      $allowed = $display->get('third_party_settings.layout_builder_restrictions.entity_view_mode_restriction.allowed_layouts') ?? [];
      if (!$display->get('third_party_settings.layout_builder_restrictions.entity_view_mode_restriction')) {
        $v[] = "$name has no layout_builder_restrictions entity_view_mode_restriction";
      }
      if (!$palette) {
        $v[] = "restrictions: layout_palette is absent or empty for a $posture posture";
      }
      foreach (array_diff($palette, $allowed) as $layout) {
        $v[] = "$name does not allow layout $layout from layout_palette";
      }
      foreach (array_diff($allowed, $palette) as $layout) {
        $v[] = "$name allows layout $layout, which is not in layout_palette";
      }
    }
    else {
      $palette = $json($arg[4]) ?? [];
      if (!$palette) {
        $v[] = "offered: block_palette is absent or empty for a $posture posture";
        break;
      }
      $entity_display = $etm->getStorage('entity_view_display')->load("$type.$bundle.$mode");
      $storage = \Drupal::service('plugin.manager.layout_builder.section_storage')->load('defaults', ['display' => \Drupal\Core\Plugin\Context\EntityContext::fromEntity($entity_display)]);
      if (!$storage) {
        $v[] = "$name has no defaults section storage";
        break;
      }
      $repository = \Drupal::service('context.repository');
      $contexts = array_filter($repository->getRuntimeContexts(array_keys($repository->getAvailableContexts())), fn ($context) => $context->hasContextValue());
      try {
        $contexts += $storage->getContextsDuringPreview();
        $blocks = \Drupal::service('plugin.manager.block');
        $filter = ['section_storage' => $storage, 'delta' => 0, 'region' => 'content'];
        $offered = $blocks->getFilteredDefinitions('layout_builder', $contexts, $filter);
        // With 'list' set, layout_builder_restrictions skips its filter and core
        // returns every block, so keep the inline blocks and filter them as the
        // module's ChooseBlockController::inlineBlockList() does.
        $inline = array_filter($blocks->getFilteredDefinitions('layout_builder', $contexts, $filter + ['list' => 'inline_blocks']), fn ($id) => str_starts_with($id, 'inline_block'), ARRAY_FILTER_USE_KEY);
        $restrictions = \Drupal::service('plugin.manager.layout_builder_restriction');
        foreach (array_keys($restrictions->getSortedPlugins()) as $restriction_id) {
          $inline = array_intersect_key($inline, array_flip($restrictions->createInstance($restriction_id)->inlineBlocksAllowedinContext($storage, 0, 'content')));
        }
        $offered += $inline;
        $matched = [];
        foreach ($offered as $id => $definition) {
          $category = $definition['category'] ?? '';
          $category = $category instanceof \Drupal\Core\StringTranslation\TranslatableMarkup ? $category->getUntranslatedString() : (string) $category;
          $hits = array_intersect($palette, [$id, $definition['id'] ?? $id, $category]);
          if (!$hits) {
            $v[] = "the Layout Builder chooser for $name offers block $id ($category), which is not in block_palette";
          }
          $matched += array_flip($hits);
        }
        foreach (array_diff($palette, array_keys($matched)) as $entry) {
          $v[] = "the Layout Builder chooser for $name offers nothing matching block_palette entry $entry";
        }
      }
      finally {
        \Drupal::service('layout_builder.sample_entity_generator')->delete($type, $bundle);
      }
    }
    break;

  case 'permissions':
  case 'editor-access':
    [$role, $type, $bundle] = $arg;
    $posture = $json($arg[3]) ?? 'curated';
    $role_config = \Drupal::config("user.role.$role");
    if ($role === '' || $type === '' || $bundle === '') {
      $v[] = "$check: the role, entity type or bundle argument is missing";
    }
    elseif (!in_array($posture, ['locked', 'curated', 'open'], TRUE)) {
      $v[] = "$check: editorial_posture '$posture' is not locked, curated or open";
    }
    elseif ($role_config->isNew()) {
      $v[] = "user.role.$role does not exist";
    }
    elseif ($check === 'permissions') {
      $palette = $json($arg[4]) ?? [];
      $inline = $posture === 'open' || in_array('Inline blocks', $palette, TRUE)
        || array_filter($palette, fn ($entry) => str_starts_with($entry, 'inline_block'));
      // Each entry is a set of permissions, any one of which satisfies it.
      $needed = [];
      if ($posture !== 'locked') {
        $needed[] = ["configure editable $bundle $type layout overrides", "configure all $bundle $type layout overrides", 'configure any layout'];
        if ($inline) {
          $needed[] = ['create and edit custom blocks'];
        }
      }
      foreach ($needed as $permissions) {
        if (!$role_config->get('is_admin') && !array_intersect($permissions, $role_config->get('permissions') ?? [])) {
          $v[] = "user.role.$role lacks the permission '" . implode("' or '", $permissions) . "'";
        }
      }
    }
    else {
      $mode = $json($arg[4]) ?? 'default';
      $definition = $etm->getDefinition($type);
      $account = $etm->getStorage('user')->create([
        'name' => 'aida_verify_' . bin2hex(random_bytes(4)),
        'status' => 1,
        'roles' => [$role],
      ]);
      $values = [$definition->getKey('label') => 'aida verify fixture'];
      if ($definition->getKey('bundle')) {
        $values[$definition->getKey('bundle')] = $bundle;
      }
      $entity = $etm->getStorage($type)->create($values);
      try {
        $account->save();
        if ($entity instanceof \Drupal\user\EntityOwnerInterface) {
          $entity->setOwnerId($account->id());
        }
        $entity->save();
        $storage = \Drupal::service('plugin.manager.layout_builder.section_storage')->load('overrides', [
          'entity' => \Drupal\Core\Plugin\Context\EntityContext::fromEntity($entity),
          'view_mode' => new \Drupal\Core\Plugin\Context\Context(new \Drupal\Core\Plugin\Context\ContextDefinition('string'), $mode),
        ]);
        $allowed = $storage && $storage->access('view', $account);
        if ($posture !== 'locked' && !$allowed) {
          $v[] = "a user with role $role cannot edit the layout of a $type of bundle $bundle they own";
        }
        if ($posture === 'locked' && $allowed) {
          $v[] = "a user with role $role can edit the layout of a $type of bundle $bundle under a locked posture";
        }
      }
      finally {
        if (!$entity->isNew()) {
          $entity->delete();
        }
        if (!$account->isNew()) {
          $account->delete();
        }
      }
    }
    break;

  case 'styles':
    $palette = $json($arg[0]) ?? [];
    if ($palette && !\Drupal::moduleHandler()->moduleExists('layout_builder_styles')) {
      $v[] = 'layout_builder_styles is not enabled, but style_palette lists styles';
      break;
    }
    foreach ($palette as $i => $group) {
      $group_id = $group['group'] ?? '';
      if ($group_id === '' || \Drupal::config("layout_builder_styles.group.$group_id")->isNew()) {
        $v[] = "style_palette[$i]: style group '$group_id' does not exist";
      }
      foreach ($group['styles'] ?? [] as $style) {
        $style_config = \Drupal::config("layout_builder_styles.style.$style");
        if ($style_config->isNew()) {
          $v[] = "layout_builder_styles.style.$style does not exist";
        }
        elseif ($style_config->get('group') !== $group_id) {
          $v[] = "layout_builder_styles.style.$style is in group '" . $style_config->get('group') . "', not '$group_id'";
        }
      }
    }
    break;

  case 'lists':
  case 'trio':
    $components = $json($arg[0]) ?? [];
    if ($check === 'trio' && $components && !isset(\Drupal::service('theme.registry')->get()['block_content'])) {
      $v[] = 'no block_content theme hook is registered, so block_content rendered as a View row has no template';
    }
    foreach ($components as $i => $component) {
      $block_bundle = $component['block_bundle'] ?? '';
      $group_field = $component['group_field'] ?? '';
      $view = $component['view'] ?? '';
      if ($block_bundle === '' || \Drupal::config("block_content.type.$block_bundle")->isNew()) {
        $v[] = "list_components[$i]: block_content type '$block_bundle' does not exist";
        continue;
      }
      if ($check === 'trio') {
        if ($view === '' || \Drupal::config("views.view.$view")->isNew()) {
          $v[] = "list_components[$i]: views.view.$view does not exist";
          continue;
        }
        $displays = \Drupal::config("views.view.$view")->get('display') ?? [];
        foreach ($displays as $display_id => $display) {
          if ($display_id !== 'default' && ($display['display_options']['defaults']['row'] ?? TRUE) === FALSE) {
            $v[] = "list_components[$i]: views.view.$view overrides the row on display $display_id; set it on the default display only";
          }
        }
        $row = $displays['default']['display_options']['row'] ?? [];
        if (($row['type'] ?? NULL) !== 'entity:block_content') {
          $v[] = "list_components[$i]: views.view.$view's default display row is not entity:block_content";
          continue;
        }
        $row_mode = $row['options']['view_mode'] ?? NULL;
        if (!is_string($row_mode) || $row_mode === '') {
          $v[] = "list_components[$i]: views.view.$view has no row view mode on its default display";
          continue;
        }
        if (in_array($row_mode, ['default', 'full'], TRUE)) {
          $v[] = "list_components[$i]: views.view.$view builds its rows in view mode $row_mode, which placed and inline blocks also use; select a dedicated view mode such as list_item";
          continue;
        }
        if (\Drupal::config("core.entity_view_mode.block_content.$row_mode")->isNew()) {
          $v[] = "list_components[$i]: core.entity_view_mode.block_content.$row_mode, the row view mode of views.view.$view, does not exist";
          continue;
        }
        $block = $etm->getStorage('block_content')->create(['type' => $block_bundle, 'info' => 'aida verify fixture']);
        // BlockContentViewBuilder::view() already runs buildMultiple().
        $build = $etm->getViewBuilder('block_content')->view($block, $row_mode);
        if (($build['#theme'] ?? NULL) !== 'block_content') {
          $v[] = "a block_content of type $block_bundle builds in view mode $row_mode, the row view mode of views.view.$view, without #theme block_content";
        }
        continue;
      }
      if ($group_field === '' || \Drupal::config("field.field.block_content.$block_bundle.$group_field")->isNew()) {
        $v[] = "list_components[$i]: field.field.block_content.$block_bundle.$group_field does not exist";
      }
      else {
        $group_storage = \Drupal::config("field.storage.block_content.$group_field");
        if ($group_storage->get('type') !== 'entity_reference' || $group_storage->get('settings.target_type') !== 'taxonomy_term') {
          $v[] = "field.storage.block_content.$group_field is not an entity_reference to taxonomy_term";
        }
      }
      $view_config = \Drupal::config("views.view.$view");
      if ($view === '' || $view_config->isNew()) {
        $v[] = "list_components[$i]: views.view.$view does not exist";
      }
      elseif ($view_config->get('base_table') !== 'block_content_field_data') {
        $v[] = "views.view.$view lists " . $view_config->get('base_table') . ', not block_content_field_data';
      }
    }
    break;

  case 'templates':
    // Render a block through the default theme as a user with contextual
    // links access. The probe attribute shows up only if the template prints
    // attributes; the contextual placeholder only if it prints title_suffix.
    $default = \Drupal::config('system.theme')->get('default');
    \Drupal::theme()->setActiveTheme(\Drupal::service('theme.initialization')->initTheme($default));
    // Each bundle is probed inline and as a reusable block. The content is an
    // unsaved block_content build, so core's #block_content suggestions
    // (block__block_content__type__BUNDLE and the view ones) apply.
    $probes = [];
    foreach (array_keys($etm->getStorage('block_content_type')->loadMultiple()) as $block_bundle) {
      $probes[] = ["inline_block:$block_bundle", 'layout_builder', $block_bundle];
      $probes[] = ['block_content:aida-verify', 'block_content', $block_bundle];
    }
    $block_view_builder = $etm->getViewBuilder('block_content');
    $switcher = \Drupal::service('account_switcher');
    $switcher->switchTo(new class extends \Drupal\Core\Session\UserSession {
      public function hasPermission(string $permission) {
        return $permission === 'access contextual links';
      }
    });
    try {
      foreach ($probes as [$plugin_id, $provider, $block_bundle]) {
        [$base, $derivative] = explode(':', $plugin_id);
        $block_entity = $etm->getStorage('block_content')->create(['type' => $block_bundle, 'reusable' => FALSE]);
        $build = [
          '#theme' => 'block',
          '#attributes' => ['data-aida-verify' => 'attributes'],
          '#configuration' => ['label' => '', 'label_display' => FALSE, 'provider' => $provider],
          '#plugin_id' => $plugin_id,
          '#base_plugin_id' => $base,
          '#derivative_plugin_id' => $derivative,
          '#in_preview' => TRUE,
          '#contextual_links' => ['aida_verify' => ['route_parameters' => []]],
          'content' => $block_view_builder->view($block_entity, 'full'),
        ];
        $html = (string) \Drupal::service('renderer')->renderInIsolation($build);
        if (!str_contains($html, 'data-aida-verify')) {
          $v[] = "$default renders block $plugin_id of bundle $block_bundle without printing {{ attributes }}";
        }
        if (!str_contains($html, 'data-contextual-id')) {
          $v[] = "$default renders block $plugin_id of bundle $block_bundle without printing {{ title_suffix }}";
        }
      }
    }
    finally {
      $switcher->switchBack();
    }
    break;

  default:
    throw new \InvalidArgumentException("unknown check '$check'");
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
