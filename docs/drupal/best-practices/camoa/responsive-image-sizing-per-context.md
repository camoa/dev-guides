---
description: Match responsive image styles to actual display size — a card image must not serve hero-sized sources.
drupal_version: "11.x"
tldr: Match responsive image styles to actual display size. A 363px card should not serve a 1440px hero image. Create purpose-specific responsive image styles rather than reusing oversized ones.
---

# Responsive Image Sizing Per Context

**What:** Match responsive image styles to actual display size. A 363px card should not serve a 1440px hero image. Create purpose-specific responsive image styles rather than reusing oversized ones.

**Rationale:** Browsers download the source listed in `srcset`/`sizes` that best matches the viewport — but only from the candidates the responsive image style provides. If your card-context responsive style includes 1440w, 1920w, and 2560w sources but the card actually renders at 363px on desktop, mobile users get tiny images, desktop users get oversized ones, LCP suffers, and bandwidth waste compounds across visitors.

**When it applies:** Every responsive image style. Audit each: does its smallest derivative match the smallest rendered size, and the largest match the largest? Create a new style if not.

**Example:**

```
Wrong — one responsive style for everything
  hero_responsive (sources: 768w, 1024w, 1440w, 1920w, 2560w)
  used by: hero, card, sidebar, related-content thumbnail

Right — purpose-specific styles
  hero_responsive       (1024w, 1440w, 1920w, 2560w)
  card_thumbnail_responsive  (300w, 600w, 900w)
  sidebar_thumbnail_responsive  (200w, 400w)
```
