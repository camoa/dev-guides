---
description: Configure AI providers - authentication, model access, rate limits, and operational settings
drupal_version: "11.x"
---

# AI Provider Configuration

## When to Use

> Configure AI providers before using any AI features. Use provider configuration when you need to establish authentication, model access, rate limits, and operational settings for AI services.

## Decision

| Provider | Best For | Model Types | Cost Model |
|----------|----------|-------------|------------|
| OpenAI | GPT-4, DALL-E, Whisper | Text, Image, Audio | Pay per token |
| Anthropic Claude | Long context, code analysis | Text only | Pay per token |
| AWS Bedrock | Enterprise, compliance | Multiple models | AWS pricing |
| Amazee.io | Local/self-hosted | Open source models | Self-managed |

## Pattern

**Step 1: Create API Key Entity**
Navigate to `/admin/config/system/keys` and create a key entity for your provider API key. Use the Key module's secure storage backend (environment variables, file, or external key management).

**Step 2: Configure Provider**
Navigate to `/admin/config/ai/providers` and configure:

```yaml
# Example OpenAI provider config
provider_id: openai
api_key: key_entity_reference
models:
  chat:
    - gpt-4-turbo-preview
    - gpt-4
    - gpt-3.5-turbo
  embeddings:
    - text-embedding-3-large
    - text-embedding-ada-002
  image_generation:
    - dall-e-3
rate_limit:
  requests_per_minute: 60
  tokens_per_minute: 90000
timeout: 30
```

**Step 3: Test Connection**
Use AI Explorer (`/admin/config/ai/explorer`) to test provider connectivity and model responses.

## Security Best Practices

**API Key Management**:
- NEVER store API keys in configuration exports
- Use Key module with environment variable backend in production
- Rotate keys quarterly or after team member changes
- Use separate keys for dev/stage/prod environments
- Restrict key access to minimum required roles

**Provider Access Control**:
- Create dedicated API keys with minimal required permissions
- Configure provider-level rate limits below API plan limits to prevent overage
- Enable request logging for audit trails
- Use IP allowlisting when provider supports it

## Common Mistakes

- **Wrong**: Storing API keys in config sync → **Right**: Keys in exported config are a critical security vulnerability; always use Key module
- **Wrong**: Using production keys in development → **Right**: Separate keys prevent dev/test usage from affecting production quotas
- **Wrong**: Not configuring rate limits → **Right**: Uncontrolled usage can exhaust API quotas and incur unexpected costs
- **Wrong**: Sharing keys across environments → **Right**: Separate keys enable independent monitoring and limit blast radius of key compromise
- **Wrong**: Ignoring model deprecation notices → **Right**: Providers deprecate models; monitor changelog and plan migrations

## See Also

- [Architecture](architecture.md)
- [Content Workflow](content-workflow.md)
- [Security & Privacy](security-privacy.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/ai
