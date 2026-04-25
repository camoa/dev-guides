---
description: Extend Bootstrap maps with map-merge() in a map-overrides partial — never overwrite them directly.
drupal_version: "11.x"
tldr: Extend Bootstrap maps with `map-merge()` in a map-overrides partial. Never overwrite Bootstrap's `$spacers`, `$theme-colors`, or other maps directly.
---

# Never Replace Bootstrap Maps

**What:** Extend Bootstrap maps with `map-merge()` in a map-overrides partial. Never overwrite Bootstrap's `$spacers`, `$theme-colors`, or other maps directly.

**Rationale:** Bootstrap maps carry default values used throughout the framework. Direct overwrites delete keys you didn't know depended on, causing silent breakage in components (badges, alerts, buttons) that reference the missing keys. `map-merge()` preserves defaults while adding/overriding specific keys.

**When it applies:** Any time you customize Bootstrap variables that are maps (not scalars). Common targets: `$theme-colors`, `$spacers`, `$grid-breakpoints`, `$utilities`.

**Example:**

```scss
// Wrong — wipes out all Bootstrap defaults
$theme-colors: (
  "primary": #0066cc,
  "brand": #ff6600,
);

// Right — extends defaults with project additions
$theme-colors: map-merge(
  $theme-colors,
  (
    "primary": #0066cc,   // overrides default
    "brand": #ff6600,     // adds new key
  )
);
```
