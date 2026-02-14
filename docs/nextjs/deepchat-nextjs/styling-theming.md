---
description: Style DeepChat with CSS variables, messageStyles, and shadow DOM techniques including dark mode and custom themes
---

# Styling & Theming

## When to Use

> Use CSS variables for brand colors. Use messageStyles for message bubbles. Use auxiliaryStyle for scrollbar and shadow DOM overrides.

## Decision

| Scenario | Pattern |
|----------|---------|
| Brand colors | CSS variables |
| Message bubbles | messageStyles |
| Dark mode | Theme object |
| Scrollbar styling | auxiliaryStyle |
| Complex overrides | auxiliaryStyle + ::part() |

## The Challenge

DeepChat uses Shadow DOM. Standard CSS doesn't penetrate shadow boundaries. Use CSS custom properties (variables) instead.

## Basic Styling

```tsx
<DeepChat
  style={{ borderRadius: '8px', height: '600px' }}
  chatStyle={{ backgroundColor: '#f5f5f5' }}
/>
```

## CSS Variables

```tsx
<DeepChat
  style={{
    '--chat-primary-color': '#007bff',
    '--chat-secondary-color': '#6c757d',
    borderRadius: '8px',
  }}
/>
```

## Message Styles

```tsx
const messageStyles = {
  default: {
    shared: {
      bubble: {
        backgroundColor: '#fff',
        borderRadius: '12px',
        padding: '12px 16px',
        maxWidth: '70%',
      },
    },
    user: {
      bubble: {
        backgroundColor: '#007bff',
        color: '#fff',
      },
    },
    ai: {
      bubble: {
        backgroundColor: '#f0f0f0',
        color: '#000',
      },
    },
  },
};

<DeepChat messageStyles={messageStyles} />
```

## Dark Mode

```tsx
const darkTheme = {
  chatStyle: { backgroundColor: '#1a1a1a' },
  messageStyles: {
    default: {
      shared: {
        bubble: {
          backgroundColor: '#2a2a2a',
          color: '#fff',
        },
      },
      user: {
        bubble: {
          backgroundColor: '#0d6efd',
        },
      },
    },
  },
  textInput: {
    styles: {
      container: {
        backgroundColor: '#2a2a2a',
        border: '1px solid #444',
        color: '#fff',
      },
    },
  },
};

<DeepChat {...darkTheme} />
```

## Auxiliary Styles (Advanced)

```tsx
<DeepChat
  auxiliaryStyle={`
    ::-webkit-scrollbar {
      width: 8px;
    }
    ::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: 4px;
    }
  `}
/>
```

## Avatars

```tsx
<DeepChat
  avatars={{
    ai: {
      src: '/images/bot-avatar.svg',
      styles: {
        avatar: {
          width: '32px',
          height: '32px',
          borderRadius: '50%',
        },
      },
    },
    user: {
      src: '/images/user-avatar.svg',
    },
  }}
/>
```

## Submit Button

```tsx
<DeepChat
  submitButtonStyles={{
    submit: {
      container: {
        default: { backgroundColor: '#007bff' },
        hover: { backgroundColor: '#0056b3' },
        click: { backgroundColor: '#004085' },
      },
    },
    disabled: {
      container: {
        default: { backgroundColor: '#ccc', cursor: 'not-allowed' },
      },
    },
  }}
/>
```

## Pattern

```tsx
// Reusable theme system
const themes = {
  light: {
    chatStyle: { backgroundColor: '#fff' },
    messageStyles: {
      default: {
        ai: { bubble: { backgroundColor: '#f0f0f0' } },
        user: { bubble: { backgroundColor: '#007bff', color: '#fff' } },
      },
    },
  },
  dark: {
    chatStyle: { backgroundColor: '#1a1a1a' },
    messageStyles: {
      default: {
        ai: { bubble: { backgroundColor: '#2a2a2a', color: '#fff' } },
        user: { bubble: { backgroundColor: '#0d6efd', color: '#fff' } },
      },
    },
  },
};

function ChatWidget({ theme = 'light' }) {
  return <DeepChat {...themes[theme]} />;
}
```

## Common Mistakes

- **Wrong**: Using standard CSS selectors → **Right**: Shadow DOM blocks them. Use CSS variables and messageStyles
- **Wrong**: Not using CSS variables for colors → **Right**: Always use `--custom-property` for dynamic values to enable theming
- **Wrong**: Forgetting `auxiliaryStyle` for webkit → **Right**: Scrollbar styles need webkit-specific CSS in auxiliaryStyle
- **Wrong**: Over-nesting messageStyles → **Right**: Keep flat. `default.shared` applies to all, then role-specific
- **Wrong**: Not testing in shadow DOM → **Right**: Styles that work outside may fail inside. Test in actual component
- **Wrong**: Inline styles on container div → **Right**: Applies to outer container, not shadow content. Use `style` or `chatStyle` prop

## See Also

- [Best Practices](best-practices.md)
- Reference: https://www.byteplus.com/en/topic/496757
- Reference: https://css-tricks.com/styling-in-the-shadow-dom-with-css-shadow-parts/
- Reference: https://gomakethings.com/styling-the-shadow-dom-with-css-variables-in-web-components/
