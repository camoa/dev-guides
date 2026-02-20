---
description: Setup and usage of the drupal/storybook module for Twig-based Storybook stories with full Drupal fidelity
drupal_version: "11.x"
---

# drupal/storybook Module — Twig Stories

## When to Use

> Use the `drupal/storybook` module when your theme uses custom Twig templates that need real Drupal rendering — actual Twig functions, filters, entity data. Do NOT use this for UI Suite DaisyUI themes; `.story.yml` is already there and is a completely separate system.

## Decision

| Scenario | Use drupal/storybook? |
|---|---|
| UI Suite DaisyUI theme | No — use `.story.yml` instead |
| Radix-based custom theme with Storybook.js UI | Yes |
| Custom Twig templates needing `drupal_block()`, `url()`, etc. | Yes |
| Offline / CI component testing without Drupal | No — use `storybook-addon-sdc` |
| Simple Drupal-native browser, no Node.js | No — use `sdc_styleguide` |

## Pattern

### Architecture

```
Storybook.js (browser)
    ↓  HTTP request with story args
Drupal backend (running DDEV/local)
    ↓  renders Twig template with args
    ↑  returns rendered HTML
Storybook.js renders HTML in iframe
```

### Drupal Setup

```bash
composer require drupal/storybook --dev
drush en storybook
```

Configure CORS in `web/sites/development.services.yml`:

```yaml
parameters:
  cors.config:
    enabled: true
    allowedHeaders: ['*']
    allowedMethods: ['GET', 'POST', 'OPTIONS']
    allowedOrigins: ['http://localhost:6006', 'https://localhost:6007']
    exposedHeaders: false
    maxAge: false
    supportsCredentials: false
services:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

### Storybook Setup

```bash
cd web/themes/custom/my_theme
npx storybook@latest init --type server
```

Configure `.storybook/main.js` (ESM format — required for Storybook v9+):

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
  docs: { autodocs: true },
};
```

### Writing Twig Stories

```twig
{# components/card/card.stories.twig #}
{% stories title="Card" %}

{% story name="Default" args={title: "Hello World", variant: "default"} %}
  {{ include('my_theme:card', {
    title: args.title,
    variant: args.variant,
  }, with_context: false) }}
{% endstory %}

{% story name="Primary" args={title: "Primary Card", variant: "primary"} %}
  {{ include('my_theme:card', {
    title: args.title,
    variant: args.variant,
  }, with_context: false) }}
{% endstory %}

{% endstories %}
```

## Common Mistakes

- **Wrong**: Installing `drupal/storybook` on a UI Suite DaisyUI theme → **Right**: Unnecessary — `.story.yml` is the right tool
- **Wrong**: No CORS config → **Right**: Stories will fail with network errors; CORS must be enabled in `development.services.yml`
- **Wrong**: Twig cache enabled during development → **Right**: Cached templates require a full cache clear on every story update; set `cache: false`
- **Wrong**: Storybook config with `module.exports = {}` on v9+ → **Right**: ESM-only — use `export default {}`
- **Wrong**: `composer require drupal/storybook` without `--dev` → **Right**: This is a dev dependency; exclude from production deploys
- **Wrong**: Previewing stories without a running Drupal instance → **Right**: Unlike addon-sdc, this module requires a live backend

## See Also

- [Tool Landscape & Decision](storybook-landscape.md)
- [storybook-addon-sdc (Offline)](addon-sdc-offline.md)
- [DDEV + Storybook Setup](ddev-storybook-setup.md)
- Reference: https://www.drupal.org/project/storybook
- Reference: https://www.lullabot.com/articles/new-storybook-module-drupal
