---
description: "Security surface, known vulnerabilities, access control, and safe Twig/JSX patterns for Canvas on Drupal production sites."
tldr: "Use this when deploying Canvas on a production site. Covers known vulnerabilities, access control model, and safe patterns for SDC and Code Component development."
drupal_version: "11.x"
---

# Security Considerations

## When to Use

> You are deploying Canvas on a production site and need to understand its security surface, known vulnerabilities, access control model, and safe patterns for component development.

## Decision

| Risk area | Action | Notes |
|---|---|---|
| SA-CONTRIB-2026-006 (unpublished page access) | Update to Canvas 1.0.4+ | Required if using unpublished Canvas pages |
| Canvas page creation | Restrict `create canvas_page content` permission | Separate from component library management |
| Component library management | Keep to developers/admins only | Controls what appears in editor component panel |
| Rich text input | Configure Canvas text formats carefully | Default toolbar is restricted; `canvas_full_html` expands it |
| Full HTML format | Restrict which roles can use it | A poorly configured full_html format is an XSS vector |

## Known Issues and Patch Status

**SA-CONTRIB-2026-006** — Canvas does not sufficiently validate access to Canvas Pages when they are unpublished. Mitigated by the fact that Canvas Pages don't have content moderation enabled by default. **Update to Canvas 1.0.4+ if using unpublished Canvas pages.** This is a real, disclosed vulnerability — check the security advisory for current status.

## Access Control Model

Canvas uses Drupal's standard role-based access control. Key permissions to configure correctly:

| Role concern | Canvas permission | Notes |
|---|---|---|
| Who can build Canvas pages | `create canvas_page content` + `edit canvas_page content` | Separate from who can administer components |
| Who can add/edit components to the library | Canvas component management permissions | Keep this restricted to developers/admins |
| Who can access unpublished Canvas pages | Requires careful configuration | See SA-CONTRIB-2026-006 |
| Who can enable/disable components | Admin-level Canvas configuration | Controls what appears in the editor component panel |

## SDC Component Security

SDC components render server-side via Drupal's Twig environment, which has Drupal's standard security protections:

- **Twig auto-escaping**: Drupal's Twig environment escapes output by default — using `{{ variable }}` is safe for string props. Use `{{ variable|raw }}` ONLY for trusted rich text content where you explicitly want HTML output
- **Rich text props**: `contentMediaType: text/html` props are stored through CKEditor and Drupal's text format filter system — the text format's allowed HTML defines what HTML is actually stored. Configure your Canvas text formats appropriately
- **canvas_full_html module**: If using `canvas_full_html`, the `full_html` format must be properly configured — restrict which roles can use it, ensure CKEditor 5 is properly limiting what HTML is allowed
- **Image props via `$ref: canvas.module/image`**: Go through Drupal's Media Library — standard Drupal media access control applies

**Safe Twig patterns for SDC:**
```twig
{# SAFE: string prop (auto-escaped) #}
<h1>{{ headline }}</h1>

{# SAFE: rich text from canvas text format (filtered by text format) #}
{{ body }}

{# UNSAFE: never use |raw on untrusted input #}
{{ user_content|raw }}  {# Only safe if you control the input source #}
```

## Code Component Security

Code Components render browser-side. Security considerations:

- **No server-side exposure**: Code Components don't have direct PHP/Drupal API access — less server-side risk
- **XSS in JSX**: React/Preact auto-escapes string interpolation in JSX — `{someString}` is safe. Use `dangerouslySetInnerHTML` ONLY for trusted rich text, and only when necessary
- **External URLs in links**: Validate that link props resolve to expected domains if you are building internal-only link navigation
- **Prop schema validation**: Canvas validates prop values against the `component.yml` JSON Schema before storing them — use `minLength`, `maxLength`, `pattern`, `enum` constraints to limit input surface

**Safe Code Component patterns:**
```jsx
{/* SAFE: JSX escapes strings automatically */}
<h1>{headline}</h1>

{/* USE WITH CAUTION: only for trusted rich text from Canvas text formats */}
<div dangerouslySetInnerHTML={{ __html: trustedHtml }} />

{/* SAFE: validate URLs before use */}
<a href={ctaUrl?.startsWith('http') ? ctaUrl : '#'}>{ctaLabel}</a>
```

## Common Mistakes

- Running Canvas 1.0.x with unpublished pages without upgrading to 1.0.4+ — see SA-CONTRIB-2026-006
- Granting "create canvas_page" to untrusted roles without testing access to unpublished pages
- Using `{{ variable|raw }}` in SDC templates for any prop that editors can input — this bypasses Twig's auto-escaping and creates XSS risk
- Granting the `full_html` text format to editor roles without reviewing what HTML CKEditor allows — a poorly configured full_html format is an XSS vector
- Not applying Drupal's standard security modules (Security Kit, etc.) to Canvas sites — Canvas is not exempt from site-wide security hardening

## See Also

- Security advisory: https://www.drupal.org/sa-contrib-2026-006
- Canvas releases: https://www.drupal.org/project/canvas/releases (check for security releases)
- OWASP XSS prevention: https://owasp.org/www-community/attacks/xss/
- Drupal security best practices: https://www.drupal.org/docs/security-in-drupal
