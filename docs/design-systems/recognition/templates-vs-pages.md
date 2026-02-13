---
description: Distinguish between layout structures (templates) and real implementations (pages)
---

# Templates vs Pages

## When to Use

> Use when analyzing page-level patterns. Use to distinguish layout structures from actual implementations.

## Decision

| Characteristic | Template | Page |
|----------------|----------|------|
| **Content Type** | Placeholder/Lorem ipsum | Real content |
| **Purpose** | Show layout structure | Show actual implementation |
| **Variations** | One template, many pages | Multiple pages from one template |
| **Testing Focus** | Layout flexibility | Content edge cases |
| **Figma/Design Tools** | Component with placeholder text/images | Instance with real content |

## Pattern

**Templates — "Page-level layouts that place organisms into structure"**

**Characteristics:**
- No real content (placeholder text, stock images, dummy data)
- Shows structure (content areas, regions, slots)
- Layout rules (spacing, alignment, responsive behavior)
- Content-agnostic (works with any fitting content)

**What Templates Define:**
- Grid system and column structure
- Organism placement (header at top, sidebar on left)
- Content area dimensions
- Responsive breakpoints and layout shifts

**Example Templates:**
- Homepage Template: Header + Hero + 3-column features + CTA + Footer
- Blog Template: Header + Sidebar + Main content + Related posts + Footer
- Dashboard Template: Top nav + Side nav + Main panel + Widget grid

**Pages — "Concrete instances of templates with real data"**

**Characteristics:**
- Real content (actual headlines, product photos, user data)
- Tests edge cases (long headlines, missing images, empty states)
- Shows variations (different user states, content scenarios)
- Validates design system (proves patterns work)

**What Pages Reveal:**
- Copy length issues (headline too long)
- Translation problems (German text longer than English)
- Missing content scenarios (no reviews, empty cart)
- Real image quality and aspect ratios

**Example Pages from Same Template:**
- Homepage (logged out) — Generic welcome
- Homepage (logged in) — Personalized content
- Homepage (new user) — Onboarding flow
- Homepage (mobile) — Condensed layout

**Recognition Strategy:**

```
1. Check content authenticity
   - Placeholder text (Lorem ipsum) → Template
   - Real text (actual product names) → Page

2. Assess purpose
   - Shows layout structure → Template
   - Shows real-world implementation → Page

3. Count variations
   - One instance showing pattern → Template
   - Multiple instances with different content → Pages

4. Identify focus
   - Testing layout flexibility → Template
   - Testing content edge cases → Page
```

**Source Recognition:**

- **Figma**: Templates = master components with placeholders; Pages = instances with overridden text/images
- **HTML/CSS**: Templates = files with `{variable}` placeholders; Pages = hardcoded content or data-bound values
- **Screenshots**: Templates = stock photos, Lorem ipsum; Pages = real product photos, actual headlines

## Common Mistakes

- **Wrong**: Real content classified as template → **Right**: Real content = page, even if similar to template
- **Wrong**: Only one page variation documented → **Right**: Multiple pages show edge cases (long titles, empty states)
- **Wrong**: Skipping templates entirely → **Right**: Templates document layout patterns
- **Wrong**: Organisms classified as templates → **Right**: Organisms = reusable sections; templates = full-page layouts

## See Also

- [Organism Recognition](./organism-recognition.md)
- [Source-Specific Recognition](./figma-analysis.md)
- [Validation Checklist](./validation-checklist.md)
- Reference: [Atomic Design Templates/Pages](https://atomicdesign.bradfrost.com/chapter-2/#templates)
- Reference: [Pages and Templates in Atomic Design](https://designsystemcentral.com/pages-templates-in-atomic-design/69/)
