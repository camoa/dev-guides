---
description: "The facets_range_widget sub-module for slider and dual-handle range facets on numeric fields"
tldr: "Use this guide when you have numeric facets (price, rating, year) and want a visual slider interface. Requires jQuery UI Slider — not bundled with Drupal 10+ core."
drupal_version: "11.x"
---

# Range Slider Widget

## When to Use

> When you have numeric facets (price, rating, year) and want a visual slider interface.

## Decision

**Module:** `facets_range_widget`

**Widgets:**

| ID | Class | Purpose |
|---|---|---|
| `slider` | SliderWidget | Single-value slider |
| `range_slider` | RangeSliderWidget | Dual-handle range slider (min/max) |

**Processors:**

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

- **Wrong**: Assuming jQuery UI is available by default → **Right**: jQuery UI is not bundled with Drupal core. You may need `drupal/jquery_ui_slider`.
- **Wrong**: Expecting noUiSlider behavior/styling → **Right**: Unlike BEF sliders (noUiSlider), Facets range widget uses jQuery UI Slider — a different library with a different look.

## See Also

- [Widgets](widgets.md) — other widget types
- [Value Transformation Processors](value-transformation-processors.md) — granular processor for grouping numbers
- Reference: `modules/facets_range_widget/`
