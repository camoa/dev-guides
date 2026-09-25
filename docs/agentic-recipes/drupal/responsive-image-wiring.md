---
# Routing block — an orchestrator reads to here and decides.
name: responsive_image_wiring
capability: responsive-image-delivery
description: Use when a Drupal site has named image use-cases (hero, card thumbnail, content inline) that must render as responsive images on image fields.
# Metadata — read only after a match.
label: Responsive image wiring
recipe_schema_version: 1.0.0
version: 0.6.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/image-styles/image-overview
  - drupal/image-styles/image-style-schema
  - drupal/image-styles/creating-styles-config
  - drupal/image-styles/core-image-effects
  - drupal/image-styles/responsive-image-config
  - drupal/image-styles/breakpoint-configuration
  - drupal/image-styles/art-direction-resolution
  - drupal/image-styles/image-field-formatters
  - drupal/image-styles/webp-avif-optimization
requires_plays:
  - drupal/best-practices/camoa/responsive-image-sizing-per-context
  - drupal/best-practices/camoa/media-view-mode-to-responsive-image-style
drupal_compatibility: "^10.3 || ^11"
requires_modules:
  - image
  - responsive_image
  - breakpoint
invokes_drupal_recipes: []
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Deliver responsive images for a Drupal site from a declared list of image use-cases, so every image field renders correctly-sized sources per breakpoint and per pixel density, with modern format optimization and a safe fallback, no bandwidth waste, and no untyped one-size-fits-all responsive style left in the project.

## Opinion

**Purpose-specific responsive image styles, one per use-case.** A hero-context responsive style is never attached to a card-context field. Source: play `drupal/best-practices/camoa/responsive-image-sizing-per-context`.

**Purpose-specific view modes, never the default.** The default media view mode is an admin fallback, not a content render target. Each use-case gets its own view mode and its own entity view display. Source: play `drupal/best-practices/camoa/media-view-mode-to-responsive-image-style`.

**Resolution switching is the default. Art direction is the exception.** Use art direction only when the layout crop genuinely changes per breakpoint, not merely the size. Source: guide `drupal/image-styles/art-direction-resolution`.

**Modern format with a safe fallback.** Emit a modern format where the toolkit supports it and fall back automatically otherwise. The effect is one of the two the format guide names: `image_convert_avif` with a WebP fallback, or `image_convert` to WebP. `formatPriority` picks between them. The recipe does not state the version floor — that is the format guide's job. Source: guide `drupal/image-styles/webp-avif-optimization`.

**Loading priority is per use-case.** Above-the-fold use-cases get `eager`; below-the-fold get `lazy`. Source: guide `drupal/image-styles/image-field-formatters`.

**Default to the active default theme's breakpoint group.** For art direction, the breakpoint group defaults to the front-end default theme's group (`system.theme.default` → that theme's `*.breakpoints.yml`). An explicit `breakpoint_group` input is an override, not a requirement. Resolution switching always uses the responsive_image module's built-in `viewport_sizing` group regardless of theme.

**Size for every breakpoint and every pixel density.** Derive enough image styles to cover each breakpoint and each multiplier the group declares (1x, 2x, 3x) — read the multipliers, never assume 1x. For resolution switching, the width ladder extends to at least 2× the use-case max width so high-DPR screens have a real source to pick.

## The chain

The three layers are built and referenced in this order, and the ordering is load-bearing:

1. **Image styles** — the derivatives. Named effect chains producing files at specific sizes and formats. Not breakpoint-aware on their own.
2. **Responsive image style** — the configuration that maps a breakpoint group (or a `sizes` ladder) to those image styles, with a fallback. Transforms nothing itself; it composes the image styles.
3. **View mode display** — uses the `responsive_image` formatter, which references the **responsive image style**.

The view mode references the responsive image style, never the raw image styles. The raw styles are only ever referenced by the responsive image style. You cannot reference a responsive image style until it exists, and it cannot exist until its image styles exist — hence the order.

## Preconditions

- Drupal 10.3+ or 11.x; `image`, `responsive_image`, `breakpoint` enabled.
- A breakpoint group is resolvable: the default theme declares one in `*.breakpoints.yml`, or one is supplied via input. The module's `responsive_image.viewport_sizing` group exists by default and is the target for resolution switching. See `drupal/image-styles/breakpoint-configuration`.
- The format-conversion capability the use-cases ask for is available on this site. The version/module floor for modern-format-with-fallback is stated in `drupal/image-styles/webp-avif-optimization`; this recipe defers to that guide and checks availability at runtime rather than asserting a version here.
- A list of image use-cases is supplied via the input contract.
- DDEV runs the site, and `ddev drush` works from the project root. The verifier's commands go through `ddev`.

## Input contract

Generic list, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
image_use_cases:
  - name: string              # machine name, snake_case, unique
    aspectRatio: string       # e.g. "16:9", "1:1", "auto"
    maxWidth: integer         # max display width in px
    purpose: string           # human description
    strategy: string          # "resolution_switching" | "art_direction"
                              # default: resolution_switching
    loadingPriority: string   # "eager" | "lazy"   (default: lazy)
    formatPriority: string    # format strategy name; resolved against the
                              # format guide  (default: modern-with-fallback)
    focalPoint: string        # crop anchor; "center-center" by default
                              # used whenever a crop is applied
    sizesAttribute: string    # required when strategy = resolution_switching
    appliesTo:                # optional; where this use-case renders
      - entity_type: string   #   if present, step 5 wires deterministically
        bundle: string        #   if absent, step 5 asks the operator, and the
        field: string         #   caller passes the confirmed triples here
        view_mode: string     #   for the verifier

breakpoint_group: string      # optional; overrides the default theme's group
                              # (only relevant to art_direction use-cases)
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate preconditions and resolve the breakpoint group.** Confirm Drupal version and modules. Resolve the art-direction breakpoint group: use `breakpoint_group` if supplied, else the default theme's group. If neither resolves and any use-case needs art direction, surface and stop. See `drupal/image-styles/breakpoint-configuration`.

2. **Create the image styles each use-case needs.** For each use-case, derive and create the derivatives its context requires; skip existing matches, flag conflicts, never overwrite.
   - Resolution switching: a width ladder covering the use-case's rendered sizes, whose widest style is at least 2× `maxWidth` for high-DPR. Crop to `aspectRatio` (at `focalPoint`) when a ratio is declared; scale otherwise.
   - Art direction: one derivative per breakpoint **and per declared multiplier** in the resolved group, cropped to the use-case aspect at the focal point.
   - For the effect chain and the format-conversion effect, see `drupal/image-styles/core-image-effects` and `drupal/image-styles/webp-avif-optimization`. For UUID/file mechanics see `drupal/image-styles/creating-styles-config`.

3. **Create the responsive image style per use-case.** One `responsive_image.styles.<use_case>` mapping the breakpoints (art direction) or the `sizes` ladder (resolution switching) to the image styles from step 2, with a fallback to the smallest. This is the entity the formatter references. See `drupal/image-styles/responsive-image-config` and `drupal/image-styles/art-direction-resolution`. Same idempotency contract.

4. **Create the purpose-specific view mode and display.** For each use-case, an entity view mode and an entity view display using the `responsive_image` formatter pointed at the use-case's responsive image style, with the declared loading attribute. See `drupal/image-styles/image-field-formatters` and the view-mode play. Same idempotency contract.

5. **Bind use-cases to fields.** For each use-case: if it declares `appliesTo`, wire those `(bundle, field, view_mode)` triples to its view mode deterministically. If it does not, discover image-bearing fields in the data model and confirm with the operator which use-case each field/view-mode renders before wiring — the recipe does not guess this mapping. See `drupal/image-styles/image-field-formatters`.

6. **Rebuild caches.** `drush cr`, so config changes take effect and the breakpoint manager re-reads any added breakpoints.

7. **Emit summary.** What was created, skipped as no-op, surfaced as conflict, or left for operator confirmation.

## Data flow

```
input: image_use_cases   (generic list, supplied by caller)
       breakpoint_group  (optional override; default = default theme's group)

reads project state:
       system.theme.default  + that theme's *.breakpoints.yml
       image.style.* / responsive_image.styles.* config
       core.entity_view_mode.* / core.entity_view_display.* config
       the data model (image-bearing fields per bundle/view-mode)
       format-conversion capability availability (per format guide)

applies opinion (plays):
       per-context sizing · purpose-specific view modes

references atomic detail (guides):
       drupal/image-styles/{ image-overview, image-style-schema,
         creating-styles-config, core-image-effects, responsive-image-config,
         breakpoint-configuration, art-direction-resolution,
         image-field-formatters, webp-avif-optimization }

emits (built in chain order):
       image.style.<name>                          (per derived style)
       responsive_image.styles.<use_case>          (per use-case)
       core.entity_view_mode.<entity>.<use_case>   (per use-case)
       core.entity_view_display ... formatter -> responsive style
       field formatters on bound (bundle, field, view_mode) triples
```

## State-awareness contract

The recipe reads existing state before writing. For every emitted config object: absent → create; present and matching the derived spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review. A missing breakpoint group fails the precondition check (step 1). A field binding that already points at the correct use-case → skip; pointing at a different use-case → conflict.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/responsive-image-wiring/verify.php` run the script in `## Files`. It prints one line per violation, prints a violation when an input it needs is missing, and exits non-zero when it printed any.

verifier:
  - id: image-styles-cover-use-case
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/responsive-image-wiring/verify.php -- image-styles {image_use_cases:json}
    pass: stdout empty
  - id: responsive-style-per-use-case
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/responsive-image-wiring/verify.php -- responsive-styles {image_use_cases:json} {breakpoint_group:json}
    pass: stdout empty
  - id: view-mode-per-use-case
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/responsive-image-wiring/verify.php -- view-modes {image_use_cases:json}
    pass: stdout empty
  - id: bindings-render-through-use-case
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/responsive-image-wiring/verify.php -- bindings {image_use_cases:json}
    pass: stdout empty
  - id: rendered-markup
    kind: live-site
    run: ddev drush php:script /var/www/html/.aida/responsive-image-wiring/verify.php -- render {image_use_cases:json} {breakpoint_group:json}
    pass: stdout empty

What the entries do not prove, and where the checks went:

- `image-styles-cover-use-case` reads every image style the use case's responsive style references, the fallback included. Each must end, by weight, in `image_convert` to `webp`, or in `image_convert_avif` whose fallback `extension` is `webp`. The entry does not read `formatPriority`: it accepts either effect. For resolution switching, the widest `sizes` style must be at least 2× `maxWidth`, measured from a very large source. The per-breakpoint and per-multiplier coverage of art direction is checked in `responsive-style-per-use-case`.
- `responsive-style-per-use-case` checks the fallback is the narrowest referenced style. For resolution switching, it checks the `responsive_image.viewport_sizing` group and one non-empty mapping, of type `sizes`, whose `sizes` equals `sizesAttribute`. For art direction, it checks the resolved group, and an `image_style` mapping for every breakpoint and multiplier the group declares. The group is `breakpoint_group` when given. Otherwise it is the default theme's group: the group named after the theme, or the only group the theme provides.
- `view-mode-per-use-case` needs a view mode named after the use case on some entity type. It also needs at least one display in that view mode with a `responsive_image` component. Every such component must reference the use case's responsive style with the declared loading attribute. An `image` formatter in that view mode fails the entry, because it references a raw image style.
- `bindings-render-through-use-case` reads each `appliesTo` entry's display. The field must use `responsive_image` with the use case's style, or render the referenced entity, such as a media item, in the use case's view mode. A use case with no `appliesTo` fails the entry: the caller passes the triples the operator confirmed in Sequence step 5.
- `rendered-markup` renders the field in process, on the newest entity of each `appliesTo` bundle with the field filled. It fails when no such entity exists. Resolution switching needs an element whose `sizes` equals `sizesAttribute` and whose `srcset` holds a width candidate from the style's derivatives. Art direction needs a `<source>` for each breakpoint with a media query, holding a candidate for each multiplier.
- The old check's browser half is not here: which derivative a small or a high-DPR viewport downloads needs a real browser. That belongs to AIDA surfaces, as a visual or end-to-end check.
- No entry checks that a crop matches `aspectRatio` or `focalPoint`.
- No entry checks the Goal's "no untyped one-size-fits-all responsive style left". The input names only this recipe's use cases, so nothing tells a leftover generic style from one another recipe or the install profile made.
- The script in `## Files` is written into the project for the verify run and removed after it. Do not commit or edit it.

## Files

The verifier's script. It runs through `ddev drush php:script`, which passes the arguments after `--` to the script as `$extra`.

```php .aida/responsive-image-wiring/verify.php
<?php

/**
 * @file
 * Verifier checks for responsive_image_wiring, run by drush php:script.
 *
 * Usage: drush php:script verify.php -- <check> <json args...>
 * Prints one line per violation and nothing when every assertion holds.
 * Throws after printing, so Drush exits non-zero.
 */

use Drupal\responsive_image\Entity\ResponsiveImageStyle;

$check = $extra[0] ?? '';
$v = [];

$json = function (int $i) use ($extra) {
  if (!array_key_exists($i, $extra)) {
    throw new \InvalidArgumentException("argument $i is missing");
  }
  $value = json_decode($extra[$i], TRUE);
  if ($value === NULL && trim($extra[$i]) !== 'null') {
    throw new \InvalidArgumentException("argument $i is not JSON");
  }
  return $value;
};

// The use cases with the Input contract's defaults applied.
$use_cases = function () use ($json, &$v) {
  $list = $json(1);
  if (!is_array($list) || !$list) {
    $v[] = 'image_use_cases is missing or empty';
    return [];
  }
  $out = [];
  foreach ($list as $use_case) {
    if (empty($use_case['name'])) {
      $v[] = 'a use case has no name';
      continue;
    }
    $out[] = $use_case + ['strategy' => 'resolution_switching', 'loadingPriority' => 'lazy'];
  }
  return $out;
};

$storage = fn(string $type) => \Drupal::entityTypeManager()->getStorage($type);

// The width an image style produces from a very large source.
$width = function (string $style_id) use ($storage) {
  $style = $storage('image_style')->load($style_id);
  if (!$style) {
    return NULL;
  }
  $dimensions = ['width' => 100000, 'height' => 100000];
  $style->transformDimensions($dimensions, 'public://aida-verify.jpg');
  return $dimensions['width'];
};

// The art-direction group: the input, else the default theme's group.
$group = function ($input) {
  if (is_string($input) && $input !== '') {
    return $input;
  }
  $theme = \Drupal::config('system.theme')->get('default');
  $manager = \Drupal::service('breakpoint.manager');
  $groups = array_keys($manager->getGroups());
  if (in_array($theme, $groups, TRUE)) {
    return $theme;
  }
  $own = array_values(array_filter($groups, fn($g) => isset($manager->getGroupProviders($g)[$theme])));
  return count($own) === 1 ? $own[0] : NULL;
};

$sizes_mappings = fn(ResponsiveImageStyle $style) => array_values(array_filter(
  $style->getImageStyleMappings(),
  fn($m) => !ResponsiveImageStyle::isEmptyImageStyleMapping($m) && $m['image_mapping_type'] === 'sizes'
));

switch ($check) {
  case 'image-styles':
    foreach ($use_cases() as $use_case) {
      $name = $use_case['name'];
      $responsive = $storage('responsive_image_style')->load($name);
      if (!$responsive) {
        $v[] = "$name: responsive_image.styles.$name does not exist, so its image styles cannot be read";
        continue;
      }
      $ids = $responsive->getImageStyleIds();
      if (!$ids) {
        $v[] = "$name: responsive_image.styles.$name references no image style";
      }
      foreach ($ids as $id) {
        $style = $storage('image_style')->load($id);
        if (!$style) {
          $v[] = "$name: image style $id does not exist";
          continue;
        }
        $last = NULL;
        $extension = NULL;
        foreach ($style->getEffects()->sort() as $effect) {
          $last = $effect->getPluginId();
          $extension = $effect->getConfiguration()['data']['extension'] ?? NULL;
        }
        // image_convert_avif keeps its fallback format in the same key.
        if (!in_array($last, ['image_convert', 'image_convert_avif'], TRUE) || $extension !== 'webp') {
          $v[] = "$name: image style $id ends in " . var_export($last, TRUE) . ' with extension ' . var_export($extension, TRUE) . ', not image_convert to webp or image_convert_avif with a webp fallback';
        }
      }
      if ($use_case['strategy'] === 'resolution_switching') {
        if (empty($use_case['maxWidth'])) {
          $v[] = "$name: maxWidth is missing";
          continue;
        }
        $widths = [];
        foreach ($sizes_mappings($responsive) as $mapping) {
          foreach ($mapping['image_mapping']['sizes_image_styles'] as $id) {
            $widths[$id] = $width($id);
          }
        }
        if (!$widths || max($widths) < 2 * $use_case['maxWidth']) {
          $v[] = "$name: the widest sizes style is " . ($widths ? max($widths) : 'absent') . 'px, below 2 x maxWidth ' . (2 * $use_case['maxWidth']) . 'px';
        }
      }
    }
    break;

  case 'responsive-styles':
    $breakpoint_group = $json(2);
    foreach ($use_cases() as $use_case) {
      $name = $use_case['name'];
      $responsive = $storage('responsive_image_style')->load($name);
      if (!$responsive) {
        $v[] = "responsive_image.styles.$name does not exist";
        continue;
      }
      $fallback = $responsive->getFallbackImageStyle();
      $fallback_width = $fallback ? $width($fallback) : NULL;
      if ($fallback_width === NULL) {
        $v[] = "$name: fallback image style " . var_export($fallback, TRUE) . ' is missing or has no width';
      }
      else {
        foreach (array_diff($responsive->getImageStyleIds(), [$fallback]) as $id) {
          if (($w = $width($id)) !== NULL && $w < $fallback_width) {
            $v[] = "$name: fallback $fallback ({$fallback_width}px) is wider than $id ({$w}px)";
          }
        }
      }
      if ($use_case['strategy'] === 'resolution_switching') {
        if ($responsive->getBreakpointGroup() !== 'responsive_image.viewport_sizing') {
          $v[] = "$name: breakpoint group is {$responsive->getBreakpointGroup()}, expected responsive_image.viewport_sizing";
        }
        $mappings = array_filter($responsive->getImageStyleMappings(), fn($m) => !ResponsiveImageStyle::isEmptyImageStyleMapping($m));
        $sizes = $sizes_mappings($responsive);
        if (count($mappings) !== 1 || count($sizes) !== 1) {
          $v[] = "$name: expected one mapping of type sizes, found " . count($mappings) . ' mapping(s), ' . count($sizes) . ' of type sizes';
        }
        elseif (!isset($use_case['sizesAttribute'])) {
          $v[] = "$name: sizesAttribute is missing";
        }
        elseif ($sizes[0]['image_mapping']['sizes'] !== $use_case['sizesAttribute']) {
          $v[] = "$name: sizes is '{$sizes[0]['image_mapping']['sizes']}', expected '{$use_case['sizesAttribute']}'";
        }
      }
      elseif ($use_case['strategy'] === 'art_direction') {
        $resolved = $group($breakpoint_group);
        if ($resolved === NULL) {
          $v[] = "$name: no breakpoint_group was given and the default theme has no single breakpoint group";
          continue;
        }
        if ($responsive->getBreakpointGroup() !== $resolved) {
          $v[] = "$name: breakpoint group is {$responsive->getBreakpointGroup()}, expected $resolved";
        }
        $breakpoints = \Drupal::service('breakpoint.manager')->getBreakpointsByGroup($resolved);
        if (!$breakpoints) {
          $v[] = "$name: breakpoint group $resolved has no breakpoints";
        }
        foreach ($breakpoints as $id => $breakpoint) {
          foreach ($breakpoint->getMultipliers() as $multiplier) {
            $mapping = $responsive->getImageStyleMapping($id, $multiplier);
            if (!$mapping || $mapping['image_mapping_type'] !== 'image_style' || empty($mapping['image_mapping'])) {
              $v[] = "$name: no image_style mapping for breakpoint $id at $multiplier";
            }
          }
        }
      }
      else {
        $v[] = "$name: unknown strategy {$use_case['strategy']}";
      }
    }
    break;

  case 'view-modes':
    foreach ($use_cases() as $use_case) {
      $name = $use_case['name'];
      $modes = array_filter(array_keys($storage('entity_view_mode')->loadMultiple()), fn($id) => str_ends_with($id, ".$name"));
      if (!$modes) {
        $v[] = "$name: no view mode core.entity_view_mode.*.$name exists";
      }
      $found = 0;
      foreach ($storage('entity_view_display')->loadByProperties(['mode' => $name]) as $display) {
        foreach ($display->getComponents() as $field => $component) {
          $type = $component['type'] ?? NULL;
          if ($type === 'image') {
            $v[] = "$name: {$display->id()} renders $field with a raw image style";
          }
          if ($type !== 'responsive_image') {
            continue;
          }
          $found++;
          $settings = $component['settings'] ?? [];
          if (($settings['responsive_image_style'] ?? NULL) !== $name) {
            $v[] = "$name: {$display->id()} $field uses responsive style " . var_export($settings['responsive_image_style'] ?? NULL, TRUE);
          }
          if (($settings['image_loading']['attribute'] ?? NULL) !== $use_case['loadingPriority']) {
            $v[] = "$name: {$display->id()} $field loads " . var_export($settings['image_loading']['attribute'] ?? NULL, TRUE) . ", expected {$use_case['loadingPriority']}";
          }
        }
      }
      if ($found === 0) {
        $v[] = "$name: no display in view mode $name uses the responsive_image formatter";
      }
    }
    break;

  case 'bindings':
    foreach ($use_cases() as $use_case) {
      $name = $use_case['name'];
      if (empty($use_case['appliesTo'])) {
        $v[] = "$name: appliesTo is missing, so its bindings cannot be checked";
        continue;
      }
      foreach ($use_case['appliesTo'] as $t) {
        if (empty($t['entity_type']) || empty($t['bundle']) || empty($t['field']) || empty($t['view_mode'])) {
          $v[] = "$name: an appliesTo entry lacks entity_type, bundle, field or view_mode";
          continue;
        }
        $id = "{$t['entity_type']}.{$t['bundle']}.{$t['view_mode']}";
        $display = $storage('entity_view_display')->load($id);
        $component = $display?->getComponent($t['field']);
        if (!$component) {
          $v[] = "$name: $id does not display {$t['field']}";
          continue;
        }
        $settings = $component['settings'] ?? [];
        if ($component['type'] === 'responsive_image') {
          if (($settings['responsive_image_style'] ?? NULL) !== $name) {
            $v[] = "$name: $id {$t['field']} uses responsive style " . var_export($settings['responsive_image_style'] ?? NULL, TRUE);
          }
          if (($settings['image_loading']['attribute'] ?? NULL) !== $use_case['loadingPriority']) {
            $v[] = "$name: $id {$t['field']} loads " . var_export($settings['image_loading']['attribute'] ?? NULL, TRUE) . ", expected {$use_case['loadingPriority']}";
          }
        }
        elseif ($component['type'] === 'entity_reference_entity_view') {
          if (($settings['view_mode'] ?? NULL) !== $name) {
            $v[] = "$name: $id {$t['field']} renders the referenced entity in view mode " . var_export($settings['view_mode'] ?? NULL, TRUE);
          }
        }
        else {
          $v[] = "$name: $id {$t['field']} uses formatter {$component['type']}, not responsive_image or entity_reference_entity_view";
        }
      }
    }
    break;

  case 'render':
    $breakpoint_group = $json(2);
    foreach ($use_cases() as $use_case) {
      $name = $use_case['name'];
      $responsive = $storage('responsive_image_style')->load($name);
      if (!$responsive) {
        $v[] = "$name: responsive_image.styles.$name does not exist";
        continue;
      }
      if (empty($use_case['appliesTo'])) {
        $v[] = "$name: appliesTo is missing, so no field can be rendered";
        continue;
      }
      foreach ($use_case['appliesTo'] as $t) {
        if (empty($t['entity_type']) || empty($t['bundle']) || empty($t['field']) || empty($t['view_mode'])) {
          $v[] = "$name: an appliesTo entry lacks entity_type, bundle, field or view_mode";
          continue;
        }
        $definition = \Drupal::entityTypeManager()->getDefinition($t['entity_type']);
        $ids = $storage($t['entity_type'])->getQuery()->accessCheck(FALSE)
          ->condition($definition->getKey('bundle'), $t['bundle'])
          ->exists($t['field'])
          ->sort($definition->getKey('id'), 'DESC')->range(0, 1)->execute();
        if (!$ids) {
          $v[] = "$name: no {$t['entity_type']} of {$t['bundle']} has {$t['field']} filled, so nothing was rendered";
          continue;
        }
        $entity = $storage($t['entity_type'])->load(reset($ids));
        $build = $entity->get($t['field'])->view($t['view_mode']);
        $html = (string) \Drupal::service('renderer')->renderInIsolation($build);
        $doc = new \DOMDocument();
        libxml_use_internal_errors(TRUE);
        $doc->loadHTML('<?xml encoding="UTF-8">' . $html);
        libxml_clear_errors();
        $where = "{$t['entity_type']} {$entity->id()} {$t['field']} in {$t['view_mode']}";
        if ($use_case['strategy'] === 'resolution_switching') {
          $ok = FALSE;
          foreach (['img', 'source'] as $tag) {
            foreach ($doc->getElementsByTagName($tag) as $element) {
              $srcset = $element->getAttribute('srcset');
              if ($element->getAttribute('sizes') !== ($use_case['sizesAttribute'] ?? NULL)) {
                continue;
              }
              foreach ($responsive->getImageStyleIds() as $id) {
                $ok = $ok || preg_match('#/styles/' . preg_quote($id, '#') . '/\S+ \d+w#', $srcset);
              }
            }
          }
          if (!$ok) {
            $v[] = "$name: $where renders no srcset of this style's derivatives with sizes '" . ($use_case['sizesAttribute'] ?? '') . "'";
          }
        }
        else {
          $resolved = $group($breakpoint_group);
          if ($resolved === NULL) {
            $v[] = "$name: no breakpoint_group was given and the default theme has no single breakpoint group";
            continue;
          }
          $sources = [];
          foreach ($doc->getElementsByTagName('source') as $source) {
            $sources[$source->getAttribute('media')] = $source->getAttribute('srcset');
          }
          foreach (\Drupal::service('breakpoint.manager')->getBreakpointsByGroup($resolved) as $id => $breakpoint) {
            $media = trim($breakpoint->getMediaQuery());
            if ($media === '') {
              continue;
            }
            if (!isset($sources[$media])) {
              $v[] = "$name: $where renders no <source> for $media";
              continue;
            }
            foreach ($breakpoint->getMultipliers() as $multiplier) {
              if (!preg_match('#\S+ ' . preg_quote($multiplier, '#') . '(,|$)#', $sources[$media])) {
                $v[] = "$name: $where <source> for $media has no $multiplier candidate";
              }
            }
          }
        }
      }
    }
    break;

  default:
    throw new \InvalidArgumentException("unknown check '$check'");
}

foreach ($v as $line) {
  echo $line, "\n";
}
if ($v) {
  throw new \RuntimeException(count($v) . ' violation(s)');
}
```

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/image-styles/image-overview` | The image style → responsive image style → view mode chain |
| `drupal/image-styles/image-style-schema` | Image style YAML schema |
| `drupal/image-styles/creating-styles-config` | UUID workflow and YAML file location |
| `drupal/image-styles/core-image-effects` | Scale, scale-and-crop, format conversion effects |
| `drupal/image-styles/responsive-image-config` | Responsive image style YAML schema |
| `drupal/image-styles/breakpoint-configuration` | Breakpoint group declaration, viewport_sizing, multipliers |
| `drupal/image-styles/art-direction-resolution` | Mapping-type decision, sizes syntax, picture-element pattern |
| `drupal/image-styles/image-field-formatters` | `responsive_image` formatter, loading attribute |
| `drupal/image-styles/webp-avif-optimization` | Modern-format-with-fallback effect and its version/module floor |

### Plays applied

| Play | Source |
|---|---|
| Match responsive image styles to actual display size | `drupal/best-practices/camoa/responsive-image-sizing-per-context` |
| Never use the default media view mode; create purpose-specific view modes | `drupal/best-practices/camoa/media-view-mode-to-responsive-image-style` |
