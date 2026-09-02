---
description: "svg makes zero HTTP requests (it inlines server-side) — svg_sprite only pays off when the same icon repeats many times per page"
tldr: "Pick the extractor by repetition, not icon count: svg is 0 HTTP requests since it inlines server-side, so 'switch to sprites to cut requests' is backwards — sprites only win when one icon repeats many times on a page."
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

You're optimizing icon rendering performance for large-scale sites with many icons or slow networks.

## Decision

The three core extractors have genuinely different cost profiles, and it is not the one usually assumed. **The `svg` extractor makes zero HTTP requests** — it reads each file server-side and inlines the markup — so "switch to sprites to cut requests" is backwards.

| Extractor | HTTP requests for N icons | Page weight | Server cost |
|---|---|---|---|
| `svg` | 0 | N copies of the markup inlined per occurrence | One file read + XML parse per distinct icon, cached in `icon_info` |
| `svg_sprite` | 1 (the sprite, browser-cached) | One `<use>` element per occurrence | One XML parse of the whole sprite at discovery |
| `path` | 1 per distinct icon URL | Minimal HTML | None — Drupal never fetches the file |

| Optimization | Impact | When to use |
|---|---|---|
| `svg_sprite` over `svg` | Smaller HTML when the same icon repeats many times per page | Icon repeated across a long list or grid |
| `svg` over `svg_sprite` | Removes the sprite request; icons inherit `currentColor` and can be styled per-element | Small set of distinct icons, above the fold |
| `path` + `loading="lazy"` | Defers below-fold image icons | Icons rendered as `<img>` |
| Icon pack consolidation | Fewer plugin definitions to build and cache | Multiple small packs with the same extractor |

## Pattern

Pick the extractor by repetition, not by icon count:

```yaml
# 8 distinct icons, each used once, above the fold -> inline them.
header_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg   # 0 HTTP requests

# 1 icon repeated 200 times in a listing -> one sprite reference each.
listing_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/all-icons.svg   # 1 HTTP request total
```

Lazy loading only works for packs whose template renders an `<img>`, and only if that template prints the setting. Settings are arbitrary context keys — `{ loading: 'lazy' }` does nothing unless the pack template contains `loading="{{ loading|default('eager') }}"`:

```twig
{# Above-fold icons - render immediately #}
<header>
  {{ icon('my_theme', 'logo', { size: 40 }) }}
</header>

{# Below-fold icons - requires a `path` pack whose template prints `loading` #}
<footer>
  {{ icon('my_theme_img', 'facebook', {
    size: 24,
    loading: 'lazy'
  }) }}
</footer>
```

Minimize pack overhead:

```yaml
# ❌ Avoid - Multiple small packs
pack_a:
  extractor: svg
  config: { sources: [icons/a/{icon_id}.svg] }

pack_b:
  extractor: svg
  config: { sources: [icons/b/{icon_id}.svg] }

# ✅ Good - Consolidated pack
combined_pack:
  extractor: svg
  config:
    sources:
      - icons/a/{icon_id}.svg
      - icons/b/{icon_id}.svg
```

Beware the merge rule when consolidating: icons are keyed by ID, so if `icons/a/home.svg` and `icons/b/home.svg` both exist, the later source wins and the earlier icon disappears silently.

Optimize templates:

```twig
{# ❌ Avoid - Complex logic in template #}
<svg width="{% if mobile %}16{% else %}24{% endif %}">
  {{ content }}
</svg>

{# ✅ Good - Pass pre-computed values #}
<svg width="{{ size|default(24) }}">
  {{ content }}
</svg>
```

Reference: Performance profiling with Webprofiler or Blackfire.

## Common Mistakes

- "Sprites cut HTTP requests" → Only versus `path`. Versus `svg` a sprite *adds* one request, because `svg` inlines the markup server-side
- Duplicate icon IDs across consolidated sources → Last source wins, silently
- Passing `loading: 'lazy'` to a pack whose template renders `<svg>` → The setting is ignored; there is no lazy loading for inline SVG
- Not preloading a critical sprite → `<link rel="preload" as="image" href="sprite.svg">` for above-fold `svg_sprite` icons
- Not minifying SVG sources → Run svgo on icon sources before deployment, but keep `viewBox` (see below)
- Complex extractor logic without caching → Cache expensive operations yourself; the base class does nothing

## See Also

- [Caching Strategy](caching-strategy.md)
- [SVG Security & Performance](svg-security-performance.md)
- Reference: [Drupal performance optimization](https://www.drupal.org/docs/managing-site-performance-and-scalability)
