---
description: "Step-by-step process for creating a new SDC or Code Component for Canvas — from decision through verification in the Canvas editor."
tldr: "Use this when building a new component for a Canvas site from scratch. Covers the full process for both SDC (Twig) and Code Components (React) — from deciding which type to use through verifying it works in the Canvas editor."
drupal_version: "11.x"
---

# Component Creation Workflow

## When to Use

> You are building a new component for a Canvas site — from scratch — and need a step-by-step process for creating it correctly, deciding which type to use, setting it up, and validating it works in Canvas.

## Steps for SDC Components (Twig)

1. **Define the component's purpose** — What does it display? What props does a content editor need to configure? Are there nested component areas (slots)?

2. **Create the directory** — Under any enabled module or theme's `components/` folder:
   ```
   my_theme/
     components/
       my-component/
         my-component.component.yml
         my-component.twig
         my-component.css        (optional)
   ```

3. **Write the `*.component.yml`** — Start with this template:
   ```yaml
   $schema: 'https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json'
   name: 'My Component'
   status: stable
   group: General
   description: 'One sentence describing what this component does.'

   props:
     type: object
     properties:
       # Add props here — see SDC Props Reference section

   slots:
     # Add slots here if needed — see SDC Slots section
   ```

4. **Define props and slots** — Use the prop types from the [SDC Props Reference](sdc-props-reference.md) section. `title` is mandatory on **every** prop and **every** slot, and `examples` is mandatory on every required prop — omitting either removes the component from Canvas entirely. Put the value you want as the default first in `examples`; Canvas ignores `default:`.

5. **Write the Twig template** — Render each prop; use `canvas:image` for image props; check for empty values before rendering wrappers.

6. **Clear Drupal caches** — `drush cr` to trigger SDC component discovery.

7. **Check eligibility before hunting in the panel** — visit **`/admin/appearance/component/status`**. Canvas discovers every SDC but only *admits* the ones that pass its requirements check, and a failing component is excluded silently. This page lists every excluded component with the exact reason. If yours is listed, fix the reason and repeat step 6 — do not go looking for it in the panel.

8. **Verify in Canvas editor** — Open Canvas, create a new page, find your component in the component panel (by its `group` and `name`), drag it onto the page, and confirm all prop widgets appear correctly.

9. **Test all prop types** — Fill in each prop in the Canvas editor, save, and verify the Twig template renders them correctly.

10. **Test empty/missing props** — Verify the component doesn't break when optional props are empty.

## Steps for Code Components (React)

1. **Set up a Nebula codebase** (if not already done):
   ```bash
   npx @drupal-canvas/create my-components --template acquia/nebula
   cd my-components && npm install
   cp .env.example .env  # add Drupal credentials
   ```

2. **Scaffold the component**:
   ```bash
   npx @drupal-canvas/cli scaffold
   ```
   This creates `components/<name>/component.yml`, `index.jsx`, `index.css`. The command is `scaffold` — there is no `canvas create`.

3. **Define props in `component.yml`** — Same structure as SDC YAML but use camelCase prop names.

4. **Write the React component in `index.jsx`** — Default export only; use Preact/React hooks; use Tailwind classes for styling.

5. **Write a Storybook story** — `my-component.stories.jsx` in the same directory; test all prop states.

6. **Run Storybook to preview**:
   ```bash
   npm run storybook
   ```

7. **Build the component**:
   ```bash
   npm run build
   ```

8. **Push to Drupal**:
   ```bash
   npx @drupal-canvas/cli push my-component-name
   ```

9. **Verify in Canvas editor** — Find the component in the panel; test prop editing; test slot drop zones.

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing SDC vs Code Component | Server-side rendering + Drupal field widgets needed | SDC component |
| Choosing SDC vs Code Component | Interactive React state or Tailwind-only needed | Code Component |
| Writing props | The prop needs the Media Library | Use `type: object` + `$ref: canvas.module/image` |
| Writing props | The prop needs a link input | Use `type: string` + `format: uri-reference` (internal + external) or `format: uri` (external only). There is no link `$ref` |
| Writing props | The prop needs rich text | Add `contentMediaType: text/html` + `x-formatting-context` |
| Writing props | You want a default value | Write it as `examples[0]`. `default:` is stripped by Canvas |
| Component missing from the panel | It was discovered but disqualified | Open `/admin/appearance/component/status` and read the recorded reason |
| Testing reveals missing widget | Canvas shows raw text input instead of expected widget | Check `$ref` and `contentMediaType` spelling exactly |
| Push fails | Auth or build error | Check `.env` credentials; run `build` before `push` |

## Common Mistakes

- Building a component without checking if an existing Canvas or contrib component already does it — duplicate components create editor confusion
- Not clearing caches after adding an SDC component — it won't appear in Canvas until `drush cr`
- Assuming a missing component means a discovery problem — far more often it was discovered and then disqualified; `/admin/appearance/component/status` tells you which
- Writing `default:` in the YAML — Canvas strips it; the stored default is `examples[0]`
- Defining a prop but not rendering it in the template — editors fill in the field but see no change on screen
- Skipping the Storybook preview step for Code Components — you catch broken props faster in Storybook than in Canvas

## See Also

- [SDC Component Format](sdc-component-format.md) — full YAML and Twig reference
- [SDC Props Reference](sdc-props-reference.md) — all prop types
- [Code Component Format](code-component-format.md) — JSX patterns and restrictions
- [Canvas CLI](canvas-cli.md) — push/pull workflow
- Building a hero component walkthrough: https://www.bonnici.co.nz/blog/drupal-11-canvas-hero-component
