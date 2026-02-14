---
description: You're storing or displaying user-generated content from Tiptap.
---

## 18.1 Security Model & XSS Prevention

### When to Use
You're storing or displaying user-generated content from Tiptap.

### Threat Model
| Attack Vector | Risk | Mitigation |
|---|---|---|
| `javascript:` URLs in links | High | Validate `href` to exclude `javascript:`, `data:`, `vbscript:` |
| `<script>` tags in HTML | High | Tiptap schema blocks `<script>` if not in schema (protection built-in) |
| Event handlers (`onclick`) | Medium | Tiptap doesn't parse event attributes (safe) |
| Base64 images | Medium | Disable `allowBase64` or validate size/type |
| User-controlled attributes | Low | Sanitize custom attributes in `parseHTML` |

### Patterns

#### Validate Link URLs
```typescript
import Link from '@tiptap/extension-link'

Link.configure({
  validate: (url) => {
    // Only allow http/https protocols
    return /^https?:\/\//.test(url)
  },
  protocols: ['http', 'https'], // Whitelist protocols
  HTMLAttributes: {
    rel: 'noopener noreferrer nofollow', // Security headers
  },
})
```

#### Server-Side Sanitization (Node.js)
```typescript
import { JSDOM } from 'jsdom'
import DOMPurify from 'isomorphic-dompurify'

function sanitizeHTML(html: string): string {
  const window = new JSDOM('').window
  const purify = DOMPurify(window)

  return purify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'h1', 'h2', 'h3', 'strong', 'em', 'a', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'class'],
    ALLOW_DATA_ATTR: false,
  })
}

// Before storing in database
const cleanHTML = sanitizeHTML(editor.getHTML())
```

#### Client-Side Sanitization
```typescript
import DOMPurify from 'dompurify'

// Before rendering user content
const cleanHTML = DOMPurify.sanitize(htmlFromDatabase, {
  ALLOWED_TAGS: ['p', 'strong', 'em', 'a'],
  ALLOWED_ATTR: ['href'],
})

document.querySelector('.preview').innerHTML = cleanHTML
```

#### Content Security Policy (CSP)
```typescript
// Next.js headers
export default function Page() {
  return { /* content */ }
}

export const metadata = {
  headers: [
    {
      key: 'Content-Security-Policy',
      value: "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    },
  ],
}

// If using injectCSS, pass nonce
const editor = new Editor({
  injectCSS: true,
  injectNonce: 'your-csp-nonce',
})
```

### Common Mistakes
- Storing HTML without sanitization → XSS when content is displayed
- Trusting `getHTML()` output → Malicious users can craft payloads; sanitize server-side
- Not validating link URLs → `javascript:alert(1)` executes when clicked (CVE-2025-14284)
- Allowing all protocols in links → Enable only `http` and `https`
- Displaying HTML with `innerHTML` → Use DOMPurify or framework's safe rendering
- Not setting CSP headers → Defense-in-depth; CSP blocks many XSS attacks
- Trusting client-side sanitization alone → Sanitize on server (client can be bypassed)

### See Also
- → 6.2 Link Mark | Link URL validation
- → 11.1 Serialization | HTML output
- Reference: https://security.snyk.io/vuln/SNYK-JS-TIPTAPEXTENSIONLINK-14222197
- OWASP XSS: https://owasp.org/www-community/attacks/xss/

