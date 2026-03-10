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

| I need to... | Guide |
|-------------|-------|
| Understand when to translate JSX 1:1 vs restructure | [Overview](overview.md) |
| Convert conditional rendering (`&&`, ternary, `??`) | [Conditional Rendering](conditional-rendering.md) |
| Convert `.map()`, `.filter()`, `.slice()` loops | [Loops & Iteration](loops-iteration.md) |
| Map React props to Twig variables and component.yml | [Props to Twig Variables](props-to-twig.md) |
| Convert children/slots to Twig blocks | [Children & Slots](children-slots.md) |
| Handle onClick, onChange, event handlers | [Event Handlers](event-handlers.md) |
| Translate component composition patterns | [Component Composition](composition.md) |
| Convert className, CSS Modules, Tailwind, CVA | [Styling Translation](styling.md) |
| Turn a TypeScript interface into component.yml | [TypeScript to Component.yml](typescript-to-component-yml.md) |
