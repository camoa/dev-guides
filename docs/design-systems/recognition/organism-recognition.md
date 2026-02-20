---
description: Design system recognition — 5. organism recognition
---

## 5. Organism Recognition




#### When to Use This Section
- You've identified atoms and molecules, now need to recognize complex sections
- You're analyzing interface sections that feel like "complete units"
- You need to distinguish organisms from templates

#### Decision Table: Organism vs Template

| Component Characteristic | Classification | Key Differentiator |
|-------------------------|----------------|-------------------|
| Discrete interface section with functionality | **Organism** | Contains multiple molecules/atoms |
| Full page layout structure | **Template** | Organizes organisms into layout |
| Reusable across pages | **Organism** | Context-independent |
| Page-specific layout | **Template** | Context-dependent structure |

#### Pattern: Common Organism Types

**Reference Sources:**
- Organism examples: [https://atomicdesign.bradfrost.com/chapter-2/#organisms](https://atomicdesign.bradfrost.com/chapter-2/)
- Complex components: [Creating Cohesive Design Systems with Atomic Design](https://selftaughttxg.com/2025/05-25/creating-cohesive-design-systems-with-atomic-design-principles/)
- IBM/Salesforce systems: [Atomic Design methodology for building design systems](https://blog.kamathrohan.com/atomic-design-methodology-for-building-design-systems-f912cf714f53)

**Organism Catalog:**

**1. Header Organism**
- **Components:** Logo (atom) + Navigation (molecule) + Search bar (molecule) + User menu (molecule)
- **Purpose:** Site-wide navigation and branding
- **Recognition:** Appears at top of every page, contains multiple molecules
- **Common variants:** Desktop header, mobile header with hamburger menu

**2. Footer Organism**
- **Components:** Logo + Link groups + Social icons + Copyright text
- **Purpose:** Site-wide secondary navigation and information
- **Recognition:** Bottom of page, multiple columns of content

**3. Hero Section Organism**
- **Components:** Heading + Paragraph + CTA buttons + Background image/video
- **Purpose:** Primary page message and call-to-action
- **Recognition:** Large, prominent section, often first on page

**4. Card Grid Organism**
- **Components:** Multiple card molecules arranged in grid
- **Purpose:** Display collection of similar items
- **Recognition:** Repeated card pattern with consistent layout
- **Example:** Product grid, blog post grid, team member grid

**5. Form Organism**
- **Components:** Multiple form field molecules + Button group + Form validation
- **Purpose:** Collect user input
- **Recognition:** Multiple input fields with submit action
- **Example:** Registration form, contact form, checkout form

**6. Data Table Organism**
- **Components:** Table headers + Rows + Pagination + Sort controls + Filters
- **Purpose:** Display structured tabular data
- **Recognition:** Rows and columns with interactive controls

**7. Navigation Menu Organism**
- **Components:** Multiple navigation item molecules + Dropdowns + Mega menu
- **Purpose:** Site navigation hierarchy
- **Recognition:** Nested navigation structure
- **Example:** Main navigation, sidebar navigation, mega menu

**8. Media Gallery Organism**
- **Components:** Multiple images + Thumbnails + Navigation arrows + Lightbox
- **Purpose:** Display image/video collection
- **Recognition:** Grid or carousel of media items with controls

**9. Comment Section Organism**
- **Components:** Multiple media object molecules (avatar + comment) + Reply buttons + Sorting
- **Purpose:** User-generated content display
- **Recognition:** Nested comment threads with user information

**10. Dashboard Widget Organism**
- **Components:** Heading + Stats molecules + Chart/graph + Action buttons
- **Purpose:** Display metrics and data visualization
- **Recognition:** Self-contained data display with title and controls

**Recognition Strategy:**

1. **Identify distinct interface sections**
   - Does this feel like a "complete section"?
   - Could you name it as a single entity? (header, footer, hero)
   - Does it combine multiple molecules?

2. **Test complexity threshold**
   - Contains molecules → Likely organism
   - Contains only atoms → Likely molecule
   - Contains other organisms → Likely template

3. **Check reusability**
   - Can it appear on multiple pages unchanged?
   - YES → Organism
   - NO (page-specific) → May be part of template

4. **Verify functional completeness**
   - Does it perform a complete function on its own?
   - YES → Organism
   - NO (needs other sections) → Part of template/page

**Recognition in Different Sources:**

**HTML/CSS:**
- Look for: `<header>`, `<footer>`, `<section>`, `<article>` semantic tags
- Check class names: `.header`, `.hero`, `.card-grid`, `.main-nav`, `.footer`
- Pattern: Container divs with multiple child molecules

**Figma:**
- Top-level components containing multiple molecules
- Sections marked with section frames
- Components with complex nested structure

**Screenshots:**
- Large interface sections with clear visual boundaries
- Sections containing multiple smaller components
- Repeated complex patterns (card grids, navigation menus)

**Behavioral Patterns (Atlassian ADG Approach):**

Modern systems (2025) emphasize **how components feel**, not just structure:
- **Animation behavior:** How organism transitions/animates
- **Interaction patterns:** How user interacts with organism
- **Responsive behavior:** How organism adapts to viewport changes

Reference: [Atomic Design in 2025: From Rigid Theory to Flexible Practice](https://medium.com/design-bootcamp/atomic-design-in-2025-from-rigid-theory-to-flexible-practice-91f7113b9274)

#### Common Mistakes
- **Organism vs template confusion** — Organisms are reusable sections; templates are page layouts
- **Over-nesting** — If an organism contains other organisms, consider if it's actually a template
- **Missing the boundary** — Organisms should have clear visual/functional boundaries
- **Ignoring semantic meaning** — Name organisms by function (header, hero) not structure

#### See Also
- [4. Molecule Recognition](#4-molecule-recognition)
- [6. Templates vs Pages](#6-templates-vs-pages)
- [8. Source-Specific Recognition](#8-source-specific-recognition)

---
