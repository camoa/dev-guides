---
description: JSX to Twig conversion patterns for React → Drupal SDC migration
guide-meta:
  concepts:
    - JSX to Twig
    - React to Drupal
    - conditional rendering translation
    - props to Twig variables
    - children to Twig blocks
    - component composition translation
    - TypeScript to component.yml
  not:
    - React component development
    - Twig template debugging
    - SDC component creation from scratch
  requires:
    - drupal/sdc
  complements:
    - design-systems/react-design-system
    - drupal/twig
    - design-systems/radix-sdc
  specializes: ""
  category: design-systems
---

# JSX to Twig

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand when to translate JSX 1:1 vs restructure | [Overview](overview.md) | Use this when you have an existing React/JSX design system and need to build equivalent Drupal SDC components. This applies whether the React source uses Tailwind, DaisyUI, Radix UI, shadcn/ui, MUI, or any other component library. |
| Convert conditional rendering (`&&`, ternary, `??`) | [Conditional Rendering](conditional-rendering.md) | Use this when converting JSX conditional expressions to Twig. React uses JavaScript expressions inside JSX; Twig uses `{% if %}` tags and filters. |
| Convert `.map()`, `.filter()`, `.slice()` loops | [Loops & Iteration](loops-iteration.md) | Use this when converting JavaScript array methods (`.map()`, `.filter()`, `.reduce()`, `.slice()`) to Twig `{% for %}` loops and filters. |
| Map React props to Twig variables and component.yml | [Props to Twig Variables](props-to-twig.md) | Use this when mapping React component props to SDC `component.yml` properties and Twig template variables. This is the core translation step for every component. |
| Convert children/slots to Twig blocks | [Children & Slots](children-slots.md) | Use this when converting React's children, named props that accept JSX, render props, or compound component patterns into Twig blocks and SDC slots. |
| Handle onClick, onChange, event handlers | [Event Handlers](event-handlers.md) | Use this when converting React event handlers (`onClick`, `onChange`, `onSubmit`, etc.) to Drupal's server-rendered architecture. React events have NO direct Twig equivalent. |
| Translate component composition patterns | [Component Composition](composition.md) | Use this when converting React patterns for combining components -- nesting, polymorphic elements, higher-order components, context providers, and compound component APIs. |
| Convert className, CSS Modules, Tailwind, CVA | [Styling Translation](styling.md) | Use this when converting React styling patterns -- `className`, CSS Modules, Tailwind utilities, `cn()`/`clsx()`, `cva()` (class-variance-authority), inline styles -- to Twig and SDC equivalents. |
| Turn a TypeScript interface into component.yml | [TypeScript to Component.yml](typescript-to-component-yml.md) | Use this when you have a TypeScript interface or Props type definition and need to produce a complete SDC `component.yml` schema. This is a step-by-step workflow for the most common translation task. |
