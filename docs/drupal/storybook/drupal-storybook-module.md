---
description: drupal/storybook module — complete stories/story Twig tag reference with argTypes Controls, setup sequence, and working examples for interactive Storybook integration
drupal_version: "11.x"
---

# drupal/storybook Module — Twig Stories

## When to Use

> Use `drupal/storybook` when your theme uses custom Twig templates that need real Drupal rendering with interactive Controls. Do NOT use for UI Suite DaisyUI themes — `.story.yml` is the correct tool.

Use when:
- Your theme uses custom Twig templates that need real Drupal rendering (actual Twig functions, entity data, theme hooks)
- You want the full Storybook.js UI with interactive Controls for design-dev handoff
- You're building a Radix-based custom theme and want Storybook integration

## Decision

| Scenario | Use drupal/storybook? |
|---|---|
| UI Suite DaisyUI theme | No — use `.story.yml` instead |
| Radix-based custom theme with Storybook.js UI | Yes |
| Custom Twig templates needing `drupal_block()`, `url()`, etc. | Yes |
| Offline / CI component testing without Drupal | No — use `storybook-addon-sdc` |
| Simple Drupal-native browser, no Node.js | No — use `sdc_styleguide` |

### Architecture

The module provides a Twig extension (via `e0ipso/twig-storybook` library) that adds `{% stories %}` / `{% story %}` tags. Storybook.js sends story args to Drupal over HTTP; Drupal renders the Twig and returns HTML.

```
Storybook.js (browser)
    ↓  HTTP request with story args
Drupal backend (running DDEV/local)
    ↓  renders Twig template with args as variables
    ↑  returns rendered HTML string
Storybook.js renders HTML in iframe
```

### `{% stories %}` Tag Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `title` | string | Storybook sidebar path — slashes create folders: `'Components/Card'` |
| `argTypes` | object | Define Controls for each arg |

### argTypes Control Types

| Control | Description | Required `options`? |
|---------|-------------|---------------------|
| `'text'` | Text input | No |
| `'number'` | Number input | No |
| `'boolean'` | Toggle | No |
| `'select'` | Dropdown | Yes — `options: [...]` |
| `'radio'` | Radio buttons | Yes — `options: [...]` |
| `'check'` | Checkboxes (multi) | Yes — `options: [...]` |
| `'color'` | Color picker | No |
| `{ type: 'number', min: N, max: N, step: N }` | Number with range | No |

### `{% story %}` Tag Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string | Display name in Storybook sidebar |
| `args` | object | Default values for this story's args — populates Controls panel initial values |
| `argTypes` | object | Story-level argType overrides (merged with stories-level) |
| `decorators` | array | Story-level decorators (Storybook wrappers around story output) |

`args` keys are available as `args.key_name` inside the `{% story %}` body. Pass them to component includes manually — they are NOT auto-mapped.

### Story File Location

Story files use the `.stories.twig` suffix (plural). Convention: alongside the component template.

```
my_theme/
  components/
    card/
      card.component.yml
      card.twig
      card.stories.twig     ← story file here
```

The `.storybook/main.js` `stories` glob must match — typically `'../components/**/*.stories.twig'`.

## Pattern

```twig
{# components/card/card.stories.twig #}
{% stories card with {
  title: 'Components/Card',
  argTypes: {
    variant: {
      options: ['default', 'compact', 'side'],
      control: 'select'
    },
    heading_level: {
      control: { type: 'number', min: 1, max: 6 }
    },
    border: {
      options: ['', 'border', 'dash'],
      control: 'radio'
    }
  }
} %}

{% story default with {
  name: 'Default',
  args: {
    title: 'Running Shoes',
    text: 'Lightweight and comfortable for all-day wear.',
    variant: 'default',
    heading_level: 2,
    border: ''
  }
} %}
  {{ include('my_theme:card', {
    title: args.title,
    text: args.text,
    variant: args.variant,
    heading_level: args.heading_level,
    border: args.border,
  }, with_context: false) }}
{% endstory %}

{% story side with {
  name: 'Side layout',
  args: {
    title: 'New movie is released!',
    text: 'Click the button to watch on Jetflix app.',
    variant: 'side',
    heading_level: 2,
    border: ''
  }
} %}
  {{ include('my_theme:card', {
    title: args.title,
    text: args.text,
    variant: args.variant,
    heading_level: args.heading_level,
  }, with_context: false) }}
{% endstory %}

{% endstories %}
```

### Setup Sequence

> **DDEV users**: Use the `tyler36/ddev-storybook` addon — it handles port exposure, Node.js, and the `ddev storybook` command without manual config. See [DDEV + Storybook Setup](ddev-storybook-setup.md).

**Drupal side:**

```bash
composer require drupal/storybook --dev
drush en storybook

# Grant anonymous user permission to render stories
# Remove this permission on production — rendering is Drupal-side, not public
drush role:perm:add anonymous 'render storybook stories'
```

Add to `web/sites/development.services.yml`:

```yaml
parameters:
  cors.config:
    enabled: true
    allowedHeaders: ['*']
    allowedMethods: ['GET', 'POST', 'OPTIONS']
    allowedOrigins: ['http://localhost:6006', 'https://localhost:6007']
services:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

**Storybook side (ESM — required since Storybook v9):**

```bash
cd web/themes/custom/my_theme
npx storybook@latest init --type server
```

Configure `.storybook/main.js`:

```js
export default {
  stories: ['../components/**/*.stories.twig'],
  addons: ['@storybook/addon-essentials'],
  framework: {
    name: '@storybook/server-webpack5',
    options: {
      fetchStoryHtml: async (url, path, params) => {
        const qs = new URLSearchParams({ path, ...params }).toString();
        const response = await fetch(`${url}?${qs}`);
        return response.text();
      },
    },
  },
};
```

## Drush Commands

The module provides Drush commands to compile `.stories.twig` files to JSON for Storybook.js to consume.

```bash
# Compile all .stories.twig files in the codebase to JSON
# Run once after adding or changing story files
drush storybook:generate-all-stories

# Compile a single story file
drush storybook:generate-stories path/to/file.stories.twig

# Watch mode — re-compiles automatically on change (Linux / macOS)
# Requires `watch` utility (pre-installed on Linux; Homebrew on macOS)
watch --color drush storybook:generate-all-stories
```

> Drush 12 is required — the module uses PHP Attributes, which Drush 11 does not support.

## Common Mistakes

- **Wrong**: Installing `drupal/storybook` for a UI Suite DaisyUI theme → **Right**: `.story.yml` is the correct tool. These systems don't interact.
- **Wrong**: Not configuring CORS → **Right**: Stories load the Storybook UI but fail to fetch rendered HTML without CORS in `development.services.yml`.
- **Wrong**: Not disabling Twig cache → **Right**: Set `cache: false` in development.services.yml — otherwise template changes require `drush cr` on every edit.
- **Wrong**: Using CJS config format (`module.exports = {}`) with Storybook v9+ → **Right**: ESM-only. Config must use `export default {}`.
- **Wrong**: Accessing `args.key` directly without passing it to the include → **Right**: Args are not auto-injected into SDC components. Pass each arg explicitly in the include hash.
- **Wrong**: Committing `drupal/storybook` to production dependencies → **Right**: Always use `composer require --dev`.
- **Wrong**: Including without `with_context: false` → **Right**: Drupal's global Twig context leaks into the component and makes stories environment-dependent.

## See Also

- [Tool Landscape & Decision](storybook-landscape.md)
- [storybook-addon-sdc (Offline)](addon-sdc-offline.md)
- Reference: `https://www.drupal.org/project/storybook`
- Reference: `https://github.com/e0ipso/twig-storybook` — Twig extension providing the `{% stories %}` / `{% story %}` tags
- Reference: `https://www.lullabot.com/articles/new-storybook-module-drupal`
- Reference: `https://storybook.js.org/docs/api/arg-types` — full argTypes and Controls documentation
