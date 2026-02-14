---
description: "Fetch JSON:API resources from Drupal for rendering in Next.js pages. All methods support filtering, sorting, includes, and sparse fieldsets."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Fetching Content

### When to Use

Fetch JSON:API resources from Drupal for rendering in Next.js pages. All methods support filtering, sorting, includes, and sparse fieldsets.

### Items

#### getResource

**Description:** Fetch a single resource by type and UUID.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | Yes | Resource type (e.g., `node--article`) |
| uuid | string | Yes | Resource UUID |
| options | object | No | params, withAuth, cache options |

**Usage Example:**

```typescript
const article = await drupal.getResource(
  "node--article",
  "dad82fe9-f2b7-463e-8c5f-02f73018d6cb",
  {
    params: {
      include: "field_image,uid",
    },
  }
)
```

**Gotchas:**
- Use UUID, not node ID (nid)
- Type format is `entity_type--bundle` with double dash

#### getResourceByPath

**Description:** Fetch a resource by its path alias.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | Yes | Path alias (e.g., `/blog/my-article`) |
| options | object | No | params, withAuth, locale |

**Usage Example:**

```typescript
const article = await drupal.getResourceByPath("/blog/my-article")
```

**Gotchas:**
- Requires path alias configuration in Drupal
- Path must start with `/`

#### getResourceCollection

**Description:** Fetch multiple resources of the same type.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | Yes | Resource type |
| options | object | No | params, withAuth |

**Usage Example:**

```typescript
const articles = await drupal.getResourceCollection("node--article", {
  params: {
    "filter[status]": "1",
    "fields[node--article]": "title,created",
    sort: "-created",
    "page[limit]": 10,
  },
})
```

**Gotchas:**
- Default limit is 50 resources
- Override limit using sparse fieldsets with `path` field (see Page Limit section)
- Returns array of resources

#### getMenu

**Description:** Fetch menu items by menu name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Menu machine name (e.g., `main`) |
| options | object | No | locale, withAuth, withCache |

**Usage Example:**

```typescript
const menu = await drupal.getMenu("main", {
  withCache: true,
  cacheKey: "menu:main",
})
```

**Gotchas:**
- Requires jsonapi_menu_items module
- Returns nested menu structure

#### getView

**Description:** Fetch view results via JSON:API Views.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| viewId | string | Yes | Format: `view_name--display_id` |
| options | object | No | params, locale |

**Usage Example:**

```typescript
const view = await drupal.getView("promoted_items--block_1", {
  params: {
    "views-argument": ["taxonomy_term_id"],
  },
})
```

**Gotchas:**
- Requires jsonapi_views module
- View must have REST export display

#### getSearchIndex

**Description:** Query Search API index via JSON:API.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| indexName | string | Yes | Search API index machine name |
| options | object | No | params (filters, facets) |

**Usage Example:**

```typescript
const results = await drupal.getSearchIndex("content_index", {
  params: {
    filter: { title: "search term" },
  },
})
```

**Gotchas:**
- Requires jsonapi_search_api module
- See Search Integration section for setup

### Common Mistakes

- **Not using sparse fieldsets** — Fetches all fields unnecessarily. WHY: Bandwidth waste, slower responses.
- **Fetching resources in loops** — N+1 query problem. WHY: Use includes and relationships instead.
- **Ignoring pagination** — Hits 50-resource limit. WHY: Use page[limit] parameter or override via sparse fieldsets.
- **Not caching global resources** — Refetches menus/blocks on every build. WHY: Use withCache option for build-time caching.

### See Also

- Building Pages
- drupal-jsonapi.md (for params syntax)
- Performance Optimization
