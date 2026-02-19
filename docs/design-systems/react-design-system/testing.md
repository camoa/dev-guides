---
description: Test React design system components using React Testing Library for behavior, jest-axe for accessibility, and Storybook for visual regression.
---

# Testing

## When to Use

> Use for every design system component. Tests protect the API contract — they catch regressions before consumers notice.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Behavior/interaction tests | React Testing Library (RTL) | Tests from user perspective; survives refactoring |
| Automated accessibility checks | jest-axe or vitest-axe | axe-core runs on rendered output; catches WCAG violations per component |
| Visual regression | Storybook + Chromatic or Playwright visual | Pixel-level comparison; catches unintended style changes |
| Type-level tests | `expectTypeOf` (vitest) or `tsd` | Verify TypeScript inference works correctly for polymorphic props |
| Component isolation | RTL `render()` without full app setup | No routing/store needed; fast; focused |

## Pattern

RTL + jest-axe (standard design system test):
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from './Button';

expect.extend(toHaveNoViolations);

describe('Button', () => {
  it('renders with correct variant class', () => {
    render(<Button variant="primary">Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Accessible</Button>);
    expect(await axe(container)).toHaveNoViolations();
  });

  it('is disabled when disabled prop is set', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Common Mistakes

- **Wrong**: Testing implementation details (class names, internal state) → **Right**: Test behavior via `getByRole`; implementation tests break on refactoring
- **Wrong**: Skipping axe tests → **Right**: Automated axe catches ~35% of WCAG violations; worth running on every component
- **Wrong**: Testing only the happy path → **Right**: Design system components must handle disabled, loading, and error states; test all behavioral variants
- **Wrong**: Using `getByTestId` as default selector → **Right**: Prefer semantic queries (`getByRole`, `getByLabelText`) that reflect how users interact
- **Wrong**: No visual regression baseline → **Right**: Style changes are invisible in unit tests; set up Storybook + Chromatic or Playwright screenshots
- **Wrong**: Mocking child components in integration tests → **Right**: Only mock network/external dependencies; mocking children defeats composition testing

## See Also

- [Performance](performance.md)
- [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md)
- Reference: [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- Reference: [jest-axe](https://github.com/nickcolley/jest-axe)
- Reference: [Storybook — Accessibility Testing](https://storybook.js.org/docs/writing-tests/accessibility-testing)
