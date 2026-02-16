---
description: Drupal translation workflows — TMGMT module, translation jobs, external services like DeepL and Google Translate
---

# Translation Workflows

### When to Use
When implementing translation processes beyond basic UI — professional translation services, translation jobs, external translators, automated workflows.

### Decision: Workflow Tool

| If you need... | Use... | Why |
|---|---|---|
| Manual translation by site editors | Core Content Translation UI | Simple, built-in, no extra modules |
| Translation jobs and tracking | TMGMT module | Job management, translator assignments, status tracking |
| Integration with translation services | TMGMT + translator plugins | DeepL, Google Translate, professional services APIs |
| Automated translation on publish | TMGMT Auto Translate (contrib) | Trigger translations on moderation state changes |
| Translation memory (TM) | TMGMT + external TM services | Reuse previous translations, consistency |

### Pattern: TMGMT Workflow Overview

**TMGMT** (Translation Management Tool) provides:
- Translation jobs (group content for translation)
- Translation sources (what to translate)
- Translators (who/what translates)
- Job items (individual pieces in a job)

**Basic workflow**:
1. Create translation job
2. Add content to job (nodes, terms, config)
3. Assign to translator (human or machine)
4. Translator completes job
5. Review and accept translations
6. Translations published

### Pattern: TMGMT Installation and Setup

**Install TMGMT**:

```bash
composer require drupal/tmgmt
drush en tmgmt tmgmt_content tmgmt_locale tmgmt_config
```

**Modules**:
- `tmgmt` — core job management
- `tmgmt_content` — translate content entities
- `tmgmt_locale` — translate interface strings
- `tmgmt_config` — translate configuration
- `tmgmt_ui` — UI for managing jobs

**Configure translator** (`/admin/tmgmt/translators`):
- Add translator (Local, Google, DeepL, etc.)
- Configure API keys if using service
- Set default translator

### Pattern: Creating Translation Job via UI

1. Go to `/admin/tmgmt/sources` or content list
2. Select content to translate
3. Click "Request translation"
4. Choose target languages
5. Choose translator
6. Submit job

**Job states**:
- Active — being translated
- Needs review — translation complete, awaiting review
- Reviewed — accepted by reviewer
- Finished — all items accepted, translations saved
- Rejected — translator rejected job
- Aborted — job cancelled

### Pattern: Programmatic TMGMT Job

```php
use Drupal\tmgmt\Entity\Job;
use Drupal\tmgmt\Entity\JobItem;

// Create job
$job = Job::create([
  'source_language' => 'en',
  'target_language' => 'es',
  'translator' => 'local', // Translator plugin ID
  'label' => 'Article translations to Spanish',
]);
$job->save();

// Add job item (node to translate)
$node = \Drupal\node\Entity\Node::load(1);
$job->addItem('content', 'node', $node->id());

// Submit job
$job->requestTranslation();

// Check job state
if ($job->isFinished()) {
  // Translations saved
}
```

**Job item workflow**:

```php
// Get job items
foreach ($job->getItems() as $item) {
  // Get translation data
  $data = $item->getData();

  // Update translation
  $item->addTranslatedData([
    'title' => ['#text' => 'Título traducido'],
    'body' => ['#text' => 'Cuerpo traducido'],
  ]);

  // Accept translation
  $item->acceptTranslation();
}
```

### Pattern: TMGMT with External Services

**Google Translate plugin**:

```bash
composer require drupal/tmgmt_google
drush en tmgmt_google
```

**Configure** (`/admin/tmgmt/translators/add`):
- Translator type: Google Translator
- API key: [your Google Cloud API key]
- Save

**DeepL plugin**:

```bash
composer require drupal/tmgmt_deepl
drush en tmgmt_deepl
```

**Jobs automatically sent to API**, translations retrieved and imported.

### Pattern: Translation Permissions

**Permissions** (`/admin/people/permissions`):
- "Submit translation jobs" — create jobs
- "Accept translation jobs" — review and accept
- "Administer translation jobs" — manage all jobs
- "Translate [entity_type]" — per entity type

**Roles**:
- Content editor — submit jobs
- Translator — accept jobs, translate
- Translation manager — administer jobs

### Common Mistakes

- **Not installing correct TMGMT submodules** → `tmgmt` alone doesn't enable content translation. Need `tmgmt_content` for nodes/entities
- **Forgetting API keys for translation services** → Google/DeepL translators fail without valid API credentials
- **Not reviewing machine translations** → Auto-translated content needs human review for quality and context
- **Mixing TMGMT workflow with manual Content Translation** → Use one workflow consistently. Mixing causes confusion about translation status
- **Not configuring permissions** → Users need specific TMGMT permissions separate from Content Translation permissions

### See Also
- → [Translating Content Entities](translating-content-entities.md) — manual translation workflow
- → [Programmatic Entity Translation](programmatic-entity-translation.md) — addTranslation() API
- Reference: https://www.drupal.org/project/tmgmt
- Reference: https://www.drupal.org/docs/contributed-modules/translation-management-tool
- Reference: https://www.vardot.com/en-us/ideas/blog/simplify-translation-workflow-management-drupal-sites
