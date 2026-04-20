---
description: Facets range slider widget — facets_range_widget sub-module, jQuery UI slider, setup, and distinctions from BEF noUiSlider
tldr: "Use this guide when you have numeric facets (price, rating, year) and want a visual slider interface."
drupal_version: "11.x"
---

# Range Slider Widget

## When to Use

> Use this guide when you have numeric facets (price, rating, year) and want a visual slider interface.

## Decision

**Module:** `facets_range_widget`

| ID | Class | Purpose |
|---|---|---|
| `slider` | SliderWidget | Single-value slider |
| `range_slider` | RangeSliderWidget | Dual-handle range slider (min/max) |

**Processors included:**

| ID | Purpose |
|---|---|
| `slider_processor` | Process slider input values |
| `range_slider_processor` | Process range slider min/max values |

**Dependencies:** jQuery UI Slider, jQuery UI Touch Punch (for touch device support)

## Pattern

```bash
drush en facets_range_widget
```

Then on the facet configuration, select "Slider" or "Range Slider" as the widget.

## Common Mistakes

- **Wrong**: Assuming jQuery UI is bundled in Drupal 10+ → **Right**: The range widget requires jQuery UI Slider. In Drupal 10+, jQuery UI is no longer bundled. You may need `drupal/jquery_ui_slider`.
- **Wrong**: Confusing this with BEF sliders → **Right**: Unlike BEF sliders (noUiSlider library), Facets range widget uses jQuery UI Slider. Different library, different look and feel.

## See Also

- [Widgets](widgets.md) — other widget types
- [Value Transformation Processors](value-transformation-processors.md) — granular processor for grouping numbers
- Reference: `web/modules/contrib/facets/modules/facets_range_widget/`
