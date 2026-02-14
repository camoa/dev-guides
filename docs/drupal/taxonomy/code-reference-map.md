---
description: Key classes, files, and code references for Drupal taxonomy
drupal_version: "11.x"
---

# Code Reference Map

## When to Use

> Use this reference to locate key taxonomy classes, methods, and files in the Drupal codebase.

## Decision

### Entity Classes

| Class | Path | Purpose |
|-------|------|---------|
| **Vocabulary** | `/core/modules/taxonomy/src/Entity/Vocabulary.php` | Config entity for vocabularies (lines 74-196) |
| **Term** | `/core/modules/taxonomy/src/Entity/Term.php` | Content entity for taxonomy terms (lines 97-299) |

### Storage & Queries

| Class | Path | Key Methods |
|-------|------|-------------|
| **TermStorage** | `/core/modules/taxonomy/src/TermStorage.php` | `loadTree()` (208-303), `loadParents()` (93-106), `loadChildren()` (184-203), `loadAllParents()` (150-179), `getVocabularyHierarchyType()` (398-430) |
| **TermStorageInterface** | `/core/modules/taxonomy/src/TermStorageInterface.php` | Interface defining term storage methods |

### Access Control

| Class | Path | Key Methods |
|-------|------|-------------|
| **TermAccessControlHandler** | `/core/modules/taxonomy/src/TermAccessControlHandler.php` | `checkAccess()` (20-72), `checkCreateAccess()` (77-79) |
| **TaxonomyPermissions** | `/core/modules/taxonomy/src/TaxonomyPermissions.php` | `buildPermissions()` (64-82) — generates per-vocabulary permissions |

### Forms

| Class | Path | Purpose |
|-------|------|---------|
| **VocabularyForm** | `/core/modules/taxonomy/src/VocabularyForm.php` | Vocabulary edit form |
| **TermForm** | `/core/modules/taxonomy/src/TermForm.php` | Term edit form |
| **OverviewTerms** | `/core/modules/taxonomy/Form/OverviewTerms.php` | Draggable term overview with weight management |

### Views Integration

| Plugin | Path | Purpose |
|--------|------|---------|
| **TaxonomyIndexTid** (filter) | `/core/modules/taxonomy/src/Plugin/views/filter/TaxonomyIndexTid.php` | Exposed filter for taxonomy terms (lines 22-450) |
| **Taxonomy** (argument) | `/core/modules/taxonomy/src/Plugin/views/argument/Taxonomy.php` | Contextual filter for term pages (lines 13-16) |
| **NodeTermData** (relationship) | `/core/modules/taxonomy/src/Plugin/views/relationship/NodeTermData.php` | Relationship from nodes to terms via taxonomy_index |

### Config & Schema

| File | Path | Purpose |
|------|------|---------|
| **taxonomy.schema.yml** | `/core/modules/taxonomy/config/schema/taxonomy.schema.yml` | Config schema for vocabulary, settings (lines 3-56) |
| **taxonomy.vocabulary.tags.yml** | `/core/recipes/tags_taxonomy/config/taxonomy.vocabulary.tags.yml` | Example vocabulary config |

### Recipes

| File | Path | Purpose |
|------|------|---------|
| **tags_taxonomy/recipe.yml** | `/core/recipes/tags_taxonomy/recipe.yml` | Recipe for tags vocabulary |
| **article_tags/recipe.yml** | `/core/recipes/article_tags/recipe.yml` | Recipe for article tags field + displays |

## Pattern

All file paths relative to Drupal root.

## See Also

- [Security & Performance](security-performance.md)
- [Taxonomy System Overview](taxonomy-overview.md)
