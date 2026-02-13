---
description: Security patterns for plugin architectures protecting against code injection and privilege escalation
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Apply these security patterns to every plugin architecture implementation. Plugin systems are vulnerable because they load and execute code dynamically.

## Decision

| Threat | Mitigation | Why |
|--------|------------|-----|
| Untrusted plugin code | Validate plugin definitions in `processDefinition()` | Plugins from contrib can contain malicious code |
| API key exposure | Use Key module or config overrides, never hardcode | Keys in code end up in version control |
| Input injection | Sanitize all plugin configuration values | Plugin config may come from user forms |
| Privilege escalation | Enforce access checks in plugin manager, not just routes | Plugins may bypass route-level access |
| SSRF via provider plugins | Validate/whitelist external URLs in provider config | Malicious providers could target internal services |

## Pattern

**Plugin Definition Validation**:

```php
// In plugin manager's processDefinition()
public function processDefinition(&$definition, $plugin_id) {
  parent::processDefinition($definition, $plugin_id);

  // Validate required fields
  if (empty($definition['label'])) {
    throw new InvalidPluginDefinitionException($plugin_id, "Missing label");
  }

  // Validate URL fields
  if (!empty($definition['api_endpoint'])) {
    if (!UrlHelper::isValid($definition['api_endpoint'], TRUE)) {
      throw new InvalidPluginDefinitionException($plugin_id, "Invalid API endpoint");
    }
  }
}
```

**Access Control in Plugin Manager**:

```php
// Enforce access checks before plugin instantiation
public function createInstance($plugin_id, array $configuration = []) {
  if (!$this->currentUser->hasPermission('use ' . $plugin_id)) {
    throw new AccessDeniedHttpException();
  }
  return parent::createInstance($plugin_id, $configuration);
}
```

**Configuration Sanitization**:

```php
// Sanitize user-provided configuration
public function buildConfigurationForm(array $form, FormStateInterface $form_state) {
  $form['api_key'] = [
    '#type' => 'textfield',
    '#title' => $this->t('API Key'),
    '#default_value' => $this->configuration['api_key'] ?? '',
    '#required' => TRUE,
    '#maxlength' => 255,
  ];
  return $form;
}

public function validateConfigurationForm(array &$form, FormStateInterface $form_state) {
  $api_key = $form_state->getValue('api_key');
  if (preg_match('/[^a-zA-Z0-9_-]/', $api_key)) {
    $form_state->setError($form['api_key'], $this->t('Invalid characters in API key'));
  }
}
```

## Common Mistakes

- **Wrong**: Storing API keys in plugin annotations → **Right**: Use Key module or environment variables
- **Wrong**: Trusting plugin-provided HTML → **Right**: Use `#plain_text` or `Xss::filter()` on plugin output
- **Wrong**: No access check on plugin operations → **Right**: Enforce permissions in plugin manager
- **Wrong**: Exposing internal service details in REST responses → **Right**: Return sanitized, minimal data

## See Also

- [Configuration Architecture](configuration-architecture.md)
- [Plugin Manager Implementation](plugin-manager-implementation.md)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Reference: [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
