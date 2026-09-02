---
description: "Taxonomy architecture, naming conventions, and maintenance strategies"
tldr: "Use these guidelines when planning taxonomy architecture, naming conventions, and maintenance strategies."
drupal_version: "11.x"
---

# Best Practices & Patterns

## When to Use

> Use these guidelines when planning taxonomy architecture, naming conventions, and maintenance strategies.

## Decision

| Principle | Guideline | Rationale |
|-----------|-----------|-----------|
| **Vocabulary size** | Keep vocabularies under 30-40 terms unless well-known (e.g., countries) | Users struggle to scan large lists; autocomplete helps but doesn't solve categorization complexity |
| **Hierarchy depth** | Limit to 2-3 levels maximum | UI becomes unwieldy; loadTree performance degrades; users get lost in deep trees |
| **MECE principle** | Categories at same level should be Mutually Exclusive, Collectively Exhaustive | Prevents confusion, improves faceted search, ensures consistent tagging |
| **Naming convention** | Use descriptive, user-facing labels; short machine names | Labels appear in UI, vids in code/URLs; keep vids under 32 chars (schema limit) |
| **Flat vs hierarchical** | Use flat for tags/keywords; hierarchical for navigational categories | Flat is simpler and faster; hierarchy adds value only when parent-child is meaningful |
| **Vocabulary reuse** | Share vocabularies across content types when categorization is common | Reduces duplication, improves consistency (e.g., "Topics" for articles, events, pages) |
| **Term reuse** | Avoid creating duplicate terms; enforce unique names per vocabulary | Duplicate terms confuse users and dilute taxonomy value; use autocomplete to surface existing terms |

## Pattern

**Config-first workflow:**

1. Define vocabularies as YAML in module `config/install/`
2. Export field config (storage, instances, displays)
3. Manage terms via UI or import tools (Default Content, Migrate)
4. Never create vocabularies programmatically unless dynamic requirement

**Naming conventions:**

```yaml
# Good vocabulary machine names (short, descriptive)
vid: tags
vid: topics
vid: product_types
vid: geo_regions

# Bad (too long, unclear, uses hyphens)
vid: article_blog_post_categorization_tags
vid: misc
vid: product-types  # Use underscores, not hyphens
```

**Performance optimization:**

- Cache term trees: Load once, store in static variable or cache bin
- Use `loadTree($vid, 0, NULL, FALSE)` for large vocabularies; load entities selectively
- Index term reference fields in Views for fast filtering
- Consider contrib Search API or Solr for faceted filtering on >10k terms

**Security:**

- Use per-vocabulary permissions instead of `administer taxonomy`
- Unpublish sensitive terms instead of deleting to preserve references
- Validate auto-created terms in hook_ENTITY_TYPE_presave() to prevent spam/XSS

**Maintenance:**

- Audit unused terms quarterly; merge or delete orphans
- Use Views to find content by term before deleting
- Document vocabulary purpose in description field
- Track term usage with Taxonomy Term Reference Count contrib module

## Common Mistakes

- Creating vocabulary per content type → Prevents reuse. Use shared vocabularies for common categorization (e.g., "Topics" across articles, events, blog posts)
- Not documenting vocabulary purpose → Future developers don't know intent. Add clear description in vocabulary config
- Allowing unlimited auto-creation without validation → Spam, typos, duplicates. Add validation hook to enforce naming rules (e.g., max 50 chars, no special characters)
- Over-categorizing with too many vocabularies → Increases cognitive load on content creators. Aim for 3-5 vocabularies site-wide; use single multi-level hierarchy instead of multiple flat vocabularies
- Deleting terms without checking usage → Breaks content references. Use Views to find tagged content first, or unpublish instead of delete
- Not enabling revisions → Can't track term changes over time. Enable `new_revision: true` in vocabulary config for audit trail

## See Also

- ← Previous: [Config Export & Recipes](taxonomy-config-recipes.md) | Next: [Anti-Patterns & Common Mistakes](anti-patterns.md) →
- Reference: [Evolvingweb.com Organizing Content With Taxonomies](https://evolvingweb.com/blog/how-organize-your-drupal-content-taxonomies)
- Reference: [Enterprise Knowledge: Taxonomy Design for Drupal](https://enterprise-knowledge.com/taxonomy-design-for-drupal/)
