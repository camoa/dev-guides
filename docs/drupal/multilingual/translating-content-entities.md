---
description: Drupal content entity translation — UI workflow for translating nodes, terms, media, managing translation status
---

# Translating Content Entities

### When to Use
When creating or managing translations for nodes, taxonomy terms, media, blocks, menu links.

### Decision: Translation Workflow Approach

| If you need... | Use... | Why |
|---|---|---|
| Manual translation via UI | Content edit → Translate tab | Simple, built-in, good for small sites |
| Translation jobs with external services | TMGMT module | Professional translation, API integration |
| Programmatic translation | `addTranslation()` API | Migrations, automated workflows, bulk operations |
| Synchronized field values | Field translation sync settings | Share images, dates across translations |

### Pattern: UI Translation Workflow

**Step 1**: Create source content in default language
- Create node/term/media in English (or default language)
- Save and publish

**Step 2**: Add translation
- Navigate to content → Translate tab
- Click "Add" for target language
- Fill in translated field values
- Save

**Step 3**: Manage translations
- Translate tab shows all translations
- Edit, delete, or change translation status per language

**Translation status**:
- Published — translation is live
- Unpublished — translation exists but not visible
- Outdated — source content changed, translation needs update

### Pattern: Programmatic Translation

See [Programmatic Entity Translation](programmatic-entity-translation.md) for detailed API usage.

### Common Mistakes

- **Translating non-translatable fields** → Non-translatable fields share same value across translations. Changing in one translation changes in all. [Field Translatability](field-translatability.md) for field configuration
- **Forgetting to publish translation** → Creating translation doesn't auto-publish. Must explicitly set status or publish via workflow
- **Not marking outdated translations** → When source content changes, translations don't auto-mark as outdated. Use Content Translation metadata to track
- **Copying source content directly** → Don't copy-paste from source to translation in same field — defeats caching optimizations. Use proper translation workflow
- **Missing translation permissions** → Users need "translate ENTITY_TYPE" permission. Check permissions if users can't access Translate tab

### See Also
- → [Field Translatability](field-translatability.md) — which fields to translate
- → [Translation & Revisions](translation-revisions.md) — revision handling with translations
- → [Programmatic Entity Translation](programmatic-entity-translation.md) — API methods
- → [Translation Workflows](translation-workflows.md) — TMGMT integration
- Reference: `core/modules/content_translation/src/ContentTranslationHandler.php`
