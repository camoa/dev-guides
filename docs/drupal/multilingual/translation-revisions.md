---
description: Drupal translation and revisions — revision handling with translations, content moderation per language, latest revision queries
---

# Translation & Revisions

### When to Use
When working with revisionable entities (nodes, media, custom entities) that support both translation and revision tracking.

### Decision: Revision Handling Approaches

| If you need... | Use... | Why |
|---|---|---|
| Independent revisions per translation | Default behavior | Each translation has own revision history |
| Draft translations with published source | Moderation states per translation | Spanish draft while English is published |
| Synchronized revision creation | Custom entity hooks | All translations get new revision simultaneously |
| Latest revision per language | `latestRevision()` entity query | Query most recent revision for specific language |

### Pattern: Translation Revision Behavior

**Default behavior**:
- Each translation has independent revision history
- Editing Spanish translation creates new revision for Spanish only
- English translation revision unchanged

**Example**:
1. Create English node, revision 1
2. Add Spanish translation, revision 2 (Spanish added, English unchanged)
3. Edit Spanish, revision 3 (Spanish updated, English unchanged)
4. Edit English, revision 4 (English updated, Spanish unchanged)

**Entity revision loading**:

```php
// Load default (published) revision
$node = \Drupal\node\Entity\Node::load(1);

// Load specific revision
$revision = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadRevision(4);

// Load latest revision
$latest = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadRevision($node->getLatestRevisionId());
```

### Pattern: Translation with Content Moderation

When using Content Moderation module, each translation can have independent moderation state.

**Example states**:
- English: Published
- Spanish: Draft
- French: Needs Review

**Workflow**:
1. Create English content, publish
2. Add Spanish translation, save as Draft
3. Spanish stays Draft, English stays Published
4. Publish Spanish independently

**Common issue**: Default revision vs latest revision
- **Default revision** — the published revision loaded by `Entity::load()`
- **Latest revision** — most recent revision regardless of published status

**Query for latest translation revision**:

```php
$query = \Drupal::entityQuery('node')
  ->condition('nid', 1)
  ->latestRevision()
  ->accessCheck(FALSE);
$result = $query->execute();
```

**Note**: `latestRevision()` is NOT language-aware. Returns latest revision ID across all languages.

### Common Mistakes

- **Assuming latestRevision() is language-aware** → `latestRevision()` returns latest revision ID regardless of language. Spanish edit creates revision 5, querying for latest English revision still returns 5
- **Confusing default revision with latest revision** → Default revision is published version. Latest revision may be unpublished draft. Loading entity by ID returns default, not latest
- **Not understanding translation independence** → Editing one translation doesn't create revision for other translations. Each translation has own revision timeline
- **Moderation state confusion** → With Content Moderation, "Published" state for Spanish is independent of English. One can be Draft while other is Published
- **Forgetting to check access on revisions** → Viewing draft revisions requires "view any unpublished content" permission. Use `accessCheck()` in queries

### See Also
- → [Translating Content Entities](translating-content-entities.md) — creating translations
- → [Language-Aware Queries](language-aware-queries.md) — querying by language and revision
- Reference: `core/lib/Drupal/Core/Entity/ContentEntityBase.php`
- Reference: https://www.drupal.org/project/drupal/issues/3088341 (latestRevision() language awareness issue)
