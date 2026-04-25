---
description: Use the sizes attribute when image width depends on layout; use breakpoint-specific image style mappings when art-direction or aspect ratio differs per breakpoint.
drupal_version: "11.x"
tldr: Use the `sizes` attribute when the image width depends on layout (e.g., 50vw desktop, 100vw mobile). Use breakpoint-specific image style mappings when you need exact image style control per breakpoint.
---

# Sizes-Based vs Breakpoint-Based

**What:** Use the `sizes` attribute when the image width depends on layout (e.g., 50vw desktop, 100vw mobile). Use breakpoint-specific image style mappings when you need exact image style control per breakpoint.

**Rationale:** `sizes` describes how the image *displays* (a hint to the browser); the browser picks from `srcset` accordingly. It's compact and lets the browser optimize. Breakpoint-specific mappings (Drupal's "Responsive image style" with per-breakpoint image styles) give precise control over which derivative loads at each breakpoint — useful when art-direction or aspect-ratio differs per breakpoint.

**When it applies:** Choose per responsive image style. Most content images (cards, articles) want `sizes`. Hero/banner art that crops differently on mobile vs desktop wants breakpoint mappings.

**Example:**

```yaml
# Sizes-based — same image, browser picks size
responsive_image.styles.card_thumbnail.yml
  image_style_mappings:
    - breakpoint_id: bootstrap.md
      multiplier: 1x
      image_mapping_type: sizes
      image_mapping:
        sizes: '(min-width: 992px) 33vw, (min-width: 768px) 50vw, 100vw'
        sizes_image_styles: [card_300, card_600, card_900]

# Breakpoint-based — different image style per breakpoint
responsive_image.styles.hero.yml
  image_style_mappings:
    - breakpoint_id: bootstrap.lg
      image_mapping_type: image_style
      image_mapping: hero_desktop_wide
    - breakpoint_id: bootstrap.md
      image_mapping_type: image_style
      image_mapping: hero_tablet_square
    - breakpoint_id: bootstrap.xs
      image_mapping_type: image_style
      image_mapping: hero_mobile_portrait
```
