---
description: Security patterns for plugin architectures protecting against code injection and privilege escalation
tldr: "Apply these security patterns to every plugin architecture implementation. Plugin systems are vulnerable because they load and execute code dynamically."
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Every plugin architecture implementation must address security. Plugin systems are particularly vulnerable because they load and execute code dynamically.

## Decision

| Threat | Mitigation | Why |
|--------|------------|-----|
| Untrusted plugin code | Validate plugin definitions in `processDefinition()` | Plugins from contrib can contain malicious code |
| API key exposure | Use `KeyModule` or config overrides, never hardcode | Keys in code end up in version control |
| Input injection | Sanitize all plugin configuration values | Plugin config may come from user forms |
| Privilege escalation | Enforce access checks in plugin manager, not just routes | Plugins may bypass route-level access |
| SSRF via provider plugins | Validate/whitelist external URLs in provider config | Malicious providers could target internal services |

## Pattern

**Plugin definition validation** - reject a malformed or hostile definition at discovery time:

```php
public function processDefinition(&$definition, $plugin_id) {
  parent::processDefinition($definition, $plugin_id);

  if (empty($definition['label'])) {
    throw new InvalidPluginDefinitionException($plugin_id, 'Missing label');
  }

  if (!empty($definition['api_endpoint'])) {
    if (!UrlHelper::isValid($definition['api_endpoint'], TRUE)) {
      throw new InvalidPluginDefinitionException($plugin_id, 'Invalid API endpoint');
    }
  }
}
```

**Access control before instantiation** - a route-level check does not cover programmatic callers:

```php
public function createInstance($plugin_id, array $configuration = []) {
  if (!$this->currentUser->hasPermission('use ' . $plugin_id)) {
    throw new AccessDeniedHttpException();
  }
  return parent::createInstance($plugin_id, $configuration);
}
```

**Configuration sanitization** - validate credential fields on the plugin's own form:

```php
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

- **Storing API keys in plugin annotations** → WHY: Annotations are cached and can be exposed via debug tools
- **Trusting plugin-provided HTML** → WHY: Plugin output rendered without sanitization enables XSS; render it as `#plain_text` or pass it through `Xss::filter()`
- **No access check on plugin operations** → WHY: Any plugin consumer can execute privileged operations
- **Exposing internal service details in REST responses** → WHY: Leaks architecture information to attackers

## See Also

- [Configuration Architecture](configuration-architecture.md)
- [Plugin Manager Implementation](plugin-manager-implementation.md)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Reference: [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
