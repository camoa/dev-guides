---
description: "Architecture decision guide — when to choose Drupal Canvas page builder vs standard SDC theming, Layout Builder, or content types."
tldr: "Use this when deciding whether to build a site with Drupal Canvas or with standard Drupal theming using SDC components, Layout Builder, or content types with Twig templates. Make this decision at project start."
drupal_version: "11.x"
---

# Canvas vs Standard SDC Decision

## When to Use

> Use this when deciding whether to build a site with Drupal Canvas or with standard Drupal theming using SDC components, Layout Builder, or content types with Twig templates. Make this decision at project start.

## Decision

| If your project has... | Choose... | Why |
|---|---|---|
| Non-technical content editors who need to build pages | Canvas | Visual drag-and-drop; no Drupal knowledge needed |
| Marketing team managing landing pages | Canvas | Self-service page building; reduces developer bottleneck |
| A small, fixed set of page layouts | Standard theming | Layout Builder or templates are simpler for fixed layouts |
| Existing Paragraphs-heavy architecture | Standard theming (short-term) | Migration to Canvas is non-trivial |
| Component-library governance requirement | Canvas | All pages built from approved SDC/Code Components enforces design system |
| A headless/decoupled architecture | Evaluate carefully | Canvas decoupled is possible but complex |
| Budget for component library development | Canvas | Requires upfront investment building Canvas-compatible components |
| Pure developer-managed content | Standard theming | Canvas editorial features add no value if developers edit everything |

## Pattern

**Key architectural differences:**

| Concern | Canvas | Standard SDC Theming |
|---|---|---|
| Page composition | Component tree stored in field | Twig templates + Layout Builder regions |
| Editor experience | Visual drag-and-drop with real-time preview | Drupal admin forms |
| Component authoring | SDC or React Code Components | SDC (Twig only) |
| Design enforcement | All pages must use defined components | Templates can be overridden; editors add free text |
| Drupal version | ^11.3 required | Drupal 9+ |
| Theming approach | Tailwind (Code) + CSS (SDC) | Bootstrap/any CSS framework |
| Existing contrib module integration | Still maturing (many modules not Canvas-aware yet) | Full contrib ecosystem compatibility |

**Hybrid approach (recommended for most sites):**

Canvas does not replace all Drupal content — it is targeted at landing pages, marketing pages, and editorial-built pages:

- **Canvas pages**: Homepage, campaign pages, landing pages, team/about pages
- **Standard content types**: Blog posts, news articles, product catalog pages, documentation
- **SDC components**: Used in BOTH contexts — Canvas uses them as page components; standard templates use them via `{% include %}`

## Common Mistakes

- **Wrong**: All-or-nothing thinking → **Right**: Most production sites will use Canvas for some content and standard Drupal for others
- **Wrong**: Rewriting existing SDC components into Code Components when they could stay as SDC → **Right**: Only convert if you need React interactivity
- **Wrong**: Choosing Canvas solely because it is new → **Right**: Evaluate against actual project requirements and editor personas
- **Wrong**: Not accounting for the component library investment → **Right**: Canvas requires a library of Canvas-compatible components before editors can be productive

## See Also

- [Canvas Overview](canvas-overview.md) for architectural context
- [Component Types Decision](component-types-decision.md) for SDC vs Code Component
- Cheppers article: https://cheppers.com/post/canvas-sdc-and-the-future-of-drupal
- ImageX article: https://imagexmedia.com/blog/drupal-canvas-released
