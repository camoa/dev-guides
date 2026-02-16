---
description: Drupal multilingual best practices — config-first setup, deployment workflows, performance optimization, security, accessibility
---

# Best Practices & Patterns

### When to Use
When planning multilingual architecture, deployment workflows, or optimizing translation management.

### Decision: Architecture Patterns

| Scenario | Pattern | Why |
|---|---|---|
| New multilingual site | Config-first approach | Version-controlled, repeatable deployments |
| Entity translation | Enable per bundle, not per entity type | Allows granular control (some bundles translatable, some not) |
| URL structure | Path prefix with no prefix for default | SEO-friendly, user-friendly, CDN-compatible |
| Language negotiation | URL → User → Browser → Selected | Explicit first, personal second, automatic last |
| Field translatability | Only translatable fields that need it | Performance — translatable fields have storage overhead |

### Pattern: Config-First Multilingual Setup

**Workflow**:
1. Add languages via config YAML
2. Configure negotiation via config YAML
3. Enable content translation per bundle via config YAML
4. Export config after UI changes
5. Deploy config consistently across environments

**Benefits**:
- Version-controlled translation settings
- Repeatable deployments
- Environment parity
- Easier testing

**Config files to track**:
```
config/sync/
  language.entity.*.yml
  language.types.yml
  language.negotiation.yml
  language.content_settings.*.*.yml
  field.field.*.*.*.yml (translatable: true)
```

### Pattern: Translation Deployment Workflow

**Development**:
1. Add/change translatable content and config
2. Export base config (English)
3. Add translations via UI or TMGMT
4. Export language-specific config overrides
5. Commit to version control

**Staging/Production**:
1. Deploy code and config
2. Import base config
3. Import language-specific overrides
4. Clear caches
5. Test language switching

**Config sync structure**:
```
config/sync/
  views.view.frontpage.yml          # Base config (English)
  language/
    es/
      views.view.frontpage.yml      # Spanish overrides
    fr/
      views.view.frontpage.yml      # French overrides
```

### Pattern: Performance Optimization

**Cache contexts**:
- Always include `languages:language_interface` for UI elements
- Include `languages:language_content` for entity displays
- Include `url.path` with path prefix negotiation

**Example render array**:

```php
$build = [
  '#markup' => $this->t('Translatable text'),
  '#cache' => [
    'contexts' => [
      'languages:language_interface',
      'url.path',
    ],
  ],
];
```

**CDN configuration**:
- Vary on URL path if using path prefixes
- Vary on `Accept-Language` header if using browser negotiation
- Don't cache language switcher blocks without proper contexts

### Pattern: Security Considerations

**Access control per language**:

```php
// Check if user can translate this entity to Spanish
if ($entity->access('update', $account) && $entity->access('translate', $account)) {
  // Allow translation
}
```

**Permission checks**:
- "translate ENTITY_TYPE" — per entity type
- "translate any entity" — global
- "translate editable entities" — only entities user can edit
- "administer languages" — language configuration

**Avoid translation privilege escalation**:
- Users shouldn't be able to translate content they can't view
- Check source content access before allowing translation
- Translation metadata (author, status) should respect permissions

### Pattern: Accessibility & UX

**Language switcher**:
- Use `hreflang` attribute on links
- Show language names in their own language (Español, not Spanish)
- Indicate current language visually
- Keyboard-accessible

**RTL language support**:
- Test layout with RTL languages (Arabic, Hebrew)
- Use logical properties in CSS (`margin-inline-start` not `margin-left`)
- Don't hardcode text direction

**Content fallback**:
- If translation doesn't exist, show source content with indicator
- Allow users to request translation
- Don't show broken layout if one language has more content

### Best Practices Summary

**DO**:
- Use config YAML for language setup
- Enable translation per bundle, not globally
- Mark only necessary fields translatable
- Use `$this->t()` with StringTranslationTrait
- Add context to ambiguous strings
- Use proper cache contexts
- Test with RTL languages
- Version control language config

**DON'T**:
- Translate user input with `t()`
- Make all fields translatable by default
- Concatenate translated strings
- Bypass placeholder sanitization (only `@`, `%`, `:` supported in `t()`)
- Hardcode language codes in business logic
- Skip testing language switching
- Forget hreflang tags for SEO

### See Also
- → [Anti-Patterns & Common Mistakes](anti-patterns.md) — what to avoid
- → [Security, Performance & Caching](security-performance-caching.md) — optimization details
- Reference: https://pantheon.io/learning-center/drupal/multilingual
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide
