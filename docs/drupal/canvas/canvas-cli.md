---
description: Step-by-step workflow for developing Canvas Code Components locally using the CLI — scaffold, build, push, and pull.
drupal_version: "11.x"
---

# Canvas CLI Workflow

## When to Use

> Use this when developing Code Components in a local IDE/editor rather than (or in addition to) the Canvas in-browser editor. The CLI enables full local development with version control and CI/CD, while staying in sync with the Canvas Drupal environment.

## Decision

| At this step... | If... | Then... |
|---|---|---|
| Choosing push vs pull | You edited in Canvas browser editor | `pull` to get the latest to your local codebase |
| Choosing push vs pull | You edited in your IDE | `pull` first to avoid overwrite conflicts, then `push` |
| Build fails | Tailwind classes not found | Check that `index.jsx` uses standard Tailwind v4 classes |
| Push fails | Auth error | Verify `.env` credentials; check Drupal Canvas API module is enabled |
| Pull gives conflicts | Both local and remote changed | Manual merge required; CLI does not auto-merge |

## Pattern

1. **Scaffold a new codebase** — Initialize the development environment using Nebula or a custom template
   ```bash
   npx @drupal-canvas/create my-canvas-components --template acquia/nebula
   cd my-canvas-components
   ```

2. **Configure Drupal connection** — Copy `.env.example` to `.env` and add credentials
   ```bash
   cp .env.example .env
   # Edit .env: DRUPAL_BASE_URL, DRUPAL_USERNAME, DRUPAL_PASSWORD (or API key)
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Create a new component** — Generate the scaffold for a new Code Component
   ```bash
   npx @drupal-canvas/cli create my-hero-banner
   # Creates: components/my-hero-banner/component.yml, index.jsx, index.css
   ```

5. **Develop the component** — Edit `component.yml`, `index.jsx`, `index.css` in your IDE

6. **Build locally** — Compile JSX and Tailwind into distributable files
   ```bash
   npm run build
   # Or directly: npx @drupal-canvas/cli build
   ```

7. **Preview in Storybook** (if using Nebula) — View components in isolation
   ```bash
   npm run storybook
   ```

8. **Push to Drupal** — Upload the built component to your Canvas environment
   ```bash
   npx @drupal-canvas/cli push
   # Push a specific component only:
   npx @drupal-canvas/cli push my-hero-banner
   ```

9. **Pull from Drupal** — Sync components edited in the browser editor back to local
   ```bash
   npx @drupal-canvas/cli pull
   ```

## Common Mistakes

- **Wrong**: Editing in both the browser editor and locally without pulling first → **Right**: Always `pull` before editing locally after browser edits; leads to overwrite conflicts otherwise
- **Wrong**: Not committing the `component.yml` to version control → **Right**: This is the source of truth for prop schema
- **Wrong**: Running `push` in production without a review process → **Right**: Treat push like a deployment; use staging environments
- **Wrong**: Skipping `build` before `push` → **Right**: Pushing un-built source files will produce broken components
- **Wrong**: Using old command names `upload`/`download` → **Right**: These are deprecated; use `push`/`pull`

## See Also

- [Acquia Nebula](acquia-nebula.md) for the full recommended codebase template
- [Code Component Format](code-component-format.md) for what files the CLI manages
- [Canvas NPM Tools](canvas-npm-tools.md) for CLI installation
- CLI issue tracker: https://www.drupal.org/project/canvas/issues?text=cli
