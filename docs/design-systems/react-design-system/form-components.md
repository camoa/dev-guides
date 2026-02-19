---
description: Build accessible form components with compound FormField, react-hook-form integration, Zod validation, and aria-describedby error linking.
---

# Form Components

## When to Use

> Use when building Input, Select, Checkbox, Textarea, or any form field component. Form components have unique requirements: validation state, error display, accessibility linking, and library integration.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Unmanaged form state (large forms) | react-hook-form with `register` | Uncontrolled inputs; minimal re-renders; schema validation |
| Controlled input in design system | `value` + `onChange` with `forwardRef` | Works with react-hook-form `Controller`; also works standalone |
| Accessible field (label + input + error) | Compound `FormField` component | Links label, input, and error via `id`/`aria-describedby` |
| Schema validation | Zod + react-hook-form `zodResolver` | Type-safe validation; errors derived from schema, not ad-hoc logic |
| Error display | `aria-describedby` on input → error `id` | Screen readers announce errors on focus; no additional JS needed |

## Pattern

Accessible FormField compound component:
```tsx
const FormFieldContext = React.createContext<{ id: string } | null>(null);

export function FormField({ children }: { children: React.ReactNode }) {
  const id = React.useId();
  return <FormFieldContext.Provider value={{ id }}>{children}</FormFieldContext.Provider>;
}
FormField.Label = function FormLabel({ children }: { children: React.ReactNode }) {
  const { id } = React.useContext(FormFieldContext)!;
  return <label htmlFor={id} className="block text-sm font-medium">{children}</label>;
};
FormField.Input = React.forwardRef<HTMLInputElement, InputProps & { errorId?: string }>(
  ({ errorId, className, ...props }, ref) => {
    const { id } = React.useContext(FormFieldContext)!;
    return (
      <input
        id={id}
        ref={ref}
        aria-describedby={errorId}
        aria-invalid={!!errorId}
        className={cn('border rounded px-3 py-2', errorId && 'border-destructive', className)}
        {...props}
      />
    );
  }
);
// role="alert" for submit-time errors; role="status" for live validation
FormField.Error = function FormError({ children, id, live = 'polite' }: { children?: React.ReactNode; id: string; live?: 'polite' | 'assertive' }) {
  if (!children) return null;
  return <p id={id} role={live === 'assertive' ? 'alert' : 'status'} className="text-sm text-destructive mt-1">{children}</p>;
};
```

react-hook-form integration:
```tsx
const { control, handleSubmit } = useForm<FormValues>({ resolver: zodResolver(schema) });
<Controller name="email" control={control} render={({ field, fieldState }) => (
  <FormField>
    <FormField.Label>Email</FormField.Label>
    <FormField.Input {...field} errorId={fieldState.error ? 'email-error' : undefined} />
    <FormField.Error id="email-error">{fieldState.error?.message}</FormField.Error>
  </FormField>
)} />
```

## Common Mistakes

- **Wrong**: Controlled inputs without `forwardRef` → **Right**: react-hook-form's `register` uses ref internally; inputs without refs fall back to uncontrolled behavior
- **Wrong**: Managing form state with `useState` per field → **Right**: One re-render per keystroke across the whole form; use react-hook-form
- **Wrong**: Displaying errors without `aria-describedby` → **Right**: Screen reader users see the visual error but don't know it's associated with the field
- **Wrong**: Using `required` HTML attribute instead of schema validation → **Right**: Doesn't integrate with react-hook-form's error system; validation displays inconsistently
- **Wrong**: Manually crafted IDs for label/input linking → **Right**: Use `React.useId()`; manually crafted IDs collide in pages with multiple forms

## See Also

- [Component Organization](component-organization.md)
- [Layout Components](layout-components.md)
- Reference: [react-hook-form — Advanced Usage](https://react-hook-form.com/advanced-usage)
- Reference: [react-hook-form — Controller](https://react-hook-form.com/docs/usecontroller/controller)
- Reference: [Zod](https://zod.dev/)
