---
description: Identify complex interface sections composed of molecules and atoms
---

# Organism Recognition

## When to Use

> Use when you've identified atoms and molecules, now need to recognize complex sections. Use to distinguish organisms from templates.

## Decision

| Component Characteristic | Classification | Key Differentiator |
|-------------------------|----------------|-------------------|
| Discrete interface section with functionality | **Organism** | Contains multiple molecules/atoms |
| Full page layout structure | **Template** | Organizes organisms into layout |
| Reusable across pages | **Organism** | Context-independent |
| Page-specific layout | **Template** | Context-dependent structure |

## Pattern

**Common Organism Types:**

| Organism | Components | Purpose | Recognition |
|----------|-----------|---------|-------------|
| **Header** | Logo + Navigation + Search bar + User menu | Site-wide navigation | Top of every page, multiple molecules |
| **Footer** | Logo + Link groups + Social icons + Copyright | Secondary navigation | Bottom, multiple columns |
| **Hero Section** | Heading + Paragraph + CTA buttons + Background | Primary message | Large, prominent, first on page |
| **Card Grid** | Multiple card molecules | Display collection | Repeated card pattern, consistent layout |
| **Form** | Multiple form fields + Button group + Validation | Collect input | Multiple input fields with submit |
| **Data Table** | Headers + Rows + Pagination + Sort + Filters | Tabular data | Rows/columns with interactive controls |
| **Navigation Menu** | Nav item molecules + Dropdowns + Mega menu | Site hierarchy | Nested navigation structure |
| **Media Gallery** | Images + Thumbnails + Navigation + Lightbox | Media collection | Grid/carousel with controls |
| **Comment Section** | Media objects + Reply buttons + Sorting | User content | Nested comment threads |
| **Dashboard Widget** | Heading + Stats + Chart + Action buttons | Metrics display | Self-contained data with controls |

**Recognition Strategy:**

```
1. Identify distinct interface sections
   - Feels like "complete section"?
   - Single entity name? (header, footer, hero)
   - Combines multiple molecules?

2. Test complexity threshold
   - Contains molecules → Likely organism
   - Contains only atoms → Likely molecule
   - Contains other organisms → Likely template

3. Check reusability
   - Appears on multiple pages unchanged → Organism
   - Page-specific → Part of template

4. Verify functional completeness
   - Performs complete function alone → Organism
   - Needs other sections → Part of template/page
```

**Source Recognition:**

- **HTML/CSS**: `<header>`, `<footer>`, `<section>`, `<article>` tags; class names like `.header`, `.hero`, `.card-grid`
- **Figma**: Top-level components with multiple molecules, complex nested structure
- **Screenshots**: Large sections with clear boundaries, repeated complex patterns

## Common Mistakes

- **Wrong**: Templates classified as organisms → **Right**: Organisms are reusable sections; templates are page layouts
- **Wrong**: Organism containing other organisms → **Right**: Consider if it's actually a template
- **Wrong**: Naming by structure (multi-column-section) → **Right**: Name by function (header, hero, footer)
- **Wrong**: Missing clear boundaries → **Right**: Organisms have distinct visual/functional boundaries

## See Also

- [Molecule Recognition](./molecule-recognition.md)
- [Templates vs Pages](./templates-vs-pages.md)
- [Source-Specific Recognition](./html-css-analysis.md)
- Reference: [Atomic Design Organisms](https://atomicdesign.bradfrost.com/chapter-2/#organisms)
