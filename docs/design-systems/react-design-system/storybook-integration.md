---
description: Document React design system components in Storybook using CSF3, argTypes, and the a11y addon.
tldr: "Use for all design system components. Storybook is the development environment, living documentation, and visual regression baseline — not optional."
---

# Storybook Integration

## When to Use

> For all design system components. Storybook is the development environment, living documentation, and visual regression baseline — not optional.

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

- One "catch-all" story with all props — hard to use as a baseline; create one story per meaningful variant state
- Storybook as an afterthought → write stories alongside the component; it forces you to design a clean API
- Not using `satisfies Meta<typeof Component>` → loses type inference on argTypes; use `satisfies` for full TypeScript support in CSF3
- Skipping `@storybook/addon-a11y` → accessibility issues found in Storybook cost nothing to fix; found in production they cost everything
- Using default export only (CSF2 style) without named story exports → CSF3 named exports enable individual story testing and better tooling integration

## See Also

- [Accessibility Patterns](accessibility-patterns.md)
- [Component Organization](component-organization.md)
- Reference: [Storybook CSF3](https://storybook.js.org/docs/api/csf)
- Reference: [Storybook a11y addon](https://storybook.js.org/docs/8/writing-tests/accessibility-testing)
- Reference: [Storybook 10 Docs](https://storybook.js.org/docs/)
- Reference: [Storybook — UI Testing Handbook: Accessibility](https://storybook.js.org/tutorials/ui-testing-handbook/react/en/accessibility-testing/)
