---
description: "Required and optional component files, and where the component's machine name actually comes from"
tldr: "Every sibling file (.twig, .css, .js) must match the .component.yml basename, not the directory name — machineName is derived from the plugin ID, which is the YAML basename. Renaming the directory does not fix a 'component not found' error; check the basename match instead."
drupal_version: "11.x"
---

# Component File Structure

## When to Use

> Use this when you're creating a new component, debugging "component not found" errors, or you need to understand automatic asset loading.

## Decision

**Required Structure:**
```
component-name/
├── component-name.component.yml  ← Metadata (REQUIRED)
└── component-name.twig           ← Template (REQUIRED)
```

**Optional Files (auto-loaded if present):**
```
component-name/
├── component-name.css            ← Styles (auto-attached as library)
├── component-name.js             ← Scripts (auto-attached as library)
├── README.md                     ← Documentation
├── thumbnail.png                 ← Preview for admin UI
└── assets/                       ← Additional assets (must reference manually)
```

**CRITICAL:** The `.component.yml` basename is the component's machine name, and every sibling file must match **that basename** — not the directory name.

**WHY:** `ComponentPluginManager::alterDefinition()` derives `machineName` by splitting the plugin ID (`[, $machine_name] = explode(':', $definition['id'])`), and the plugin ID came from `basename($file, '.component.yml')`. The Twig, CSS and JS are then located by `machineName`. The directory name is never read.

Matching directory to basename is still the right convention: it keeps the folder greppable and matches every example in core and contrib. But when you are debugging "component not found", **renaming the directory will not fix it** — check that the ID you are calling equals `provider:{yml basename}` and that the `.twig` shares that basename.

Core proves this with a fixture: `core/modules/system/tests/themes/sdc_theme_test/components/mismatching-folder-name/` contains `foo.component.yml` + `foo.twig`, and `ComponentPluginManagerTest` asserts that `sdc_theme_test:foo` **is** found while `sdc_theme_test:mismatching-folder-name` throws `ComponentNotFoundException`.

## Pattern

```
✓ CORRECT (conventional — keep doing this):
my-button/
├── my-button.component.yml
├── my-button.twig
├── my-button.css
└── my-button.js

✓ ALSO WORKS (directory name is ignored):
some-folder/
├── my-button.component.yml   ← ID is provider:my-button
└── my-button.twig

✗ BROKEN — the template basename does not match the YAML basename:
my-button/
├── my-button.component.yml
└── my_button.twig             ← template not found
```

**Automatic Library Generation:** each component generates a library automatically.
- Format: `core/components.{provider}--{component-name}`
- Example: `core/components.my_theme--hero-banner`
- Includes CSS/JS files named identically to component
- Loaded automatically when component renders

## Common Mistakes

- **Wrong**: Renaming the directory to fix "component not found" → **Right**: The directory name is never read; check that the ID equals `provider:{yml basename}` and that the `.twig` shares that basename.
- **Wrong**: Using underscores in component names → **Right**: Component names should use hyphens (kebab-case) per Drupal conventions. Underscores in provider names are converted to hyphens in library names.

## See Also

- Reference: `/core/lib/Drupal/Core/Theme/ComponentPluginManager.php:343-352` — `machineName` from the plugin ID, template found by `machineName`
- Reference: `/core/tests/Drupal/KernelTests/Components/ComponentPluginManagerTest.php:29-53` — the mismatching-folder-name assertions
- Reference: `/core/themes/olivero/components/teaser/` — Reference implementation
- Reference: `/themes/contrib/radix/components/button/` — Radix button example
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [JavaScript in SDCs](javascript-in-sdcs.md)
