---
description: The gotcha when enabling content_moderation on a bundle that already has content — existing revisions get no moderation state until resaved, because moderation_state is a computed field backed by separate content_moderation_state entities and there is no automatic backfill.
tldr: "Enabling moderation on a bundle does NOT retroactively create moderation state for existing content. moderation_state is a computed field backed by content_moderation_state entities; there is no hook_update_N backfill. Existing revisions read as un-moderated until each entity is resaved — batch-resave them as a required post-step."
drupal_version: "11.x"
---

# Enabling Moderation on Existing Content

## When to Use

> When you are switching on content moderation for a content type that **already has published or draft content**. This is the step most moderation rollouts miss, and the failure is silent: existing content behaves as though it is outside the workflow until you explicitly backfill it.

## Foundation

`moderation_state` is not a stored column on the moderated entity. It is a **computed field** (`ModerationStateFieldItemList`) backed by a separate `content_moderation_state` content entity, one per moderated revision. When you enable moderation on a bundle, `content_moderation` wires handler classes and route templates onto the entity type — but it does **not** walk existing rows and create `content_moderation_state` entities for them.

There is no automatic backfill: `content_moderation.install` ships no `hook_update_N` that seeds state for pre-existing content. So every revision created *before* moderation was enabled has no corresponding state entity, and reads as un-moderated / default until the entity is next saved. Only on save does Drupal create or update the `content_moderation_state` entity for that revision.

## Decision

| Situation | Action |
|---|---|
| Enabling moderation on a **new/empty** bundle | Nothing extra — all future saves get state automatically |
| Enabling moderation on a bundle with **existing content** | Backfill required: resave (or explicitly seed state for) every existing entity before declaring the rollout done |
| Large content set where a synchronous resave would time out | Backfill in a **batch** (Batch API / a queue), not a single request |
| You cannot backfill immediately | Surface an operator-visible flag; do not report the workflow as fully live |

## Pattern

Backfill by loading each entity of the bundle and resaving it, which triggers creation of its `content_moderation_state` entity. For anything beyond a handful of nodes, do it in a batch so it does not time out:

```php
// Backfill moderation state for existing nodes of a moderated bundle.
$storage = \Drupal::entityTypeManager()->getStorage('node');
$ids = $storage->getQuery()
  ->accessCheck(FALSE)
  ->condition('type', 'article')
  ->execute();

foreach (array_chunk($ids, 50) as $chunk) {
  foreach ($storage->loadMultiple($chunk) as $node) {
    // Set a sensible state for pre-existing content, then save to
    // materialise the content_moderation_state entity.
    $node->set('moderation_state', $node->isPublished() ? 'published' : 'draft');
    $node->save();
  }
}
```

Map the pre-existing publish status to a moderation state deliberately: already-published content should land in a `published` state, unpublished content in `draft` (or your workflow's equivalent) — otherwise a resave can flip visibility.

## Common Mistakes

- **Wrong**: Assuming enabling moderation retroactively moderates existing content → **Right**: Existing revisions have no state entity until resaved; there is no automatic backfill
- **Wrong**: Resaving thousands of nodes in one request → **Right**: Use Batch API / a queue so the backfill does not time out or exhaust memory
- **Wrong**: Blindly saving with the default state → **Right**: Map existing publish status to the correct moderation state, or you may unpublish live content
- **Wrong**: Treating the workflow as live the moment the config imports → **Right**: The bundle is only fully moderated once existing content is backfilled; flag it until then
- **Wrong**: Looking for a `hook_update_N` to do this → **Right**: None ships; the backfill is the site builder's explicit responsibility

## See Also

- [Content Moderation State Machine](content-moderation-state-machine.md) — the workflow config this operates on
- Reference: [Content Moderation](https://www.drupal.org/docs/administering-a-drupal-site/managing-content/content-moderation)
