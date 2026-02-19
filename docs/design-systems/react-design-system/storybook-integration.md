---
description: Document React design system components in Storybook using CSF3, argTypes, and the a11y addon.
---

# Storybook Integration

## When to Use

> Use for all design system components. Storybook is the development environment, living documentation, and visual regression baseline — not optional.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Interactive prop controls | `argTypes` with `control` type | Designers can explore variants without code |
| Document all variants visually | One story per variant state | Regression baseline; visual diff catches unintended changes |
| Accessibility audit in Storybook | `@storybook/addon-a11y` | axe-core runs on every story; surfaces WCAG violations during development |
| Design token visualization | `@storybook/addon-themes` or custom decorator | Show tokens alongside components; keeps design/dev in sync |
| Full CSF3 (Component Story Format) | Named exports as stories | Current standard; works with Storybook 7+ and 8+ |

## Pattern

CSF3 story with argTypes (current standard):
```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  component: Button,
  title: 'Components/Button',
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary', 'ghost'] },
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
    disabled: { control: 'boolean' },
    children: { control: 'text' },
  },
} satisfies Meta<typeof Button>;
export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { variant: 'primary', children: 'Button' } };
export const Ghost: Story = { args: { variant: 'ghost', children: 'Ghost Button' } };
export const AllVariants: Story = {
  render: () => (
    <div className="flex gap-4">
      {(['primary', 'secondary', 'ghost'] as const).map(v => (
        <Button key={v} variant={v}>{v}</Button>
      ))}
    </div>
  ),
};
```

## Common Mistakes

- **Wrong**: One "catch-all" story with all props → **Right**: Create one story per meaningful variant state; each is an independent regression baseline
- **Wrong**: Writing stories after the component → **Right**: Write the story first; it forces a clean API and acts as the first consumer
- **Wrong**: Not using `satisfies Meta<typeof Component>` → **Right**: Use `satisfies` for full TypeScript support in CSF3; without it argTypes lose inference
- **Wrong**: Skipping `@storybook/addon-a11y` → **Right**: Accessibility issues found in Storybook cost nothing; found in production they cost everything
- **Wrong**: Default export only without named story exports (CSF2 style) → **Right**: CSF3 named exports enable individual story testing and better tooling integration

## See Also

- [Accessibility Patterns](accessibility-patterns.md)
- [Component Organization](component-organization.md)
- Reference: [Storybook CSF3](https://storybook.js.org/docs/api/csf)
- Reference: [Storybook — Accessibility Testing](https://storybook.js.org/docs/writing-tests/accessibility-testing)
