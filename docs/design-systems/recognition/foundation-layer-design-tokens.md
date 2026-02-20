---
description: Design system recognition — 1. foundation layer: design tokens
---

## 1. Foundation Layer: Design Tokens

### When to Use This Section
- You're looking at ANY design system source and need to identify the foundational values
- You need to extract design decisions from CSS custom properties, Figma styles, or JSON files
- You're mapping visual patterns to a structured token system

### 1.1 Color Token Recognition

#### Decision Table: Identifying Color Systems

| If You See... | It's Probably... | Token Category |
|---------------|------------------|----------------|
| Numbered scales (50-950) | Tailwind-style palette | Reference tokens (primitives) |
| Semantic names (primary, surface, on-surface) | Material Design 3 style | Semantic tokens |
| `--color-*` CSS custom properties | Token implementation | Token variables |
| RGB/Hex values in JSON with `$type: "color"` | W3C DTCG format | Standard tokens |
| OKLCH/OKLAB values | Modern color space | Perceptually uniform tokens |
| Color + "light/dark" variants | Theme-aware system | Contextual tokens |

#### Pattern: Modern Color Token Structure

**Hierarchical Organization (3 layers):**

```
Reference Tokens (Primitives)
  ↓
Semantic Tokens (Context)
  ↓
Component Tokens (Application)
```

**Reference Sources:**
- Tailwind CSS palette: [https://tailwindcss.com/docs/colors](https://tailwindcss.com/docs/colors)
- Material Design 3 color system: [Design Tokens & Theming guide](https://materialui.co/blog/design-tokens-and-theming-scalable-ui-2025)
- W3C DTCG spec: [https://www.designtokens.org/tr/drafts/format/](https://www.designtokens.org/tr/drafts/format/)
- OKLCH color space: [OKLCH in CSS guide](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)

**Recognition Cues:**

1. **Numbered Scales (Tailwind-style)**
   - Look for: `50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`
   - Pattern: Lower numbers = lighter, higher numbers = darker
   - Base tone typically at `500`
   - Example naming: `gray-50`, `blue-500`, `red-950`

2. **Semantic Names (Material Design 3)**
   - Look for: `primary`, `secondary`, `tertiary`, `error`, `surface`, `on-primary`, `on-surface`
   - Pattern: Color role names that describe function, not appearance
   - "On-" prefix indicates contrasting text/icon color
   - Theme-aware (light/dark mode variations)

3. **CSS Custom Properties**
   - Look for: `--color-*`, `--clr-*`, or similar prefixes
   - Pattern: Defined at `:root` level for global tokens
   - May use `var()` references to other tokens
   - Example: `--color-primary: var(--color-blue-500);`

4. **W3C DTCG JSON Format**
   - Look for: Objects with `$value` and `$type` properties
   - Required: `$type: "color"`
   - Optional: `$description`, `$deprecated`
   - Example structure: See [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/)

5. **OKLCH/OKLAB Values**
   - Look for: `oklch()` or `oklab()` CSS functions
   - Pattern: `oklch(L C H)` where L=lightness, C=chroma, H=hue
   - Perceptually uniform (equal visual spacing between shades)
   - Modern browsers support (Chrome, Safari, Firefox)

**Contrast & Accessibility:**

Recognize WCAG compliance indicators:
- **WCAG 2.2 Level AA:** 4.5:1 for normal text, 3:1 for large text (18pt+/14pt+ bold)
- **WCAG 2.2 Level AAA:** 7:1 for normal text, 4.5:1 for large text
- **Non-text elements:** 3:1 minimum contrast
- Reference: [WCAG Contrast Requirements](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

**Why 3-Layer Token Hierarchy Matters:**

**What breaks with only 1 or 2 layers:**
- **1-layer systems (raw values only):** Every component hardcodes hex values. Changing brand colors requires find-replace across hundreds of files. Theming is impossible. Multi-brand support requires duplicating entire codebases.
- **2-layer systems (raw + semantic):** Components still couple to semantic tokens. Rebranding means updating semantic token values, but components like Button can't have component-specific overrides without breaking the semantic layer's meaning.
- **3-layer systems (raw + semantic + component):** Reference tokens change without breaking semantics. Semantic tokens change without breaking components. Component tokens provide targeted overrides. Multi-brand/multi-theme systems become possible.

**Best practice:** Tokens should exist in three tiers as documented in [Design Tokens & Theming 2025](https://materialui.co/blog/design-tokens-and-theming-scalable-ui-2025): reference tokens are raw values like `color.blue.500 = #0066cc`, semantic tokens map meaning like `color.primary = color.blue.500`, and component tokens target context like `button.background = color.primary`. Layering is fundamental to avoiding token sprawl and enables teams to change reference values without breaking component logic.

#### Common Mistakes

- **Confusing reference tokens with semantic tokens** — Reference tokens are raw values (blue-500); semantic tokens are contextual mappings (color-primary). **What goes wrong:** Teams use raw tokens directly in components, making rebranding impossible without global find-replace.
- **Ignoring color space** — OKLCH provides better perceptual uniformity than HSL/RGB for palette generation. **What goes wrong:** HSL-based palettes have uneven brightness progression (yellow-500 appears lighter than blue-500 at same L value), breaking visual hierarchy and making accessible color pairs harder to maintain.
- **Missing theme variants** — Modern systems often have light/dark/high-contrast variants for the same semantic token. **What goes wrong:** Teams build separate component sets for dark mode instead of swapping token values, creating maintenance burden and version drift.
- **Overlooking composite tokens** — Some color systems include alpha/opacity as part of the token structure. **What goes wrong:** Components hardcode opacity values (rgba(color, 0.5)), making it impossible to adjust transparency systematically for accessibility or theming needs.
- **Skipping accessibility validation** — Color pairs may look fine but fail WCAG contrast requirements. **What goes wrong:** Common color blindness issues include red/green confusion (deuteranopia affects 6% of males), blue/yellow confusion (tritanopia), and reduced contrast sensitivity. Using only color to convey meaning (red = error, green = success) without icons or text makes interfaces unusable for 8% of male users and 0.5% of female users. Reference: [Designing for Colorblindness](https://www.smashingmagazine.com/2024/02/designing-for-colorblindness/)

#### See Also
- [1.2 Typography Token Recognition](#12-typography-token-recognition)
- [8.1 HTML/CSS Analysis](#81-htmlcss-analysis)
- [10. Standards & Specifications](#10-standards-specifications)

---

### 1.2 Typography Token Recognition

#### Decision Table: Identifying Typography Systems

| If You See... | It's Probably... | Recognition Strategy |
|---------------|------------------|----------------------|
| Font sizes with ratio progression (1.25×, 1.333×) | Modular scale | Calculate ratio between adjacent sizes |
| CSS `clamp()` functions for font-size | Fluid typography | Extract min/max viewport ranges |
| Font weight numbers (100-900) | Variable font system | Map to semantic names (light, regular, bold) |
| Line-height as unitless ratio | Typography tokens | Separate from font-size tokens |
| `@font-face` declarations | Custom fonts | Extract font family names and file paths |

#### Pattern: Type Scale Recognition

**Common Modular Scale Ratios:**

| Ratio Name | Multiplier | When to Use |
|------------|------------|-------------|
| Minor Third | 1.200 | Subtle hierarchy, dense content |
| Major Third | 1.250 | **Most common** — balanced hierarchy |
| Perfect Fourth | 1.333 | Strong hierarchy, spacious layouts |
| Perfect Fifth | 1.500 | Dramatic hierarchy |
| Golden Ratio | 1.618 | Mathematical/aesthetic harmony |

**Recognition Process:**
1. Extract all font-size values from the system
2. Divide adjacent sizes to find ratio: `size[n+1] / size[n]`
3. If ratio is consistent (±0.05), it's a modular scale
4. If ratio varies, it may be a custom scale or t-shirt sizing

**Reference Sources:**
- Type scale guide: [The 2025 Guide to Responsive Typography](https://designshack.net/articles/typography/guide-to-responsive-typography-sizing-and-scales/)
- Scale ratios: [Type Scale Calculator](https://www.forgedock.dev/tools/typescale)
- Fluid typography: [Exploring Responsive Type Scales](https://medium.com/sketch-app-sources/exploring-responsive-type-scales-cf1da541be54)

**Token Structure Patterns:**

1. **Semantic Naming (Recommended)**
   - `--font-size-xs`, `--font-size-sm`, `--font-size-base`, `--font-size-lg`, `--font-size-xl`
   - Clear hierarchy without exposing implementation details

2. **Numeric Scale**
   - `--font-size-1`, `--font-size-2`, `--font-size-3` (Material Design style)
   - Abstract numbering, no implied size relationship

3. **Heading Levels**
   - `--font-size-h1`, `--font-size-h2`, `--font-size-h3`
   - Maps directly to HTML heading hierarchy

4. **Contextual Naming**
   - `--font-size-body`, `--font-size-caption`, `--font-size-display`
   - Application-specific, describes usage context

**Fluid Typography Recognition:**

Look for CSS `clamp()` functions:
```css
font-size: clamp(1rem, 0.5rem + 2vw, 2rem);
/*              min    flexible   max    */
```

Pattern indicates:
- Responsive sizing without media queries
- Viewport-based interpolation
- Minimum and maximum constraints

**Font Weight Mapping:**

| Numeric Value | Keyword Name | Common Usage |
|---------------|--------------|--------------|
| 100 | Thin | Rare, decorative |
| 200 | Extra Light | Rare |
| 300 | Light | Subtle emphasis |
| 400 | Regular/Normal | **Body text default** |
| 500 | Medium | Slightly emphasized |
| 600 | Semi Bold | Strong emphasis |
| 700 | Bold | **Headings, strong emphasis** |
| 800 | Extra Bold | Display text |
| 900 | Black | Rare, high impact |

**Typography Best Practices:**

**Why System Font Stacks Matter:**
System fonts load instantly (no network request), provide native look-and-feel, and respect user's OS accessibility settings. [2025 Web Almanac data](https://almanac.httparchive.org/en/2025/fonts) shows generic sans-serif remains the most common family name (89% of pages). Using system fonts spares optimization effort and avoids font-loading performance issues entirely.

**System font stack example (2025 best practice):**
```
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Web Font Performance Trade-offs:**

**FOIT (Flash Of Invisible Text):** Browser shows invisible text until web font downloads. **What goes wrong:** Users see blank screen for 3+ seconds on slow connections. Accessibility failure for screen readers timing out before text renders. SEO impact from delayed content visibility.

**FOUT (Flash Of Unstyled Text):** Browser renders text with fallback font until web font downloads. **What goes wrong:** Layout shifts as web font loads (different metrics than fallback). Visual "pop" distracts users. Better than FOIT but still jarring.

**2025 Best Practice:** Use `font-display: swap` for web fonts, ensuring text is always visible with fallback font until custom font loads. About 12% of sites now preload fonts with `<link rel="preload">` to reduce FOUT duration. [Font performance optimization](https://www.debugbear.com/blog/website-font-performance) shows WOFF2 format (81% of font requests in 2025) provides best compression.

**Performance Impact:** Each web font adds 20-200KB download, plus render-blocking time. High-traffic sites (BBC, GitHub) stick to system fonts for this reason. Use web fonts only when brand identity requires it, and limit to 2-3 font files maximum.

#### Common Mistakes

- **Confusing font-size with line-height** — These are separate token categories (dimension vs ratio). **What goes wrong:** Teams create tokens like `typography-heading-lg` that bundle size + line-height, preventing responsive line-height adjustments.
- **Missing responsive variants** — Modern systems often have mobile vs desktop base sizes. **What goes wrong:** 16px body text readable on desktop becomes too small on mobile. Fixed type scale breaks readability across viewports.
- **Ignoring font loading strategy** — Token analysis should note FOUT/FOIT handling patterns. **What goes wrong:** Beautiful typography tokens mean nothing if users see blank pages for 3 seconds while fonts load. `font-display: swap` is critical for usability.
- **Overlooking variable fonts** — Modern systems may use single variable font file with weight/width axes. **What goes wrong:** Teams load 5 font files (Light, Regular, Semibold, Bold, Black) when one variable font would suffice, bloating page weight unnecessarily.

#### See Also
- [1.3 Spacing Token Recognition](#13-spacing-token-recognition)
- [8.1 HTML/CSS Analysis](#81-htmlcss-analysis)

---

### 1.3 Spacing Token Recognition

#### Decision Table: Identifying Spacing Systems

| If You See... | It's Probably... | Base Unit |
|---------------|------------------|-----------|
| Values divisible by 8 (8, 16, 24, 32) | 8px base system | 8px |
| Values divisible by 4 (4, 8, 12, 16) | 4px base system | 4px |
| T-shirt sizes (xs, sm, md, lg, xl) | Semantic naming | Varies |
| Powers of 2 (2, 4, 8, 16, 32, 64) | Binary progression | 2px |
| Fibonacci sequence (3, 5, 8, 13, 21) | Fibonacci system | Varies |
| Multiplier notation (x1, x2, x3) | Baseline multiplier | Varies |

#### Pattern: Spacing Scale Analysis

**Geometric Progression (Most Common):**

Formula: `base × ratio^n` where n = step number

Example (8px base, 2× ratio):
- Step 0: 8px (8 × 2^0)
- Step 1: 16px (8 × 2^1)
- Step 2: 32px (8 × 2^2)
- Step 3: 64px (8 × 2^3)

**Reference Sources:**
- Atlassian spacing: [https://atlassian.design/foundations/spacing/](https://atlassian.design/foundations/spacing/)
- GitLab Pajamas: [https://design.gitlab.com/product-foundations/spacing/](https://design.gitlab.com/product-foundations/spacing/)
- Spacing best practices: [Spacing systems & scales in UI design](https://blog.designary.com/p/spacing-systems-and-scales-ui-design)

**Recognition Strategies:**

1. **Identify Base Unit**
   - Find smallest spacing value in the system
   - Check if other values are multiples of this base
   - Common bases: 4px, 8px, 10px

2. **Determine Progression Pattern**
   - **Linear:** Each step adds constant value (8, 16, 24, 32)
   - **Geometric:** Each step multiplies by constant ratio (8, 16, 32, 64)
   - **Augmented:** Hybrid approach (GitLab: 8 × 2^n, then n × 1.5 after 16px)

3. **Map Naming Convention**
   - **Numeric:** `space-1`, `space-2`, `space-3`
   - **T-shirt:** `space-xs`, `space-sm`, `space-md`, `space-lg`, `space-xl`
   - **Multiplier:** `space-x1`, `space-x2`, `space-x3`
   - **Contextual:** `space-inline`, `space-stack`, `space-section`

**Common Patterns by System:**

| Design System | Base | Scale | Naming |
|---------------|------|-------|--------|
| Material Design | 8px | Linear (8dp increments) | Numeric |
| Shopify Polaris | 4px | `space-2` = 8px, `space-3` = 12px | Numeric multiplier |
| Atlassian | 8px | Limited set (8, 16, 24, 32) | Pixel values |
| GitLab Pajamas | 8px | Geometric + augmented | Numeric |
| Tailwind CSS | 4px (0.25rem) | `4` = 16px, `8` = 32px | Numeric (× 4px) |

**Layout-Specific Spacing:**

Recognize specialized spacing categories:
- **Inline spacing:** Horizontal gaps (between inline elements)
- **Stack spacing:** Vertical rhythm (between stacked elements)
- **Inset spacing:** Internal padding (component padding)
- **Grid gutters:** Column/row gaps in layouts

**Spacing Best Practices:**

**Why Consistent Spacing Scales Matter:**

**Visual Rhythm and Predictability:** Using a pattern of similar spacing creates predictable rhythm for users to follow. As documented in [Spacing & Alignment in UI](https://www.designsystemscollective.com/spacing-alignment-in-ui-creating-visual-rhythm-and-breathing-room-2c382b112272), consistent vertical spacing makes content feel structured, readable, and intentional. Spacing creates hierarchy—more space means weaker relationship, less space means stronger visual grouping.

**What Goes Wrong with Ad-Hoc Spacing:**
- **Visual chaos:** Interface has 47 different spacing values (12px here, 15px there, 18px somewhere else). No rhythm or predictability. Users can't distinguish which elements are related.
- **Developer confusion:** Team debates whether to use 14px or 16px gap. No system to guide decisions. Every spacing choice becomes a bikeshed discussion.
- **Maintenance nightmare:** Rebranding requires adjusting spacing across hundreds of components with no systematic way to scale up/down. Responsive breakpoints require recreating all spacing rules.
- **Inconsistent grouping:** Related form fields have 20px gap while unrelated sections have 18px gap. Visual hierarchy inverted by accident.

**The 8px Grid System:**

The 8pt grid creates a design language that feels intuitive to both users and teams. By adopting it, you create products easier to scale, easier to hand off, and easier to use. Reference: [The 8pt Grid System Guide](https://www.rejuvenate.digital/news/designing-rhythm-power-8pt-grid-ui-design)

**Why 8px specifically:**
- Divides evenly for responsive scaling (8 → 4 at 0.5× scale)
- Aligns with common screen densities (1×, 1.5×, 2×, 3×)
- Large enough to create noticeable hierarchy differences
- Small enough to provide fine-grained control

**Foundation for Complex Interfaces:** As interfaces grow, complex dashboards, SaaS apps, ecommerce sites, and content-heavy products cannot survive without vertical rhythm. Small spacing mistakes compound into usability and scalability issues. Reference: [Vertical Rhythm in UI](https://uinica.com/vertical-rhythm-in-ui-the-hidden-system-that-makes-interfaces-feel-clean-and-readable/)

#### Common Mistakes

- **Confusing spacing with sizing** — Spacing is gaps/margins; sizing is dimensions (width/height). **What goes wrong:** Teams create tokens like `space-button` instead of `size-button-height`, mixing concerns and preventing proper composition.
- **Missing contextual variants** — Some systems have dense/comfortable/spacious variants. **What goes wrong:** Data tables need tight spacing, but marketing pages need generous whitespace. One spacing scale can't serve both without variant tokens.
- **Ignoring responsive scaling** — Spacing may change at different breakpoints. **What goes wrong:** Desktop spacing (32px sections) creates excessive scrolling on mobile. Fixed spacing prevents proper responsive adaptation.
- **Overlooking negative space philosophy** — Some systems intentionally limit spacing options for consistency. **What goes wrong:** Teams create 15 spacing tokens when 6 would suffice. Token bloat makes system harder to learn and maintain. [Atlassian Design System](https://atlassian.design/foundations/spacing/) intentionally limits to 8, 16, 24, 32px for this reason.
- **Breaking the scale for "just this one component"** — Ad-hoc values like 13px or 22px creep into system. **What goes wrong:** Every exception weakens the system. Users notice inconsistency even if they can't articulate it. System becomes unlearnable for new team members.

#### See Also
- [1.4 Surface Token Recognition](#14-surface-token-recognition)
- [2. Component Classification Framework](#2-component-classification-framework)

---

### 1.4 Surface Token Recognition

#### Decision Table: Identifying Surface Tokens

| Token Category | Recognition Cues | Example Values |
|----------------|------------------|----------------|
| **Border Radius** | `border-radius`, `rounded-*` | 4px (small), 8px (medium), 16px (large) |
| **Shadows** | `box-shadow`, `--shadow-*` | Composite values (offset, blur, spread, color) |
| **Elevation** | Numbered levels (0-24) | Material/Carbon style layer system |
| **Border Styles** | `border-width`, `border-style` | 1px solid, 2px dashed |
| **Opacity** | `opacity`, `--alpha-*` | 0.1, 0.5, 0.75, 1.0 |

#### Pattern: Shadow & Elevation Systems

**Shadow Token Structure (W3C DTCG Composite):**

A shadow token contains:
1. **Color:** RGBA/OKLCH value with alpha
2. **offsetX:** Horizontal offset
3. **offsetY:** Vertical offset
4. **blur:** Blur radius
5. **spread:** Spread radius

**Reference Sources:**
- Shadow tokens: [U.S. Web Design System Shadow](https://designsystem.digital.gov/design-tokens/shadow/)
- Elevation design: [Elevation Design Patterns](https://designsystems.surf/articles/depth-with-purpose-how-elevation-adds-realism-and-hierarchy)
- Atlassian elevation: [https://atlassian.design/foundations/elevation/](https://atlassian.design/foundations/elevation/)
- IBM Carbon layers: [https://carbondesignsystem.com/guidelines/layer/](https://v9.carbondesignsystem.com/guidelines/layer/)

**Elevation Level Recognition:**

| Level Range | Typical Usage | Shadow Intensity |
|-------------|---------------|------------------|
| 0-2 | Base surface, cards | Subtle/none |
| 3-6 | Raised cards, buttons | Light shadows |
| 7-12 | Dropdowns, popovers | Medium shadows |
| 13-18 | Modals, dialogs | Strong shadows |
| 19-24 | Top-level overlays | Dramatic shadows |

**IBM Carbon Example:**
- Range: 0 (base) to 24 (highest)
- Only elevation and shadow define a layer
- Tokens: `elevation/level-0`, `elevation/level-1`, `elevation/modal`

**Material Design Example:**
- Elevation expressed in dp (density-independent pixels)
- Maps to specific shadow definitions
- Tonal surface variations in Material 3

**Border Radius Patterns:**

| Size | Typical Value | Usage |
|------|---------------|-------|
| None | 0 | Sharp corners, tables, data grids |
| Small | 2-4px | Badges, tags, small buttons |
| Medium | 6-8px | Cards, form inputs, standard buttons |
| Large | 12-16px | Large cards, CTAs |
| XL | 20-24px | Hero sections, feature cards |
| Full | 9999px/50% | Pills, circular avatars |

**Recognition Strategy:**
1. Extract all `border-radius` values
2. Identify distinct tiers (usually 4-6 levels)
3. Note if system uses single value or corner-specific values
4. Check for component-specific overrides

#### Common Mistakes
- **Treating shadows as single values** — Shadows are composite tokens with multiple properties
- **Ignoring elevation semantics** — Elevation implies z-index hierarchy, not just visual shadow
- **Missing dark mode variants** — Shadow opacity/color often changes in dark themes
- **Confusing border-radius with border-width** — These are separate token categories

#### See Also
- [1.1 Color Token Recognition](#11-color-token-recognition)
- [3. Atom Recognition](#3-atom-recognition)
