---
description: The core EmDash build workflow — defining collections and fields in the visual schema builder, generating TypeScript types, querying via Astro live collections, modelling structured content with Portable Text, and editorial workflow (revisions, drafts, scheduling, search).
tldr: "Define collections in EmDash's visual schema builder, run `npx emdash types`, and query via Astro live collections (`getEmDashCollection`/`getEmDashEntry`). Content is Portable Text JSON (not serialized HTML), rendered with `<PortableText>`."
emdash_version: "0.20.0 / main@23c37f3 (2026-06-17)"
# Verified against: github.com/emdash-cms/emdash README + main@23c37f35dfe9ce23fca0d48acea228299d25e19e (2026-06-17); release emdash@0.20.0; official docs https://docs.emdashcms.com/ (fetched 2026-06-16/17). UNVERIFIED items flagged inline (FTS5 engine name; per-collection SQL table). Third-party emdashcms.dev NOT used.
---

# EmDash: Content Modeling

> **Beta preview software.** Verify field types, commands, and APIs against the [docs](https://docs.emdashcms.com/) and [repo](https://github.com/emdash-cms/emdash) — they change between releases.

## When to Use

Use this when designing a content model in EmDash: defining content types ("collections") and their fields in the visual schema builder, generating typed query helpers, querying content in Astro templates, and deciding how to structure rich content (Portable Text) plus editorial workflow (revisions, drafts, scheduling, search).

## Core Concept — Collections and Fields

A **collection is a content type** (posts, pages, products); its field definitions set the shape of each entry ([Collections](https://docs.emdashcms.com/concepts/collections/), [Content Model](https://docs.emdashcms.com/concepts/content-model/)). You "create and edit collections and fields **visually in the admin panel** under Content Types, or with the CLI" ([Content Model](https://docs.emdashcms.com/concepts/content-model/)). A collection is described by:

```json
{
  "slug": "posts",
  "label": "Blog Posts",
  "labelSingular": "Post",
  "supports": ["drafts", "revisions", "preview", "scheduling"]
}
```

Collection properties: `slug`, `label`, `labelSingular`, `description`, `icon` (Lucide icon name), and `supports` ("Features like drafts, revisions, preview, scheduling, search, seo").

Every entry also carries **system fields** managed by EmDash: `id`, `slug`, `status`, `author_id`, `created_at`/`updated_at`/`published_at`, `deleted_at` (soft delete — "the row is kept"), and `version` ("increments on each save") ([Content Model](https://docs.emdashcms.com/concepts/content-model/)). Reserved slugs you cannot reuse for your own fields include `id`, `slug`, `status`, `author_id`, `created_at`, `updated_at`, `published_at`, `scheduled_at`, `deleted_at`, `version`, `terms`, `bylines`.

**Schema safety:** "Adding a field is always safe. Removing one drops its data. Rename rather than remove-and-recreate to preserve values."

> **DB-to-table caveat (UNVERIFIED specifics).** Each field type "maps to a SQLite column type" ([Field Types](https://docs.emdashcms.com/reference/field-types/)), so the model is backed by real database columns. The docs do **not** state verbatim that "each collection produces its own SQL table" — that mechanic is implied by the column mappings but not documented in those words. Treat it as "DB-backed columns," not a documented per-collection-table guarantee.

## Field Types

EmDash "provides **16 field types**… Each type maps to a SQLite column type and provides appropriate admin UI" ([Field Types](https://docs.emdashcms.com/reference/field-types/)):

| Field type | SQLite column | Use for |
|---|---|---|
| `string` | TEXT | titles, names, short values |
| `text` | TEXT | descriptions, excerpts, longer plain text |
| `url` | TEXT | URL value |
| `number` | REAL | prices, ratings, measurements |
| `integer` | INTEGER | quantities, counts, order |
| `boolean` | INTEGER | toggles, flags |
| `datetime` | TEXT | ISO 8601 timestamps |
| `select` | TEXT | single choice from options |
| `multiSelect` | JSON | multiple choices |
| `portableText` | JSON | rich text (Portable Text) |
| `image` | TEXT | reference to an uploaded image (dimensions, alt) |
| `file` | TEXT | reference to an uploaded file (doc/PDF) |
| `reference` | TEXT | reference to another entry |
| `json` | JSON | arbitrary nested structures |
| `slug` | TEXT | URL-safe identifier |
| `repeater` | JSON | repeating group of fields |

(The CLI `schema add-field` help text lists only 10 of these — a docs gap, not necessarily a feature gap.)

## Steps — Define a Model and Generate Types

1. In the admin, open **Content Types** and use the **schema builder** to create a collection, then add fields (from the 16 field types) and toggle `supports` features.
2. **Generate TypeScript types** from the live model:
   ```bash
   npx emdash types
   ```
   This "writes `.emdash/types.ts` with an interface per collection and typed query overloads" plus a `schema.json` alongside for reference. "Re-run the command after changing the model to keep types in sync." Useful flags: `--url` (default `http://localhost:4321`), `--token`, `--output` (default `.emdash/types.ts`). You can also pass `--types` to `npx emdash dev` to regenerate on dev start. ([Content Model](https://docs.emdashcms.com/concepts/content-model/), [CLI](https://docs.emdashcms.com/reference/cli/))
3. Types augment the `"emdash"` module via declaration merging, so the query helpers become fully typed per collection.

## Pattern — Querying Content

Content is queried in Astro templates with two helpers. The docs describe this as using "Astro's live content collections with automatic caching"; the public surface is `getEmDashCollection` / `getEmDashEntry` (there is no separately branded "Live Collections" API name). ([Querying Content](https://docs.emdashcms.com/guides/querying-content/), [API Reference](https://docs.emdashcms.com/reference/api/), [Create a Blog](https://docs.emdashcms.com/guides/create-a-blog/))

```typescript
import { getEmDashCollection, getEmDashEntry } from "emdash";

// List (filtered)
const { entries: posts } = await getEmDashCollection("posts", {
  status: "published",
  limit: 5,
  where: { category: "news" }, // multiple values use OR logic
});

// Single entry — returns { entry, error, isPreview }; entry is null (not an error) when missing
const { entry, isPreview } = await getEmDashEntry("posts", Astro.params.slug);
```

`CollectionFilter` accepts `status` (`"draft" | "published" | "archived"`), `limit`, and `where`. **Sort order is not guaranteed** — "Sort results in your template." Field values are read from `entry.data.*` (e.g. `post.data.slug`, `post.data.content`).

For visual/inline editing, spread the `edit` proxy onto elements (`{...entry.edit.title}`); "in production, the proxy spreads produce no output."

## Pattern — Portable Text vs WordPress Serialized HTML

The `portableText` field stores rich content as **structured JSON** (SQLite `JSON` column), not as an HTML string. "Portable Text is a specification for structured rich text. See portabletext.org for details." ([Field Types](https://docs.emdashcms.com/reference/field-types/)). It is authored in the **TipTap** editor (README) and rendered with a component:

```tsx
import { PortableText } from "emdash/ui";

<PortableText value={post.data.content} />
```

Why this matters for a content model: WordPress's `the_content()` emits a single serialized HTML blob, mixing content with presentation. EmDash maps `the_content()` → `<PortableText />` and "Gutenberg blocks convert to Portable Text"; collections "work like Custom Post Types" ([Coming from WordPress](https://docs.emdashcms.com/coming-from/wordpress/)). Because the body is structured JSON, the same content can be rendered to different presentations, queried, and transformed — decoupling content from markup.

> The exact phrase "JSON vs serialized HTML" is **not** stated verbatim in the docs; it is the documented `the_content()` → `<PortableText />` mapping plus the Portable Text spec reference, presented here as an adoption consequence. Conversion helpers `prosemirrorToPortableText` / `portableTextToProsemirror` are exported from `emdash` ([API Reference](https://docs.emdashcms.com/reference/api/)).

## Editing, Revisions, Drafts, and Scheduling

The editor supports headings (H2–H6), inline formatting, lists, links, media-library images, code blocks (syntax highlighting), sanitized HTML blocks, embeds (YouTube/Vimeo/Twitter), and reusable **Sections** via a `/section` command. HTML blocks "are sanitized before rendering on the frontend to prevent XSS"; by default iframes are allowed only from `www.youtube.com` and `player.vimeo.com` ([Working with Content](https://docs.emdashcms.com/guides/working-with-content/)).

- **Statuses:** "Every entry has one of three statuses": **Draft** (admin only), **Published** (public), **Archived** (admin only). The `CollectionFilter` type confirms `"draft" | "published" | "archived"`. *Doc inconsistency to flag: the content-model system-fields table calls the third status "scheduled," but the TypeScript type and the working-with-content page agree it is "archived." Scheduling is achieved via Draft + a future date, not a discrete `scheduled` status.*
- **Revisions:** enabled by the `revisions` support; "track content history with version snapshots," viewable from a sidebar **Revisions** list with timestamps. No maximum revision count is documented. `version` increments on each save. (REST exposes revision list/get/restore endpoints.)
- **Scheduled publishing:** with the `scheduling` support, set status to Draft and a future **Publication date**; "when the publication date arrives, the content automatically becomes published." (`scheduled_at` is a system field.)
- **Drafts & preview:** the `preview` support generates "secure, time-limited URLs" with "HMAC-SHA256 signed tokens"; `getEmDashEntry` returns `isPreview` ([Preview](https://docs.emdashcms.com/guides/preview/)).

## Search

Collections opt into search via the `search` support. EmDash exposes full-text search:

```typescript
import { search } from "emdash";
const results = await search("hello world", {
  collections: ["posts", "pages"],
  status: "published",
  limit: 20,
});
```

There is also a REST surface: `GET /_emdash/api/search?q=…` (params `q`, `collections`, `status`, `limit`, `cursor`) and `POST /_emdash/api/search/rebuild` to rebuild the FTS index ([REST API](https://docs.emdashcms.com/reference/rest-api/), [API Reference](https://docs.emdashcms.com/reference/api/)).

> **UNVERIFIED — FTS engine name.** The docs mention an "FTS index" and a rebuild endpoint but **do not name SQLite FTS5**. Do not claim "FTS5" as documented — treat it as "a (SQLite) full-text search index" with the engine name unconfirmed.

## Common Mistakes

- **Expecting guaranteed ordering from `getEmDashCollection`.** It is not guaranteed — sort in the template.
- **Treating Portable Text as an HTML string.** It is structured JSON; render with `<PortableText>` (or convert via the prosemirror helpers), not by injecting HTML.
- **Forgetting to re-run `npx emdash types`.** Types drift from the model after schema edits; regenerate to keep query helpers typed.
- **Assuming a `scheduled` status exists.** Statuses are draft/published/archived; scheduling = Draft + future publication date.
- **Removing a field to "rename" it.** Removing drops its data; rename in place to preserve values.

## See Also

- Previous: [Getting Started and Architecture](getting-started-and-architecture.md)
- Reference: [Collections](https://docs.emdashcms.com/concepts/collections/), [Content Model](https://docs.emdashcms.com/concepts/content-model/), [Field Types](https://docs.emdashcms.com/reference/field-types/), [Querying Content](https://docs.emdashcms.com/guides/querying-content/)
