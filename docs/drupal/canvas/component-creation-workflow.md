---
description: Step-by-step process for creating a new SDC or Code Component for Canvas — from decision through verification in the Canvas editor.
drupal_version: "11.x"
---

# Component Creation Workflow

## When to Use

> Use this when building a new component for a Canvas site from scratch. Covers the full process for both SDC (Twig) and Code Components (React) — from deciding which type to use through verifying it works in the Canvas editor.

## Decision

| At this step... | If... | Then... |
|---|---|---|
| Choosing SDC vs Code Component | Server-side rendering + Drupal field widgets needed | SDC component |
| Choosing SDC vs Code Component | Interactive React state or Tailwind-only needed | Code Component |
| Writing props | The prop needs the Media Library | Use `$ref: canvas.module/image` |
| Writing props | The prop needs a link input | Use `$ref: canvas.module/link` |
| Writing props | The prop needs rich text | Add `contentMediaType: text/html` + `x-formatting-context` |
| Testing reveals missing widget | Canvas shows raw text input instead of expected widget | Check `$ref` and `contentMediaType` spelling exactly |
| Push fails | Auth or build error | Check `.env` credentials; run `build` before `push` |

## Pattern

### Steps for SDC Components (Twig)

1. **Define the component's purpose** — What does it display? What props does a content editor need? Are there nested component areas (slots)?

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

4. **Define props and slots** — Use the prop types from the [SDC Props Reference](sdc-props-reference.md). Add `title`, `description`, and `examples` to every prop.

5. **Write the Twig template** — Render each prop; use `canvas:image` for image props; check for empty values before rendering wrappers.

6. **Clear Drupal caches** — `drush cr` to trigger SDC component discovery.

7. **Verify in Canvas editor** — Open Canvas, create a new page, find your component in the component panel (by its `group` and `name`), drag it onto the page, and confirm all prop widgets appear correctly.

8. **Test all prop types** — Fill in each prop in the Canvas editor, save, and verify the Twig template renders them correctly.

9. **Test empty/missing props** — Verify the component doesn't break when optional props are empty.

### Steps for Code Components (React)

1. **Set up a Nebula codebase** (if not already done):
   ```bash
   npx @drupal-canvas/create my-components --template acquia/nebula
   cd my-components && npm install
   cp .env.example .env  # add Drupal credentials
   ```

2. **Scaffold the component**:
   ```bash
   npx @drupal-canvas/cli create my-component-name
   ```
   This creates `components/my-component-name/component.yml`, `index.jsx`, `index.css`.

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

## Common Mistakes

- **Wrong**: Building a component without checking if an existing Canvas or contrib component already does it → **Right**: Duplicate components create editor confusion; check the component panel first
- **Wrong**: Not clearing caches after adding an SDC component → **Right**: It won't appear in Canvas until `drush cr`
- **Wrong**: Defining a prop but not rendering it in the template → **Right**: Editors fill in the field but see no change on screen
- **Wrong**: Skipping the Storybook preview step for Code Components → **Right**: You catch broken props faster in Storybook than in Canvas

## See Also

- [SDC Component Format](sdc-component-format.md) — full YAML and Twig reference
- [SDC Props Reference](sdc-props-reference.md) — all prop types
- [Code Component Format](code-component-format.md) — JSX patterns and restrictions
- [Canvas CLI](canvas-cli.md) — push/pull workflow
- Building a hero component walkthrough: https://www.bonnici.co.nz/blog/drupal-11-canvas-hero-component
