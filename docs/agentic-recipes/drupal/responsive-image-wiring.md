---
# Routing block — an orchestrator reads to here and decides.
name: responsive_image_wiring
capability: responsive-image-delivery
description: Use when a Drupal site has named image use-cases (hero, card thumbnail, content inline) that must render as responsive images on image fields.
# Metadata — read only after a match.
label: Responsive image wiring
recipe_schema_version: 1.0.0
version: 0.5.0
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

**Modern format with a safe fallback.** Emit a modern format where the toolkit supports it and fall back automatically otherwise. The recipe does not name the effect or its version floor — that is the format guide's job. Source: guide `drupal/image-styles/webp-avif-optimization`.

**Loading priority is per use-case.** Above-the-fold use-cases get `eager`; below-the-fold get `lazy`. Source: guide `drupal/image-styles/image-field-formatters`.

**Default to the active default theme's breakpoint group.** For art direction, the breakpoint group defaults to the front-end default theme's group (`system.theme.default` → that theme's `*.breakpoints.yml`). An explicit `breakpoint_group` input is an override, not a requirement. Resolution switching always uses the responsive_image module's built-in `viewport_sizing` group regardless of theme.

**Size for every breakpoint and every pixel density.** Derive enough image styles to cover each breakpoint and each multiplier the group declares (1x, 2x, 3x) — read the multipliers, never assume 1x. For resolution switching, the width ladder extends up to roughly 2× the use-case max width so high-DPR screens have a real source to pick.

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
      - bundle: string        #   if present, step 6 wires deterministically
        field: string         #   if absent, step 6 asks the operator
        view_mode: string

breakpoint_group: string      # optional; overrides the default theme's group
                              # (only relevant to art_direction use-cases)
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate preconditions and resolve the breakpoint group.** Confirm Drupal version and modules. Resolve the art-direction breakpoint group: use `breakpoint_group` if supplied, else the default theme's group. If neither resolves and any use-case needs art direction, surface and stop. See `drupal/image-styles/breakpoint-configuration`.

2. **Create the image styles each use-case needs.** For each use-case, derive and create the derivatives its context requires; skip existing matches, flag conflicts, never overwrite.
   - Resolution switching: a width ladder covering the use-case's rendered sizes up to ~2× `maxWidth` for high-DPR. Crop to `aspectRatio` (at `focalPoint`) when a ratio is declared; scale otherwise.
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

After the recipe runs, verify:

1. Every use-case has image styles covering each of its breakpoints and declared multipliers (art direction) or its width ladder including a high-DPR source (resolution switching), each ending in the format-conversion effect per the format guide.
2. Every use-case has a `responsive_image.styles.<use_case>` entity with the correct breakpoint group, fallback, and mapping type matching its strategy.
3. Every use-case has its own view mode and a display whose `responsive_image` formatter references the use-case's responsive image style (not a raw image style) with the declared loading attribute.
4. Every bound `(bundle, field, view_mode)` triple renders through the intended use-case's view mode.
5. A real page renders a `<picture>`/`srcset` for resolution switching or per-breakpoint `<source>` elements for art direction, the smallest derivative is served on the smallest viewport, and a high-DPR viewport pulls a 2× source rather than an upscaled 1×.

The recipe does not ship an executable verifier in v0.4.0. The checks above are the manual / agent-driven verification protocol.

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
