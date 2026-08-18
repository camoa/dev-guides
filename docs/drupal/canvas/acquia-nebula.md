---
description: "Acquia Nebula — the official Canvas Code Component development template with Storybook, Vite, ESLint, and AI agent skills preconfigured."
tldr: "Use Nebula when starting a new Canvas Code Component development codebase. It is the official Acquia-maintained template for `@drupal-canvas/create` and the recommended starting point for any Canvas Code Component project."
drupal_version: "11.x"
---

# Acquia Nebula

## When to Use

> Use Nebula when starting a new Canvas Code Component development codebase. It is the official Acquia-maintained template for `@drupal-canvas/create` and the recommended starting point for any Canvas Code Component project.

## Decision

| Situation | Choose | Why |
|---|---|---|
| New Canvas Code Component codebase | Nebula template | Fully preconfigured; Storybook, Vite, SWC, ESLint, AI skills out of the box |
| Agency house-standard template | Fork Nebula, customize | Use your fork as `--template your-org/your-fork` |
| Canvas SDC (Twig) components | canvas_sdc_starterkit | Nebula is for Code Components (React); Starterkit is for SDC (Twig) |

## Pattern

**Setup:**

```bash
# Create a new codebase from the Nebula template
npx @drupal-canvas/create my-components --template acquia/nebula

cd my-components
npm install

# Configure Drupal connection
cp .env.example .env
# Edit .env with your Drupal Canvas site credentials

# Start Storybook for component development
npm run storybook

# Start Vite dev server (if applicable)
npm run dev
```

**What Nebula provides:**
- **Storybook** — Preconfigured for Canvas component development with viewports matching Canvas's viewport sizes
- **Vite + SWC** — Fast build tooling using `@vitejs/plugin-react-swc` for JSX compilation
- **ESLint** — Canvas-specific lint rules (includes required validation for Code Components to work in Canvas, plus recommended rules on top)
- **AI agent skill files** — Coding agent instruction files in `.agents/skills/` for AI-assisted development:
  - `nebula-*` skills: Nebula-specific conventions and workflows
  - `canvas-*` skills: Generic Canvas Code Component guidance (from `drupal-canvas/skills`)
  - Compatible with: Amp, Codex, Gemini CLI, GitHub Copilot, Kimi Code CLI, OpenCode, and other agents that read from `.agents/skills/`
- **Tailwind CSS 4** — Global Tailwind configuration
- **Example components** — Sample components demonstrating patterns and conventions

**Creating your own template:**

1. Fork `github.com/acquia/nebula`
2. Modify Storybook configuration, ESLint rules, example components, or `.agents/skills/` files
3. Use your fork as the template: `npx @drupal-canvas/create my-project --template your-org/your-fork`

## Common Mistakes

- **Wrong**: Creating a component codebase from scratch instead of using Nebula → **Right**: You lose preconfigured tooling, ESLint, and Storybook
- **Wrong**: Forking Nebula but never updating it as Canvas evolves → **Right**: Periodically merge upstream changes from `github.com/acquia/nebula`
- **Wrong**: Ignoring the `.agents/skills/` files → **Right**: These are critical context for AI-assisted development; read them before asking an agent to generate components
- **Wrong**: Confusing Nebula (Code Component development template) with the Canvas SDC Starterkit → **Right**: Nebula is for Code Components (React); Starterkit is for SDC components (Twig)

## See Also

- Nebula GitHub: https://github.com/acquia/nebula
- [Canvas CLI](canvas-cli.md) for the push/pull workflow used with Nebula
- Canvas SDC Starterkit (for SDC/Twig components): https://www.drupal.org/project/canvas_sdc_starterkit
