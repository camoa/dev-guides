---
description: "Source references and maintenance manifest for the plus suite guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Plus Suite install script | https://git.drupalcode.org/project/plus_suite/-/raw/1.1.x/install.sh | 2.1 | 2026-04-08 |
| Issue #3517909 — recipe fails on existing Layout Builder sites | https://www.drupal.org/project/plus_suite/issues/3517909 | 2.1, 25.1 | 2026-04-08 |
| DropzoneJS release archive (enyo/dropzone 6.0.0-beta.2) | https://github.com/dropzone/dropzone/releases/download/v6.0.0-beta.2/dist.zip | 2.1 | 2026-04-08 |
| Issue #3535241 — DropzoneJS composer repository must be added manually | https://www.drupal.org/project/plus_suite/issues/3535241 | 25.1 | 2026-04-08 |
| Issue #3518649 — Navigation+ incompatibilities on existing sites | https://www.drupal.org/project/plus_suite/issues/3518649 | 25.1 | 2026-04-08 |

## Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| Plus Suite (recipe) | contrib/recipes/plus_suite/ (recipe source checkout, outside the /web install root) | 2.1, 3.1, 23.1, 25.1 | 1.1.21, stable (tracks declaration — recipe.yml carries no version field) |
| Navigation+ | modules/contrib/navigation_plus/ | 2.1-6.1, 13.1-14.1, 16.1, 19.1-23.1, 25.1 | 2.3.9 (installed; guide header states 2.3.4 — not re-verified against the newer release) |
| LB+ | modules/contrib/lb_plus/ | 2.1-3.1, 6.1-8.1, 10.1-12.1, 16.1, 18.1-23.1, 26.1-29.1 | 3.6.12 (installed; guide header states 3.6.8 — not re-verified against the newer release) |
| Edit+ | modules/contrib/edit_plus/ | 2.1-3.1, 6.1, 9.1-10.1, 14.1, 16.1, 18.1-26.1, 28.1-29.1 | 2.3.3 (installed; guide header states 2.3.0 — not re-verified against the newer release) |
| Tempstore+ | modules/contrib/tempstore_plus/ | 1.1-3.1, 9.1-10.1, 17.1, 23.1-24.1 | 1.0.4 (matches guide header) |
| Field Sample Value | modules/contrib/field_sample_value/ | 2.1-3.1, 7.1, 11.1, 18.1, 23.1, 25.1-26.1, 28.1-29.1 | 1.0.9 (installed; guide header states 1.0.8 — not re-verified against the newer release) |
| Twig Events | modules/contrib/twig_events/ | 2.1-3.1, 16.1, 21.1, 23.1 | 1.0.1 (matches guide header) |
| Section Library | modules/contrib/section_library/ | 1.1-3.1, 6.1, 8.1, 12.1, 14.1-15.1, 18.1, 23.1, 29.1 | 1.2.2 (matches guide header) |

DropzoneJS is not installed as a module on the research install and is not present in its composer files. It could not be verified in this pass and is omitted from this table; the guide's references to it (sections 2.1, 13.1) rest on the Web Sources above and on the guide's own prose only.

## Version History
| Date | Change |
|------|--------|
| 2026-04-08 | Manifest reconstructed from the guide's own citations and the installed source. Installed navigation_plus, lb_plus, edit_plus, and field_sample_value are newer than the versions recorded in this guide's header — worth a currency pass, not corrected here. |
