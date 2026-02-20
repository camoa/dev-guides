---
description: storybook-addon-sdc for offline/decoupled Storybook development with interactive Controls, without a running Drupal instance
drupal_version: "11.x"
---

# storybook-addon-sdc — Offline/Decoupled

## When to Use

> Use `storybook-addon-sdc` when you need interactive Controls without a running Drupal instance — offline development, CI/CD pipelines, or rapid prototyping. Tradeoff: Drupal-specific Twig functions are not available — output may differ from real Drupal rendering.

Use when:
- You need to develop components offline (no running Drupal instance)
- CI/CD pipelines need visual component testing without a backend
- Rapid prototyping without Docker/DDEV overhead

## Decision

| Need | Tool |
|---|---|
| Interactive Controls, real Drupal rendering | `drupal/storybook` module — requires running Drupal |
| Interactive Controls, no Drupal required | `storybook-addon-sdc` — Vite + Twig.js |
| Static variant browsing, zero Node.js | UI Patterns 2 `.story.yml` |

`storybook-addon-sdc` processes SDC `.component.yml` files and renders component stories using **Vite + Twig.js** (a JavaScript port of Twig). Stories are defined inline in `thirdPartySettings.sdcStorybook` inside the component YAML.

### Drupal Twig Feature Availability

| Drupal Twig Feature | Available in addon-sdc? |
|---|---|
| `drupal_block()` | No |
| `drupal_field()` | No |
| `path()` / `url()` | No |
| `t()` translation | Partial (mock) |
| `attach_library()` | No |
| Standard Twig filters (`|upper`, `|default`) | Yes |
| Basic `{% include %}` with SDC components | Yes |

## Pattern

### How Stories Are Defined (in `.component.yml`)

```yaml
# components/card/card.component.yml
name: Card
slots:
  title:
    title: Title
  text:
    title: Text
props:
  type: object
  properties:
    variant:
      type: string
      enum: [default, primary]

third_party_settings:
  sdcStorybook:
    stories:
      Default:
        args:
          variant: default
          title: "Card Title"
          text: "Card description text."
      Primary:
        args:
          variant: primary
          title: "Featured Card"
          text: "This card uses the primary variant."
```

### Setup

```bash
# In your theme directory
npm install --save-dev @iberdinsky/storybook-addon-sdc
npx storybook@latest init --type vite
```

Configure `.storybook/main.js`:

```js
export default {
  addons: ['@iberdinsky/storybook-addon-sdc'],
  framework: { name: '@storybook/html-vite' },
  stories: ['../components/**/*.component.yml'],
};
```

## Common Mistakes

- **Wrong**: Using `drupal_block()`, `drupal_field()`, or `url()` in Twig templates intended for addon-sdc → **Right**: These are PHP functions — not available in JavaScript (Twig.js) runtime. They throw errors.
- **Wrong**: Assuming addon-sdc output matches Drupal output → **Right**: Especially differs for components using Drupal-specific preprocessing or hooks. Always verify in real Drupal before deploying.
- **Wrong**: Using this as the sole test environment → **Right**: Use for development speed, but validate in real Drupal.
- **Wrong**: Storing stories in `.component.yml` AND writing `.story.yml` files for the same component → **Right**: These are different systems. Pick one approach per component.

## See Also

- [drupal/storybook Module](drupal-storybook-module.md)
- [DDEV + Storybook Setup](ddev-storybook-setup.md)
- Reference: `https://github.com/iberdinsky-skilld/sdc-addon`
- Reference: `drupal-ui-patterns.md` — SDC component structure
