---
description: Design system recognition — 8. source-specific recognition
---

## 8. Source-Specific Recognition

### 8.1 HTML/CSS Analysis

#### When to Use This Section
- You're analyzing an HTML design system or component library
- You need to extract design tokens from CSS custom properties
- You're reverse-engineering an existing website's design system

#### Pattern: CSS Custom Properties as Tokens

**Reference Sources:**
- CSS variables guide: [The developer's guide to design tokens and CSS variables](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- Token organization: [Design Tokens using CSS custom properties](https://backlight.dev/docs/design-tokens-using-css-custom-properties)
- Token layers: [Simple Design Tokens with CSS Custom Properties](https://medium.com/design-bootcamp/simple-design-tokens-with-css-custom-properties-7ab69b71d8ad)

**Recognition Process:**

**Step 1: Extract Token Definitions**

Look for `:root` or `html` selector in CSS:

```css
:root {
  /* Color tokens */
  --color-blue-500: #0052CC;
  --color-primary: var(--color-blue-500);

  /* Typography tokens */
  --font-size-base: 16px;
  --font-size-lg: 1.25rem;

  /* Spacing tokens */
  --space-2: 8px;
  --space-4: 16px;

  /* Surface tokens */
  --border-radius-md: 8px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.1);
}
```

**Step 2: Identify Token Layers**

Modern systems use **3-layer abstraction**:

1. **Global Primitives (Reference Tokens)**
   - Raw values
   - Example: `--color-blue-600: #0052CC;`

2. **Semantic Mappings (Semantic Tokens)**
   - Contextual meaning
   - Example: `--color-interactive: var(--color-blue-600);`

3. **Component-Specific Tokens**
   - Application-specific
   - Example: `--button-background: var(--color-interactive);`

**Step 3: Map CSS Classes to Components**

**Class Naming Patterns:**

| Pattern | Example | Component Type |
|---------|---------|----------------|
| `.btn`, `.button` | `<button class="btn">` | Atom (button) |
| `.form-field` | `<div class="form-field">` | Molecule |
| `.card` | `<div class="card">` | Molecule/Organism |
| `.header`, `.nav` | `<header class="header">` | Organism |

**BEM Naming Recognition:**

Block-Element-Modifier methodology indicates component boundaries:

```html
<!-- Block = Molecule/Organism -->
<div class="card">
  <!-- Element = Atom within block -->
  <h2 class="card__title">Title</h2>
  <p class="card__text">Content</p>
  <!-- Modifier = Variant -->
  <button class="card__button card__button--primary">CTA</button>
</div>
```

**Recognition rules:**
- **Block** (`.card`) = Component boundary
- **Element** (`.card__title`) = Child atom
- **Modifier** (`.card__button--primary`) = Variant state

**Step 4: Identify Component Boundaries**

**Semantic HTML as Boundaries:**

| HTML Element | Likely Component Type |
|--------------|----------------------|
| `<button>`, `<input>`, `<label>` | Atoms |
| `<form>` with multiple inputs | Molecule/Organism |
| `<header>`, `<footer>`, `<nav>` | Organisms |
| `<section>`, `<article>` | Organisms/Templates |
| `<main>` with layout | Template |

**Wrapper Patterns:**

Consistent wrapper classes indicate molecules:
- `.search-bar` wrapping input + button
- `.form-group` wrapping label + input
- `.media-object` wrapping image + text

**Step 5: Extract Theme Variations**

**Dark Mode Recognition:**

```css
:root {
  --color-background: #ffffff;
  --color-text: #000000;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #1a1a1a;
    --color-text: #ffffff;
  }
}
```

Or class-based:

```css
.theme-dark {
  --color-background: #1a1a1a;
  --color-text: #ffffff;
}
```

**Recognition cues:**
- `prefers-color-scheme` media query
- `.theme-dark`, `.dark-mode` classes
- Same token names, different values

#### Common Mistakes
- **Missing token references** — Some tokens reference others via `var()`; track the chain
- **Ignoring computed values** — Browser DevTools shows computed values; you need source definitions
- **Confusing utility classes with components** — `.mt-4`, `.text-center` are utilities, not atoms
- **Overlooking cascade specificity** — Component tokens may override global tokens; note specificity

#### See Also
- [1. Foundation Layer: Design Tokens](#1-foundation-layer-design-tokens)
- [2. Component Classification Framework](#2-component-classification-framework)
- [10. Standards & Specifications](#10-standards-specifications)

---

### 8.2 Figma Analysis

#### When to Use This Section
- You're analyzing a Figma design file to extract a design system
- You need to map Figma components to atomic hierarchy
- You're documenting a design system from Figma source

#### Pattern: Figma Component Hierarchy Recognition

**Reference Sources:**
- Figma components: [2025 Figma Walkthrough — Components and Variants](https://medium.com/@ashish.garg25/2025-figma-walkthrough-components-and-variants-5f1c1de507b5)
- Building libraries: [How to Build and Document a Scalable Component Library in Figma](https://designilo.com/2025/07/08/how-to-build-and-document-a-scalable-component-library-in-figma/)
- Token-based approach: [How to Build a Token-Based Component Library in Figma](https://designilo.com/2025/07/10/how-to-build-a-token-based-component-library-in-figma/)
- Auto-layout: [Auto Layout & Variants in Figma: Design Hacks Guide](https://svitla.com/blog/hacks-creating-designs-with-auto-layout-and-variants-in-figma/)

**Step 1: Identify Design Tokens in Figma**

**Figma Variables (Design Tokens):**

Since June 2023, Figma supports **variables** as design tokens:

**Variable Types:**
- **Color:** Fill, stroke, effect colors
- **Number:** Spacing, sizing, opacity values
- **String:** Text content, font family names
- **Boolean:** Show/hide states

**Recognition Strategy:**
- Open **Local variables** panel (Design tab)
- Variables organized in collections (Light, Dark, etc.)
- Variable naming: `color/primary`, `spacing/md`, `border-radius/lg`

**Figma Styles (Legacy Tokens):**

Pre-variable era token system:
- **Color styles:** Named color swatches
- **Text styles:** Typography presets
- **Effect styles:** Shadow/blur effects
- **Grid styles:** Layout grid definitions

**Step 2: Map Figma Components to Atomic Hierarchy**

**Figma Component Structure:**

```
Components (Assets Panel)
├── Atoms
│   ├── Button
│   ├── Input
│   └── Icon
├── Molecules
│   ├── Search Bar
│   ├── Form Field
│   └── Card
└── Organisms
    ├── Header
    ├── Footer
    └── Navigation
```

**Naming Convention Recognition:**

Figma uses **slash naming** for hierarchy:

| Figma Name | Component Type | Reasoning |
|------------|----------------|-----------|
| `Button/Primary` | Atom variant | Single element |
| `Form/Field/Text` | Molecule | Compound element |
| `Navigation/Header/Desktop` | Organism | Complex section |

**Recognition rules:**
- **Single level** (`Button`) = Likely atom
- **Two levels** (`Form/Field`) = Likely molecule
- **Three+ levels** (`Navigation/Header/Desktop`) = Likely organism

**Step 3: Analyze Component Sets & Variants**

**Component Sets** group variants of the same component:

Example: Button component set
- **Properties:** Size (sm, md, lg), State (default, hover, active), Type (primary, secondary)
- **Variants:** All combinations (sm/primary/default, md/secondary/hover, etc.)

**Recognition Strategy:**
- Component set icon: purple diamond with 4 smaller diamonds
- Right panel shows **Properties** and **Values**
- Each variant is an instance of the set

**Variants indicate:**
- Same component, different states/sizes
- NOT different component types
- Example: `Button/Primary` and `Button/Secondary` are variants, not separate atoms

**Step 4: Identify Auto-Layout Patterns**

**Auto-Layout** indicates designed spacing system:

**Recognition Cues:**
- Blue outline when selected (indicates auto-layout frame)
- **Spacing between items:** Shows spacing token value
- **Padding:** Shows inset spacing token
- **Direction:** Horizontal or vertical stacking

**Auto-Layout Properties:**
- **Direction:** Row (horizontal) or Column (vertical)
- **Spacing:** Gap between children
- **Padding:** Internal spacing
- **Alignment:** Flex alignment properties
- **Resizing:** Hug contents or Fill container

**Spacing Token Extraction:**
- Note spacing values (8px, 16px, 24px)
- Consistent values indicate spacing scale
- Map to design token system

**Step 5: Extract Layout Grids**

**Grid Styles** define layout systems:

**Grid Types:**
- **Rows:** Horizontal layout grid
- **Columns:** Vertical grid system (12-col, 16-col, etc.)
- **Grid:** Square grid for alignment

**Recognition Strategy:**
- Check frame **Layout Grid** properties
- Note column count, gutter size, margin size
- Identifies responsive breakpoint system

**Example Analysis:**
- Desktop: 12 columns, 24px gutter, 80px margin
- Tablet: 8 columns, 16px gutter, 40px margin
- Mobile: 4 columns, 16px gutter, 20px margin

**Step 6: Map Component Nesting**

**Component Instance Recognition:**

In Figma, components can contain other components:

**Hierarchy Indicators:**
- **Atom:** Contains no component instances (only shapes/text)
- **Molecule:** Contains 2-3 atom instances
- **Organism:** Contains molecule instances or many atoms
- **Template:** Full-frame layout with organism instances

**How to Check:**
1. Select component
2. Expand layers panel
3. Look for purple diamond icons (component instances)
4. Count nested components → Determines hierarchy level

#### Common Mistakes
- **Confusing variants with separate components** — Variants are states of same component
- **Missing variable collections** — Modern Figma uses variables, not just styles
- **Ignoring auto-layout spacing** — Auto-layout values ARE spacing tokens
- **Treating frames as components** — Frames are containers; components are reusable elements

#### See Also
- [1. Foundation Layer: Design Tokens](#1-foundation-layer-design-tokens)
- [2. Component Classification Framework](#2-component-classification-framework)
- [8.1 HTML/CSS Analysis](#81-htmlcss-analysis)

---

### 8.3 Screenshot Analysis

#### When to Use This Section
- You're analyzing UI screenshots to extract design patterns
- You need to recognize components without access to source files
- You're documenting a competitor's design system from visual inspection

#### Pattern: Visual Pattern Recognition

**Reference Sources:**
- Computer vision for UI: [Computer Vision for UI Testing: Leveraging Image](https://www.techrxiv.org/users/898550/articles/1282199/master/file/data/Computer_Vision_for_UI_Testing_Himanshu_Pathak/Computer_Vision_for_UI_Testing_Himanshu_Pathak.pdf?inline=true)
- UI component recognition: [How Do You Use Deep Learning to Identify UI Components?](https://www.alibabacloud.com/blog/how-do-you-use-deep-learning-to-identify-ui-components_597859)
- Visual testing: [AI-Assisted Visual Testing: Beyond Screenshots with Intelligent UI Validation](https://www.deepakkamboj.com/blog/ai-assisted-visual-testing/)
- Screenshot understanding: [Turning Screenshots into Data](https://medium.com/data-science-collective/turning-screensots-int-data-html-126bdcaa4821)

**Step 1: Identify Visual Boundaries**

**Recognition Cues:**

| Visual Pattern | Indicates... | Component Type |
|----------------|--------------|----------------|
| **Consistent spacing** | Intentional grouping | Molecule/Organism |
| **Visual container** (border/shadow/background) | Component boundary | Molecule/Organism |
| **Repeated patterns** | Reusable component | Atom/Molecule |
| **Color consistency** | Semantic token usage | Token system |
| **Typographic hierarchy** | Type scale | Token system |

**Layout Analysis Process:**
1. **Identify major sections** — Header, main content, sidebar, footer
2. **Mark visual boundaries** — Boxes, cards, panels, groups
3. **Note repeated patterns** — Same component used multiple times
4. **Observe spacing** — Consistent gaps indicate spacing system

**Step 2: Extract Color Tokens**

**Visual Color Sampling:**

1. **Identify all unique colors** in screenshot
2. **Group similar shades** — Likely from same color family
3. **Count shade variations** — 3-11 shades suggests structured palette
4. **Note semantic usage** — Primary actions, errors, success states

**Recognition Patterns:**

- **Numbered scale appearance:**
  - Very light → Light → Medium → Dark → Very dark
  - Consistent visual progression
  - 5-11 steps per hue

- **Semantic color usage:**
  - Blue for primary actions (buttons, links)
  - Red for errors/destructive actions
  - Green for success/confirmation
  - Yellow/orange for warnings
  - Gray for neutral elements

**Step 3: Recognize Typography Hierarchy**

**Visual Type Analysis:**

1. **Count distinct font sizes** — Modern systems use 6-8 sizes
2. **Measure visual progression** — Equal visual spacing suggests modular scale
3. **Identify font weights** — Light, regular, semibold, bold
4. **Note font families** — Headings vs body text

**Recognition Cues:**

- **Modular scale appearance:**
  - Each level noticeably larger than previous
  - Consistent size jumps
  - Example: 12px → 16px → 20px → 24px → 32px

- **Font weight hierarchy:**
  - Headings: Bold (700) or Semibold (600)
  - Body: Regular (400)
  - Captions/labels: Regular (400) or Light (300)

**Step 4: Identify Spacing System**

**Visual Spacing Recognition:**

**How to Measure:**
1. Use screenshot in design tool (Figma, Sketch)
2. Measure gaps between elements
3. Look for consistent values

**Common Patterns:**

| Measured Gap | Likely Base Unit | System Type |
|--------------|------------------|-------------|
| 8, 16, 24, 32, 40, 48 | 8px | 8px linear |
| 4, 8, 12, 16, 20, 24 | 4px | 4px linear |
| 8, 16, 32, 64 | 8px | 8px geometric |

**Visual Cues:**
- **Consistent alignment** — Elements align to invisible grid
- **Predictable gaps** — Same spacing repeated throughout
- **Visual rhythm** — Regular vertical spacing between sections

**Step 5: Classify Components**

**Atom Recognition in Screenshots:**

Look for:
- **Buttons** — Rectangular with text, consistent styling
- **Inputs** — Text fields with borders
- **Icons** — Small, monochromatic graphics
- **Badges** — Small labels with background color
- **Avatars** — Circular images (profile photos)

**Molecule Recognition in Screenshots:**

Look for:
- **Search bars** — Input + icon/button
- **Form fields** — Label + input + error text
- **Cards** — Container with image + text + button
- **Nav items** — Icon + text link

**Organism Recognition in Screenshots:**

Look for:
- **Headers** — Top section with logo + nav + actions
- **Footers** — Bottom section with links + info
- **Card grids** — Multiple cards in grid layout
- **Forms** — Multiple form fields grouped
- **Data tables** — Rows and columns with headers

**Step 6: Identify Design System Patterns**

**Modern Design System Indicators:**

| Visual Pattern | Indicates... | Reference System |
|----------------|--------------|------------------|
| Rounded corners (4-8px) | Border radius tokens | Material, Bootstrap |
| Subtle shadows on cards | Elevation system | Material Design |
| Numbered color scales visible | Tailwind-style palette | Tailwind CSS |
| Consistent icon style | Icon system | Heroicons, Font Awesome |
| Grid-based layout | Layout tokens | Bootstrap Grid, CSS Grid |

**Design System Fingerprints:**

- **Material Design:**
  - Floating action button (FAB)
  - Elevation shadows
  - Ripple effects on buttons
  - Roboto font

- **Bootstrap:**
  - 12-column grid visible alignment
  - Rounded corners (0.25rem default)
  - Blue primary color (#0d6efd)
  - Button group patterns

- **Tailwind:**
  - Utility-first appearance (tight composition)
  - Gray scale from slate/zinc families
  - Rounded corners (0.375rem default)
  - Specific blue shades (sky-500)

- **Shopify Polaris:**
  - Green primary color
  - Tight spacing
  - Sans-serif (Inter font)
  - Subtle borders

#### Common Mistakes
- **Guessing instead of measuring** — Always measure spacing/sizes when possible
- **Missing visual boundaries** — Subtle backgrounds/borders define component boundaries
- **Ignoring repeated patterns** — Same visual pattern = reusable component
- **Overlooking shadows/elevation** — Shadow depth indicates hierarchy level

#### See Also
- [1. Foundation Layer: Design Tokens](#1-foundation-layer-design-tokens)
- [2. Component Classification Framework](#2-component-classification-framework)
- [9. Reference Design Systems](#9-reference-design-systems)

---

### 8.4 Tailwind CSS Token Identification

#### When to Use This Section
- You're analyzing a design that uses Tailwind CSS
- You need to map Tailwind utility classes to design tokens
- You're identifying DaisyUI semantic tokens in a Tailwind-based design

#### Pattern: Tailwind Class-to-Token Mapping

When analyzing a Tailwind-based design, tokens are expressed through utility class naming conventions rather than CSS custom properties.

**Color Tokens:**

| Tailwind Class Pattern | Token Type | Example |
|---|---|---|
| `bg-*` | Background color | `bg-blue-500`, `bg-slate-100` |
| `text-*` (color context) | Text color | `text-gray-900`, `text-red-600` |
| `border-*` | Border color | `border-gray-200` |
| `ring-*` | Ring/outline color | `ring-blue-500` |

In Tailwind v4, these map to `--color-*` CSS variables generated from the `@theme {}` block.
In Tailwind v3, these map to values defined in `tailwind.config.js` under `theme.extend.colors`.

**Spacing Tokens:**

| Tailwind Class Pattern | Token Type | Scale |
|---|---|---|
| `p-*`, `px-*`, `py-*` | Padding | 4px base unit (v3), CSS-first in v4 |
| `m-*`, `mx-*`, `my-*` | Margin | Same scale as padding |
| `gap-*` | Flex/grid gap | Same scale |
| `space-x-*`, `space-y-*` | Child spacing | Same scale |

Common scale values: `0.5` = 2px, `1` = 4px, `2` = 8px, `4` = 16px, `8` = 32px, `16` = 64px.

**Typography Tokens:**

| Tailwind Class Pattern | Token Type | Examples |
|---|---|---|
| `text-xs` through `text-9xl` | Font size | `text-sm` (14px), `text-base` (16px), `text-lg` (18px) |
| `font-thin` through `font-black` | Font weight | `font-normal` (400), `font-semibold` (600), `font-bold` (700) |
| `font-sans`, `font-serif`, `font-mono` | Font family | Maps to `--font-*` CSS variables |
| `leading-*` | Line height | `leading-tight` (1.25), `leading-normal` (1.5) |
| `tracking-*` | Letter spacing | `tracking-tight` (-0.025em), `tracking-wide` (0.025em) |

**Token Definition Locations:**

| Tailwind Version | Token Source | Recognition Cue |
|---|---|---|
| v4 (CSS-first) | `@theme {}` block in CSS file | No `tailwind.config.js`, tokens in CSS with `@theme` |
| v3 (config-first) | `tailwind.config.js` under `theme.extend` | Config file with `module.exports` |

#### Pattern: DaisyUI Semantic Tokens

DaisyUI adds a semantic token layer on top of Tailwind's utility classes:

**Recognition Cues:**

| DaisyUI Class Pattern | Token Type | Maps To |
|---|---|---|
| `btn-primary`, `btn-secondary` | Action colors | `--p`, `--s` CSS variables |
| `bg-base-100`, `bg-base-200`, `bg-base-300` | Surface hierarchy | `--b1`, `--b2`, `--b3` CSS variables |
| `text-base-content`, `text-primary-content` | Text on surface | `--bc`, `--pc` CSS variables |
| `alert-info`, `alert-success`, `alert-error` | Status colors | `--in`, `--su`, `--er` CSS variables |

DaisyUI uses OKLCH color format internally and provides 30+ predefined themes.

**Key Difference from Raw Tailwind:**
- Tailwind utilities describe **appearance** (`bg-blue-500`)
- DaisyUI classes describe **purpose** (`btn-primary`, `bg-base-100`)
- DaisyUI themes swap underlying values; Tailwind utilities are static

#### Common Mistakes
- **Treating Tailwind utility classes as component classes** — `mt-4`, `flex`, `text-center` are utilities, not component boundaries. Look for wrapper elements or component framework markup (React, Vue) for component identification
- **Assuming Tailwind v3 config when v4 is used** — v4 has no `tailwind.config.js`. Check for `@theme {}` in CSS files
- **Ignoring DaisyUI semantic layer** — If `btn-primary` or `bg-base-*` classes appear, the design uses DaisyUI's semantic tokens, not raw Tailwind colors
- **Reading spacing values wrong** — Tailwind's `p-4` is 16px (4 * 4px), not 4px

#### See Also
- [1.3 Spacing Token Recognition](#13-spacing-token-recognition)
- [8.1 HTML/CSS Analysis](#81-htmlcss-analysis)
- `design-system-tailwind.md` — full Tailwind documentation
