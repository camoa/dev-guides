---
description: Taxonomy architecture, naming conventions, and maintenance strategies
drupal_version: "11.x"
---

# Best Practices & Patterns

## When to Use

> Use these guidelines when planning taxonomy architecture, naming conventions, and maintenance strategies.

## Decision

| Principle | Guideline | Rationale |
|-----------|-----------|-----------|
| **Vocabulary size** | Keep vocabularies under 30-40 terms unless well-known (e.g., countries) | Users struggle to scan large lists |
| **Hierarchy depth** | Limit to 2-3 levels maximum | UI becomes unwieldy; loadTree performance degrades |
| **MECE principle** | Categories at same level should be Mutually Exclusive, Collectively Exhaustive | Prevents confusion, improves faceted search |
| **Naming convention** | Use descriptive, user-facing labels; short machine names | Labels appear in UI, vids in code/URLs; keep vids under 32 chars |
| **Flat vs hierarchical** | Use flat for tags/keywords; hierarchical for navigational categories | Flat is simpler and faster |
| **Vocabulary reuse** | Share vocabularies across content types when categorization is common | Reduces duplication, improves consistency |
| **Term reuse** | Avoid creating duplicate terms; enforce unique names per vocabulary | Duplicate terms confuse users |

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

- **Wrong**: Creating vocabulary per content type → **Right**: Use shared vocabularies for common categorization
- **Wrong**: Not documenting vocabulary purpose → **Right**: Add clear description in vocabulary config
- **Wrong**: Allowing unlimited auto-creation without validation → **Right**: Add validation hook to enforce naming rules
- **Wrong**: Over-categorizing with too many vocabularies → **Right**: Aim for 3-5 vocabularies site-wide
- **Wrong**: Deleting terms without checking usage → **Right**: Use Views to find tagged content first, or unpublish instead
- **Wrong**: Not enabling revisions → **Right**: Enable `new_revision: true` in vocabulary config for audit trail

## See Also

- [Config Export & Recipes](taxonomy-config-recipes.md)
- [Anti-Patterns & Common Mistakes](anti-patterns.md)
- Reference: [Evolvingweb.com Organizing Content With Taxonomies](https://evolvingweb.com/blog/how-organize-your-drupal-content-taxonomies)
- Reference: [Enterprise Knowledge: Taxonomy Design for Drupal](https://enterprise-knowledge.com/taxonomy-design-for-drupal/)
