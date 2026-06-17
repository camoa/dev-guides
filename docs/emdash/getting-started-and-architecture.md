---
description: Onboarding and architecture for building a real site on EmDash — the Astro integration model, scaffolding, what you get out of the box, the deploy-target decision, and when EmDash fits vs Next.js-headless or WordPress.
tldr: "Beta full-stack TypeScript CMS on Astro. Scaffold with `npm create emdash`, wire via `emdash({ database, storage })`, deploy to Cloudflare (D1+R2+Workers) or Node+SQLite. Sandboxed plugins need Cloudflare's paid Worker Loaders."
emdash_version: "0.20.0 / main@23c37f3 (2026-06-17)"
# Verified against: github.com/emdash-cms/emdash README + main@23c37f35dfe9ce23fca0d48acea228299d25e19e (2026-06-17); release emdash@0.20.0; official docs https://docs.emdashcms.com/ (fetched 2026-06-16/17). Third-party emdashcms.dev NOT used.
---

# EmDash: Getting Started and Architecture

> **Beta preview software.** EmDash is "in beta preview" — APIs, flags, and config shapes change between releases. Verify against the [docs](https://docs.emdashcms.com/) and [repo](https://github.com/emdash-cms/emdash) before relying on any detail here.

## When to Use

Reach for this when you are evaluating or adopting EmDash to build a real site: you need to understand the Astro-integration model, scaffold and run a project locally, decide where to deploy it, and judge whether EmDash is the right tool versus a Next.js-headless setup or WordPress.

**What EmDash is.** A full-stack TypeScript CMS built on Astro. Content is defined and edited in a built-in admin UI and served *in-process* at runtime through Astro's live content collections — it is **not** a headless CMS where your frontend fetches content over HTTP ([docs: Introduction](https://docs.emdashcms.com/introduction/)). It markets itself as a modern successor to WordPress (README). Status: **beta preview** (README).

**What you get out of the box** ([docs: Introduction](https://docs.emdashcms.com/introduction/), [Admin Panel](https://docs.emdashcms.com/concepts/admin-panel/)):

- **Visual content modelling** — "Define and change collections and fields from the admin UI; changes take effect immediately."
- **Live content queries** — "Content is served at runtime, so edits appear immediately."
- **Admin panel** — dashboard, content editors, media library, an admin-only schema builder, navigation menus, widget areas, taxonomies, site settings, and plugin pages. Roles: Subscriber, Contributor, Author, Editor, Admin.
- **Plugin system** — "WordPress-inspired hooks, storage, settings, and admin UI extensions."
- **Auth** — passkeys / WebAuthn primary, with OAuth and magic-link alternatives (README; [Getting Started](https://docs.emdashcms.com/getting-started/)).
- **Rich text editing via TipTap** with structured (Portable Text) storage (README).
- **A REST API** under `/_emdash/api/` for management, search, revisions, and WordPress import ([REST API](https://docs.emdashcms.com/reference/rest-api/)) — for management/migration, not your render path.
- **Built-in MCP server and agent skill files** for AI tooling (described in the project README).
- **WordPress migration tooling** (README; `/_emdash/api/import/wordpress`).

## Steps — Scaffold and Run Locally

Prerequisite: **Node.js v22.12.0 or higher** ("odd-numbered versions are not supported") ([Getting Started](https://docs.emdashcms.com/getting-started/)).

1. **Scaffold** a project:
   ```bash
   npm create emdash@latest
   # or: pnpm create emdash@latest
   # or: yarn create emdash
   ```
2. **Install and run:**
   ```bash
   npm install
   npm run dev
   ```
3. Open the site at `http://localhost:4321` and the admin at `http://localhost:4321/_emdash/admin`.
4. First run launches a **Setup Wizard** (site title, tagline, admin email) and registers a **passkey** instead of a password.

## The Astro Integration Model

EmDash is an Astro integration that takes a `database` and a `storage` adapter. Local development with SQLite + local filesystem:

```javascript
// astro.config.mjs
import { defineConfig } from "astro/config";
import emdash, { local } from "emdash/astro";
import { sqlite } from "emdash/db";

export default defineConfig({
  integrations: [
    emdash({
      database: sqlite({ url: "file:./data.db" }),
      storage: local({
        directory: "./uploads",
        baseUrl: "/_emdash/api/media/file",
      }),
    }),
  ],
});
```

Querying is enabled through Astro's live content collections via an `emdashLoader`:

```typescript
// src/live.config.ts
import { defineLiveCollection } from "astro:content";
import { emdashLoader } from "emdash/runtime";

export const collections = {
  _emdash: defineLiveCollection({ loader: emdashLoader() }),
};
```

Import-path map:

| Import | Exports |
|---|---|
| `emdash/astro` | `emdash` (default integration), `local`, `s3` storage adapters |
| `emdash/db` | `sqlite`, `libsql`, `postgres`, `d1` database adapters |
| `emdash/runtime` | `emdashLoader` (Astro live-collections loader) |
| `emdash/ui` | `PortableText` renderer component |

Typical scaffolded project shape:

```
my-emdash-site/
├── astro.config.mjs
├── src/
│   ├── live.config.ts
│   ├── pages/
│   ├── layouts/
│   └── components/
├── .emdash/
│   ├── seed.json
│   └── types.ts
└── package.json
```

(Sources: [Getting Started](https://docs.emdashcms.com/getting-started/), [Architecture](https://docs.emdashcms.com/concepts/architecture/), [Node.js deployment](https://docs.emdashcms.com/deployment/nodejs/), [Configuration](https://docs.emdashcms.com/reference/configuration/).)

## Decision — Choosing a Deploy Target

EmDash "runs on Cloudflare (Workers + D1 + R2) or Node.js, with SQLite, libSQL, or PostgreSQL and any S3-compatible storage" ([Introduction](https://docs.emdashcms.com/introduction/)).

| Layer | Cloudflare | Node.js |
|---|---|---|
| Compute | Cloudflare Workers | Any Node host (`@astrojs/node`, `output: "server"`) |
| Database | `d1()` (serverless SQLite; read replication) | `sqlite()` (better-sqlite3), `libsql()` (remote), or `postgres()` (needs `pg`) |
| Storage | `r2()` binding (zero-config, Workers-only) | `local()` (dev) or `s3()` (R2-via-S3-API, MinIO, any S3-compatible) |
| **Sandboxed plugins** | **Work — but require Cloudflare's Dynamic Worker Loaders (paid plan)** | **Skipped unless a workerd-based runner is installed (in development)** |
| Migrations | Auto on first request after deploy; on boot when new | On first request; seed applied if DB empty and setup not done |

(Sources: [Cloudflare](https://docs.emdashcms.com/deployment/cloudflare/), [Node.js](https://docs.emdashcms.com/deployment/nodejs/), [Database](https://docs.emdashcms.com/deployment/database/), [Storage](https://docs.emdashcms.com/deployment/storage/).)

Database adapter notes ([Database options](https://docs.emdashcms.com/deployment/database/)):

- `d1()` — "Cloudflare's serverless SQLite database. Use it when deploying to Cloudflare Workers."
- `libsql()` — "a fork of SQLite that supports remote connections. Use it when you need a remote database without Cloudflare D1." (The adapter is `libsql()`; the README's "Turso" mention refers to the same libSQL platform.)
- `sqlite()` — "the simplest option for Node.js deployments." Requires a **persistent** filesystem — "Ephemeral filesystems will lose your database on restart."
- `postgres()` — full relational; production Node.js.

Generate the per-environment encryption key ([Node.js](https://docs.emdashcms.com/deployment/nodejs/), [Cloudflare](https://docs.emdashcms.com/deployment/cloudflare/)):

```bash
npx emdash secrets generate   # produces EMDASH_ENCRYPTION_KEY
```

"The key is provided by you and never stored in the database; only encrypted ciphertext is."

## Plugins and the Paid-Plan Caveat

Two plugin formats ([Plugin Overview](https://docs.emdashcms.com/plugins/overview/)):

- **Sandboxed** — "run in an isolated runtime managed by a configurable sandbox runner… subject to capability and resource enforcement, and reach only the APIs they declare." One-click marketplace install. On Cloudflare the isolation uses **Worker Loaders**: "Worker Loader caches the V8 isolate per plugin id so the isolate cold-start cost is only paid once" ([Choosing a Format](https://docs.emdashcms.com/plugins/creating-plugins/choosing-a-format/)).- **Native** — "run in the same process as your Astro site… full access to the runtime, can ship React admin pages and Portable Text rendering components, and inject HTML into public pages." Install via a code change plus a deploy, from npm rather than the marketplace.

Plugins are declared with `definePlugin()` plus a **capabilities** manifest (e.g. `capabilities: ["read:content", "email:send"]`) and lifecycle `hooks` (README example).

**The paid-plan caveat** — *README-only; not on the fetched docs pages:*

- "Dynamic Workers are currently only available on paid accounts." "Upgrade your account (starting at $5/mo)" — or "comment out the `worker_loaders` block of your `wrangler.jsonc`… to disable plugins."

**On non-Cloudflare / no runner**, the docs are internally inconsistent — surfaced honestly:

- [Choosing a Format](https://docs.emdashcms.com/plugins/creating-plugins/choosing-a-format/) and [Capabilities](https://docs.emdashcms.com/plugins/creating-plugins/capabilities/): when "no runner is configured, or if the configured runner reports as unavailable… plugins listed under `sandboxed: []` are skipped at startup with a debug-level log."
- [Capabilities](https://docs.emdashcms.com/plugins/creating-plugins/capabilities/) *also* says without a runner a plugin can run "in-process — but then there's no V8 isolate, no resource limits… Treat that as native-level trust."
- Runners "for other platforms (Node.js via workerd, and potentially Deno) are in development."

Net: on a free Cloudflare plan or a Node host without a workerd runner, **sandboxed plugins effectively do not run** (skipped). The "in-process / native-level trust" wording is a documented contradiction — verify the behavior in your runtime before depending on plugins off Cloudflare.

## Decision — EmDash vs Next.js-headless vs WordPress

| Choose… | When |
|---|---|
| **EmDash** | One TypeScript/Astro app that owns both content modelling and rendering, content served in-process (no separate API layer), passkey-first auth, structured Portable Text content, optional sandboxed plugins. Best fit on Cloudflare; Node+SQLite for simpler hosts. Accept beta-preview risk. |
| **Next.js + headless CMS** (Drupal/JSON:API, Sanity, …) | A decoupled architecture where the CMS is consumed over HTTP by one or more frontends, a mature/stable platform, or an existing editorial backend. EmDash is deliberately *not* headless for content delivery. |
| **WordPress** | You need today's plugin/theme ecosystem, PHP hosting ubiquity, and a large talent pool. EmDash targets WordPress's use cases (CPT-like collections, hooks, themes, WP import) on a TypeScript/serverless stack, but the ecosystem is nascent. |

## Common Mistakes

- **Assuming plugins "just work" everywhere.** Sandboxed plugins require Cloudflare's (paid) Worker Loaders; on Node or free Cloudflare they are skipped. Plan for native plugins or the paid plan.
- **Using an ephemeral filesystem with `sqlite()`.** The DB is lost on restart — use a persistent volume, `libsql()`, `postgres()`, or D1.
- **Treating EmDash as headless.** Content is queried in-process via Astro live collections, not fetched from a REST endpoint. The REST API is for management/import/search.
- **Running an odd-numbered Node version.** Requires Node v22.12.0+; odd majors are unsupported.
- **Forgetting `npx emdash secrets generate`.** Production needs `EMDASH_ENCRYPTION_KEY`.

## See Also

- Next: [Content Modeling](content-modeling.md)
- Reference: [Getting Started](https://docs.emdashcms.com/getting-started/), [Architecture](https://docs.emdashcms.com/concepts/architecture/), [Deployment](https://docs.emdashcms.com/deployment/cloudflare/)
- Repo: [github.com/emdash-cms/emdash](https://github.com/emdash-cms/emdash)
