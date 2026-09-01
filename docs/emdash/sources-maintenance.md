---
description: "Source references and maintenance manifest for the emdash guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| EmDash docs home | https://docs.emdashcms.com/ | - | 2026-06-17 |
| Introduction | https://docs.emdashcms.com/introduction/ | Getting Started and Architecture | 2026-06-17 |
| Admin Panel concept | https://docs.emdashcms.com/concepts/admin-panel/ | Getting Started and Architecture | 2026-06-17 |
| Getting Started guide | https://docs.emdashcms.com/getting-started/ | Getting Started and Architecture | 2026-06-17 |
| REST API reference | https://docs.emdashcms.com/reference/rest-api/ | Getting Started and Architecture, Content Modeling | 2026-06-17 |
| Architecture concept | https://docs.emdashcms.com/concepts/architecture/ | Getting Started and Architecture | 2026-06-17 |
| Cloudflare deployment | https://docs.emdashcms.com/deployment/cloudflare/ | Getting Started and Architecture | 2026-06-17 |
| Node.js deployment | https://docs.emdashcms.com/deployment/nodejs/ | Getting Started and Architecture | 2026-06-17 |
| Database deployment | https://docs.emdashcms.com/deployment/database/ | Getting Started and Architecture | 2026-06-17 |
| Plugins overview | https://docs.emdashcms.com/plugins/overview/ | Getting Started and Architecture | 2026-06-17 |
| Choosing a plugin format | https://docs.emdashcms.com/plugins/creating-plugins/choosing-a-format/ | Getting Started and Architecture | 2026-06-17 |
| Collections concept | https://docs.emdashcms.com/concepts/collections/ | Content Modeling | 2026-06-17 |
| Field Types reference | https://docs.emdashcms.com/reference/field-types/ | Content Modeling | 2026-06-17 |
| Content Model concept | https://docs.emdashcms.com/concepts/content-model/ | Content Modeling | 2026-06-17 |
| Querying Content guide | https://docs.emdashcms.com/guides/querying-content/ | Content Modeling | 2026-06-17 |
| Coming from WordPress | https://docs.emdashcms.com/coming-from/wordpress/ | Content Modeling | 2026-06-17 |
| Working with Content guide | https://docs.emdashcms.com/guides/working-with-content/ | Content Modeling | 2026-06-17 |
| EmDash repository | https://github.com/emdash-cms/emdash | Getting Started and Architecture | 2026-06-17 |

Some prose in the guide also cites relative doc paths (e.g. `/reference/configuration/`, `/reference/cli/`, `/reference/api/`, `/guides/create-a-blog/`, `/guides/preview/`) alongside a full URL in the same parenthetical. Those are not standalone URLs in the guide text, so they are not listed as separate rows here.

## Code Sources
No local install of the `emdash` npm package was available for this pass — there is no `node_modules/emdash` or cloned repo checkout on this machine to read against. Code blocks in the guide (the `astro.config.mjs` integration example, the `live.config.ts` loader, the `getEmDashCollection`/`getEmDashEntry` query example, the collection JSON shape, and the `PortableText` render example) are transcribed from the official docs pages listed above, not read from an installed package.

| Source | Relative Path | Guide Sections | Version |
|--------|----------------|-----------------|---------|
| emdash (npm) | not installed in this pass — no local checkout found | Getting Started and Architecture, Content Modeling | 0.20.0, per the guide's own source-verification pin and the tracks declaration for this pass; not verified against an installed package.json |

## Version History
| Date | Change |
|------|--------|
| 2026-06-17 | Manifest reconstructed from the guide's own citations. No installed source was available; code examples are drawn from the official docs pages, not from a local package install. |
