---
description: storybook-addon-sdc for offline/decoupled Storybook development without a running Drupal instance
drupal_version: "11.x"
---

# storybook-addon-sdc — Offline/Decoupled

## When to Use

> Use `storybook-addon-sdc` when you need offline component development (no running Drupal instance), CI/CD visual testing without a backend, or rapid prototyping without Docker/DDEV overhead. Tradeoff: Drupal-specific Twig functions are NOT available — output may differ from real Drupal rendering.

## Decision

| Need | Use addon-sdc? |
|---|---|
| Offline development, no Drupal instance | Yes |
| CI/CD pipeline visual component testing | Yes |
| Rapid prototyping without DDEV overhead | Yes |
| Components using `drupal_block()` / `url()` / `path()` | No — use `drupal/storybook` module |
| Final rendering verification before deploy | No — always verify in real Drupal |

## Pattern

### How Stories Are Defined

Stories go inside `third_party_settings.sdcStorybook` in the `.component.yml` file:

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

### Drupal Twig Feature Availability

| Drupal Twig Feature | Available in addon-sdc? |
|---|---|
| `drupal_block()` | No |
| `drupal_field()` | No |
| `path()` / `url()` | No |
| `t()` translation | Partial (mock) |
| `attach_library()` | No |
| Standard Twig filters (`\|upper`, `\|default`) | Yes |
| Basic `{% include %}` with SDC components | Yes |

Never treat addon-sdc output as ground truth. Always verify components against real Drupal rendering before deploying.

## Common Mistakes

- **Wrong**: Using `drupal_block()`, `drupal_field()`, or `url()` in Twig templates intended for addon-sdc → **Right**: These are PHP functions — Twig.js (JavaScript) throws errors on them
- **Wrong**: Using addon-sdc output as the sole test environment → **Right**: Use it for speed, but validate in real Drupal before deploying
- **Wrong**: Storing stories in both `.component.yml` (sdcStorybook) AND `.story.yml` files → **Right**: These are different systems; pick one approach per component

## See Also

- [Tool Landscape & Decision](storybook-landscape.md)
- [drupal/storybook Module](drupal-storybook-module.md)
- [DDEV + Storybook Setup](ddev-storybook-setup.md)
- Reference: https://github.com/iberdinsky-skilld/sdc-addon
- Reference: `drupal-ui-patterns.md` — SDC component structure
