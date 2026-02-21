---
description: Security surface, known vulnerabilities, access control, and safe Twig/JSX patterns for Canvas on Drupal production sites.
drupal_version: "11.x"
---

# Security Considerations

## When to Use

> Use this when deploying Canvas on a production site. Covers known vulnerabilities, access control model, and safe patterns for SDC and Code Component development.

## Decision

| Risk area | Action | Notes |
|---|---|---|
| SA-CONTRIB-2026-006 (unpublished page access) | Update to Canvas 1.0.4+ | Required if using unpublished Canvas pages |
| Canvas page creation | Restrict `create canvas_page content` permission | Separate from component library management |
| Component library management | Keep to developers/admins only | Controls what appears in editor component panel |
| Rich text input | Configure Canvas text formats carefully | Default toolbar is restricted; `canvas_full_html` expands it |
| Full HTML format | Restrict which roles can use it | A poorly configured full_html format is an XSS vector |

## Pattern

**Safe Twig patterns for SDC:**

```twig
{# SAFE: string prop (auto-escaped) #}
<h1>{{ headline }}</h1>

{# SAFE: rich text from canvas text format (filtered by text format) #}
{{ body }}

{# UNSAFE: never use |raw on untrusted input #}
{{ user_content|raw }}  {# Only safe if you control the input source #}
```

**Safe Code Component patterns:**

```jsx
{/* SAFE: JSX escapes strings automatically */}
<h1>{headline}</h1>

{/* USE WITH CAUTION: only for trusted rich text from Canvas text formats */}
<div dangerouslySetInnerHTML={{ __html: trustedHtml }} />

{/* SAFE: validate URLs before use */}
<a href={ctaUrl?.startsWith('http') ? ctaUrl : '#'}>{ctaLabel}</a>
```

**Access control model:**

| Role concern | Canvas permission | Notes |
|---|---|---|
| Who can build Canvas pages | `create canvas_page content` + `edit canvas_page content` | Separate from who can administer components |
| Who can add/edit components to the library | Canvas component management permissions | Keep this restricted to developers/admins |
| Who can access unpublished Canvas pages | Requires careful configuration | See SA-CONTRIB-2026-006 |
| Who can enable/disable components | Admin-level Canvas configuration | Controls what appears in the editor component panel |

**SDC component security notes:**
- Drupal's Twig environment escapes output by default — `{{ variable }}` is safe for string props
- `contentMediaType: text/html` props are stored through CKEditor and Drupal's text format filter system — configure Canvas text formats appropriately
- Image props via `$ref: canvas.module/image` go through Drupal's Media Library — standard media access control applies

**Code Component security notes:**
- Code Components render browser-side — no direct PHP/Drupal API access; less server-side risk
- React/Preact auto-escapes string interpolation in JSX — `{someString}` is safe
- Use `dangerouslySetInnerHTML` only for trusted rich text, and only when necessary
- Canvas validates prop values against the `component.yml` JSON Schema — use `minLength`, `maxLength`, `pattern`, `enum` constraints to limit input surface

## Common Mistakes

- **Wrong**: Running Canvas 1.0.x with unpublished pages without upgrading → **Right**: Update to Canvas 1.0.4+ immediately (see SA-CONTRIB-2026-006)
- **Wrong**: Granting "create canvas_page" to untrusted roles without testing access to unpublished pages → **Right**: Test access controls before production launch
- **Wrong**: Using `{{ variable|raw }}` in SDC templates for any prop that editors can input → **Right**: This bypasses Twig's auto-escaping and creates XSS risk
- **Wrong**: Granting the `full_html` text format to editor roles without reviewing what HTML CKEditor allows → **Right**: A poorly configured full_html format is an XSS vector
- **Wrong**: Not applying Drupal's standard security modules (Security Kit, etc.) to Canvas sites → **Right**: Canvas is not exempt from site-wide security hardening

## See Also

- Security advisory: https://www.drupal.org/sa-contrib-2026-006
- Canvas releases: https://www.drupal.org/project/canvas/releases (check for security releases)
- OWASP XSS prevention: https://owasp.org/www-community/attacks/xss/
- Drupal security best practices: https://www.drupal.org/docs/security-in-drupal
