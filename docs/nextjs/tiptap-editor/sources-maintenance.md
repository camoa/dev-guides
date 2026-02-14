---
description: TipTap Editor guide
---

## Sources & Maintenance Manifest

### Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Tiptap Official Docs | https://tiptap.dev/docs/editor/getting-started/overview | 1.1, 2.1, 4.1, 9.1 | 2026-02-14 |
| Tiptap Next.js Install | https://tiptap.dev/docs/editor/getting-started/install/nextjs | 2.2, 13.1 | 2026-02-14 |
| Tiptap React Install | https://tiptap.dev/docs/editor/getting-started/install/react | 2.2, 17.1 | 2026-02-14 |
| Tiptap Schema Docs | https://tiptap.dev/docs/editor/core-concepts/schema | 3.2 | 2026-02-14 |
| Tiptap Extensions Docs | https://tiptap.dev/docs/editor/core-concepts/extensions | 8.1 | 2026-02-14 |
| Tiptap Editor API | https://tiptap.dev/docs/editor/api/editor | 4.1, 10.1 | 2026-02-14 |
| Tiptap Events API | https://tiptap.dev/docs/editor/api/events | 10.1 | 2026-02-14 |
| Tiptap Commands API | https://tiptap.dev/docs/editor/api/commands | 9.1 | 2026-02-14 |
| Tiptap Performance Guide | https://tiptap.dev/docs/guides/performance | 17.1, 17.2 | 2026-02-14 |
| Tiptap Output JSON/HTML | https://tiptap.dev/docs/guides/output-json-html | 4.2, 11.1 | 2026-02-14 |
| Tiptap Custom Extensions | https://tiptap.dev/docs/editor/extensions/custom-extensions | 8.1, 8.2, 19.1 | 2026-02-14 |
| Tiptap Collaboration | https://tiptap.dev/docs/editor/extensions/functionality/collaboration | 15.1 | 2026-02-14 |
| Tiptap Security Page | https://tiptap.dev/security | 18.1 | 2026-02-14 |
| ProseMirror Guide | https://prosemirror.net/docs/guide/ | 3.1 | 2026-02-14 |
| Y.js Docs | https://docs.yjs.dev/ | 15.1 | 2026-02-14 |
| Hocuspocus Docs | https://tiptap.dev/hocuspocus/introduction | 15.2 | 2026-02-14 |
| Liveblocks Editor Comparison | https://liveblocks.io/blog/which-rich-text-editor-framework-should-you-choose-in-2025 | 1.2 | 2026-02-14 |
| Liveblocks Tiptap Best Practices | https://liveblocks.io/docs/guides/tiptap-best-practices-and-tips | 17.1, 19.2 | 2026-02-14 |
| Snyk XSS Vulnerability (Link) | https://security.snyk.io/vuln/SNYK-JS-TIPTAPEXTENSIONLINK-14222197 | 6.2, 18.1 | 2026-02-14 |
| Tiptap GitHub Discussion (Sanitization) | https://github.com/ueberdosis/tiptap/discussions/2845 | 18.1 | 2026-02-14 |
| Next.js Route Handlers | https://nextjs.org/docs/app/building-your-application/routing/route-handlers | 13.2 | 2026-02-14 |
| Drupal JSON API Docs | https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module | 14.1 | 2026-02-14 |
| OWASP XSS Guide | https://owasp.org/www-community/attacks/xss/ | 18.1 | 2026-02-14 |

### Code Sources
**Note:** No Drupal research install needed for this guide. All code references are from Tiptap's npm packages and local documentation at `/home/camoa/workspace/claude_memory/future_skills/tiptap-docs/`.

| Source | Path | Guide Sections | Version |
|--------|------|----------------|---------|
| Tiptap Local Docs | `/home/camoa/workspace/claude_memory/future_skills/tiptap-docs/src/content/editor/` | All sections | 2.5+ |
| Tiptap Core Package | `node_modules/@tiptap/core` | 3.1, 8.1, 9.1 | 3.11.1 |
| Tiptap React Package | `node_modules/@tiptap/react` | 2.2, 17.1 | 3.11.1 |
| Tiptap StarterKit | `node_modules/@tiptap/starter-kit` | 7.1 | 3.11.1 |

### Maintenance Notes
- Tiptap version 3.x (as of 2026-02-14) is current; verify compatibility when updating
- Security vulnerabilities actively monitored; check Snyk for new CVEs
- ProseMirror is Tiptap's foundation; breaking changes in ProseMirror affect Tiptap
- Y.js and Hocuspocus versions must be compatible with Tiptap Collaboration extension

**Last Updated:** 2026-02-14
**Guide Version:** 1.0

