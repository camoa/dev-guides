---
description: "Source references and maintenance manifest for the canvas guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: `web/modules/contrib/canvas` (Canvas 1.5.1) for cross-checking; the SDC prop, image, eligibility, import-map and CLI facts in this guide were verified line-by-line against the **1.10.1** tag from `git.drupalcode.org`, which is the version this guide documents.

The load-bearing files, if you need to re-verify:

| File | What it settles |
|---|---|
| `schema.json` (`$defs`) | The complete list of `$ref` definitions and the exact keys on each |
| `src/JsonSchemaInterpreter/JsonSchemaObjectRef.php` | The closed enum of three usable `$ref` URIs |
| `src/JsonSchemaInterpreter/JsonSchemaType.php` | Which prop schemas resolve to a storable field type + widget, and which return `NULL` |
| `src/JsonSchemaInterpreter/JsonSchemaStringFormat.php` | The `format: uri` / `uri-reference` → `link` field mapping, including `title: 0` |
| `src/ComponentMetadataRequirementsChecker.php` | Every hard eligibility gate |
| `src/ComponentSource/ComponentSourceManager.php` | That a failing component is disabled, and its reason stored |
| `src/Controller/ComponentStatusController.php` + `canvas.routing.yml` | The `/admin/appearance/component/status` diagnosis page |
| `src/PropShape/PropShape.php` | That `default:` is unset from every prop schema |
| `src/Plugin/Canvas/ComponentSource/JsonSchemaPropsComponentDiscoveryBase.php` | That `examples[0]` is the value Canvas stores as the default |
| `components/image/image.twig` + `image.component.yml` | The real `canvas:image` signature (`src`, not `image`) |
| `tests/modules/canvas_test_sdc/components/` | Canvas's own worked examples — the most readable spec for what it accepts |
| `src/GlobalImports.php` | The authoritative Code Component import map |
| `packages/eslint-config/src/rules/component-imports.ts` | Which imports Canvas's own lint rejects, and why |
| `packages/cli/src/index.ts` | The real CLI command list |

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Canvas Official Docs (project pages) | https://project.pages.drupalcode.org/canvas/ | All sections | 2026-02-21 |
| Canvas SDC Components docs | https://project.pages.drupalcode.org/canvas/sdc-components/ | SDC Component Format, SDC Props, SDC Slots | 2026-02-21 |
| Canvas SDC Props docs | https://project.pages.drupalcode.org/canvas/sdc-components/props/ | SDC Props Reference | 2026-02-21 |
| Canvas SDC Slots docs | https://project.pages.drupalcode.org/canvas/sdc-components/slots/ | SDC Slots | 2026-02-21 |
| Canvas SDC Images docs | https://project.pages.drupalcode.org/canvas/sdc-components/image/ | SDC Image Handling | 2026-02-21 |
| Canvas Code Components docs | https://project.pages.drupalcode.org/canvas/code-components/ | Code Component Format | 2026-02-21 |
| Canvas Code Component Packages docs | https://project.pages.drupalcode.org/canvas/code-components/packages/ | Canvas NPM Tools, Code Component Format | 2026-02-21 |
| Canvas Responsive Images docs | https://project.pages.drupalcode.org/canvas/code-components/responsive-images/ | SDC Image Handling | 2026-02-21 |
| Canvas AI Assistant docs | https://project.pages.drupalcode.org/canvas/ai-assistant/ | Canvas AI Assistant | 2026-02-21 |
| Drupal.org Canvas project page | https://www.drupal.org/project/canvas | Canvas Overview | 2026-07-03 |
| Canvas releases | https://www.drupal.org/project/canvas/releases | Canvas Overview, Security | 2026-07-03 |
| Canvas security advisory SA-CONTRIB-2026-006 | https://www.drupal.org/sa-contrib-2026-006 | Security Considerations | 2026-02-21 |
| Balint Kleri - Decoupled frontend with Drupal Canvas | https://balintbrews.com/blog/drupal-canvas-decoupled/ | Decoupled Frontend Patterns | 2026-02-21 |
| Balint Kleri - 19 things about Canvas (DrupalCon Vienna) | https://balintbrews.com/blog/drupalcon-vienna-19-things-about-canvas | Canvas Overview, Code Component Format | 2026-02-21 |
| Balint Kleri - DrupalCon Vienna demo repo | https://github.com/balintbrews/drupalcon-vienna-2025-canvas-js-frontend | Decoupled Frontend Patterns | 2026-02-21 |
| Balint Kleri - canvas-starter | https://github.com/balintbrews/canvas-starter | Code Component Format, Canvas CLI | 2026-02-21 |
| Acquia Nebula GitHub | https://github.com/acquia/nebula | Acquia Nebula, Canvas CLI, Storybook | 2026-02-21 |
| @drupal-canvas/cli on npmjs.com | https://www.npmjs.com/package/@drupal-canvas/cli | Canvas NPM Tools, Canvas CLI | 2026-02-21 |
| Drupal.org Decoupled Canvas docs | https://www.drupal.org/docs/develop/decoupled-drupal/decoupled-drupal-canvas | Decoupled Frontend Patterns | 2026-02-21 |
| canvas_extjs module | https://www.drupal.org/project/canvas_extjs | Decoupled Frontend Patterns, Component Types Decision | 2026-02-21 |
| canvas_full_html module | https://www.drupal.org/project/canvas_full_html | SDC Props Reference (rich text) | 2026-02-21 |
| Canvas SDC Starterkit | https://www.drupal.org/project/canvas_sdc_starterkit | Acquia Nebula, Storybook Integration | 2026-02-21 |
| xb_ai_assistant module | https://www.drupal.org/project/xb_ai_assistant | Canvas AI Assistant | 2026-02-21 |
| Lupus Decoupled module | https://www.drupal.org/project/lupus_decoupled | Decoupled Frontend Patterns | 2026-02-21 |
| Specbee - Canvas Full HTML | https://www.specbee.com/blogs/extending-drupal-canvas-with-canvas-full-html | SDC Props Reference (rich text) | 2026-02-21 |
| Bonnici - Building Hero Component with Canvas | https://www.bonnici.co.nz/blog/drupal-11-canvas-hero-component | Component Creation Workflow, SDC Component Format | 2026-02-21 |
| Bonnici - Drupal Canvas 5 Tips | https://www.bonnici.co.nz/blog/drupal-canvas-5-tips-tricks | SDC Props Reference | 2026-02-21 |
| Bonnici - Canvas AI Native Page Building | https://www.bonnici.co.nz/blog/drupal-ai-native-page-building-canvas-ai-context | Canvas AI Assistant | 2026-02-21 |
| Dripyard - Handling images across Drupal and Canvas | https://dripyard.com/blog/handling-images-drupal-and-canvas-same-component | SDC Image Handling | 2026-02-21 |
| WebWash - Tailwind CSS theme for Canvas | https://www.webwash.net/tailwind-css-theme-setup-for-drupal-canvas/ | Design Tokens and Theming | 2026-02-21 |
| Cheppers - Canvas, SDC, and Future of Drupal | https://cheppers.com/post/canvas-sdc-and-the-future-of-drupal | Canvas vs Standard SDC Decision | 2026-02-21 |
| The Drop Times - Building Decoupled Frontends with Canvas | https://www.thedroptimes.com/55248/building-fully-decoupled-frontends-with-drupal-canvas-and-code-components | Decoupled Frontend Patterns | 2026-02-21 |
| The Drop Times - Canvas SDC Starterkit | https://www.thedroptimes.com/55869/pravesh-poonia-introduces-canvas-sdc-starterkit-accelerate-component-development-in-drupal | Acquia Nebula | 2026-02-21 |
| Drupal SDC Props and Slots docs | https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming | SDC Props Reference, SDC Slots | 2026-02-21 |
| Drupal.org Canvas 1.0 announcement | https://www.drupal.org/blog/drupal-canvas-is-now-available-inside-drupals-new-visual-page-building | Canvas Overview | 2026-02-21 |
| Acquia - Drupal Canvas 1.0 Released | https://www.acquia.com/blog/drupal-canvas-10-released | Canvas Overview | 2026-02-21 |
| Tailwind CSS v4 theme docs | https://tailwindcss.com/docs/theme | Design Tokens and Theming | 2026-02-21 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Canvas | modules/contrib/canvas/ | All sections | 1.10.1 / ^11.3 |
| Canvas (submodules) | modules/contrib/canvas/modules/canvas_ai/ | Canvas AI Assistant | 1.10.1 |
| canvas_extjs | modules/contrib/canvas_extjs/ | Decoupled Frontend Patterns | contrib |
| canvas_full_html | modules/contrib/canvas_full_html/ | SDC Props Reference | contrib |
| canvas_sdc_starterkit | modules/contrib/canvas_sdc_starterkit/ | Acquia Nebula, Storybook | contrib |
| Drupal SDC core | core/modules/sdc/ | SDC Component Format, SDC Props Reference, SDC Slots | 11.x |

## Unverified / Needs Follow-up

The following items could not be fully verified due to WebFetch being unavailable during research. Treat with caution and verify against official docs:

- **`skills.sh`** — Referenced in the research request. This may refer to the `.agents/skills/` directory in the Acquia Nebula repository (AI coding agent skill files), not a separate tool called `skills.sh`. No standalone `skills.sh` tool was found in research. **Action**: Check the Nebula GitHub README for clarification.
- **Code Component `drupal-canvas` package API** — The exact exports from the `drupal-canvas` npm package (utilities and base components) are not fully documented in available search results. **Action**: Check `https://project.pages.drupalcode.org/canvas/code-components/packages/` for the current API.
- **Design token editor UI in Canvas** — The mechanism for exposing design tokens as editor-adjustable values in the Canvas UI is referenced in community articles but the implementation details were not confirmed in research. **Action**: Check the Canvas project docs for the current state of this feature.
- **Multi-value prop repeater UI maturity** — Multi-value prop UI configuration shipped in Canvas 1.3.0 (issue #3571917) and value persistence in Canvas 1.4.0 (issue #3572553). A remaining required-field-validation gap for multi-value props is tracked in issue #3576124 (open/closed status inferred from changelog absence, not a definitive badge). **Action**: Check issue #3576124 for current status.

---
