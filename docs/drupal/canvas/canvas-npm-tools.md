---
description: "Reference for Canvas npm packages — @drupal-canvas/cli, @drupal-canvas/create, drupal-canvas runtime, and Tailwind CSS 4."
tldr: "Use this when setting up a local development environment for Canvas Code Components, or when you need to understand which npm packages are part of the Canvas ecosystem and what each one does."
drupal_version: "11.x"
---

# Canvas NPM Tools

## When to Use

> Use this when setting up a local development environment for Canvas Code Components, or when you need to understand which npm packages are part of the Canvas ecosystem and what each one does.

## Decision

| Package | Purpose | Install |
|---|---|---|
| `@drupal-canvas/cli` | Scaffold, build, push, pull Code Components | `npm install -g @drupal-canvas/cli` |
| `@drupal-canvas/create` | Scaffold a new component codebase from a template | `npx @drupal-canvas/create` |
| `drupal-canvas` | Runtime utilities and base components (available in import map) | No install — available at runtime |
| Tailwind CSS 4 | Utility classes globally available to all Code Components | Configured in Nebula codebase |

## Pattern

#### @drupal-canvas/cli

```bash
npm install -g @drupal-canvas/cli
# or use npx
npx @drupal-canvas/cli --help

# Authenticate against the Drupal site
npx @drupal-canvas/cli login

# Create a new component directory with scaffold files
npx @drupal-canvas/cli scaffold --name my-component   # --name optional; prompts if omitted

# Check local components and pages before pushing
npx @drupal-canvas/cli validate

# Build local components (creates dist/ in each component dir)
npx @drupal-canvas/cli build

# Build and upload to Drupal (replaces old "upload" command)
npx @drupal-canvas/cli push

# Download components from Drupal to local filesystem (replaces old "download")
npx @drupal-canvas/cli pull

# Pull site context for local AI coding agents
npx @drupal-canvas/cli agents-context
```

- The scaffold command is `scaffold`, not `create` — `canvas create` does not exist. (`@drupal-canvas/create`, below, is a separate package for scaffolding a whole *codebase*)
- `download` and `upload` are registered as hidden stubs that print "use pull/push instead" and exit non-zero
- `build` compiles JSX → JS and builds Tailwind CSS into a `dist/` directory per component
- `push`/`pull` are the new names for the sync commands (previously `upload`/`download`)
- Requires Drupal Canvas module + API credentials configured in `.env`

---

#### @drupal-canvas/create

```bash
# Create a new component codebase using the Nebula template (recommended)
npx @drupal-canvas/create my-canvas-components --template acquia/nebula

# Create with a custom template
npx @drupal-canvas/create my-canvas-components --template your-org/your-template
```

- Nebula (`acquia/nebula`) is the official recommended template — fully configured with Storybook, Vite, SWC, ESLint, and AI agent skill files
- Any GitHub repository can be used as a template
- The created codebase includes `.env.example` for Drupal connection credentials

---

#### drupal-canvas (runtime package)

```jsx
import { SomeUtil } from 'drupal-canvas';
```

Available inside Code Components at runtime. Provides helper functions and pre-built components. Bundled utilities are available outside Canvas as of recent releases.

---

#### Tailwind CSS 4

```css
/* index.css — can reference Tailwind utilities */
@import "tailwindcss";

@layer components {
  .hero-gradient {
    @apply bg-gradient-to-r from-blue-600 to-blue-800;
  }
}
```

- The CLI builds global Tailwind CSS assets for all components together, not per-component
- Tailwind 4's `@theme` directive can be used in the global CSS file to define design tokens as CSS custom properties
- Tailwind class purging is handled by the CLI build

## Common Mistakes

- **Wrong**: Assuming a `canvas create` command exists → **Right**: the scaffold command is `canvas scaffold`
- **Wrong**: Assuming npm packages outside the base import map can never be used → **Right**: that is true of the in-browser editor only. The CLI bundles third-party deps at `build` and registers them in the site's import map at `push`
- **Wrong**: Using `@drupal/canvas-cli` (wrong scope) → **Right**: The correct package is `@drupal-canvas/cli`
- **Wrong**: Running the CLI without configuring Drupal connection credentials in `.env` → **Right**: push/pull commands need API access
- **Wrong**: Installing the CLI globally when a project-local install is more reproducible → **Right**: Prefer project-level devDependency

## See Also

- [Canvas CLI](canvas-cli.md) for the full CLI workflow
- [Acquia Nebula](acquia-nebula.md) for the recommended template
- [Code Component Format](code-component-format.md) for what the CLI builds
- npmjs.com: https://www.npmjs.com/package/@drupal-canvas/cli
- Canvas packages docs: https://project.pages.drupalcode.org/canvas/code-components/packages/
