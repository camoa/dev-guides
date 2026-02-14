---
description: "Narrow down collection results based on field values. Essential for search, listing published content, filtering by author, date ranges, and complex queries."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Filtering

### When to Use

Narrow down collection results based on field values. Essential for search, listing published content, filtering by author, date ranges, and complex queries.

### Items

#### Simple Equality Filter

**Description:** Filter by exact field value match.

**Syntax:**
```
?filter[field_name]=value
```

**Usage Example:**
```bash
# Published articles only
GET /jsonapi/node/article?filter[status]=1

# Articles by specific author email
GET /jsonapi/node/article?filter[uid.mail]=admin@example.com
```

**Gotchas:**
- Works for single values only
- Default operator is `=` (equals)
- For complex conditions, use operator syntax

#### Operator-Based Filter

**Description:** Filter with specific comparison operators.

**Syntax:**
```
?filter[label][condition][path]=field_name
&filter[label][condition][operator]=OPERATOR
&filter[label][condition][value]=search_value
```

**Operator Table:**

| Operator | Description | Example Use Case |
|----------|-------------|------------------|
| `=` | Equals (default) | Exact match |
| `<>` | Not equals | Exclude specific value |
| `>` | Greater than | Date after timestamp |
| `>=` | Greater or equal | Published after date |
| `<` | Less than | Date before timestamp |
| `<=` | Less or equal | Published before date |
| `STARTS_WITH` | String starts with | Title starts with "How to" |
| `CONTAINS` | String contains | Body contains "Drupal" |
| `ENDS_WITH` | String ends with | Email ends with "@example.com" |
| `IN` | Value in array | Status in [0, 1] |
| `NOT IN` | Value not in array | Exclude multiple IDs |
| `BETWEEN` | Between two values | Created between dates |
| `NOT BETWEEN` | Not between values | Outside date range |
| `IS NULL` | Field is null | Image field empty |
| `IS NOT NULL` | Field not null | Has image |

**Usage Example:**
```bash
# Title contains "Drupal"
GET /jsonapi/node/article?filter[title-filter][condition][path]=title&filter[title-filter][condition][operator]=CONTAINS&filter[title-filter][condition][value]=Drupal

# Created after specific date
GET /jsonapi/node/article?filter[date-filter][condition][path]=created&filter[date-filter][condition][operator]=%3E&filter[date-filter][condition][value]=1640995200
```

**Gotchas:**
- Operators must be URL-encoded (`>` becomes `%3E`)
- Label (`title-filter`) is arbitrary but must be unique
- BETWEEN requires value array

#### Filter on Relationship Fields

**Description:** Filter based on referenced entity fields.

**Syntax:**
```
?filter[label][condition][path]=relationship.field
&filter[label][condition][value]=value
```

**Usage Example:**
```bash
# Articles by author name
GET /jsonapi/node/article?filter[author-name][condition][path]=uid.name&filter[author-name][condition][value]=admin

# Articles with specific tag (by UUID)
GET /jsonapi/node/article?filter[tag-filter][condition][path]=field_tags.id&filter[tag-filter][condition][value]={tag-uuid}
```

**Gotchas:**
- Use dot notation for relationship traversal
- Can filter on relationship fields but not deeply nested (max 1 level)
- Filtering on relationship field name requires UUID

#### Filter Groups (AND/OR Logic)

**Description:** Combine multiple conditions with AND or OR logic.

**Syntax:**
```
?filter[group-name][group][conjunction]=OR
&filter[cond1][condition][path]=field1
&filter[cond1][condition][value]=val1
&filter[cond1][condition][memberOf]=group-name
&filter[cond2][condition][path]=field2
&filter[cond2][condition][value]=val2
&filter[cond2][condition][memberOf]=group-name
```

**Usage Example:**
```bash
# Articles where title contains "Drupal" OR "PHP"
GET /jsonapi/node/article?filter[keywords-group][group][conjunction]=OR&filter[drupal-filter][condition][path]=title&filter[drupal-filter][condition][operator]=CONTAINS&filter[drupal-filter][condition][value]=Drupal&filter[drupal-filter][condition][memberOf]=keywords-group&filter[php-filter][condition][path]=title&filter[php-filter][condition][operator]=CONTAINS&filter[php-filter][condition][value]=PHP&filter[php-filter][condition][memberOf]=keywords-group
```

**Gotchas:**
- Default conjunction is AND
- Group name must match in `memberOf` parameters
- Nested groups not supported
- All conditions in group must have `memberOf`

### Common Mistakes

**Not URL-encoding operators:** `>` must be `%3E`, `<` must be `%3C`. WHY: URL special characters must be encoded. Use proper encoding functions.

**Using internal field machine names incorrectly:** Field names are case-sensitive. WHY: `field_tags` works, `Field_Tags` doesn't. Check entity definition.

**Filtering on computed or inaccessible fields:** Some fields can't be filtered. WHY: Only stored entity fields support filtering. Computed fields (like `url`) aren't in the database.

**Not accounting for field access:** Filtering on restricted fields fails silently. WHY: Field access control applies. If user can't view field, it can't be filtered.

**Expecting full-text search:** CONTAINS is case-insensitive substring match, not full-text search. WHY: Database LIKE queries, not search indices. For true search, use Search API with JSON:API integration.

### See Also
- [Fetching Resources (GET)](fetching-resources.md)
- [Code Reference Map](code-reference-map.md) (`src/Query/Filter.php`)
