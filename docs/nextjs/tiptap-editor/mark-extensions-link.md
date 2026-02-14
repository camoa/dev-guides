---
description: You need hyperlinks with URL validation and target control.
---

## 6.2 Link Mark & URL Handling

### When to Use
You need hyperlinks with URL validation and target control.

### Description
Link mark enables clickable hyperlinks with attributes: href, target, rel, class.

### Options
| Option | Type | Default | Notes |
|---|---|---|---|
| openOnClick | boolean | true | Click link to open URL |
| linkOnPaste | boolean | true | Auto-link pasted URLs |
| autolink | boolean | true | Auto-detect URLs while typing |
| protocols | Array | ['http', 'https', ...] | Allowed URL protocols |
| HTMLAttributes | Object | {} | Default attributes (target, rel) |
| validate | function | undefined | Custom URL validation |

### Usage Example
```typescript
import Link from '@tiptap/extension-link'

Link.configure({
  openOnClick: false, // Disable click to open (edit mode)
  linkOnPaste: true,
  protocols: ['http', 'https', 'mailto'], // Restrict protocols
  validate: (url) => /^https?:\/\//.test(url), // Only http/https
  HTMLAttributes: {
    target: '_blank',
    rel: 'noopener noreferrer nofollow',
    class: 'external-link',
  },
})

// Set link
editor.commands.setLink({ href: 'https://example.com' })

// Toggle link (set if not exists, unset if exists)
editor.commands.toggleLink({ href: 'https://example.com' })

// Unset link
editor.commands.unsetLink()

// Check if link is active
editor.isActive('link') // true or false

// Get link attributes
editor.getAttributes('link').href
```

### Gotchas
- **XSS vulnerability:** Link extension doesn't sanitize `javascript:` URLs by default (CVE-2025-14284). MUST validate URLs to exclude `javascript:`, `data:`, `vbscript:` protocols
- Links are NOT exitable by default (cursor trapped at end); set `exitable: true` in custom link extension if needed
- `openOnClick: true` makes links hard to edit (cursor clicks navigate away); disable in edit mode
- Link mark is inclusive by default (typing after link extends it); most editors want `inclusive: false`

### Common Mistakes
- Allowing `javascript:` URLs → Critical XSS vector; validate protocol explicitly
- Not setting `rel="noopener noreferrer"` on external links → Security and SEO issue
- Using default `openOnClick: true` in editing UI → Users can't select/edit links easily
- Forgetting to unset link when removing href → Empty link marks persist invisibly
- Not validating pasted URLs → Users can paste malicious links; use `validate` option

### See Also
- → 18.1 Security Model | XSS prevention
- → 6.3 Highlight & Text Style | Other marks
- Reference: https://tiptap.dev/docs/editor/extensions/marks/link
- Security: https://security.snyk.io/vuln/SNYK-JS-TIPTAPEXTENSIONLINK-14222197

