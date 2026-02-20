---
description: Design system recognition — 6. templates vs pages
---

## 6. Templates vs Pages




#### When to Use This Section
- You need to distinguish between layout structures (templates) and real implementations (pages)
- You're analyzing page-level patterns in a design system
- You're documenting layout systems vs actual page instances

#### Decision Table: Template vs Page

| Characteristic | Template | Page |
|----------------|----------|------|
| **Content Type** | Placeholder/Lorem ipsum | Real content |
| **Purpose** | Show layout structure | Show actual implementation |
| **Variations** | One template, many pages | Multiple pages from one template |
| **Testing Focus** | Layout flexibility | Content edge cases |
| **Figma/Design Tools** | Component with placeholder text/images | Instance with real content |

#### Pattern: Template Identification

**Reference Sources:**
- Brad Frost templates/pages: [https://atomicdesign.bradfrost.com/chapter-2/#templates](https://atomicdesign.bradfrost.com/chapter-2/)
- Distinction explained: [Pages and Templates: the Other End of Atomic Design](https://designsystemcentral.com/pages-templates-in-atomic-design/69/)
- Practical guidance: [Atomic Design Methodology in UX/UI Design](https://medium.com/@qamarjafari1717/atomic-design-methodology-in-ux-ui-design-from-atoms-to-pages-a9f20ab12841)

**Templates — "Page-level layouts that place organisms and molecules into a structure"**

**Characteristics:**
- **No real content** — Uses placeholder text, stock images, dummy data
- **Shows structure** — Demonstrates content areas, regions, slots
- **Layout rules** — Defines spacing, alignment, responsive behavior
- **Content-agnostic** — Works with any content that fits the pattern

**What Templates Define:**
- Grid system and column structure
- Organism placement (header at top, sidebar on left, etc.)
- Content area dimensions
- Responsive breakpoints and layout shifts
- White space and vertical rhythm

**Example Template:**
- Homepage Template: Header + Hero + 3-column feature section + CTA + Footer
- Blog Template: Header + Sidebar + Main content area + Related posts + Footer
- Dashboard Template: Top nav + Side nav + Main panel + Widget grid

**Pages — "Concrete instances of templates populated with real data/content"**

**Characteristics:**
- **Real content** — Actual headlines, product photos, user data
- **Tests edge cases** — Long headlines, missing images, empty states
- **Shows variations** — Different user states, content scenarios
- **Validates design system** — Proves patterns work in reality

**What Pages Reveal:**
- Copy length issues (headline too long)
- Translation problems (German text longer than English)
- Missing content scenarios (no reviews, empty cart)
- Real image quality and aspect ratios
- Accessibility with actual content

**Example Pages from Same Template:**
- Homepage (logged out) — Generic welcome message
- Homepage (logged in) — Personalized content
- Homepage (new user) — Onboarding flow
- Homepage (mobile) — Condensed layout

**Recognition Strategy:**

1. **Check content authenticity**
   - Placeholder text (Lorem ipsum, "Product Name Here") → **Template**
   - Real text ("iPhone 15 Pro", actual product description) → **Page**

2. **Assess purpose**
   - Shows layout structure → **Template**
   - Shows real-world implementation → **Page**

3. **Count variations**
   - One instance showing pattern → **Template**
   - Multiple instances with different content → **Pages**

4. **Identify focus**
   - Testing layout flexibility → **Template**
   - Testing content edge cases → **Page**

**Development Context:**

**Templates in Code:**
- Presentational components
- Define regions/slots
- Fetch data in parent, pass to template
- Keep templates mostly presentational

**Pages in Code:**
- Container components
- Fetch data (API calls)
- Handle analytics events
- Test performance with realistic data

Reference: [Atomic Design in Practice](https://www.mykolaaleksandrov.dev/posts/2025/11/atomic-design-in-practice/)

**Recognition in Different Sources:**

**Figma:**
- **Templates:** Master components with placeholder content
- **Pages:** Component instances with overridden text/images
- Look for: Text overrides, image swaps, variant selections

**HTML/CSS:**
- **Templates:** Files with `{variable}` placeholders or template syntax
- **Pages:** Files with hardcoded content or data-bound values
- Look for: Template engines (Twig, Blade, JSX), data binding

**Screenshots:**
- **Templates:** Stock photos, "Lorem ipsum", generic content
- **Pages:** Real product photos, actual headlines, user-generated content

**Design Systems Documentation:**
- **Templates:** Show layout grid overlays, spacing annotations
- **Pages:** Show accessibility audit results, performance metrics

#### Common Mistakes
- **Treating pages as templates** — If content is real, it's a page even if it looks similar to template
- **Missing page variations** — Multiple pages from one template show edge cases (long titles, empty states)
- **Skipping templates entirely** — Templates are essential for documenting layout patterns
- **Confusing with organisms** — Organisms are reusable sections; templates are full-page layouts

#### See Also
- [5. Organism Recognition](#5-organism-recognition)
- [8. Source-Specific Recognition](#8-source-specific-recognition)
- [11. Validation Checklist](#11-validation-checklist)
