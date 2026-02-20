---
description: Design system recognition — 4. molecule recognition
---

## 4. Molecule Recognition




#### When to Use This Section
- You've identified atoms and now need to find grouped patterns
- You're analyzing composite components that combine 2-3 atoms
- You need to determine if a component is a molecule vs organism

#### Decision Table: Molecule vs Not-Molecule

| Component Has... | Classification | Reasoning |
|------------------|----------------|-----------|
| 2-3 atoms, single purpose | **Molecule** | Simple functional group |
| 1 atom only | **Atom** | Not composite |
| Many atoms, multiple purposes | **Organism** | Too complex |
| Layout structure for organisms | **Template** | Page-level organization |

#### Pattern: Common Molecule Types

**Reference Sources:**
- Molecule examples: [https://atomicdesign.bradfrost.com/chapter-2/#molecules](https://atomicdesign.bradfrost.com/chapter-2/)
- Card molecules: [Atomic design components in UI design](https://blog.logrocket.com/ux-design/atomic-design-components-ui-design/)
- Form molecules: [Building design systems with atomic design](https://medium.com/design-bootcamp/building-design-systems-with-atomic-design-fd21e86f34c5)

**Molecule Catalog:**

**1. Form Field Molecule**
- **Atoms:** Label + Input + (optional) Error message
- **Purpose:** Single data entry point
- **Recognition:** Always appears together as unit
- **Example:** "Email" label + text input + "Invalid email" error

**2. Search Bar Molecule**
- **Atoms:** Input + Button + (optional) Icon
- **Purpose:** Search functionality
- **Recognition:** Input with attached submit button
- **Example:** Search input + magnifying glass icon + "Search" button

**3. Card Content Molecule**
- **Atoms:** Image + Heading + Text + (optional) Button
- **Purpose:** Present discrete content unit
- **Recognition:** Consistently grouped content block
- **Example:** Product photo + product name + price + "Add to cart" button

**4. Navigation Item Molecule**
- **Atoms:** Link + Icon
- **Purpose:** Single navigation element
- **Recognition:** Clickable navigation element with visual indicator
- **Example:** Home icon + "Home" link

**5. Media Object Molecule**
- **Atoms:** Image/Avatar + Text block
- **Purpose:** Content with associated media
- **Recognition:** Fixed-size image aligned with text
- **Example:** User avatar + comment text

**6. Button Group Molecule**
- **Atoms:** 2-3 related buttons
- **Purpose:** Mutually exclusive or related actions
- **Recognition:** Visually connected buttons
- **Example:** "Cancel" + "Save" buttons or segmented control

**7. Breadcrumb Molecule**
- **Atoms:** Multiple links + Dividers
- **Purpose:** Show navigation hierarchy
- **Recognition:** Horizontal path of links with separators
- **Example:** Home > Products > Category > Item

**8. Stats Display Molecule**
- **Atoms:** Icon + Number + Label
- **Purpose:** Show single metric
- **Recognition:** Data visualization unit
- **Example:** Heart icon + "1,234" + "Likes"

**9. Alert/Toast Molecule**
- **Atoms:** Icon + Message + Close button
- **Purpose:** Show notification
- **Recognition:** Temporary message container
- **Example:** Warning icon + "Changes saved" + X button

**10. Pagination Control Molecule**
- **Atoms:** Previous button + Page numbers + Next button
- **Purpose:** Navigate through pages
- **Recognition:** Sequential navigation controls
- **Example:** "< Prev" + "1 2 3" + "Next >"

**Recognition Strategy:**

1. **Identify functional grouping**
   - Do these atoms always appear together?
   - Do they serve a single purpose?
   - Can they be reused as a unit?

2. **Count components**
   - 2-3 atoms → Likely molecule
   - 4+ atoms or multiple molecules → Likely organism

3. **Test single responsibility**
   - Does it do ONE thing well?
   - YES → Molecule
   - NO (multiple purposes) → Organism

4. **Check independence**
   - Can it exist outside its current context?
   - YES → Molecule
   - NO (context-dependent) → May be part of organism

**Recognition in Different Sources:**

**HTML/CSS:**
- Look for: Wrapper divs containing multiple atoms
- Check class names: `.search-bar`, `.card`, `.form-field`, `.nav-item`
- Pattern: Consistent grouping in markup

**Figma:**
- Component sets with variants (button group states)
- Components containing multiple atom instances
- Named groups in component structure

**Screenshots:**
- Repeated patterns of atoms appearing together
- Visual boundaries around grouped elements
- Consistent spacing between grouped atoms

#### Common Mistakes
- **Molecule bloat** — Adding too many atoms makes it an organism; keep molecules simple
- **Confusing with organisms** — If it contains other molecules, it's an organism
- **Missing the group** — Individual atoms used together aren't a molecule unless intentionally grouped
- **Over-molecularizing** — Not every atom pairing needs to be a molecule; only if reused as unit

#### See Also
- [3. Atom Recognition](#3-atom-recognition)
- [5. Organism Recognition](#5-organism-recognition)
- [2. Component Classification Framework](#2-component-classification-framework)

---
