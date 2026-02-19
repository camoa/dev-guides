---
description: Use DaisyUI in React with CVA variant management, theme switching, and Radix UI accessibility integration
---

# DaisyUI and React

## When to Use

> Building React components that use DaisyUI classes, managing variants with CVA, and integrating DaisyUI theming with React patterns.

## Decision

| If you need... | Pattern | Why |
|----------------|---------|-----|
| Simple DaisyUI component | Direct class strings in JSX | No abstraction needed for single-use |
| Component with multiple variants | CVA + DaisyUI modifier classes | CVA manages the combination logic |
| Theme-aware custom styling | CSS custom property overrides | Respects DaisyUI theming without bypassing it |
| Accessible interactive patterns | DaisyUI HTML structure + Radix UI | DaisyUI handles visuals; Radix handles ARIA |

## Pattern

### Direct JSX Usage

```tsx
export function SaveButton({ onClick }: { onClick: () => void }) {
  return (
    <button className="btn btn-primary" onClick={onClick}>
      Save Changes
    </button>
  );
}
```

### CVA for Variant Management

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils"; // tailwind-merge + clsx

const buttonVariants = cva("btn", {
  variants: {
    intent: {
      primary: "btn-primary",
      secondary: "btn-secondary",
      ghost: "btn-ghost",
      danger: "btn-error btn-outline",
    },
    size: { sm: "btn-sm", md: "btn-md", lg: "btn-lg" },
    block: { true: "btn-block" },
  },
  defaultVariants: { intent: "primary", size: "md" },
});

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants>;

export function Button({ intent, size, block, className, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ intent, size, block }), className)} {...props} />
  );
}
```

### Theme Switching in React

```tsx
"use client";
import { useState } from "react";

export function ThemeSwitcher() {
  const [theme, setTheme] = useState("light");
  const toggleTheme = () => {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
  };
  return (
    <button className="btn btn-ghost btn-square" onClick={toggleTheme} aria-label="Toggle theme">
      {theme === "light" ? <MoonIcon /> : <SunIcon />}
    </button>
  );
}
```

### DaisyUI CSS + Radix Accessibility

```tsx
import * as Dialog from "@radix-ui/react-dialog";

export function Modal({ open, onClose, title, children }) {
  return (
    <Dialog.Root open={open} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal modal-open" />
        <Dialog.Content className="modal-box" aria-describedby="modal-desc">
          <Dialog.Title className="text-lg font-bold">{title}</Dialog.Title>
          <div id="modal-desc" className="py-4">{children}</div>
          <div className="modal-action">
            <Dialog.Close asChild>
              <button className="btn">Close</button>
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

## Common Mistakes

- **Wrong**: CSS-only DaisyUI checkbox tricks (modal-toggle, drawer-toggle) in React — **Right**: Manage open/closed in component state and toggle the `-open` class: `cn("drawer", isOpen && "drawer-open")`
- **Wrong**: String concatenation for conditional classes — **Right**: Use `cn()` from tailwind-merge + clsx
- **Wrong**: Missing `"use client"` on theme switcher in Next.js App Router — **Right**: Components using `useState` require the directive

## See Also

- [Customization Patterns](customization-patterns.md)
- [Security and Accessibility](security-accessibility.md)
- Reference: `react-design-system.md` Section 5 — `cn()` setup with tailwind-merge + clsx
- Reference: `react-design-system.md` Section 6 — CVA variant patterns
- Reference: `design-system-tailwind.md` Section 10.3 — tailwind-merge conflict resolution
